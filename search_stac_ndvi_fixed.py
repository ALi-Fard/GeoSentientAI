
from pystac_client import Client

# Connect to Copernicus STAC API
stac_url = "https://catalogue.dataspace.copernicus.eu/stac"
client = Client.open(stac_url)

# Define the search area (Surrey, BC) and date range
search = client.search(
    collections=["sentinel-2-l2a"],
    bbox=[-122.8945, 49.2070, -122.8920, 49.2090],
    datetime="2025-04-01/2025-05-06",
    max_items=1
)

items = list(search.get_items())

if items:
    item = items[0]
    print("🛰 Found Product:", item.id)
    print("Title:", item.get('title', 'N/A'))
    print("Available Assets:", item.assets.keys())
    print("Red Band (B04):", item.assets.get("B04").href if "B04" in item.assets else "Not found")
    print("NIR Band (B08):", item.assets.get("B08").href if "B08" in item.assets else "Not found")
else:
    print("No suitable Sentinel-2 product found.")
