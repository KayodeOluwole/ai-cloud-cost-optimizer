import json

def fetch_cost_data():
    with open("mock_azure_consumption_api.json", "r") as f:
        data = json.load(f)
    print("Mock data fetched successfully.")
    return data
