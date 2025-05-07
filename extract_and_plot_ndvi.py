
import os
import requests
import zipfile
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Download the zip file from Google Drive if not already present
GDRIVE_URL = "https://drive.google.com/uc?export=download&id=1WPFexy8fB44N4b9DAo9kuZs-vytthtsh"
ZIP_FILENAME = "S2A_SAFE.zip"
SAFE_FOLDER_NAME = "S2A_MSIL2A_20250416T191831_N0511_R056_T10UDV_20250417T014615.SAFE"

if not os.path.exists(ZIP_FILENAME):
    print("📥 Downloading ZIP from Google Drive...")
    r = requests.get(GDRIVE_URL)
    with open(ZIP_FILENAME, 'wb') as f:
        f.write(r.content)
    print("✅ Download complete.")

# Step 2: Extract ZIP if folder doesn’t exist
if not os.path.exists(SAFE_FOLDER_NAME):
    print("🗂️ Extracting ZIP file...")
    with zipfile.ZipFile(ZIP_FILENAME, 'r') as zip_ref:
        zip_ref.extractall()
    print("✅ Extraction complete.")

# Step 3: Locate bands inside the SAFE folder
band4_path = None
band8_path = None

for root, dirs, files in os.walk(SAFE_FOLDER_NAME):
    for file in files:
        if "B04_10m.jp2" in file:
            band4_path = os.path.join(root, file)
        elif "B08_10m.jp2" in file:
            band8_path = os.path.join(root, file)

if not band4_path or not band8_path:
    raise FileNotFoundError("❌ Could not find required bands (B04 and B08) in the .SAFE folder.")

# Step 4: Read bands using Rasterio
with rasterio.open(band4_path) as red_src:
    red = red_src.read(1).astype('float32')

with rasterio.open(band8_path) as nir_src:
    nir = nir_src.read(1).astype('float32')

# Step 5: Compute NDVI
ndvi = (nir - red) / (nir + red + 1e-10)
ndvi = np.clip(ndvi, -1, 1)

# Step 6: Plot the NDVI result
plt.figure(figsize=(10, 8))
ndvi_plot = plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(ndvi_plot, label='NDVI')
plt.title("NDVI - Patullo Bridge Area (Sentinel-2)")
plt.axis('off')
plt.tight_layout()
plt.show()
