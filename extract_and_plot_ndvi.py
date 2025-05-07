
import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from zipfile import ZipFile

# Path to the downloaded .SAFE zip file
safe_zip_path = 'downloaded_product.zip'
extract_folder = 'extracted_safe_product'

# Step 1: Unzip the .SAFE file
with ZipFile(safe_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

# Step 2: Locate band files (assumes L2A product format)
band_red = None
band_nir = None

for root, dirs, files in os.walk(extract_folder):
    for file in files:
        if file.endswith('B04_10m.jp2'):
            band_red = os.path.join(root, file)
        if file.endswith('B08_10m.jp2'):
            band_nir = os.path.join(root, file)

if not band_red or not band_nir:
    raise FileNotFoundError("Required band files not found (B04 and B08)")

# Step 3: Read bands
with rasterio.open(band_red) as red:
    red_band = red.read(1).astype('float32')
with rasterio.open(band_nir) as nir:
    nir_band = nir.read(1).astype('float32')

# Step 4: Calculate NDVI
ndvi = (nir_band - red_band) / (nir_band + red_band)
ndvi = np.clip(ndvi, -1, 1)

# Step 5: Plot
plt.figure(figsize=(10, 6))
ndvi_plot = plt.imshow(ndvi, cmap='RdYlGn')
plt.colorbar(ndvi_plot, label='NDVI')
plt.title('NDVI from Sentinel-2')
plt.axis('off')
plt.tight_layout()
plt.show()
