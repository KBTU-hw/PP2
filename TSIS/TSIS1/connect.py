import psycopg2

def con():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Ai474663",
        host="localhost",
        port="5432"
    )
