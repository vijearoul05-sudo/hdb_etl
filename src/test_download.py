import requests
import pandas as pd

# Use ONE dataset first
dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"

url = f"https://api-production.data.gov.sg/v2/public/api/datasets/{dataset_id}/data?limit=10000"

response = requests.get(url)
data = response.json()

print(data.keys())  # inspect structure

# Try to extract rows
records = data.get("data", {}).get("records", [])

print(f"Number of records: {len(records)}")

df = pd.DataFrame(records)

df.to_csv("data/raw/test.csv", index=False)

print("Saved test.csv")