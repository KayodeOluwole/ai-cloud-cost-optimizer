from db_connection import get_db_connection

def load_to_db(df):
    conn = get_db_connection()

    df.to_sql("azure_costs", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()

    print("Data successfully loaded into the database.")
