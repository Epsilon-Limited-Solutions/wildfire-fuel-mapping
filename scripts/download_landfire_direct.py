"""
Direct download of LANDFIRE data for Hermits Peak area
Using LANDFIRE Data Distribution System
"""

import requests
import json
from pathlib import Path
from tqdm import tqdm

DATA_DIR = Path("data/landfire")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Hermits Peak fire area bounding box
# From our GeoJSON: 35.6°N - 36.0°N, 105.3°W - 105.9°W
BBOX = {
    'minx': -105.9,
    'miny': 35.6,
    'maxx': -105.3,
    'maxy': 36.0
}

def try_landfire_wms():
    """
    Try to download via WMS (Web Map Service)
    This gets a rendered image, not the raw raster, but it's better than nothing
    """
    print("\n=== Attempting LANDFIRE WMS Download ===")

    # LANDFIRE WMS endpoint
    wms_base = "https://edcintl.cr.usgs.gov/geoserver/landfire/wms"

    # Layers to download
    layers = {
        'FBFM40': 'landfire:LF2020_FBFM40_220',  # Fire Behavior Fuel Model
        'CBD': 'landfire:LF2020_CBD_220',         # Canopy Bulk Density
        'CH': 'landfire:LF2020_CH_220'            # Canopy Height
    }

    # WMS GetMap parameters
    width = 2048  # Image width in pixels
    height = 2048  # Image height in pixels

    for layer_name, layer_id in layers.items():
        print(f"\nDownloading {layer_name}...")

        params = {
            'service': 'WMS',
            'version': '1.1.0',
            'request': 'GetMap',
            'layers': layer_id,
            'bbox': f"{BBOX['minx']},{BBOX['miny']},{BBOX['maxx']},{BBOX['maxy']}",
            'width': width,
            'height': height,
            'srs': 'EPSG:4326',
            'format': 'image/geotiff',
            'styles': ''
        }

        try:
            response = requests.get(wms_base, params=params, timeout=120)

            if response.status_code == 200:
                # Check if we got a GeoTIFF or an error message
                content_type = response.headers.get('content-type', '')

                if 'image' in content_type or 'application/octet-stream' in content_type:
                    output_file = DATA_DIR / f"LF2020_{layer_name}_hermits_peak.tif"
                    with open(output_file, 'wb') as f:
                        f.write(response.content)

                    file_size = len(response.content) / (1024 * 1024)  # MB
                    print(f"  ✓ Downloaded: {output_file}")
                    print(f"  Size: {file_size:.2f} MB")
                else:
                    print(f"  ✗ Error: Got {content_type} instead of image")
                    print(f"  Response preview: {response.text[:200]}")
            else:
                print(f"  ✗ HTTP {response.status_code}: {response.text[:200]}")

        except Exception as e:
            print(f"  ✗ Error: {e}")

def try_landfire_direct_download():
    """
    Try to find direct download links for LANDFIRE tiles
    LANDFIRE data is distributed as tiles covering regions
    """
    print("\n=== Checking for LANDFIRE Direct Download ===")

    # LANDFIRE distributes data by map zones
    # Hermits Peak is approximately in map zone 13 (New Mexico)

    print("\nLANDFIRE data is distributed by map zones.")
    print("Hermits Peak area is in:")
    print("  - Map Zone: 13 (Southwest)")
    print("  - Tiles covering: Northern New Mexico")

    # Try to access the data distribution site
    distribution_base = "https://landfire.gov/bulk/downloadfile.php"

    print("\nDirect tile download requires knowing exact tile IDs.")
    print("This is complex to automate without their tile grid.")

    return False

def create_download_instructions():
    """
    Create detailed manual download instructions
    """
    instructions = """
================================================================================
LANDFIRE MANUAL DOWNLOAD INSTRUCTIONS
================================================================================

Since automated download is complex, here's the fastest manual approach:

METHOD 1: LANDFIRE Viewer (RECOMMENDED - 15 minutes)
────────────────────────────────────────────────────────

1. Go to: https://www.landfire.gov/viewer/

2. In the search box, enter: "Hermits Peak, New Mexico"
   OR enter coordinates: 35.8, -105.6

3. Click "Get Data" button (top right)

4. In the Data Download panel:
   a. Select "LF 2020" from the version dropdown
   b. Check these layers:
      ☐ FBFM40 (40 Scott and Burgan Fire Behavior Fuel Models) ← CRITICAL
      ☐ CBD (Canopy Bulk Density)
      ☐ CH (Canopy Height)

5. Define your area:
   a. Click "Draw Rectangle" tool
   b. Draw a box covering these coordinates:
      - Northwest corner: 36.0°N, 105.9°W
      - Southeast corner: 35.6°N, 105.3°W

   OR use our exact coordinates:
      - Min Longitude: -105.9
      - Max Longitude: -105.3
      - Min Latitude: 35.6
      - Max Latitude: 36.0

6. Select output format: "GeoTIFF"

7. Enter your email address (they'll send download link)

8. Click "Submit Request"

9. Wait for email (usually 5-15 minutes)

10. Download ZIP file from email link

11. Extract and move files to:
    {data_dir}

Expected files:
  - LF2020_FBFM40_*.tif  (Fuel behavior models) ~50-100 MB
  - LF2020_CBD_*.tif     (Canopy density) ~50-100 MB
  - LF2020_CH_*.tif      (Canopy height) ~50-100 MB


METHOD 2: Bulk Download (Alternative)
────────────────────────────────────────

1. Go to: https://landfire.gov/version_download.php

2. Select:
   - Version: LF 2020
   - Geography: CONUS (Continental US)
   - Map Zone: 13 (Southwest)

3. Download tiles covering Northern New Mexico

4. Use GIS software to clip to Hermits Peak area

⚠️  Warning: This downloads larger area, requires more processing


VALIDATION:
───────────

After download, verify files with this command:

    source venv/bin/activate
    python -c "import rasterio; print(rasterio.open('data/landfire/LF2020_FBFM40*.tif').bounds)"

You should see coordinates approximately:
    (-105.9, 35.6, -105.3, 36.0)


TROUBLESHOOTING:
────────────────

Q: Email not arriving?
A: Check spam folder, or try different email address

Q: Download link expired?
A: Re-submit the request (links expire after 24-48 hours)

Q: Files won't extract?
A: Make sure you have a ZIP utility (built into macOS)

Q: Need help?
A: LANDFIRE Help Desk: https://www.landfire.gov/contact.php


TIMELINE:
─────────

Total time: 15-20 minutes
  - Form submission: 2 min
  - Wait for email: 5-15 min
  - Download & extract: 3-5 min

Do this TONIGHT so data is ready for tomorrow!

================================================================================
"""

    output_file = Path("LANDFIRE_DOWNLOAD_INSTRUCTIONS.txt")
    with open(output_file, 'w') as f:
        f.write(instructions.format(data_dir=DATA_DIR.absolute()))

    print(f"\n✓ Created detailed instructions: {output_file}")
    return output_file

def check_existing_data():
    """
    Check if LANDFIRE data already exists
    """
    print("\n=== Checking for Existing LANDFIRE Data ===")

    tif_files = list(DATA_DIR.glob("*.tif"))

    if tif_files:
        print(f"\n✓ Found {len(tif_files)} existing LANDFIRE files:")
        for f in tif_files:
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name} ({size_mb:.1f} MB)")
        return True
    else:
        print("\n✗ No LANDFIRE data found yet")
        return False

def main():
    print("=" * 80)
    print("LANDFIRE DATA DOWNLOAD")
    print("Hermits Peak Fire Area - Northern New Mexico")
    print("=" * 80)

    # Check if data already exists
    if check_existing_data():
        print("\n✓ LANDFIRE data already present!")
        print("If you need to re-download, delete existing files first.")
        return

    # Try automated download via WMS
    print("\nAttempting automated download via WMS...")
    try_landfire_wms()

    # Check if WMS download worked
    if check_existing_data():
        print("\n" + "=" * 80)
        print("✓ SUCCESS! LANDFIRE data downloaded via WMS")
        print("=" * 80)
        print(f"\nFiles saved to: {DATA_DIR.absolute()}")
        print("\nYou can now proceed with the analysis!")
        return

    # If automated failed, provide manual instructions
    print("\n" + "=" * 80)
    print("WMS download may require manual steps")
    print("=" * 80)

    instructions_file = create_download_instructions()

    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print(f"\n1. Open: {instructions_file}")
    print("2. Follow METHOD 1 (LANDFIRE Viewer)")
    print("3. Takes ~15 minutes total")
    print("4. Come back when files are in data/landfire/")

    print("\n💡 TIP: Start the download request now while you work on other tasks!")
    print("The email will arrive in 5-15 minutes.\n")

if __name__ == "__main__":
    main()
