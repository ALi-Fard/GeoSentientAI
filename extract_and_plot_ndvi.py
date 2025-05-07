
import os
import gdown
import zipfile
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Google Drive file ID (from shared link)
FILE_ID = "1WPFexy8fB44N4b9DAo9kuZs-vytthtsh"
ZIP_FILENAME = "S2A_SAFE.zip"
SAFE_FOLDER_NAME = "S2A_MSIL2A_20250416T191831_N0511_R056_T10UDV_20250417T014615.SAFE"

# Step 1: Download using gdown
if not os.path.exists(ZIP_FILENAME):
    print("📥 Downloading .SAFE ZIP file using gdown...")
    gdown.download(id=FILE_ID, output=ZIP_FILENAME, quiet=False)
    print("✅ Download complete:", ZIP_FILENAME)

# Step 2: Unzip
if not os.path.exists(SAFE_FOLDER_NAME):
    print("🗂️ Extracting:", ZIP_FILENAME)
    with zipfile.ZipFile(ZIP_FILENAME, 'r') as zip_ref:
        zip_ref.extractall()
    print("✅ Extraction complete.")

# Step 3: Locate bands
band4_path, band8_path = None, None
for root, _, files in os.walk(SAFE_FOLDER_NAME):
    for file in files:
        if "B04_10m.jp2" in file:
            band4_path = os.path.join(root, file)
        elif "B08_10m.jp2" in file:
            band8_path = os.path.join(root, file)

if not band4_path or not band8_path:
    raise FileNotFoundError("❌ Could not find both B04 and B08 10m bands.")

# Step 4: Read and compute NDVI
with rasterio.open(band4_path) as red_src:
    red = red_src.read(1).astype('float32')

with rasterio.open(band8_path) as nir_src:
    nir = nir_src.read(1).astype('float32')

ndvi = (nir - red) / (nir + red + 1e-10)
ndvi = np.clip(ndvi, -1, 1)

# Step 5: Plot NDVI
plt.figure(figsize=(10, 8))
ndvi_plot = plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(ndvi_plot, label='NDVI')
plt.title("NDVI — Patullo Bridge Zone")
plt.axis('off')
plt.tight_layout()
plt.show()
