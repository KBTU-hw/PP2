import psycopg2
from connec import connec

conn=connec()
cur=conn.cursor()

with open(r"Practice8/procedures.sql", "r", encoding="utf-8") as file:
    cur.execute(file.read())
    conn.commit()
with open(r"Practice8/functions.sql", "r", encoding="utf-8") as file:
    cur.execute(file.read())
    conn.commit()





def get_user(s):
    cur.execute("SELECT * FROM get_user(%s)", (int(s),))
    print(cur.fetchall())
def show_users(s):
    cur.execute("SELECT * FROM show_users(%s)", (f"{s}",))
    print(cur.fetchall())
def list_user(s):
    a, b=map(int, s.split())
    cur.execute("SELECT * FROM list_user(%s, %s)", (a, b,))
    for row in cur.fetchall():
        print(row)
def add_user(s):
    a, b=s.split()
    cur.execute("CALL add_user(%s, %s)", (a, b,))
    conn.commit()
def update_phone(s):
    a, b=s.split()
    cur.execute("CALL update_phone(%s, %s)", (int(a), b,))
    conn.commit()
def delete_user(s):
    cur.execute("CALL delete_user(%s)", (int(s),))
    conn.commit()

n=input()
while n:
    a, b=n.split()
    s=input()
    if a=="fun":
        if b=="get_user": get_user(s)
        elif b=="show_users": show_users(s)
        elif b=="list_user": list_user(s)
    elif a=="pro":
        if b=="add_user": add_user(s)
        elif b=="update_phone": update_phone(s)
        elif b=="delete_user": delete_user(s)
    n=input()
cur.close()
conn.close()