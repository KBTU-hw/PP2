import psycopg2

def connec():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Ai474663",
        host="localhost",
        port="5432"
    )