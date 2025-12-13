import sqlite3

DB_PATH = "cost_data.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn
