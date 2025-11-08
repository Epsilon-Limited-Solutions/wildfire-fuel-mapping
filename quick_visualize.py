"""
Quick visualization of satellite data (downsampled for speed)
"""

import rasterio
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data/satellite")
LANDFIRE_DIR = Path("data/landfire")

def downsample(arr, factor=10):
    """Downsample array for faster visualization"""
    return arr[::factor, ::factor]

print("Creating visualizations...")

# Create a big overview figure
fig = plt.figure(figsize=(20, 12))

# SENTINEL-2 PRE-FIRE
prefire = DATA_DIR / "hermits_peak_prefire_2020_2022.tif"
if prefire.exists():
    print(f"  Loading {prefire.name}...")
    with rasterio.open(prefire) as src:
        # Read and downsample
        b4 = downsample(src.read(3))  # Red
        b3 = downsample(src.read(2))  # Green
        b2 = downsample(src.read(1))  # Blue
        ndvi = downsample(src.read(7))  # NDVI
        nbr = downsample(src.read(8))   # NBR

    # True color
    ax1 = plt.subplot(2, 4, 1)
    rgb = np.dstack([b4, b3, b2])
    rgb_norm = np.clip(rgb / 2000, 0, 1)
    ax1.imshow(rgb_norm)
    ax1.set_title('Sentinel-2 Pre-Fire\nTrue Color RGB', fontsize=12)
    ax1.axis('off')

    # NDVI
    ax2 = plt.subplot(2, 4, 2)
    ndvi_plot = ax2.imshow(ndvi, cmap='RdYlGn', vmin=-0.2, vmax=0.9)
    ax2.set_title('NDVI (Vegetation Health)\nGreen=Healthy', fontsize=12)
    ax2.axis('off')
    plt.colorbar(ndvi_plot, ax=ax2, fraction=0.046)

    # NBR
    ax3 = plt.subplot(2, 4, 3)
    nbr_plot = ax3.imshow(nbr, cmap='RdYlGn', vmin=-0.5, vmax=0.8)
    ax3.set_title('NBR (Burn Ratio)\nGreen=Unburned', fontsize=12)
    ax3.axis('off')
    plt.colorbar(nbr_plot, ax=ax3, fraction=0.046)

# MODIS PRE-FIRE
modis_pre = DATA_DIR / "hermits_peak_modis_prefire.tif"
if modis_pre.exists():
    print(f"  Loading {modis_pre.name}...")
    with rasterio.open(modis_pre) as src:
        modis_ndvi = downsample(src.read(1)) * 0.0001

    ax4 = plt.subplot(2, 4, 4)
    modis_plot = ax4.imshow(modis_ndvi, cmap='RdYlGn', vmin=0, vmax=1)
    ax4.set_title('MODIS NDVI Pre-Fire\n(250m resolution)', fontsize=12)
    ax4.axis('off')
    plt.colorbar(modis_plot, ax=ax4, fraction=0.046)

# MODIS POST-FIRE
modis_post = DATA_DIR / "hermits_peak_modis_postfire.tif"
if modis_post.exists():
    print(f"  Loading {modis_post.name}...")
    with rasterio.open(modis_post) as src:
        modis_ndvi_post = downsample(src.read(1)) * 0.0001

    ax5 = plt.subplot(2, 4, 5)
    modis_plot2 = ax5.imshow(modis_ndvi_post, cmap='RdYlGn', vmin=0, vmax=1)
    ax5.set_title('MODIS NDVI Post-Fire\n(Aug-Dec 2022)', fontsize=12)
    ax5.axis('off')
    plt.colorbar(modis_plot2, ax=ax5, fraction=0.046)

    # CHANGE DETECTION
    if modis_pre.exists():
        ax6 = plt.subplot(2, 4, 6)
        change = modis_ndvi_post - modis_ndvi
        change_plot = ax6.imshow(change, cmap='RdBu_r', vmin=-0.3, vmax=0.3)
        ax6.set_title('NDVI Change (Post - Pre)\nRed=Vegetation Loss', fontsize=12)
        ax6.axis('off')
        plt.colorbar(change_plot, ax=ax6, fraction=0.046)

# LANDFIRE
landfire = LANDFIRE_DIR / "LF2020_HermitsPeak_multiband.tif"
if landfire.exists():
    print(f"  Loading {landfire.name}...")
    with rasterio.open(landfire) as src:
        fbfm = downsample(src.read(1), factor=2)  # Fuel model
        cbd = downsample(src.read(2), factor=2)   # Canopy density
        ch = downsample(src.read(3), factor=2)    # Canopy height

    ax7 = plt.subplot(2, 4, 7)
    fbfm_plot = ax7.imshow(fbfm, cmap='tab20', vmin=90, vmax=200)
    ax7.set_title('LANDFIRE Fuel Types\n(Static 2020 baseline)', fontsize=12)
    ax7.axis('off')
    plt.colorbar(fbfm_plot, ax=ax7, fraction=0.046, label='Fuel Code')

    ax8 = plt.subplot(2, 4, 8)
    cbd_plot = ax8.imshow(cbd, cmap='Greens', vmin=0, vmax=300)
    ax8.set_title('Canopy Bulk Density\n(kg/m³)', fontsize=12)
    ax8.axis('off')
    plt.colorbar(cbd_plot, ax=ax8, fraction=0.046)

plt.suptitle('Hermits Peak Fire Area - Satellite & LANDFIRE Data Overview', fontsize=16, fontweight='bold')
plt.tight_layout()

output_file = Path("data/satellite/data_overview.png")
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"\n✓ Visualization saved to: {output_file}")
print(f"\nOpen this file to see your data!")

# Print summary
print("\n" + "="*70)
print("DATA SUMMARY")
print("="*70)
print("""
What you're seeing:

TOP ROW (Pre-Fire 2020-2022):
  - Panel 1: True color satellite image (what your eye would see)
  - Panel 2: NDVI vegetation health (green = healthy forest)
  - Panel 3: NBR burn ratio (shows fuel/vegetation)
  - Panel 4: MODIS NDVI (coarser resolution, frequent updates)

BOTTOM ROW (Post-Fire + Baseline):
  - Panel 5: MODIS NDVI after fire (notice the changes?)
  - Panel 6: CHANGE DETECTION (red = vegetation lost to fire!)
  - Panel 7: LANDFIRE fuel types (your baseline map from 2020)
  - Panel 8: Canopy density (how dense the tree canopy is)

The dark/red areas in the change map show where the fire burned!

Your hackathon goal: Use the satellite changes to UPDATE the static
LANDFIRE map to reflect current conditions (drought, stress, fuel buildup).
""")

plt.close()
print("\nDone!")
