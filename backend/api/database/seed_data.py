import sqlite3

def seed_data():
    conn = sqlite3.connect("costs.db")
    cursor = conn.cursor()

    sample_data = [
        ("vm-001", 24.55, "USD", "2025-12-01", "Compute"),
        ("vm-002", 12.89, "USD", "2025-12-01", "Compute"),
        ("storage-001", 5.60, "USD", "2025-12-01", "Storage"),
        ("sql-db-01", 44.32, "USD", "2025-12-02", "Database"),
    ]

    cursor.executemany("""
        INSERT INTO azure_costs (resource_id, cost_amount, currency, usage_date, meterCategory)
        VALUES (?, ?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()
    print("Sample data inserted successfully")

if __name__ == "__main__":
    seed_data()
