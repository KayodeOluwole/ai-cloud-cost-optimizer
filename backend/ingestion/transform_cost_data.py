import pandas as pd

def transform_cost_data(raw_data):
    df = pd.DataFrame(raw_data)

    df = df.rename(columns={
        "resourceId": "resource_id",
        "cost": "cost_amount",
        "usageDate": "usage_date"
    })

    print("Data transformation complete.")
    return df
