
from pystac_client import Client

# Connect to the Copernicus STAC API
stac_url = "https://catalogue.dataspace.copernicus.eu/stac"
client = Client.open(stac_url)

# Define the search area (Surrey, BC coordinates) and date range
search = client.search(
    collections=["sentinel-2-l2a"],
    bbox=[-122.8945, 49.2070, -122.8920, 49.2090],
    datetime="2025-04-01/2025-05-06",
    query={"eo:cloud_cover": {"lt": 20}},
    max_items=1
)

# Retrieve and print the first matching product
items = list(search.get_items())

if items:
    item = items[0]
    print("🛰 Found Product:", item.id)
    print("Title:", item.get('title', 'N/A'))
    print("Cloud Cover:", item.properties.get("eo:cloud_cover", "N/A"))
    print("Red Band (B04):", item.assets["B04"].href)
    print("NIR Band (B08):", item.assets["B08"].href)
else:
    print("No suitable Sentinel-2 product found for the specified criteria.")
