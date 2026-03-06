import sqlite3
from contextlib import contextmanager

DB_NAME = "items.db"
INTERNET_USAGE_DB_NAME = "internet_usage.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        """)

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()  # Automatically commit if no errors occur
    except Exception:
        conn.rollback() # Rollback if something goes wrong
        raise
    finally:
        conn.close()   # Always close the connection

@contextmanager
def get_internet_usage_db():
    conn = sqlite3.connect(INTERNET_USAGE_DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()  # Automatically commit if no errors occur
    except Exception:
        conn.rollback() # Rollback if something goes wrong
        raise
    finally:
        conn.close()   # Always close the connection