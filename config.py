import psycopg2

DB_HOST = "localhost"
DB_NAME = "proyecto"
DB_USER = "aquuz"
DB_PASS = "123"

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    return conn
