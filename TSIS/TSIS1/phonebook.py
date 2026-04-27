import csv
import json
from datetime import datetime
from pathlib import Path

from connect import con

BASE = Path(__file__).resolve().parent
SORT = {"name": "c.name", "birthday": "c.birthday", "date": "c.created_at"}


def parse_date(text):
    text = (text or "").strip()
    if not text:
        return None
    return datetime.strptime(text, "%Y-%m-%d").date()

def setup_db(cur, conn):
    for file_name in ["schema.sql", "procedures.sql"]:
        cur.execute((BASE / file_name).read_text(encoding="utf-8"))
    conn.commit()

def ensure_group(cur, group_name):
    cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT(name) DO NOTHING", (group_name,))
    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    return cur.fetchone()[0]

def get_contact_id(cur, name):
    cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
    row = cur.fetchone()
    return row[0] if row else None

def upsert_contact(cur, name, email, birthday, group_name, overwrite):
    cid = get_contact_id(cur, name)
    gid = ensure_group(cur, group_name or "Other")
    if cid is None:
        cur.execute(
            "INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s) RETURNING id",
            (name, email, birthday, gid),
        )
        return cur.fetchone()[0]
    if not overwrite:
        return cid
    cur.execute("UPDATE contacts SET email=%s,birthday=%s,group_id=%s WHERE id=%s", (email, birthday, gid, cid))
    cur.execute("DELETE FROM phones WHERE contact_id=%s", (cid,))
    return cid

def print_rows(rows):
    if not rows:
        print("No contacts.")
        return
    for r in rows:
        print(f"{r[1]} | {r[2] or '-'} | {r[3] or '-'} | {r[4] or '-'} | {r[6] or '-'}")

def filter_search_sort(cur):
    group_name = input("Group (empty any): ").strip() or None
    email_q = input("Email contains: ").strip() or None
    sort_key = input("Sort name/birthday/date: ").strip().lower() or "name"
    order = SORT.get(sort_key, SORT["name"])
    cur.execute(
        f"""
        SELECT c.id,c.name,c.email,c.birthday,g.name,c.created_at,
               COALESCE(STRING_AGG(p.type||':'||p.phone_number, ', ' ORDER BY p.type), '')
        FROM contacts c
        LEFT JOIN groups g ON g.id=c.group_id
        LEFT JOIN phones p ON p.contact_id=c.id
        WHERE (%s IS NULL OR g.name=%s)
          AND (%s IS NULL OR COALESCE(c.email,'') ILIKE '%%' || %s || '%%')
        GROUP BY c.id,c.name,c.email,c.birthday,g.name,c.created_at
        ORDER BY {order} NULLS LAST
        """,
        (group_name, group_name, email_q, email_q),
    )
    print_rows(cur.fetchall())

def paginate(cur):
    size = 5
    page = 0
    while True:
        cur.execute(
            """
            SELECT c.id,c.name,c.email,c.birthday,g.name,c.created_at,
                   COALESCE(STRING_AGG(p.type||':'||p.phone_number, ', ' ORDER BY p.type), '')
            FROM contacts c
            LEFT JOIN groups g ON g.id=c.group_id
            LEFT JOIN phones p ON p.contact_id=c.id
            GROUP BY c.id,c.name,c.email,c.birthday,g.name,c.created_at
            ORDER BY c.name
            LIMIT %s OFFSET %s
            """,
            (size, page * size),
        )
        rows = cur.fetchall()
        if not rows and page > 0:
            page -= 1
            continue
        print(f"Page {page + 1}")
        print_rows(rows)
        cmd = input("next/prev/quit: ").strip().lower()
        if cmd == "next":
            page += 1
        elif cmd == "prev":
            page = max(0, page - 1)
        elif cmd == "quit":
            break

def export_json(cur):
    out_path = input("Output JSON: ").strip() or str(BASE / "contacts_export.json")
    cur.execute(
        """
        SELECT c.name,c.email,c.birthday,g.name,
               COALESCE(
                 JSON_AGG(JSON_BUILD_OBJECT('phone_number',p.phone_number,'type',p.type))
                 FILTER (WHERE p.id IS NOT NULL),
                 '[]'::json
               )
        FROM contacts c
        LEFT JOIN groups g ON g.id=c.group_id
        LEFT JOIN phones p ON p.contact_id=c.id
        GROUP BY c.id,c.name,c.email,c.birthday,g.name
        ORDER BY c.name
        """
    )
    payload = []
    for name, email, birthday, group_name, phones in cur.fetchall():
        payload.append(
            {
                "name": name,
                "email": email,
                "birthday": birthday.isoformat() if birthday else None,
                "group": group_name,
                "phones": phones,
            }
        )
    Path(out_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("Exported", len(payload))

def import_json(cur, conn):
    in_path = input("Input JSON: ").strip() or str(BASE / "contacts_import.json")
    data = json.loads(Path(in_path).read_text(encoding="utf-8"))
    for c in data:
        name = (c.get("name") or "").strip()
        if not name:
            continue
        overwrite = False
        if get_contact_id(cur, name) is not None:
            ans = input(f"{name} exists. skip/overwrite: ").strip().lower()
            if ans == "skip":
                continue
            overwrite = ans == "overwrite"
            if not overwrite:
                continue
        cid = upsert_contact(cur, name, c.get("email"), parse_date(c.get("birthday")), c.get("group") or "Other", overwrite)
        for p in c.get("phones", []):
            num = (p.get("phone_number") or "").strip()
            typ = (p.get("type") or "mobile").strip().lower()
            if num and typ in {"home", "work", "mobile"}:
                cur.execute("INSERT INTO phones(contact_id,phone_number,type) VALUES(%s,%s,%s)", (cid, num, typ))
    conn.commit()
    print("Import done")

def import_csv(cur, conn):
    csv_path = input("CSV path: ").strip() or str(BASE / "contacts.csv")
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue
            cid = upsert_contact(
                cur,
                name,
                (row.get("email") or "").strip() or None,
                parse_date(row.get("birthday")),
                (row.get("group") or "Other").strip() or "Other",
                False,
            )
            phone = (row.get("phone") or "").strip()
            typ = (row.get("phone_type") or "mobile").strip().lower()
            if phone and typ in {"home", "work", "mobile"}:
                cur.execute("INSERT INTO phones(contact_id,phone_number,type) VALUES(%s,%s,%s)", (cid, phone, typ))
    conn.commit()
    print("CSV import done")

def search_contacts(cur):
    q = input("Search query: ").strip()
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    print_rows(cur.fetchall())

def add_phone(cur, conn):
    name = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    ptype = input("Type home/work/mobile: ").strip().lower()
    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
    conn.commit()

def move_group(cur, conn):
    name = input("Contact name: ").strip()
    group_name = input("Target group: ").strip() or "Other"
    cur.execute("CALL move_to_group(%s,%s)", (name, group_name))
    conn.commit()

conn = con()
cur = conn.cursor()
while True:
    print("\n1.Filter/Search/Sort 2.Pages 3.SearchProc 4.AddPhone 5.MoveGroup 6.ExportJSON 7.ImportJSON 8.ImportCSV 9.Exit")
    c = input("Choose: ").strip()
    if c == "1":
        filter_search_sort(cur)
    elif c == "2":
        paginate(cur)
    elif c == "3":
        search_contacts(cur)
    elif c == "4":
        add_phone(cur, conn)
    elif c == "5":
        move_group(cur, conn)
    elif c == "6":
        export_json(cur)
    elif c == "7":
        import_json(cur, conn)
    elif c == "8":
        import_csv(cur, conn)
    elif c == "9":
        break
cur.close()
conn.close()
