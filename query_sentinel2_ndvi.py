
import requests
import json

# Define the search URL
search_url = "https://catalogue.dataspace.copernicus.eu/stac/search"

# Vancouver BBOX and time range
payload = {
    "collections": ["SENTINEL-2"],
    "bbox": [-123.3, 49.1, -122.7, 49.4],
    "datetime": "2023-06-01T00:00:00Z/2023-06-30T23:59:59Z",
    "limit": 3
}

headers = {"Content-Type": "application/json"}

# Send POST request
response = requests.post(search_url, headers=headers, data=json.dumps(payload))

# Parse and display results
results = response.json()

print(f"Found {len(results['features'])} items:\n")
for item in results["features"]:
    print(f"ID: {item['id']}")
    for band, asset in item["assets"].items():
        if "B04" in band or "B08" in band:
            print(f"  {band} → {asset['href']}")
    print()
