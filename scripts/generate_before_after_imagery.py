#!/usr/bin/env python3
"""
Generate before/after satellite imagery visualizations
Shows the Hermits Peak fire area before (2020) and after (2022) the fire
"""

import numpy as np
import matplotlib.pyplot as plt
import rasterio
from pathlib import Path
from matplotlib.gridspec import GridSpec

# Paths
DATA_DIR = Path(__file__).parent.parent / 'data'
OUTPUT_DIR = Path(__file__).parent.parent / 'outputs'
MAPS_ONLY_DIR = OUTPUT_DIR / 'maps_only'
SATELLITE_DIR = DATA_DIR / 'satellite'

def load_multiband_image(filepath):
    """Load a multiband satellite image"""
    print(f"  Loading: {filepath.name}")

    with rasterio.open(filepath) as src:
        # Read all bands
        num_bands = src.count
        print(f"  Found {num_bands} bands")

        bands = {}
        for i in range(1, num_bands + 1):
            data = src.read(i).astype(np.float32)

            # Normalize based on typical ranges
            # Most satellite data is in 0-10000 or 0-255 range
            max_val = np.nanpercentile(data[data > 0], 99.9)

            if max_val > 1000:
                # Likely 0-10000 range (Sentinel-2, Landsat SR)
                data = data / 10000.0
            elif max_val > 10:
                # Likely 0-255 range
                data = data / 255.0
            # else already normalized to 0-1

            data = np.clip(data, 0, 1)
            bands[f'band_{i}'] = data

        return bands

def create_true_color(red, green, blue):
    """Create true color RGB composite with enhanced contrast"""
    # Stack bands
    rgb = np.dstack([red, green, blue])

    # Apply gamma correction for better visualization
    gamma = 2.2
    rgb = np.power(rgb, 1/gamma)

    # Stretch to 2-98 percentile for better contrast
    p2, p98 = np.percentile(rgb[~np.isnan(rgb)], (2, 98))
    rgb = np.clip((rgb - p2) / (p98 - p2), 0, 1)

    return rgb

def create_false_color(nir, red, green):
    """Create false color composite (NIR-R-G) to highlight vegetation"""
    # Stack bands: NIR as red, Red as green, Green as blue
    false_color = np.dstack([nir, red, green])

    # Apply gamma correction
    gamma = 2.2
    false_color = np.power(false_color, 1/gamma)

    # Stretch to 2-98 percentile
    p2, p98 = np.percentile(false_color[~np.isnan(false_color)], (2, 98))
    false_color = np.clip((false_color - p2) / (p98 - p2), 0, 1)

    return false_color

def generate_before_after_comparison():
    """Generate before/after comparison imagery"""
    print("Generating before/after satellite imagery comparison...")
    print()

    # Load pre-fire imagery
    print("Loading PRE-FIRE imagery (2020-2022 composite)...")
    pre_file = SATELLITE_DIR / 'hermits_peak_prefire_2020_2022.tif'
    if not pre_file.exists():
        # Try Landsat pre-fire
        pre_file = SATELLITE_DIR / 'hermits_peak_landsat8_prefire.tif'

    if not pre_file.exists():
        print(f"ERROR: Pre-fire imagery not found")
        print(f"Searched: {SATELLITE_DIR}")
        return

    pre_bands = load_multiband_image(pre_file)

    print()
    print("Loading POST-FIRE imagery (2022)...")
    post_file = SATELLITE_DIR / 'hermits_peak_postfire_2022.tif'

    if not post_file.exists():
        print(f"ERROR: Post-fire imagery not found: {post_file}")
        return

    post_bands = load_multiband_image(post_file)

    print()
    print("Creating visualizations...")

    # Determine band mapping based on number of bands
    # Typical order: B1=Blue, B2=Green, B3=Red, B4=NIR or
    # For some products: B1=Red, B2=Green, B3=Blue, B4=NIR

    num_pre_bands = len(pre_bands)
    num_post_bands = len(post_bands)

    print(f"  Pre-fire bands: {num_pre_bands}, Post-fire bands: {num_post_bands}")

    # Assume standard order: bands 1-3 are RGB or BGR, band 4+ is NIR
    if num_pre_bands >= 4 and num_post_bands >= 4:
        # Try RGB order first (band_3=R, band_2=G, band_1=B)
        pre_rgb = create_true_color(pre_bands['band_3'], pre_bands['band_2'], pre_bands['band_1'])
        post_rgb = create_true_color(post_bands['band_3'], post_bands['band_2'], post_bands['band_1'])

        # False color: NIR-R-G (band_4, band_3, band_2)
        pre_false = create_false_color(pre_bands['band_4'], pre_bands['band_3'], pre_bands['band_2'])
        post_false = create_false_color(post_bands['band_4'], post_bands['band_3'], post_bands['band_2'])
    elif num_pre_bands >= 3 and num_post_bands >= 3:
        # Only RGB, no NIR
        pre_rgb = create_true_color(pre_bands['band_3'], pre_bands['band_2'], pre_bands['band_1'])
        post_rgb = create_true_color(post_bands['band_3'], post_bands['band_2'], post_bands['band_1'])
        pre_false = pre_rgb  # No false color without NIR
        post_false = post_rgb
    else:
        print("ERROR: Not enough bands for RGB composite")
        return

    # Generate comparison figures

    # 1. True Color Before/After
    print("  Creating true color comparison...")
    fig = plt.figure(figsize=(20, 10), facecolor='white')
    gs = GridSpec(1, 2, figure=fig, wspace=0.05)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(pre_rgb, interpolation='bilinear')
    ax1.set_title('BEFORE Fire (2020)\nTrue Color Satellite Imagery',
                  fontsize=20, fontweight='bold', pad=20)
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(post_rgb, interpolation='bilinear')
    ax2.set_title('AFTER Fire (2022)\nTrue Color Satellite Imagery',
                  fontsize=20, fontweight='bold', pad=20)
    ax2.axis('off')

    plt.suptitle('Hermits Peak-Calf Canyon Fire: Satellite Imagery Comparison',
                 fontsize=24, fontweight='bold', y=0.98)

    output_file = MAPS_ONLY_DIR / 'before_after_true_color.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

    # 2. False Color Before/After (Vegetation Analysis)
    print("  Creating false color comparison...")
    fig = plt.figure(figsize=(20, 10), facecolor='white')
    gs = GridSpec(1, 2, figure=fig, wspace=0.05)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(pre_false, interpolation='bilinear')
    ax1.set_title('BEFORE Fire (2020)\nFalse Color (NIR-Red-Green)',
                  fontsize=20, fontweight='bold', pad=20)
    ax1.text(0.02, 0.98, 'Healthy vegetation = bright red',
             transform=ax1.transAxes, fontsize=14, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(post_false, interpolation='bilinear')
    ax2.set_title('AFTER Fire (2022)\nFalse Color (NIR-Red-Green)',
                  fontsize=20, fontweight='bold', pad=20)
    ax2.text(0.02, 0.98, 'Burned areas = dark/brown',
             transform=ax2.transAxes, fontsize=14, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax2.axis('off')

    plt.suptitle('Hermits Peak-Calf Canyon Fire: Vegetation Impact Analysis',
                 fontsize=24, fontweight='bold', y=0.98)

    output_file = MAPS_ONLY_DIR / 'before_after_false_color.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

    # 3. Stacked version (all 4 images)
    print("  Creating 4-panel comparison...")
    fig = plt.figure(figsize=(20, 20), facecolor='white')
    gs = GridSpec(2, 2, figure=fig, hspace=0.1, wspace=0.05)

    # Top left: Pre true color
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.imshow(pre_rgb, interpolation='bilinear')
    ax1.set_title('BEFORE (2020) - True Color', fontsize=18, fontweight='bold', pad=15)
    ax1.axis('off')

    # Top right: Post true color
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.imshow(post_rgb, interpolation='bilinear')
    ax2.set_title('AFTER (2022) - True Color', fontsize=18, fontweight='bold', pad=15)
    ax2.axis('off')

    # Bottom left: Pre false color
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.imshow(pre_false, interpolation='bilinear')
    ax3.set_title('BEFORE (2020) - False Color (Vegetation)', fontsize=18, fontweight='bold', pad=15)
    ax3.text(0.02, 0.98, 'Red = healthy vegetation',
             transform=ax3.transAxes, fontsize=12, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax3.axis('off')

    # Bottom right: Post false color
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.imshow(post_false, interpolation='bilinear')
    ax4.set_title('AFTER (2022) - False Color (Vegetation)', fontsize=18, fontweight='bold', pad=15)
    ax4.text(0.02, 0.98, 'Dark = burned areas',
             transform=ax4.transAxes, fontsize=12, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax4.axis('off')

    plt.suptitle('Hermits Peak-Calf Canyon Fire: Complete Satellite Analysis\n341,735 acres burned | $4 billion damage',
                 fontsize=24, fontweight='bold', y=0.99)

    output_file = MAPS_ONLY_DIR / 'before_after_4panel.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

    print()
    print("=" * 60)
    print("✓ Before/after imagery generated successfully!")
    print("=" * 60)

def main():
    """Generate all before/after imagery"""
    print("=" * 60)
    print("GENERATING BEFORE/AFTER SATELLITE IMAGERY")
    print("=" * 60)
    print()

    generate_before_after_comparison()

if __name__ == '__main__':
    main()
