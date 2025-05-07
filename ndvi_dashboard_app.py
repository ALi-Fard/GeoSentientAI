
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import planetary_computer
import pystac_client

st.set_page_config(layout="wide", page_title="GeoSentientAI: NDVI Dashboard")
st.title("🌱 GeoSentientAI: Real-time NDVI Visualization")

# Define region of interest
bbox = [-123.2, 49.1, -122.8, 49.3]  # Roughly Vancouver

st.markdown("**Region of Interest:** Vancouver, Canada")
st.map(data={"lat": [49.25], "lon": [-123.1]}, zoom=9)

st.subheader("🛰️ Fetching NDVI from Sentinel-2 (Planetary Computer)")

catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=bbox,
    datetime="2023-07-01/2023-07-10",
    query={"eo:cloud_cover": {"lt": 10}},
    max_items=1
)

items = list(search.get_items())
if not items:
    st.error("No Sentinel-2 imagery found for this time range.")
    st.stop()

item = items[0]
signed_item = planetary_computer.sign(item)

with rasterio.open(signed_item.assets["B04"].href) as red,      rasterio.open(signed_item.assets["B08"].href) as nir:

    red_band = red.read(1).astype("float32")
    nir_band = nir.read(1).astype("float32")

    ndvi = (nir_band - red_band) / (nir_band + red_band)
    ndvi = np.clip(ndvi, -1, 1)

    fig, ax = plt.subplots(figsize=(10, 6))
    img = ax.imshow(ndvi, cmap="YlGn", vmin=0, vmax=1)
    ax.set_title("NDVI (Normalized Difference Vegetation Index)")
    fig.colorbar(img, ax=ax, orientation="vertical", label="NDVI")

    st.pyplot(fig)

st.success("✅ NDVI visualization generated successfully.")
