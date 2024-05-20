import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('memory.db')  # Creates a SQLite database named 'memory'
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    try:
        sql_create_table = """CREATE TABLE IF NOT EXISTS memories (
                                    date text,
                                    title text,
                                    type text,
                                    data text,
                                    priority integer
                                );"""
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)

# create a database connection
conn = create_connection()

if conn is not None:
    # create memories table
    create_table(conn)
else:
    print("Error! cannot create the database connection.")