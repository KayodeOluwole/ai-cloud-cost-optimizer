from api.database.database import get_connection

def fetch_all_costs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM azure_costs")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def fetch_latest_costs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM azure_costs
        ORDER BY usage_date DESC
        LIMIT 20
    """)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def fetch_cost_by_resource(resource_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM azure_costs WHERE resource_id = ?", 
        (resource_id,)
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def fetch_cost_between_dates(start_date: str, end_date: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM azure_costs WHERE usage_date BETWEEN ? AND ?", 
        (start_date, end_date)
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def cost_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT meterCategory,
               SUM(cost_amount) AS total_cost
        FROM azure_costs
        GROUP BY meterCategory
    """)
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
