# Project Structure

## Directory Layout

```
hackathon/
├── README.md                           # Main project documentation
├── STRUCTURE.md                        # This file
├── requirements.txt                    # Python dependencies
├── run.py                             # Main execution script
│
├── application/                        # Main application code
│   ├── __init__.py
│   ├── dashboard_app.py               # Streamlit dashboard
│   │
│   ├── preprocessing/                 # Data preprocessing modules
│   │   ├── __init__.py
│   │   └── preprocess_data.py         # Reproject, clip, normalize
│   │
│   ├── analysis/                      # Fuel mapping analysis
│   │   ├── __init__.py
│   │   └── fuel_mapping.py            # Change detection, validation
│   │
│   ├── visualization/                 # Visualization modules
│   │   ├── __init__.py
│   │   └── 05_create_interactive_map.py  # Folium HTML maps
│   │
│   └── utils/                         # Shared utilities
│       ├── __init__.py
│       ├── config.py                  # Configuration management
│       └── logger.py                  # Logging setup
│
├── scripts/                           # Data download scripts
│   ├── download_data.py               # Main download orchestrator
│   ├── download_fire_perimeter.py     # Fire boundary download
│   ├── download_landfire_direct.py    # LANDFIRE WMS download
│   ├── download_landfire_lfps.py      # LANDFIRE LFPS download
│   └── download_satellite_gee.py      # Google Earth Engine download
│
├── data/                              # All data files
│   ├── fire_perimeters/               # Fire boundary data
│   │   └── hermits_peak_area_of_interest.geojson
│   ├── landfire/                      # LANDFIRE fuel maps
│   │   ├── LF2020_FBFM40_*.tif
│   │   ├── LF2020_CBD_*.tif
│   │   └── LF2020_CH_*.tif
│   ├── satellite/                     # Satellite imagery
│   │   ├── sentinel2/                 # Sentinel-2 10m imagery
│   │   └── modis/                     # MODIS 250m imagery
│   ├── processed/                     # Preprocessed data (output)
│   │   ├── *_processed.tif           # Reprojected/clipped rasters
│   │   ├── ndvi_change.tif
│   │   ├── nbr_change.tif
│   │   ├── dnbr.tif
│   │   └── burn_severity_classified.tif
│   └── results/                       # Analysis results (output)
│       ├── fuel_increase_areas.tif
│       ├── change_magnitude.tif
│       └── fuel_hazard_enhanced.tif
│
├── outputs/                           # Final outputs for presentation
│   ├── figures/                       # Static PNG/PDF figures
│   │   ├── figure_main_comparison.png
│   │   ├── figure_validation_scatter.png
│   │   └── PRESENTATION_SUMMARY.png
│   ├── maps/                          # Interactive HTML maps
│   │   ├── hermits_peak_interactive_map.html
│   │   └── hermits_peak_comparison_map.html
│   └── reports/                       # Text reports and statistics
│       └── validation_results.txt
│
├── config/                            # Configuration files
│   └── credentials_template.env       # API keys template
│
├── docs/                              # Documentation
│   ├── PROJECT_SPEC.md                # Complete technical specification
│   ├── VISUALIZATION_GUIDE.md         # Visualization strategies
│   ├── DATA_DOWNLOAD_SUMMARY.md       # Data download instructions
│   ├── STATUS_REPORT.md               # Project status
│   └── HOW_TO_DOWNLOAD_LANDFIRE.md    # LANDFIRE specific guide
│
└── venv/                              # Python virtual environment
```

---

## Module Descriptions

### `application/`
Main application code organized by function.

#### `preprocessing/`
- **`preprocess_data.py`**: Loads raw data, reprojects to UTM, clips to AOI, calculates derived products
- Functions: reproject, clip, calculate indices (NDVI, NBR), compute burn severity

#### `analysis/`
- **`fuel_mapping.py`**: Detects fuel changes, creates enhanced maps, validates against burn severity
- Functions: change detection, fuel hazard mapping, correlation analysis

#### `visualization/`
- **`05_create_interactive_map.py`**: Creates Folium HTML maps with layer controls
- **`create_figures.py`**: (Optional) Static matplotlib figures

#### `utils/`
- **`config.py`**: Centralized configuration (paths, CRS, thresholds)
- **`logger.py`**: Logging setup and formatting

### `scripts/`
Standalone scripts for data acquisition. Run once to download data.

- **`download_data.py`**: Main orchestrator
- **`download_fire_perimeter.py`**: Creates fire AOI GeoJSON
- **`download_landfire_direct.py`**: Downloads LANDFIRE via WMS
- **`download_satellite_gee.py`**: Downloads Sentinel-2/MODIS via Google Earth Engine

### `data/`
All input and intermediate data. Organized by source.

**Input (manual/scripted downloads):**
- `fire_perimeters/`: Fire boundary vectors
- `landfire/`: LANDFIRE fuel maps (manual download required)
- `satellite/sentinel2/`: Sentinel-2 imagery (GEE export)
- `satellite/modis/`: MODIS vegetation indices (GEE export)

**Output (generated by pipeline):**
- `processed/`: Reprojected, clipped, normalized rasters
- `results/`: Enhanced fuel maps, change detection outputs

### `outputs/`
Final deliverables for presentation and demo.

- `figures/`: High-res static images for slides
- `maps/`: Interactive HTML maps for live demo
- `reports/`: Validation statistics and summaries

### `config/`
Configuration and credentials.

- `credentials_template.env`: Template for API keys (GEE, etc.)

### `docs/`
Comprehensive documentation.

- **`PROJECT_SPEC.md`**: Complete technical specification
- **`VISUALIZATION_GUIDE.md`**: Visualization strategies and demo narrative
- Other guides for data download and status

---

## Workflow

### 1. Setup (One-time)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Authenticate Google Earth Engine
earthengine authenticate
```

### 2. Data Download
```bash
# Manual: Download LANDFIRE from https://www.landfire.gov/viewer/
# Save to data/landfire/

# Automated: Download satellite data
python scripts/download_satellite_gee.py
# Then start export tasks in GEE, download from Google Drive to data/satellite/
```

### 3. Run Pipeline
```bash
# Run entire pipeline
python run.py --step all

# Or run individual steps
python run.py --step preprocess   # Preprocessing only
python run.py --step analysis     # Analysis only
python run.py --step visualize    # Visualizations only
```

### 4. Generate Outputs
```bash
# Create interactive maps
python run.py --step map

# Launch dashboard
python run.py --step dashboard
```

### 5. Demo
Open `outputs/maps/hermits_peak_comparison_map.html` in browser for live demo.

---

## Data Flow

```
Raw Data → Preprocessing → Analysis → Visualization
    ↓            ↓             ↓            ↓
LANDFIRE     Reproject     Detect      Static PNG
Sentinel-2   Clip          Changes     Interactive HTML
MODIS        Normalize     Validate    Dashboard
Fire AOI     Indices       Stats       Reports
```

**Detailed:**
1. **Raw Data** (`data/landfire/`, `data/satellite/`)
2. **Preprocessing** (`application/preprocessing/`) → `data/processed/`
3. **Analysis** (`application/analysis/`) → `data/results/`
4. **Visualization** (`application/visualization/`) → `outputs/`

---

## Key Configuration

Edit `application/utils/config.py` to change:

- **Paths**: Data directories, output locations
- **CRS**: Target coordinate reference system (default: UTM 13N)
- **Thresholds**: NDVI/NBR change detection thresholds
- **Fire metadata**: Name, dates, size, damage

---

## Adding New Features

### New preprocessing step:
1. Add method to `application/preprocessing/preprocess_data.py`
2. Call from `main()` function

### New analysis:
1. Add method to `application/analysis/fuel_mapping.py`
2. Or create new module in `application/analysis/`

### New visualization:
1. Create script in `application/visualization/`
2. Add function to `run.py` to execute it

---

## Output Locations

| Output Type | Location | Generated By |
|-------------|----------|--------------|
| Preprocessed rasters | `data/processed/` | `run.py --step preprocess` |
| Enhanced fuel maps | `data/results/` | `run.py --step analysis` |
| Static figures | `outputs/figures/` | `run.py --step visualize` |
| Interactive maps | `outputs/maps/` | `run.py --step map` |
| Validation reports | `outputs/reports/` | `run.py --step analysis` |

---

## Quick Reference

```bash
# Activate environment
source venv/bin/activate

# Run full pipeline
python run.py

# Check validation results
cat outputs/reports/validation_results.txt

# Open interactive map
open outputs/maps/hermits_peak_comparison_map.html

# Launch dashboard
python run.py --step dashboard
```

---

## Clean Build

To reset and start fresh:

```bash
# Remove generated outputs (keeps raw data)
rm -rf data/processed/* data/results/* outputs/*

# Re-run pipeline
python run.py --step all
```

---

## Dependencies

See `requirements.txt` for full list. Key packages:

- **Geospatial**: rasterio, geopandas, pyproj, fiona
- **Analysis**: numpy, pandas, scikit-learn, scipy
- **Visualization**: matplotlib, folium, streamlit, plotly
- **Data download**: earthengine-api, requests

---

## Notes

- **Virtual environment**: Always activate `venv` before running scripts
- **LANDFIRE**: Must be downloaded manually (scripted downloads have limitations)
- **GEE**: Requires authentication and approved account
- **CRS**: All data reprojected to UTM 13N for analysis, converted back to WGS84 for web maps
- **File sizes**: Raw data ~700MB, processed ~1GB, outputs ~100MB
