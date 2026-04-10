import psycopg2
import csv
import re

def show():
    cur.execute("SELECT * FROM phone_book;")
    for i in cur.fetchall():
        print(i)
def add(s):
    l=s.split()
    cur.execute(f"INSERT INTO phone_book (name, phone) VALUES ('{l[0]}', '{l[1]}');")
    conn.commit()
def search(s):
    if re.fullmatch(r"\d+", s):
        cur.execute(f"SELECT * FROM phone_book WHERE phone LIKE '{s}%';")
    else: cur.execute(f"SELECT * FROM phone_book WHERE name LIKE '{s}%';")
    for i in cur.fetchall():
        print(i)
def update(s):
    l=s.split()
    a=int(l[0])
    if re.fullmatch(r"\d+", l[1]): cur.execute(f"UPDATE phone_book SET phone='{l[1]}' WHERE id={a}")
    else: cur.execute(f"UPDATE phone_book SET name='{l[1]}' WHERE id={a}")
    conn.commit()
def delete(s):
    a=int(s)
    cur.execute(f"DELETE FROM phone_book WHERE id={a}")
    conn.commit()

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Ai474663",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS phone_book (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(20)
);
""")

# with open(r"Practice7/contacts.csv", "r", encoding="utf-8") as file:
#     reader = csv.reader(file)
#     next(reader)
#     for row in reader:
#         name = row[0]
#         phone = row[1]
#         cur.execute(f"INSERT INTO phone_book (name, phone) VALUES ('{name}', '{phone}');")
# conn.commit()

n=int(input())
for _ in range(n):
    i=input()
    if i=="show": show()
    elif i=="add": add(input())
    elif i=="search": search(input())
    elif i=="update": update(input())
    elif i=="delete": delete(input())
        
cur.close()
conn.close()