# Analysis Pipeline

This directory contains the analysis scripts for the wildfire fuel mapping project.

## Directory Structure

```
analysis/           # Analysis scripts (run in order)
├── 01_change_detection.py
├── 02_burn_severity.py
├── 03_enhanced_fuel_map.py
├── 04_validation.py
└── 05_visualization.py

outputs/            # All outputs organized by type
├── change_maps/        # Vegetation change detection results
├── burn_severity/      # Actual fire severity analysis
├── enhanced_fuel/      # Your improved fuel maps
├── validation/         # Correlation plots and statistics
└── presentation/       # Final demo-ready images
```

## How to Run

Execute scripts in numerical order:

```bash
# Activate environment
source venv/bin/activate

# Run analysis pipeline
python analysis/01_change_detection.py
python analysis/02_burn_severity.py
python analysis/03_enhanced_fuel_map.py
python analysis/04_validation.py
python analysis/05_visualization.py
```

Each script:
- Reads from `data/` directory
- Writes outputs to appropriate `outputs/` subdirectory
- Can be run independently (checks for dependencies)
- Prints progress and summary statistics

## Output Files

### outputs/change_maps/
- `ndvi_change.tif` - NDVI decline 2020→2022
- `nbr_change.tif` - NBR change (burn ratio)
- `ndmi_change.tif` - Moisture stress change
- `stress_score.tif` - Combined stress indicator
- `change_summary.png` - Visualization

### outputs/burn_severity/
- `dnbr.tif` - Differenced NBR (pre vs post fire)
- `burn_severity_classified.tif` - Severity categories
- `burn_severity_map.png` - Visualization

### outputs/enhanced_fuel/
- `enhanced_fbfm40.tif` - Your improved fuel map
- `fuel_adjustment_factor.tif` - Where/how much fuel changed
- `comparison_map.png` - Side-by-side LANDFIRE vs Enhanced

### outputs/validation/
- `correlation_landfire.png` - Baseline performance
- `correlation_enhanced.png` - Your performance
- `spatial_comparison.png` - Map overlay
- `metrics.json` - Quantitative statistics

### outputs/presentation/
- `01_overview.png` - 4-panel overview
- `02_change_detection.png` - What changed
- `03_prediction.png` - What you predicted
- `04_validation.png` - Proof it worked
- `05_summary.png` - Key statistics

## Time Estimates

- 01_change_detection.py: 45-60 min
- 02_burn_severity.py: 30-45 min
- 03_enhanced_fuel_map.py: 45-60 min
- 04_validation.py: 30-45 min
- 05_visualization.py: 30-45 min

**Total: 3-4 hours**
