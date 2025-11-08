"""
Alternative download script for Hermits Peak fire perimeter
Using NIFC and ArcGIS services
"""

import requests
import json
from pathlib import Path

DATA_DIR = Path("data/fire_perimeters")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_nifc_historic_perimeters():
    """
    Download from NIFC Historic Perimeters
    Using ArcGIS REST API
    """
    print("\n=== Attempting download from NIFC Historic Perimeters ===")

    # NIFC Historic Fire Perimeters feature service
    # We'll query for the Hermits Peak/Calf Canyon fire from 2022
    base_url = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services"

    # Try querying the historic perimeters layer
    # Note: exact endpoint may need adjustment based on current NIFC structure
    endpoints = [
        "/Historic_Perimeters/FeatureServer/0/query",
        "/US_Fire_Perimeters/FeatureServer/0/query",
        "/WFIGS_Historic_Perimeters/FeatureServer/0/query"
    ]

    params = {
        'where': "fire_name LIKE '%Hermit%' OR fire_name LIKE '%Calf%' AND fire_year='2022'",
        'outFields': '*',
        'f': 'geojson',
        'returnGeometry': 'true'
    }

    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"Trying: {url}")
            response = requests.get(url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if 'features' in data and len(data['features']) > 0:
                    output_file = DATA_DIR / "hermits_peak_2022.geojson"
                    with open(output_file, 'w') as f:
                        json.dump(data, f)
                    print(f"✓ Downloaded Hermits Peak fire perimeter!")
                    print(f"  Location: {output_file}")
                    print(f"  Features found: {len(data['features'])}")
                    return True
        except Exception as e:
            print(f"  Failed: {e}")
            continue

    print("Could not download from NIFC endpoints")
    return False

def try_geomac_alternative():
    """
    Try alternative GeoMAC/NIFC sources
    """
    print("\n=== Trying alternative fire perimeter sources ===")

    # WFIGS (Wildland Fire Interagency Geospatial Services)
    wfigs_url = "https://data-nifc.opendata.arcgis.com/datasets/nifc::wfigs-2022-wildland-fire-perimeters-to-date/about"

    print("Alternative source (may require manual download):")
    print(f"  {wfigs_url}")
    print("\nYou can also download directly from:")
    print("  1. https://data-nifc.opendata.arcgis.com/ (search 'Hermits Peak')")
    print("  2. https://hermits-peak-calf-canyon-fire-resources-nmhu.hub.arcgis.com/")
    print("  3. https://burnseverity.cr.usgs.gov/baer/baer-imagery-support-data-download/2022/hermits-peak")

    return False

def create_manual_hermits_peak_boundary():
    """
    Create a simple polygon boundary for Hermits Peak area
    based on known coordinates from the fire
    """
    print("\n=== Creating approximate boundary for Hermits Peak area ===")

    # Approximate bounding box for Hermits Peak/Calf Canyon fire
    # Based on fire reports: ~341,000 acres
    # Center approximately at: 35.8°N, 105.6°W

    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "properties": {
                "name": "Hermits Peak / Calf Canyon Fire 2022",
                "fire_name": "HERMITS PEAK",
                "acres": 341735,
                "fire_year": 2022,
                "start_date": "2022-04-06",
                "contain_date": "2022-08-21",
                "note": "Approximate boundary - use for area of interest definition",
                "source": "Manually created from reported fire statistics"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-105.9, 35.6],  # SW corner
                    [-105.9, 36.0],  # NW corner
                    [-105.3, 36.0],  # NE corner
                    [-105.3, 35.6],  # SE corner
                    [-105.9, 35.6]   # Close polygon
                ]]
            }
        }]
    }

    output_file = DATA_DIR / "hermits_peak_area_of_interest.geojson"
    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)

    print(f"✓ Created approximate area of interest")
    print(f"  Location: {output_file}")
    print(f"  This is a ~40km x 40km box around the fire area")
    print(f"  Use this to download satellite imagery and LANDFIRE data")

    return True

def main():
    print("=" * 60)
    print("HERMITS PEAK FIRE PERIMETER DOWNLOAD")
    print("=" * 60)

    # Try automated downloads
    success = download_nifc_historic_perimeters()

    if not success:
        try_geomac_alternative()

    # Create approximate boundary for data downloads
    create_manual_hermits_peak_boundary()

    print("\n" + "=" * 60)
    print("RECOMMENDATION:")
    print("=" * 60)
    print("\nFor the hackathon, you have two options:")
    print("\n1. Use the approximate boundary to download data")
    print("   - This is sufficient for a demo")
    print("   - Covers the fire area + buffer zone")
    print("\n2. Manually download exact perimeter from:")
    print("   - https://data-nifc.opendata.arcgis.com/")
    print("   - Search for 'WFIGS 2022' or 'Hermits Peak'")
    print("   - Download as GeoJSON or Shapefile")
    print(f"   - Save to: {DATA_DIR}")
    print("\nFor tonight: Option 1 is fine to get started!")

if __name__ == "__main__":
    main()
