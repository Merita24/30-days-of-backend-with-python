import sqlite3

DB_NAME="users.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_db() as conn:
        cursor=conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                       )""")
        conn.commit()