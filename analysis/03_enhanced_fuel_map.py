"""
Step 3: Enhanced Fuel Map Creation
Combine LANDFIRE baseline with satellite-detected stress to create improved fuel map

This script:
1. Loads LANDFIRE 2020 baseline (FBFM40, CBD, CH)
2. Loads stress scores from change detection
3. Creates fuel adjustment factors based on stress
4. Generates enhanced fuel map
5. Compares LANDFIRE vs Enhanced side-by-side

Logic:
- High stress areas → Higher fuel load estimate
- Low NDVI + high stress → Upgrade fuel model category
- Dry conditions (low NDMI) → Increase fire risk factor

Outputs:
- outputs/enhanced_fuel/enhanced_fbfm40.tif
- outputs/enhanced_fuel/fuel_risk_score.tif
- outputs/enhanced_fuel/comparison_map.png
- outputs/enhanced_fuel/enhancement_statistics.json
"""

import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
import json

print("="*70)
print("STEP 3: ENHANCED FUEL MAP CREATION")
print("="*70)

# Paths
LANDFIRE_DIR = Path("data/landfire")
CHANGE_DIR = Path("outputs/change_maps")
OUTPUT_DIR = Path("outputs/enhanced_fuel")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Input files
LANDFIRE_FILE = LANDFIRE_DIR / "LF2020_HermitsPeak_multiband.tif"
STRESS_SCORE = CHANGE_DIR / "stress_score.tif"
NDVI_CHANGE = CHANGE_DIR / "ndvi_change.tif"
NDMI_CHANGE = CHANGE_DIR / "ndmi_change.tif"

# Check files exist
print("\n1. Checking input files...")
required_files = [LANDFIRE_FILE, STRESS_SCORE, NDVI_CHANGE, NDMI_CHANGE]
for filepath in required_files:
    if filepath.exists():
        print(f"  ✓ {filepath.name}")
    else:
        print(f"  ✗ MISSING: {filepath.name}")
        exit(1)

print("\n2. Loading LANDFIRE baseline data...")
with rasterio.open(LANDFIRE_FILE) as src:
    # LANDFIRE has 3 bands: FBFM40, CBD, CH
    fbfm40 = src.read(1)  # Fire Behavior Fuel Model
    cbd = src.read(2)     # Canopy Bulk Density
    ch = src.read(3)      # Canopy Height

    landfire_profile = src.profile.copy()
    landfire_transform = src.transform
    landfire_crs = src.crs

    print(f"  LANDFIRE dimensions: {src.width} x {src.height}")
    print(f"  FBFM40 range: {np.min(fbfm40)} to {np.max(fbfm40)}")
    print(f"  CBD range: {np.min(cbd)} to {np.max(cbd)} kg/m³")
    print(f"  CH range: {np.min(ch)} to {np.max(ch)} m")

print("\n3. Loading stress data...")
with rasterio.open(STRESS_SCORE) as src:
    stress_profile = src.profile
    stress_transform = src.transform
    stress_crs = src.crs

print(f"  Stress data dimensions: {stress_profile['width']} x {stress_profile['height']}")
print(f"  Stress CRS: {stress_crs}")
print(f"  LANDFIRE CRS: {landfire_crs}")

print("\n4. Reprojecting stress data to match LANDFIRE...")
# Need to reproject satellite data to LANDFIRE coordinate system

# Read stress score
with rasterio.open(STRESS_SCORE) as src:
    stress_score_orig = src.read(1)

# Reproject stress to LANDFIRE grid
stress_score_reproj = np.empty((landfire_profile['height'], landfire_profile['width']), dtype=np.float32)

with rasterio.open(STRESS_SCORE) as src:
    reproject(
        source=rasterio.band(src, 1),
        destination=stress_score_reproj,
        src_transform=stress_transform,
        src_crs=stress_crs,
        dst_transform=landfire_transform,
        dst_crs=landfire_crs,
        resampling=Resampling.bilinear
    )

print(f"  ✓ Stress data reprojected to LANDFIRE grid")
print(f"  Stress score range after reprojection: {np.nanmin(stress_score_reproj):.3f} to {np.nanmax(stress_score_reproj):.3f}")

# Reproject NDVI change
ndvi_change_reproj = np.empty_like(stress_score_reproj)
with rasterio.open(NDVI_CHANGE) as src:
    reproject(
        source=rasterio.band(src, 1),
        destination=ndvi_change_reproj,
        src_transform=stress_transform,
        src_crs=stress_crs,
        dst_transform=landfire_transform,
        dst_crs=landfire_crs,
        resampling=Resampling.bilinear
    )

# Reproject NDMI change
ndmi_change_reproj = np.empty_like(stress_score_reproj)
with rasterio.open(NDMI_CHANGE) as src:
    reproject(
        source=rasterio.band(src, 1),
        destination=ndmi_change_reproj,
        src_transform=stress_transform,
        src_crs=stress_crs,
        dst_transform=landfire_transform,
        dst_crs=landfire_crs,
        resampling=Resampling.bilinear
    )

print("\n5. Creating fuel risk adjustment factors...")

# Create fuel risk score (0-100 scale for easier interpretation)
# Combines stress, vegetation decline, and moisture deficit

# Normalize components to 0-1
stress_norm = np.clip(stress_score_reproj, 0, 1)
ndvi_stress_norm = np.clip(ndvi_change_reproj / 0.5, 0, 1)  # NDVI change > 0.5 = max stress
ndmi_stress_norm = np.clip(ndmi_change_reproj / 0.5, 0, 1)  # NDMI change > 0.5 = max stress

# Combined risk score (0-100)
fuel_risk_score = (
    40 * stress_norm +           # 40% weight: overall stress
    35 * ndvi_stress_norm +      # 35% weight: vegetation decline
    25 * ndmi_stress_norm        # 25% weight: moisture deficit
)

print(f"  Fuel risk score range: {np.nanmin(fuel_risk_score):.1f} to {np.nanmax(fuel_risk_score):.1f}")
print(f"  Mean fuel risk: {np.nanmean(fuel_risk_score):.1f}")

# Calculate risk distribution
high_risk_pct = np.sum(fuel_risk_score > 60) / fuel_risk_score.size * 100
mod_risk_pct = np.sum((fuel_risk_score > 40) & (fuel_risk_score <= 60)) / fuel_risk_score.size * 100
low_risk_pct = np.sum(fuel_risk_score <= 40) / fuel_risk_score.size * 100

print(f"\n  Fuel Risk Distribution:")
print(f"    High risk (>60):    {high_risk_pct:5.1f}%")
print(f"    Moderate risk (40-60): {mod_risk_pct:5.1f}%")
print(f"    Low risk (<40):     {low_risk_pct:5.1f}%")

print("\n6. Creating enhanced fuel model...")

# Enhanced FBFM40
# Where stress is high, we flag areas for upgraded fuel models
# This is a simplified approach - in practice, you'd have fuel model lookup tables

enhanced_fbfm40 = fbfm40.copy()

# Fuel model adjustment logic:
# For high stress areas (risk > 60), flag for potential upgrade
# We create a continuous risk surface rather than discrete fuel model changes
# This preserves more information for validation

# Create a fuel load adjustment factor (1.0 = no change, 2.0 = double)
fuel_load_factor = 1.0 + (fuel_risk_score / 100)  # Range: 1.0 to 2.0

print(f"  Fuel load adjustment factor range: {np.nanmin(fuel_load_factor):.2f}x to {np.nanmax(fuel_load_factor):.2f}x")
print(f"  Mean adjustment: {np.nanmean(fuel_load_factor):.2f}x")

# Enhanced canopy bulk density (adjusted by stress)
enhanced_cbd = cbd * fuel_load_factor
enhanced_cbd = np.clip(enhanced_cbd, 0, 1000)  # Cap at reasonable max

print(f"  Enhanced CBD range: {np.nanmin(enhanced_cbd):.1f} to {np.nanmax(enhanced_cbd):.1f} kg/m³")
print(f"  Original CBD mean: {np.nanmean(cbd):.1f}, Enhanced CBD mean: {np.nanmean(enhanced_cbd):.1f}")

print("\n7. Saving outputs...")

# Save fuel risk score
profile_out = landfire_profile.copy()
profile_out.update(count=1, dtype='float32', compress='lzw')

with rasterio.open(OUTPUT_DIR / "fuel_risk_score.tif", 'w', **profile_out) as dst:
    dst.write(fuel_risk_score.astype('float32'), 1)
print(f"  ✓ Saved fuel_risk_score.tif")

# Save enhanced FBFM40
profile_int = landfire_profile.copy()
profile_int.update(count=1, dtype='int16', compress='lzw')

with rasterio.open(OUTPUT_DIR / "enhanced_fbfm40.tif", 'w', **profile_int) as dst:
    dst.write(enhanced_fbfm40.astype('int16'), 1)
print(f"  ✓ Saved enhanced_fbfm40.tif")

# Save enhanced CBD
with rasterio.open(OUTPUT_DIR / "enhanced_cbd.tif", 'w', **profile_out) as dst:
    dst.write(enhanced_cbd.astype('float32'), 1)
print(f"  ✓ Saved enhanced_cbd.tif")

# Save fuel load factor
with rasterio.open(OUTPUT_DIR / "fuel_load_factor.tif", 'w', **profile_out) as dst:
    dst.write(fuel_load_factor.astype('float32'), 1)
print(f"  ✓ Saved fuel_load_factor.tif")

print("\n8. Creating comparison visualizations...")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Enhanced Fuel Mapping - LANDFIRE Baseline vs Satellite-Enhanced',
             fontsize=16, fontweight='bold')

# LANDFIRE FBFM40
ax1 = axes[0, 0]
im1 = ax1.imshow(fbfm40, cmap='tab20c', vmin=90, vmax=200)
ax1.set_title('LANDFIRE 2020\nFuel Model (FBFM40)', fontsize=12)
ax1.axis('off')
plt.colorbar(im1, ax=ax1, fraction=0.046, label='Fuel Code')

# LANDFIRE CBD
ax2 = axes[0, 1]
im2 = ax2.imshow(cbd, cmap='Greens', vmin=0, vmax=300)
ax2.set_title('LANDFIRE 2020\nCanopy Bulk Density', fontsize=12)
ax2.axis('off')
plt.colorbar(im2, ax=ax2, fraction=0.046, label='kg/m³')

# Stress Score
ax3 = axes[0, 2]
im3 = ax3.imshow(stress_score_reproj, cmap='YlOrRd', vmin=0, vmax=1)
ax3.set_title('Detected Stress\n(from Satellite 2020-2022)', fontsize=12)
ax3.axis('off')
plt.colorbar(im3, ax=ax3, fraction=0.046, label='Stress (0-1)')

# Fuel Risk Score
ax4 = axes[1, 0]
im4 = ax4.imshow(fuel_risk_score, cmap='YlOrRd', vmin=0, vmax=100)
ax4.set_title('Enhanced Fuel Risk Score\n(Higher = More fuel/risk)', fontsize=12)
ax4.axis('off')
plt.colorbar(im4, ax=ax4, fraction=0.046, label='Risk (0-100)')

# Enhanced CBD
ax5 = axes[1, 1]
im5 = ax5.imshow(enhanced_cbd, cmap='Greens', vmin=0, vmax=300)
ax5.set_title('Enhanced CBD\n(Adjusted for stress)', fontsize=12)
ax5.axis('off')
plt.colorbar(im5, ax=ax5, fraction=0.046, label='kg/m³')

# CBD Change
ax6 = axes[1, 2]
cbd_change = enhanced_cbd - cbd
im6 = ax6.imshow(cbd_change, cmap='RdBu_r', vmin=-50, vmax=50)
ax6.set_title('CBD Adjustment\n(Red = Increased fuel estimate)', fontsize=12)
ax6.axis('off')
plt.colorbar(im6, ax=ax6, fraction=0.046, label='kg/m³ change')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "comparison_map.png", dpi=150, bbox_inches='tight')
print(f"  ✓ Saved comparison_map.png")
plt.close()

print("\n9. Generating statistics...")

stats = {
    "fuel_risk_score": {
        "mean": float(np.nanmean(fuel_risk_score)),
        "std": float(np.nanstd(fuel_risk_score)),
        "high_risk_percent": float(high_risk_pct),
        "moderate_risk_percent": float(mod_risk_pct),
        "low_risk_percent": float(low_risk_pct)
    },
    "fuel_load_adjustment": {
        "mean_factor": float(np.nanmean(fuel_load_factor)),
        "max_factor": float(np.nanmax(fuel_load_factor)),
        "areas_increased_20pct": float(np.sum(fuel_load_factor > 1.2) / fuel_load_factor.size * 100)
    },
    "cbd_enhancement": {
        "original_mean": float(np.nanmean(cbd)),
        "enhanced_mean": float(np.nanmean(enhanced_cbd)),
        "mean_increase": float(np.nanmean(enhanced_cbd - cbd)),
        "percent_increase": float((np.nanmean(enhanced_cbd) - np.nanmean(cbd)) / np.nanmean(cbd) * 100)
    }
}

with open(OUTPUT_DIR / "enhancement_statistics.json", 'w') as f:
    json.dump(stats, f, indent=2)
print(f"  ✓ Saved enhancement_statistics.json")

print("\n" + "="*70)
print("ENHANCED FUEL MAP CREATION COMPLETE")
print("="*70)
print(f"\nOutputs saved to: {OUTPUT_DIR}")
print("\nKey Findings:")
print(f"  - High risk areas: {high_risk_pct:.1f}%")
print(f"  - Mean fuel load increase: {(np.nanmean(fuel_load_factor) - 1) * 100:.1f}%")
print(f"  - CBD increased by: {stats['cbd_enhancement']['percent_increase']:.1f}%")
print(f"  - Areas with >20% fuel increase: {stats['fuel_load_adjustment']['areas_increased_20pct']:.1f}%")

print("\nInterpretation:")
print("  Your enhanced fuel map now accounts for:")
print("    ✓ Vegetation stress detected by satellites")
print("    ✓ Moisture deficit (dry conditions)")
print("    ✓ Vegetation decline from 2020 baseline")
print("\n  LANDFIRE 2020 was static - your map reflects 2022 pre-fire conditions")

print("\nNext step: Run 04_validation.py to prove your enhanced map is better!")
print("="*70)
