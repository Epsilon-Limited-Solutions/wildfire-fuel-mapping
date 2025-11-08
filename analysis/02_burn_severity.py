"""
Step 2: Burn Severity Analysis
Calculate actual fire burn severity using pre-fire and post-fire satellite data

This script:
1. Loads Sentinel-2 pre-fire and post-fire data
2. Calculates dNBR (differenced Normalized Burn Ratio)
3. Classifies burn severity using USGS standards
4. Creates burn severity maps

dNBR Classification (USGS):
  < 0.1:      Unburned
  0.1-0.27:   Low severity
  0.27-0.44:  Moderate-low severity
  0.44-0.66:  Moderate-high severity
  > 0.66:     High severity

Outputs:
- outputs/burn_severity/dnbr.tif
- outputs/burn_severity/burn_severity_classified.tif
- outputs/burn_severity/burn_severity_map.png
- outputs/burn_severity/burn_statistics.json
"""

import numpy as np
import rasterio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from pathlib import Path
import json

print("="*70)
print("STEP 2: BURN SEVERITY ANALYSIS")
print("="*70)

# Paths
DATA_DIR = Path("data/satellite")
OUTPUT_DIR = Path("outputs/burn_severity")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Input files
SENTINEL_PREFIRE = DATA_DIR / "hermits_peak_prefire_2020_2022.tif"
SENTINEL_POSTFIRE = DATA_DIR / "hermits_peak_postfire_2022.tif"

# Check files exist
print("\n1. Checking input files...")
for filepath in [SENTINEL_PREFIRE, SENTINEL_POSTFIRE]:
    if filepath.exists():
        print(f"  ✓ {filepath.name}")
    else:
        print(f"  ✗ MISSING: {filepath.name}")
        print(f"\nERROR: Post-fire data is required!")
        print(f"Please ensure hermits_peak_postfire_2022.tif is in {DATA_DIR}/")
        exit(1)

print("\n2. Loading pre-fire data...")
with rasterio.open(SENTINEL_PREFIRE) as src:
    # Band 8 is NBR (Normalized Burn Ratio)
    nbr_prefire = src.read(8)

    # Store metadata
    profile = src.profile.copy()
    profile.update(count=1, dtype='float32', compress='lzw')

    print(f"  Dimensions: {src.width} x {src.height} pixels")
    print(f"  NBR pre-fire range: {np.nanmin(nbr_prefire):.3f} to {np.nanmax(nbr_prefire):.3f}")
    print(f"  NBR pre-fire mean: {np.nanmean(nbr_prefire):.3f}")

print("\n3. Loading post-fire data...")
with rasterio.open(SENTINEL_POSTFIRE) as src:
    # Band 8 is NBR
    nbr_postfire = src.read(8)

    print(f"  NBR post-fire range: {np.nanmin(nbr_postfire):.3f} to {np.nanmax(nbr_postfire):.3f}")
    print(f"  NBR post-fire mean: {np.nanmean(nbr_postfire):.3f}")

print("\n4. Calculating dNBR (differenced NBR)...")
# dNBR = NBR_prefire - NBR_postfire
# Higher values indicate more severe burns
dnbr = nbr_prefire - nbr_postfire

print(f"  dNBR range: {np.nanmin(dnbr):.3f} to {np.nanmax(dnbr):.3f}")
print(f"  dNBR mean: {np.nanmean(dnbr):.3f}")

# Mask invalid values
dnbr = np.where(np.isfinite(dnbr), dnbr, np.nan)

print("\n5. Classifying burn severity...")
# USGS burn severity classification
burn_severity = np.zeros_like(dnbr)

# 0 = Unburned (dNBR < 0.1)
burn_severity[dnbr < 0.1] = 0

# 1 = Low severity (0.1 <= dNBR < 0.27)
burn_severity[(dnbr >= 0.1) & (dnbr < 0.27)] = 1

# 2 = Moderate-low severity (0.27 <= dNBR < 0.44)
burn_severity[(dnbr >= 0.27) & (dnbr < 0.44)] = 2

# 3 = Moderate-high severity (0.44 <= dNBR < 0.66)
burn_severity[(dnbr >= 0.44) & (dnbr < 0.66)] = 3

# 4 = High severity (dNBR >= 0.66)
burn_severity[dnbr >= 0.66] = 4

# Calculate percentages
total_pixels = np.sum(np.isfinite(dnbr))
unburned_pct = np.sum(burn_severity == 0) / total_pixels * 100
low_pct = np.sum(burn_severity == 1) / total_pixels * 100
mod_low_pct = np.sum(burn_severity == 2) / total_pixels * 100
mod_high_pct = np.sum(burn_severity == 3) / total_pixels * 100
high_pct = np.sum(burn_severity == 4) / total_pixels * 100

print(f"\n  Burn Severity Distribution:")
print(f"    Unburned:           {unburned_pct:5.1f}%")
print(f"    Low severity:       {low_pct:5.1f}%")
print(f"    Moderate-low:       {mod_low_pct:5.1f}%")
print(f"    Moderate-high:      {mod_high_pct:5.1f}%")
print(f"    High severity:      {high_pct:5.1f}%")
print(f"    ----")
print(f"    Burned (any level): {100 - unburned_pct:5.1f}%")

print("\n6. Saving outputs...")

# Save dNBR
with rasterio.open(OUTPUT_DIR / "dnbr.tif", 'w', **profile) as dst:
    dst.write(dnbr.astype('float32'), 1)
print(f"  ✓ Saved dnbr.tif")

# Save classified burn severity
profile_int = profile.copy()
profile_int.update(dtype='int16', nodata=-9999)
with rasterio.open(OUTPUT_DIR / "burn_severity_classified.tif", 'w', **profile_int) as dst:
    dst.write(burn_severity.astype('int16'), 1)
print(f"  ✓ Saved burn_severity_classified.tif")

print("\n7. Creating visualizations...")

# Downsample for visualization
def downsample(arr, factor=5):
    return arr[::factor, ::factor]

fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('Hermits Peak Fire - Burn Severity Analysis', fontsize=16, fontweight='bold')

# NBR Pre-fire
ax1 = axes[0, 0]
im1 = ax1.imshow(downsample(nbr_prefire), cmap='RdYlGn', vmin=-0.5, vmax=0.8)
ax1.set_title('NBR Pre-Fire (2020-2022)\nBaseline conditions', fontsize=12)
ax1.axis('off')
plt.colorbar(im1, ax=ax1, fraction=0.046, label='NBR')

# NBR Post-fire
ax2 = axes[0, 1]
im2 = ax2.imshow(downsample(nbr_postfire), cmap='RdYlGn', vmin=-0.5, vmax=0.8)
ax2.set_title('NBR Post-Fire (Aug-Dec 2022)\nAfter fire', fontsize=12)
ax2.axis('off')
plt.colorbar(im2, ax=ax2, fraction=0.046, label='NBR')

# dNBR (continuous)
ax3 = axes[1, 0]
im3 = ax3.imshow(downsample(dnbr), cmap='hot', vmin=-0.1, vmax=1.0)
ax3.set_title('dNBR (Differenced NBR)\nHigher = More severe burn', fontsize=12)
ax3.axis('off')
plt.colorbar(im3, ax=ax3, fraction=0.046, label='dNBR')

# Burn severity classified
ax4 = axes[1, 1]
# Custom colormap for severity classes
colors = ['#2E7D32', '#FDD835', '#FB8C00', '#E53935', '#5D0000']  # Green to dark red
cmap_severity = ListedColormap(colors)
bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
norm = BoundaryNorm(bounds, cmap_severity.N)

im4 = ax4.imshow(downsample(burn_severity), cmap=cmap_severity, norm=norm)
ax4.set_title('Burn Severity Classification\n(USGS Standard)', fontsize=12)
ax4.axis('off')

# Custom legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2E7D32', label=f'Unburned ({unburned_pct:.1f}%)'),
    Patch(facecolor='#FDD835', label=f'Low ({low_pct:.1f}%)'),
    Patch(facecolor='#FB8C00', label=f'Moderate-Low ({mod_low_pct:.1f}%)'),
    Patch(facecolor='#E53935', label=f'Moderate-High ({mod_high_pct:.1f}%)'),
    Patch(facecolor='#5D0000', label=f'High ({high_pct:.1f}%)')
]
ax4.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "burn_severity_map.png", dpi=150, bbox_inches='tight')
print(f"  ✓ Saved burn_severity_map.png")
plt.close()

print("\n8. Generating statistics...")

stats = {
    "dnbr": {
        "mean": float(np.nanmean(dnbr)),
        "std": float(np.nanstd(dnbr)),
        "min": float(np.nanmin(dnbr)),
        "max": float(np.nanmax(dnbr))
    },
    "burn_severity_distribution": {
        "unburned_percent": float(unburned_pct),
        "low_severity_percent": float(low_pct),
        "moderate_low_percent": float(mod_low_pct),
        "moderate_high_percent": float(mod_high_pct),
        "high_severity_percent": float(high_pct),
        "total_burned_percent": float(100 - unburned_pct)
    },
    "nbr_change": {
        "pre_fire_mean": float(np.nanmean(nbr_prefire)),
        "post_fire_mean": float(np.nanmean(nbr_postfire)),
        "mean_change": float(np.nanmean(dnbr))
    }
}

with open(OUTPUT_DIR / "burn_statistics.json", 'w') as f:
    json.dump(stats, f, indent=2)
print(f"  ✓ Saved burn_statistics.json")

print("\n" + "="*70)
print("BURN SEVERITY ANALYSIS COMPLETE")
print("="*70)
print(f"\nOutputs saved to: {OUTPUT_DIR}")
print("\nKey Findings:")
print(f"  - Total area burned: {100 - unburned_pct:.1f}%")
print(f"  - High severity burn: {high_pct:.1f}%")
print(f"  - Moderate-high burn: {mod_high_pct:.1f}%")
print(f"  - Mean dNBR: {stats['dnbr']['mean']:.3f}")

print("\nInterpretation:")
if high_pct + mod_high_pct > 20:
    print(f"  ⚠️  Severe fire impact - {high_pct + mod_high_pct:.1f}% burned at moderate-high or high severity")
else:
    print(f"  ✓ Moderate fire impact - {high_pct + mod_high_pct:.1f}% high severity")

print("\nThis burn severity data will be used to validate fuel predictions in Step 4.")
print("\nNext step: Run 03_enhanced_fuel_map.py to create improved fuel predictions")
print("="*70)
