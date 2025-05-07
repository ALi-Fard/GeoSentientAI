
import planetary_computer
import pystac_client
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show
from shapely.geometry import box
import geopandas as gpd

# Define Area of Interest (Vancouver area)
bbox = [-123.1, 49.1, -122.8, 49.3]  # [min lon, min lat, max lon, max lat]
aoi_geom = box(*bbox)

# Create GeoDataFrame for bbox
aoi = gpd.GeoDataFrame({"geometry": [aoi_geom]}, crs="EPSG:4326")

# Connect to Planetary Computer STAC
catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
search = catalog.search(
    collections=["sentinel-2-l2a"],
    intersects=aoi_geom,
    query={"eo:cloud_cover": {"lt": 10}},
    sortby=[{"field": "properties.datetime", "direction": "desc"}],
    limit=1,
)

item = next(search.get_items())
print("Found image:", item.id)

# Sign the item to access it
signed_item = planetary_computer.sign(item)

# Load bands B04 (red) and B08 (nir)
red_asset = signed_item.assets["B04"].href
nir_asset = signed_item.assets["B08"].href

with rasterio.open(red_asset) as red_src, rasterio.open(nir_asset) as nir_src:
    red = red_src.read(1).astype("float32")
    nir = nir_src.read(1).astype("float32")
    profile = red_src.profile

# Calculate NDVI
ndvi = (nir - red) / (nir + red)
ndvi = np.clip(ndvi, -1, 1)

# Plot NDVI
plt.figure(figsize=(8, 6))
ndvi_plot = plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(ndvi_plot, label="NDVI")
plt.title("NDVI - Sentinel-2 - Vancouver")
plt.axis("off")
plt.tight_layout()
plt.show()
