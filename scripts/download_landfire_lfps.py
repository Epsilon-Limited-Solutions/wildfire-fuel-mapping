"""
Download LANDFIRE data using the LANDFIRE Product Service (LFPS)
https://lfps.usgs.gov

This submits a request and downloads the result directly!
"""

import requests
import time
import json
from pathlib import Path

DATA_DIR = Path("data/landfire")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Hermits Peak fire area bounding box
# WGS84 coordinates (required by LFPS)
BBOX = {
    'west': -105.9,
    'south': 35.6,
    'east': -105.3,
    'north': 36.0
}

# LANDFIRE Product Service endpoint
LFPS_URL = "https://lfps.usgs.gov/api/order"

def submit_lfps_request():
    """
    Submit a request to LANDFIRE Product Service
    """
    print("=" * 60)
    print("LANDFIRE Product Service Download")
    print("=" * 60)

    # Layers to request (semicolon delimited)
    # LF 2020 layer codes:
    layers = [
        "220FBFM40",  # LF 2020 FBFM40 (Fire Behavior Fuel Model)
        "220CBD",     # LF 2020 CBD (Canopy Bulk Density)
        "220CH"       # LF 2020 CH (Canopy Height)
    ]

    layer_string = ";".join(layers)

    # Create the request payload
    payload = {
        'layers': layer_string,
        'area': f"{BBOX['west']},{BBOX['south']},{BBOX['east']},{BBOX['north']}",
        'projection': 'GEO',  # WGS84 geographic coordinates
        'resolution': 30,      # 30 meter resolution
        'format': 'GTIFF'      # GeoTIFF output
    }

    print("\nRequest Details:")
    print(f"  Layers: {layer_string}")
    print(f"  Area: {payload['area']}")
    print(f"  Projection: {payload['projection']}")
    print(f"  Resolution: {payload['resolution']}m")

    try:
        print("\nSubmitting request to LFPS...")
        print("This may take 30-60 seconds...\n")

        # Submit the request
        response = requests.post(LFPS_URL, data=payload, timeout=300)

        if response.status_code == 200:
            print("✓ Request submitted successfully!")

            # Check if we got JSON response (order ID) or direct download
            content_type = response.headers.get('content-type', '')

            if 'application/json' in content_type:
                # Got an order ID - need to poll for completion
                order_info = response.json()
                print(f"\nOrder ID: {order_info.get('orderId', 'N/A')}")
                print("Waiting for processing...")

                # This would require polling the order status
                # For now, print instructions
                print("\nCheck order status at:")
                print(f"https://lfps.usgs.gov/order/{order_info.get('orderId')}")

                return False

            elif 'image' in content_type or 'application/octet-stream' in content_type:
                # Got the file directly!
                output_file = DATA_DIR / "LF2020_HermitsPeak_multiband.tif"

                with open(output_file, 'wb') as f:
                    f.write(response.content)

                file_size = len(response.content) / (1024 * 1024)  # MB
                print(f"\n✓ Downloaded: {output_file}")
                print(f"  Size: {file_size:.2f} MB")

                return True
            else:
                print(f"\nUnexpected response type: {content_type}")
                print(f"Response preview: {response.text[:500]}")
                return False

        else:
            print(f"✗ Request failed with status {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False

    except requests.exceptions.Timeout:
        print("✗ Request timed out")
        print("The server may be processing a large request.")
        print("Try the web interface at: https://lfps.usgs.gov")
        return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def try_simple_form_submission():
    """
    Try submitting via the web form interface
    This mimics what a browser would do
    """
    print("\n" + "=" * 60)
    print("Attempting form submission...")
    print("=" * 60)

    # The actual form endpoint might be different
    # Let's try common patterns

    form_urls = [
        "https://lfps.usgs.gov/helptexts/productselectionnew.php",
        "https://lfps.usgs.gov/api/products",
        "https://lfps.usgs.gov/products"
    ]

    # Form data matching the web interface
    form_data = {
        'product': '220FBFM40;220CBD;220CH',
        'aoi': f"{BBOX['west']},{BBOX['south']},{BBOX['east']},{BBOX['north']}",
        'proj': 'GEO',
        'resolution': '30'
    }

    for url in form_urls:
        try:
            print(f"\nTrying: {url}")
            response = requests.post(url, data=form_data, timeout=60)

            if response.status_code == 200:
                print(f"  ✓ Got response ({len(response.content)} bytes)")

                # Save response for inspection
                with open("lfps_response.html", 'w') as f:
                    f.write(response.text)

                print(f"  Response saved to: lfps_response.html")

                # Check if it looks like a success
                if 'download' in response.text.lower() or 'order' in response.text.lower():
                    print("  ✓ Looks like a successful submission!")
                    return True
            else:
                print(f"  ✗ Status: {response.status_code}")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue

    return False

def create_manual_instructions():
    """
    Create instructions for using the web interface manually
    """
    instructions = f"""
================================================================================
LANDFIRE PRODUCT SERVICE - MANUAL INSTRUCTIONS
================================================================================

Since automated download may not work immediately, here's how to use the web
interface manually (takes 5-10 minutes):

1. Go to: https://lfps.usgs.gov

2. Fill in the form:

   **Layers (semicolon separated):**
   220FBFM40;220CBD;220CH

   **Area of Interest (comma separated coordinates):**
   {BBOX['west']},{BBOX['south']},{BBOX['east']},{BBOX['north']}

   **Projection:**
   GEO (or ALBERS)

   **Resolution:**
   30

3. Click "Submit" or "Process"

4. Wait for processing (usually 30-60 seconds)

5. Download the resulting GeoTIFF file

6. Save to: {DATA_DIR.absolute()}

Expected output:
  - Multi-band GeoTIFF with all 3 layers
  - Size: ~100-200 MB
  - Bands: FBFM40, CBD, CH

================================================================================
"""

    with open("LFPS_INSTRUCTIONS.txt", 'w') as f:
        f.write(instructions)

    print(instructions)
    print(f"\n✓ Instructions saved to: LFPS_INSTRUCTIONS.txt")

def main():
    print("\n" + "=" * 60)
    print("LANDFIRE DATA DOWNLOAD via LFPS")
    print("Hermits Peak Area, New Mexico")
    print("=" * 60)

    # Try automated submission
    success = submit_lfps_request()

    if not success:
        print("\n" + "=" * 60)
        print("Automated download didn't work.")
        print("=" * 60)

        # Try alternative methods
        try_simple_form_submission()

        # Provide manual instructions
        print("\n" + "=" * 60)
        print("RECOMMENDATION: Use the web interface manually")
        print("=" * 60)

        create_manual_instructions()

        print("\n💡 TIP: The LFPS web interface is actually very fast!")
        print("It takes just 5 minutes and gives you all 3 layers at once.\n")

if __name__ == "__main__":
    main()
