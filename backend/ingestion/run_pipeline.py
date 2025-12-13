from fetch_cost_data import fetch_cost_data
from transform_cost_data import transform_cost_data
from load_to_db import load_to_db


def run_pipeline():
    raw_data = fetch_cost_data()
    df = transform_cost_data(raw_data)
    load_to_db(df)
    print("\nPipeline executed successfully.")


if __name__ == "__main__":
    run_pipeline()
