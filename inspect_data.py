"""
Inspect the contents of satellite and LANDFIRE data files
"""

import rasterio
from pathlib import Path
import numpy as np

def inspect_file(filepath):
    """
    Show detailed information about a GeoTIFF file
    """
    print(f"\n{'='*70}")
    print(f"FILE: {filepath.name}")
    print('='*70)

    with rasterio.open(filepath) as src:
        print(f"\n📐 DIMENSIONS:")
        print(f"  Width:  {src.width:,} pixels")
        print(f"  Height: {src.height:,} pixels")
        print(f"  Total:  {src.width * src.height:,} pixels")

        print(f"\n📊 BANDS (layers of data):")
        print(f"  Number of bands: {src.count}")
        if src.descriptions:
            for i, desc in enumerate(src.descriptions, 1):
                print(f"    Band {i}: {desc}")
        else:
            print(f"    (No band descriptions available)")

        print(f"\n🗺️  GEOGRAPHIC INFO:")
        print(f"  Coordinate system: {src.crs}")
        print(f"  Bounds (lat/lon):")
        print(f"    North: {src.bounds.top:.4f}°")
        print(f"    South: {src.bounds.bottom:.4f}°")
        print(f"    East:  {src.bounds.right:.4f}°")
        print(f"    West:  {src.bounds.left:.4f}°")

        print(f"\n📏 RESOLUTION:")
        print(f"  Pixel size: {abs(src.transform[0]):.2f} x {abs(src.transform[4]):.2f} degrees")
        # Convert to meters (approximate at 35°N)
        meters_per_degree = 111000 * np.cos(np.radians(35.8))
        pixel_meters = abs(src.transform[0]) * meters_per_degree
        print(f"  Approximately: {pixel_meters:.1f} x {pixel_meters:.1f} meters per pixel")

        print(f"\n💾 DATA TYPE:")
        print(f"  {src.dtypes[0]} (data stored as {src.dtypes[0]})")

        print(f"\n📈 SAMPLE DATA (Band 1):")
        # Read a small sample
        sample = src.read(1, window=((0, min(100, src.height)), (0, min(100, src.width))))
        print(f"  Min value:  {np.nanmin(sample):.4f}")
        print(f"  Max value:  {np.nanmax(sample):.4f}")
        print(f"  Mean value: {np.nanmean(sample):.4f}")
        print(f"  Data range: {np.nanmax(sample) - np.nanmin(sample):.4f}")

        # Show what each pixel represents
        print(f"\n🔍 WHAT EACH PIXEL MEANS:")
        return src.count, src.descriptions

def explain_sentinel2():
    """Explain Sentinel-2 data structure"""
    print("\n" + "="*70)
    print("SENTINEL-2 DATA STRUCTURE")
    print("="*70)
    print("""
Your Sentinel-2 files have 9 BANDS (layers):

Band 1: B2 (Blue light)       - Values ~0-3000 (surface reflectance)
Band 2: B3 (Green light)      - Values ~0-3000
Band 3: B4 (Red light)        - Values ~0-3000
Band 4: B8 (Near-Infrared)    - Values ~0-3000 (plants reflect NIR!)
Band 5: B11 (SWIR 1)          - Values ~0-3000 (sensitive to moisture)
Band 6: B12 (SWIR 2)          - Values ~0-3000 (sensitive to fire)
Band 7: NDVI                  - Values -1 to +1 (vegetation health)
Band 8: NBR                   - Values -1 to +1 (burn detection)
Band 9: NDMI                  - Values -1 to +1 (moisture content)

EACH PIXEL represents a 10m x 10m square on the ground!

Example pixel interpretation:
- NDVI = 0.8  → Healthy, dense vegetation
- NDVI = 0.3  → Sparse vegetation or stressed plants
- NDVI < 0.1  → Bare soil, rock, or burned area
- NBR < -0.3  → Recently burned area
""")

def explain_modis():
    """Explain MODIS data structure"""
    print("\n" + "="*70)
    print("MODIS DATA STRUCTURE")
    print("="*70)
    print("""
Your MODIS files have 2 BANDS:

Band 1: NDVI                  - Values -0.2 to +1 (after scaling)
Band 2: EVI                   - Values -0.2 to +1 (Enhanced Vegetation Index)

EACH PIXEL represents a 250m x 250m square on the ground!

Note: MODIS pixels are BIGGER (coarser) than Sentinel-2
  - Sentinel-2: 10m x 10m
  - MODIS: 250m x 250m (625 times larger!)

But MODIS updates more frequently and has longer historical record.
""")

def explain_landsat():
    """Explain Landsat data structure"""
    print("\n" + "="*70)
    print("LANDSAT 8 DATA STRUCTURE")
    print("="*70)
    print("""
Your Landsat files have 3 BANDS:

Band 1: SR_B4 (Red)           - Values ~0-30000 (needs scaling)
Band 2: SR_B5 (Near-Infrared) - Values ~0-30000
Band 3: ST_B10 (Thermal)      - Values in Kelvin (needs conversion to °C)

EACH PIXEL represents a 30m x 30m square on the ground!

Landsat's thermal band is unique - it measures surface temperature!
This can detect fire scars, stressed vegetation (hotter), and moisture.
""")

def explain_landfire():
    """Explain LANDFIRE data structure"""
    print("\n" + "="*70)
    print("LANDFIRE DATA STRUCTURE")
    print("="*70)
    print("""
LANDFIRE files typically have 1 BAND per file, with CATEGORICAL data:

FBFM40 (Fire Behavior Fuel Model):
  - Values 1-40 represent different fuel types
  - Example: 101 = Grass, 141 = Conifer forest, 165 = Hardwood litter
  - Each number = a specific vegetation/fuel combination

CBD (Canopy Bulk Density):
  - Values represent kg/m³ of canopy fuel
  - Higher = denser tree canopy

CH (Canopy Height):
  - Values in meters (tree height)

EACH PIXEL represents a 30m x 30m square on the ground!

Note: LANDFIRE is STATIC (from 2020), while satellites update regularly!
""")

def main():
    """
    Main inspection function
    """
    print("="*70)
    print("GEOTIFF DATA INSPECTOR")
    print("="*70)

    # Inspect satellite files
    satellite_dir = Path("data/satellite")
    if satellite_dir.exists():
        for tif_file in sorted(satellite_dir.glob("*.tif")):
            count, descs = inspect_file(tif_file)

    # Inspect LANDFIRE files
    landfire_dir = Path("data/landfire")
    if landfire_dir.exists() and any(landfire_dir.glob("*.tif")):
        print("\n\n" + "="*70)
        print("LANDFIRE FILES")
        print("="*70)
        for tif_file in sorted(landfire_dir.glob("*.tif")):
            inspect_file(tif_file)

    # Print explanations
    explain_sentinel2()
    explain_modis()
    explain_landsat()
    explain_landfire()

    print("\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print("""
1. GeoTIFF = Multi-dimensional array + GPS coordinates
   - Like a spreadsheet where each cell is a location on Earth
   - Each cell contains measurements (reflectance, temperature, etc.)

2. Multi-band = Multiple measurements per location
   - Sentinel-2: 9 different measurements per 10m pixel
   - MODIS: 2 measurements per 250m pixel
   - LANDFIRE: 1 classification per 30m pixel

3. The DATA is just numbers, but they mean:
   - Spectral bands: How much light was reflected
   - Indices (NDVI, NBR): Calculated ratios indicating vegetation/fire
   - Categories (FBFM40): Classification codes for fuel types

4. Your hackathon goal: COMBINE these different data sources
   - Use high-res Sentinel-2 (10m) for detail
   - Use frequent MODIS (250m) for change detection
   - Use LANDFIRE (30m) as baseline fuel map
   - Fuse them to create better fuel predictions!
""")

if __name__ == "__main__":
    main()
