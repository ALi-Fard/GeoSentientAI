
import requests

# Replace this with your actual SAFE product download URL
safe_url = "https://download.dataspace.copernicus.eu/odata/v1/Products(45451763-a6f6-4bc6-ab27-ca06fac68d32)/$value"

# OPTIONAL: If you have a bearer token (access_token), use the headers below
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN"  # Replace YOUR_ACCESS_TOKEN if needed
}

# Output file name
output_filename = "sentinel2_product.zip"

print("Downloading NDVI .SAFE product...")
response = requests.get(safe_url, headers=headers, stream=True)

if response.status_code == 200:
    with open(output_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Download complete. Saved as {output_filename}")
else:
    print(f"Failed to download. Status code: {response.status_code}")
    print(response.text)
