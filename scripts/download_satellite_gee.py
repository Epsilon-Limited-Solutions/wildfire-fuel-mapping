"""
Google Earth Engine Script for Downloading Satellite Imagery
Hermits Peak Fire Area - 2020-2022

RUN THIS AFTER YOU GET GEE APPROVAL AND AUTHENTICATE:
  1. earthengine authenticate
  2. python download_satellite_gee.py
"""

import ee
import json
from pathlib import Path
from datetime import datetime

# Initialize Earth Engine
# You'll need to authenticate first: earthengine authenticate
try:
    ee.Initialize(project='wildfire-hackathon-nov0825')
    print("✓ Earth Engine initialized successfully!")
except Exception as e:
    print("✗ Earth Engine initialization failed!")
    print("Did you run: earthengine authenticate?")
    print(f"Error: {e}")
    exit(1)

# Load the fire area of interest
DATA_DIR = Path("data")
FIRE_PERIMETER = DATA_DIR / "fire_perimeters" / "hermits_peak_area_of_interest.geojson"
OUTPUT_DIR = DATA_DIR / "satellite"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load fire boundary
with open(FIRE_PERIMETER) as f:
    geojson = json.load(f)

# Convert GeoJSON to Earth Engine geometry
coords = geojson['features'][0]['geometry']['coordinates'][0]
aoi = ee.Geometry.Polygon(coords)

print(f"Area of Interest loaded: {FIRE_PERIMETER}")

# Date ranges
PRE_FIRE_START = '2020-01-01'
PRE_FIRE_END = '2022-04-01'  # Just before fire started
DURING_FIRE = '2022-04-06'
POST_FIRE_START = '2022-08-22'  # After containment
POST_FIRE_END = '2022-12-31'

def get_sentinel2_composite(start_date, end_date, aoi, name):
    """
    Get Sentinel-2 composite for a date range
    Calculate vegetation indices
    """
    print(f"\nProcessing Sentinel-2: {name}")
    print(f"  Date range: {start_date} to {end_date}")

    # Load Sentinel-2 surface reflectance
    s2 = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
          .filterDate(start_date, end_date)
          .filterBounds(aoi)
          .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
          .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12']))

    # Get collection size
    count = s2.size().getInfo()
    print(f"  Images found: {count}")

    if count == 0:
        print("  ⚠️  No images found for this period")
        return None

    # Create median composite (reduces clouds)
    composite = s2.median()

    # Calculate vegetation indices
    # NDVI (Normalized Difference Vegetation Index)
    ndvi = composite.normalizedDifference(['B8', 'B4']).rename('NDVI')

    # NBR (Normalized Burn Ratio - sensitive to fire damage)
    nbr = composite.normalizedDifference(['B8', 'B12']).rename('NBR')

    # NDMI (Normalized Difference Moisture Index)
    ndmi = composite.normalizedDifference(['B8', 'B11']).rename('NDMI')

    # Combine all bands and cast to Float32 for consistent data types
    result = composite.addBands([ndvi, nbr, ndmi]).toFloat()

    print(f"  ✓ Composite created with {result.bandNames().size().getInfo()} bands")

    return result

def export_to_drive(image, description, aoi):
    """
    Export image to Google Drive
    Note: This creates an export task that runs in the background
    """
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=description,
        folder='EarthEngineExports',
        region=aoi,
        scale=10,  # 10m resolution (Sentinel-2 native)
        crs='EPSG:4326',
        maxPixels=1e13
    )

    task.start()
    print(f"  Export task started: {description}")
    print(f"  Check status at: https://code.earthengine.google.com/tasks")
    return task

def download_sentinel2_time_series():
    """
    Download Sentinel-2 composites for different time periods
    """
    print("\n" + "="*60)
    print("DOWNLOADING SENTINEL-2 IMAGERY")
    print("="*60)

    # Pre-fire composite (baseline conditions)
    pre_fire = get_sentinel2_composite(PRE_FIRE_START, PRE_FIRE_END, aoi, "Pre-Fire")
    if pre_fire:
        export_to_drive(pre_fire, 'hermits_peak_prefire_2020_2022', aoi)

    # Post-fire composite
    post_fire = get_sentinel2_composite(POST_FIRE_START, POST_FIRE_END, aoi, "Post-Fire")
    if post_fire:
        export_to_drive(post_fire, 'hermits_peak_postfire_2022', aoi)

    print("\n" + "="*60)
    print("EXPORT TASKS CREATED")
    print("="*60)
    print("\nGo to: https://code.earthengine.google.com/tasks")
    print("Click 'RUN' on each task")
    print("Downloads will appear in your Google Drive in 'EarthEngineExports' folder")
    print("Each file will be a GeoTIFF you can download")

def get_modis_vegetation():
    """
    Get MODIS vegetation data (coarser but goes back further)
    """
    print("\n" + "="*60)
    print("DOWNLOADING MODIS VEGETATION INDICES")
    print("="*60)

    # MODIS NDVI (250m resolution)
    modis = (ee.ImageCollection('MODIS/061/MOD13Q1')
             .filterDate(PRE_FIRE_START, POST_FIRE_END)
             .filterBounds(aoi)
             .select(['NDVI', 'EVI']))

    count = modis.size().getInfo()
    print(f"  Images found: {count}")

    if count > 0:
        # Get mean NDVI for pre-fire period
        pre_modis = modis.filterDate(PRE_FIRE_START, PRE_FIRE_END).mean()
        export_to_drive(pre_modis, 'hermits_peak_modis_prefire', aoi)

        # Get mean NDVI for post-fire period
        post_modis = modis.filterDate(POST_FIRE_START, POST_FIRE_END).mean()
        export_to_drive(post_modis, 'hermits_peak_modis_postfire', aoi)

        print("  ✓ MODIS exports created")

def get_landsat_thermal():
    """
    Get Landsat 8 data including thermal band
    """
    print("\n" + "="*60)
    print("DOWNLOADING LANDSAT 8 THERMAL DATA")
    print("="*60)

    landsat = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
               .filterDate(PRE_FIRE_START, PRE_FIRE_END)
               .filterBounds(aoi)
               .filter(ee.Filter.lt('CLOUD_COVER', 20))
               .select(['SR_B4', 'SR_B5', 'ST_B10']))

    count = landsat.size().getInfo()
    print(f"  Images found: {count}")

    if count > 0:
        composite = landsat.median()
        export_to_drive(composite, 'hermits_peak_landsat8_prefire', aoi)
        print("  ✓ Landsat export created")

def main():
    """
    Main execution
    """
    print("=" * 60)
    print("EARTH ENGINE SATELLITE DATA DOWNLOAD")
    print("Hermits Peak Fire Area")
    print("=" * 60)

    try:
        # Download different datasets
        download_sentinel2_time_series()
        get_modis_vegetation()
        get_landsat_thermal()

        print("\n" + "=" * 60)
        print("ALL EXPORT TASKS CREATED!")
        print("=" * 60)
        print("\nIMPORTANT: These are EXPORT TASKS, not direct downloads")
        print("\nSteps to complete:")
        print("  1. Go to: https://code.earthengine.google.com/tasks")
        print("  2. You'll see your tasks listed")
        print("  3. Click 'RUN' on each task")
        print("  4. Confirm the export settings")
        print("  5. Wait 5-30 minutes for processing")
        print("  6. Download from Google Drive 'EarthEngineExports' folder")
        print("  7. Move downloaded files to: data/satellite/")

        print("\nExpected files:")
        print("  - hermits_peak_prefire_2020_2022.tif (Sentinel-2)")
        print("  - hermits_peak_postfire_2022.tif (Sentinel-2)")
        print("  - hermits_peak_modis_prefire.tif (MODIS)")
        print("  - hermits_peak_modis_postfire.tif (MODIS)")
        print("  - hermits_peak_landsat8_prefire.tif (Landsat 8)")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("  - Make sure you ran: earthengine authenticate")
        print("  - Check your internet connection")
        print("  - Verify the fire perimeter file exists")

if __name__ == "__main__":
    main()
