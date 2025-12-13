import sqlite3

def initialize_database():
    conn = sqlite3.connect("costs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS azure_costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id TEXT,
            cost_amount REAL,
            currency TEXT,
            usage_date TEXT,
            meterCategory TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    initialize_database()
