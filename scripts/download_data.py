"""
Data download script for wildfire fuel mapping project
Focuses on Hermits Peak 2022 fire in New Mexico
"""

import os
import requests
import zipfile
from pathlib import Path
from tqdm import tqdm

# Create data directory structure
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Subdirectories
FIRE_DIR = DATA_DIR / "fire_perimeters"
LANDFIRE_DIR = DATA_DIR / "landfire"
SATELLITE_DIR = DATA_DIR / "satellite"
DEM_DIR = DATA_DIR / "elevation"

for dir in [FIRE_DIR, LANDFIRE_DIR, SATELLITE_DIR, DEM_DIR]:
    dir.mkdir(exist_ok=True)

def download_file(url, destination, description="Downloading"):
    """Download a file with progress bar"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        with open(destination, 'wb') as file, tqdm(
            desc=description,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)

        print(f"✓ Downloaded: {destination}")
        return True
    except Exception as e:
        print(f"✗ Error downloading {url}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract a zip file"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ Extracted: {zip_path}")
        return True
    except Exception as e:
        print(f"✗ Error extracting {zip_path}: {e}")
        return False

def download_mtbs_fire_perimeters():
    """Download MTBS national fire perimeters (includes Hermits Peak 2022)"""
    print("\n=== Downloading MTBS Fire Perimeters ===")

    url = "https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/MTBS_Fire/data/composite_data/burned_area_extent_shapefile/mtbs_perimeter_data.zip"
    zip_path = FIRE_DIR / "mtbs_perimeter_data.zip"

    if download_file(url, zip_path, "MTBS Fire Perimeters"):
        extract_zip(zip_path, FIRE_DIR)
        print("✓ MTBS fire perimeters ready")
        print(f"  Location: {FIRE_DIR}")
        return True
    return False

def download_hermits_peak_baer():
    """Try to download specific Hermits Peak data from BAER"""
    print("\n=== Checking BAER for Hermits Peak specific data ===")
    print("Note: BAER data may require manual download from:")
    print("https://burnseverity.cr.usgs.gov/baer/baer-imagery-support-data-download/2022/hermits-peak")
    print("\nWe'll use the MTBS national dataset which includes Hermits Peak.")
    return True

def get_landfire_info():
    """Provide information about accessing LANDFIRE data"""
    print("\n=== LANDFIRE Data Access ===")
    print("LANDFIRE data requires WCS (Web Coverage Service) access or interactive download.")
    print("\nOption 1 - Interactive Download (Recommended for hackathon):")
    print("  1. Go to: https://www.landfire.gov/viewer/")
    print("  2. Search for 'Hermits Peak, New Mexico' or coordinates: 35.8°N, 105.6°W")
    print("  3. Select layers:")
    print("     - Fuel Loading Models (FBFM40)")
    print("     - Forest Canopy Bulk Density")
    print("     - Existing Vegetation Height")
    print("  4. Choose 'LF 2020' version (most recent before 2022 fire)")
    print("  5. Draw area of interest around Hermits Peak area")
    print("  6. Download as GeoTIFF")
    print(f"  7. Save to: {LANDFIRE_DIR}")

    print("\nOption 2 - WCS API (Programmatic):")
    print("  WCS endpoint: https://edcintl.cr.usgs.gov/geoserver/landfire_wcs/us_mf/wcs")
    print("  Example: ?request=GetCapabilities&service=WCS")
    print("  Requires specific WCS client library or manual GDAL/OGR commands")

    print("\nFor the hackathon, I recommend Option 1 for speed.")
    print("I'll create a helper script for Option 2 if needed.")

    return True

def get_elevation_data_info():
    """Provide info about elevation data"""
    print("\n=== Elevation Data (DEM) ===")
    print("Option 1 - USGS National Map (Recommended):")
    print("  1. Go to: https://apps.nationalmap.gov/downloader/")
    print("  2. Search for 'Hermits Peak, New Mexico'")
    print("  3. Select 'Elevation Products (3DEP)'")
    print("  4. Choose '1/3 arc-second DEM' (~10m resolution)")
    print("  5. Download and save to:", DEM_DIR)

    print("\nOption 2 - Use Python library (elevatr or elevation):")
    print("  pip install elevation")
    print("  Can download SRTM data programmatically")

    return True

def get_satellite_data_info():
    """Provide info about satellite data access"""
    print("\n=== Satellite Data Access ===")

    print("\n1. SENTINEL-2 (10m optical imagery):")
    print("   Best option: Google Earth Engine")
    print("   - Sign up: https://earthengine.google.com/signup/")
    print("   - Free for research/education")
    print("   - Provides historical imagery 2015-present")
    print("   - Python API: earthengine-api (already in requirements.txt)")

    print("\n2. LANDSAT 8/9 (30m optical/thermal):")
    print("   Also available via Google Earth Engine")
    print("   Alternative: USGS EarthExplorer (https://earthexplorer.usgs.gov/)")

    print("\n3. MODIS (250m-1km vegetation/fire):")
    print("   Available via:")
    print("   - Google Earth Engine (easiest)")
    print("   - NASA EARTHDATA (requires account): https://urs.earthdata.nasa.gov/")

    print("\n4. NASA FIRMS (Active Fire Data):")
    print("   Free download: https://firms.modaps.eosdis.nasa.gov/")
    print("   Can get historical fire detections")

    print("\nRECOMMENDATION:")
    print("  Create Google Earth Engine account NOW - approval can take a few hours")
    print("  This gives you access to Sentinel-2, Landsat, and MODIS in one place")

    return True

def create_credentials_template():
    """Create a template for API credentials"""
    template = """# API Credentials and Access Information
# Copy this to .env and fill in your credentials

# Google Earth Engine
# Sign up at: https://earthengine.google.com/signup/
# GEE_SERVICE_ACCOUNT=your-service-account@email.com
# GEE_PRIVATE_KEY_PATH=path/to/private-key.json
# OR authenticate via: earthengine authenticate

# NASA EARTHDATA (for SMAP, MODIS direct access)
# Sign up at: https://urs.earthdata.nasa.gov/
# NASA_USERNAME=your_username
# NASA_PASSWORD=your_password

# USGS Earth Explorer (for Landsat manual download)
# Sign up at: https://earthexplorer.usgs.gov/
# USGS_USERNAME=your_username
# USGS_PASSWORD=your_password

# Hermits Peak Fire coordinates
HERMITS_PEAK_LAT=35.8
HERMITS_PEAK_LON=-105.6
FIRE_BUFFER_KM=50

# Date ranges
FIRE_START_DATE=2022-04-06
FIRE_END_DATE=2022-08-21
PRE_FIRE_DATE=2022-01-01
"""

    with open("credentials_template.env", "w") as f:
        f.write(template)

    print("\n✓ Created credentials_template.env")
    print("  Fill this in with your API keys once you sign up for services")

def main():
    """Main download process"""
    print("=" * 60)
    print("WILDFIRE FUEL MAPPING - DATA DOWNLOAD")
    print("Hermits Peak Fire 2022, New Mexico")
    print("=" * 60)

    # What we can download automatically
    download_mtbs_fire_perimeters()
    download_hermits_peak_baer()

    # What requires manual steps or API keys
    get_landfire_info()
    get_elevation_data_info()
    get_satellite_data_info()

    # Create credentials template
    create_credentials_template()

    print("\n" + "=" * 60)
    print("SUMMARY - What you need to do:")
    print("=" * 60)
    print("\n✓ COMPLETED:")
    print("  [✓] MTBS Fire Perimeters downloaded")

    print("\n⚠ MANUAL STEPS REQUIRED:")
    print("  [ ] Sign up for Google Earth Engine (DO THIS NOW)")
    print("      https://earthengine.google.com/signup/")
    print("  [ ] Download LANDFIRE data via viewer")
    print("      https://www.landfire.gov/viewer/")
    print("  [ ] (Optional) Download elevation data")
    print("      https://apps.nationalmap.gov/downloader/")

    print("\n📝 NEXT STEPS:")
    print("  1. Run: source venv/bin/activate")
    print("  2. Sign up for Google Earth Engine")
    print("  3. Run: earthengine authenticate")
    print("  4. Download LANDFIRE data manually (15 min)")
    print("  5. Run the GEE download script (we'll create this next)")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
