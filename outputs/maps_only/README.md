# Individual Map Visualizations

High-resolution, presentation-ready maps for the Hermits Peak wildfire fuel mapping project.

## Generated Maps

### Before/After Satellite Imagery

**NEW - Satellite Imagery Comparisons:**

1. **before_after_true_color.png** (15 MB)
   - Side-by-side comparison: 2020 (pre-fire) vs 2022 (post-fire)
   - True color RGB satellite imagery
   - Shows visual impact of 341,735 acre fire

2. **before_after_false_color.png** (15 MB)
   - False color (NIR-Red-Green) comparison
   - Highlights vegetation changes
   - Healthy vegetation appears bright red
   - Burned areas appear dark/brown

3. **before_after_4panel.png** (31 MB)
   - Complete 4-panel comparison
   - Top row: True color (before/after)
   - Bottom row: False color vegetation analysis (before/after)
   - Comprehensive visual analysis

### Change Detection Maps (2020-2022)

1. **stress_score_map.png** (20 MB)
   - Vegetation stress score combining NDVI, NBR, and NDMI changes
   - Scale: 0 (healthy) to 1 (severe stress)
   - Shows 25.6% high stress, 47.6% moderate stress

2. **ndvi_change_map.png** (15 MB)
   - Normalized Difference Vegetation Index change
   - Scale: -0.3 to +0.3
   - Negative values indicate vegetation loss

3. **nbr_change_map.png** (14 MB)
   - Normalized Burn Ratio change
   - Scale: -0.3 to +0.3
   - Negative values indicate fuel accumulation

4. **ndmi_change_map.png** (9.5 MB)
   - Normalized Difference Moisture Index change
   - Scale: -0.3 to +0.3
   - Negative values indicate moisture deficit

### Enhanced Fuel Maps

5. **fuel_load_map.png** (5.8 MB)
   - Enhanced fuel load factor
   - Scale: 1.0 (baseline) to 2.0 (double)
   - Mean increase: 46%

6. **fuel_risk_map.png** (197 KB)
   - Comprehensive fuel risk score
   - Scale: 0 (low risk) to 10 (extreme risk)
   - Combines fuel load, vegetation stress, and topography

### Burn Severity Maps (Actual Fire)

7. **burn_severity_map.png** (118 KB)
   - Actual burn severity measured by dNBR
   - Scale: 0 to 800
   - Higher values = more severe burning

8. **burn_severity_classified_map.png** (1.5 MB)
   - Classified burn severity
   - 6 classes: Unburned, Low, Moderate-Low, Moderate-High, High, Extreme
   - Used for validation

## Usage

These maps are designed for:
- **Presentations**: High resolution (300 DPI) for projection
- **Reports**: Publication-quality figures
- **Analysis**: Visual comparison of different metrics
- **Stakeholder Communication**: Clear, interpretable visualizations

## Technical Details

- **Format**: PNG
- **Resolution**: 300 DPI
- **Size**: 12" x 10" (3600 x 3000 pixels)
- **Colormap**:
  - Change maps: RdYlGn (Red-Yellow-Green)
  - Fuel maps: YlOrRd (Yellow-Orange-Red)
  - Burn severity: Hot (reversed)
- **Projection**: UTM Zone 13N (EPSG:32613)

## Key Findings Visualized

1. **Vegetation Stress**: 73.2% of area showed moderate to high stress
2. **Fuel Load Increase**: Mean 46% increase from baseline
3. **Burn Severity**: Strong correlation with enhanced fuel map (R² = 0.138)
4. **Improvement**: 43.1% better than LANDFIRE baseline alone

## File Locations

```
outputs/maps_only/
├── stress_score_map.png           # Combined vegetation stress
├── ndvi_change_map.png            # Vegetation loss
├── nbr_change_map.png             # Fuel accumulation
├── ndmi_change_map.png            # Moisture deficit
├── fuel_load_map.png              # Enhanced fuel load
├── fuel_risk_map.png              # Risk score
├── burn_severity_map.png          # Actual dNBR
└── burn_severity_classified_map.png  # Severity classes
```

## Regeneration

To regenerate these maps:

```bash
cd /Users/thomasduquemin/epsilon/applications/hackathon
source venv/bin/activate
python scripts/generate_individual_maps.py
```

## Citation

Hermits Peak-Calf Canyon Fire Fuel Mapping Analysis
Climate Hackathon 2025
Data: Sentinel-2, MODIS, LANDFIRE, NIFC
