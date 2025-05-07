
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from pystac_client import Client
from planetary_computer import sign
from shapely.geometry import box

# Vancouver coordinates
bbox = [-122.95, 49.15, -122.85, 49.25]  # [west, south, east, north]
bbox_geom = box(*bbox)

# Connect to Planetary Computer
api_url = "https://planetarycomputer.microsoft.com/api/stac/v1"
client = Client.open(api_url)

# Search for Sentinel-2 data
search = client.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2023-08-01/2023-08-10",
    query={"eo:cloud_cover": {"lt": 20}},
    limit=1
)

items = list(search.get_items())
if not items:
    raise ValueError("No data found for the given coordinates and date.")
item = items[0]

# Sign asset URLs for download
item = sign(item)

# Load RED and NIR bands
red_href = item.assets["B04"].href
nir_href = item.assets["B08"].href

with rasterio.open(red_href) as red_src:
    red = red_src.read(1).astype("float32")
    red_meta = red_src.meta

with rasterio.open(nir_href) as nir_src:
    nir = nir_src.read(1).astype("float32")

# Compute NDVI
ndvi = (nir - red) / (nir + red + 1e-5)

# Plot NDVI
plt.figure(figsize=(8, 6))
plt.imshow(ndvi, cmap="RdYlGn")
plt.colorbar(label="NDVI")
plt.title("NDVI over Vancouver (Sentinel-2)")
plt.axis("off")
plt.show()
