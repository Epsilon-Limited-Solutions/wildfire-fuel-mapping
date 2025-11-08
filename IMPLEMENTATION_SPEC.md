# Implementation Specification - Wildfire Fuel Mapping

## Project Goal
Create an enhanced fuel map by fusing LANDFIRE baseline data with satellite-detected changes (2020→2022), then validate against actual Hermits Peak fire burn severity.

---

# PATH 1: PRAGMATIC HACKATHON APPROACH (RECOMMENDED)
**Total Time: 3-4 hours**

## Overview
Generate static visualizations and analysis outputs. Present with slides or images. Focus on scientific rigor over UI polish.

## File Structure
```
hackathon/
├── analysis/
│   ├── 01_change_detection.py          # Detect vegetation changes 2020→2022
│   ├── 02_burn_severity.py              # Calculate actual burn severity
│   ├── 03_enhanced_fuel_map.py          # Create LANDFIRE + changes fusion
│   ├── 04_validation.py                 # Validate predictions vs reality
│   └── 05_visualization.py              # Generate all demo images
├── outputs/
│   ├── change_maps/                     # NDVI, NBR, NDMI change rasters
│   ├── burn_severity/                   # Actual fire severity from post-fire data
│   ├── enhanced_fuel/                   # Your improved fuel map
│   ├── validation/                      # Correlation plots, statistics
│   └── presentation/                    # Final demo images
└── analysis_summary.json                # Key metrics and statistics
```

## Step-by-Step Implementation

### STEP 1: Change Detection (45-60 min)
**File:** `analysis/01_change_detection.py`

**Inputs:**
- `data/satellite/hermits_peak_prefire_2020_2022.tif` (Sentinel-2)
- `data/satellite/hermits_peak_modis_prefire.tif` (MODIS baseline)
- `data/satellite/hermits_peak_modis_postfire.tif` (for time series)

**Process:**
1. Calculate baseline vegetation indices (2020):
   - NDVI mean from Sentinel-2 pre-fire composite
   - NBR mean
   - NDMI mean

2. Simulate 2022 pre-fire conditions using time series:
   - Use MODIS temporal trend to estimate Sentinel-2 values in early 2022
   - Calculate NDVI/NBR/NDMI for early 2022 (before fire started)

3. Calculate change maps:
   - NDVI_change = NDVI_2022_prefir - NDVI_2020
   - NBR_change = NBR_2022_prefire - NBR_2020
   - NDMI_change = NDMI_2022_prefire - NDMI_2020

4. Identify stressed areas:
   - NDVI decline > 0.1 = vegetation stress
   - NDMI decline > 0.15 = moisture stress
   - Combined stress score = weighted average

**Outputs:**
- `outputs/change_maps/ndvi_change.tif`
- `outputs/change_maps/nbr_change.tif`
- `outputs/change_maps/ndmi_change.tif`
- `outputs/change_maps/stress_score.tif`
- `outputs/change_maps/change_summary.png` (visualization)

**Command:**
```bash
python analysis/01_change_detection.py
```

---

### STEP 2: Burn Severity Calculation (30-45 min)
**File:** `analysis/02_burn_severity.py`

**Inputs:**
- `data/satellite/hermits_peak_prefire_2020_2022.tif`
- `data/satellite/hermits_peak_postfire_2022.tif`

**Process:**
1. Calculate dNBR (differenced Normalized Burn Ratio):
   - NBR_prefire from pre-fire Sentinel-2
   - NBR_postfire from post-fire Sentinel-2
   - dNBR = NBR_prefire - NBR_postfire

2. Classify burn severity (USGS standard):
   - dNBR < 0.1: Unburned
   - 0.1 - 0.27: Low severity
   - 0.27 - 0.44: Moderate-low
   - 0.44 - 0.66: Moderate-high
   - > 0.66: High severity

3. Create burn severity map

**Outputs:**
- `outputs/burn_severity/dnbr.tif`
- `outputs/burn_severity/burn_severity_classified.tif`
- `outputs/burn_severity/burn_severity_map.png`

**Command:**
```bash
python analysis/02_burn_severity.py
```

---

### STEP 3: Enhanced Fuel Map Creation (45-60 min)
**File:** `analysis/03_enhanced_fuel_map.py`

**Inputs:**
- `data/landfire/LF2020_HermitsPeak_multiband.tif` (FBFM40, CBD, CH)
- `outputs/change_maps/stress_score.tif`

**Process:**
1. Resample all data to common 30m grid (LANDFIRE resolution)

2. Create fuel adjustment factor:
   - Where stress_score > 0.2: increase fuel load estimate by 20-40%
   - Where NDVI declined significantly: flag for fuel model upgrade
   - Example: Grass (FBFM101) + high stress → Heavy grass (FBFM102)

3. Generate enhanced fuel map:
   - Base = LANDFIRE FBFM40
   - Adjust fuel categories based on detected stress
   - Increase CBD estimates in stressed areas
   - Flag areas of concern for managers

4. Create comparison:
   - Side-by-side: LANDFIRE 2020 vs Enhanced 2022

**Outputs:**
- `outputs/enhanced_fuel/enhanced_fbfm40.tif`
- `outputs/enhanced_fuel/fuel_adjustment_factor.tif`
- `outputs/enhanced_fuel/comparison_map.png`

**Command:**
```bash
python analysis/03_enhanced_fuel_map.py
```

---

### STEP 4: Validation (30-45 min)
**File:** `analysis/04_validation.py`

**Inputs:**
- `data/landfire/LF2020_HermitsPeak_multiband.tif` (baseline)
- `outputs/enhanced_fuel/enhanced_fbfm40.tif` (your prediction)
- `outputs/burn_severity/burn_severity_classified.tif` (ground truth)

**Process:**
1. Extract values at burned pixels only (exclude unburned areas)

2. Calculate correlation:
   - LANDFIRE fuel vs actual burn severity (R²)
   - Enhanced fuel vs actual burn severity (R²)
   - Compare improvement

3. Spatial analysis:
   - Where did enhanced map predict high fuel?
   - Did those areas burn more intensely?
   - Where did LANDFIRE miss?

4. Generate statistics:
   - Confusion matrix
   - Precision/Recall for high severity prediction
   - Overall accuracy improvement

**Outputs:**
- `outputs/validation/correlation_landfire.png` (scatter plot)
- `outputs/validation/correlation_enhanced.png` (scatter plot)
- `outputs/validation/spatial_comparison.png` (map overlay)
- `outputs/validation/metrics.json` (quantitative results)

**Command:**
```bash
python analysis/04_validation.py
```

---

### STEP 5: Presentation Visualizations (30-45 min)
**File:** `analysis/05_visualization.py`

**Process:**
Create final presentation-ready images:

1. **Overview Map** (4-panel):
   - LANDFIRE 2020 fuel map
   - Enhanced 2022 fuel map
   - Actual burn severity
   - Difference highlighting improvements

2. **Story Panels**:
   - "What Changed 2020→2022" (NDVI decline map)
   - "What We Predicted" (enhanced fuel)
   - "What Actually Happened" (fire severity)
   - "We Were Right" (overlay showing match)

3. **Validation Graphics**:
   - Correlation scatter plots
   - Bar chart: LANDFIRE R² vs Enhanced R²
   - Accuracy metrics comparison

4. **Summary Slide**:
   - Key statistics
   - % improvement over baseline
   - Business value proposition

**Outputs:**
- `outputs/presentation/01_overview.png`
- `outputs/presentation/02_change_detection.png`
- `outputs/presentation/03_prediction.png`
- `outputs/presentation/04_validation.png`
- `outputs/presentation/05_summary.png`

**Command:**
```bash
python analysis/05_visualization.py
```

---

## Final Summary Generation

**File:** `generate_summary.py`

Aggregates all metrics into:
- `analysis_summary.json` (for programmatic access)
- `RESULTS_SUMMARY.md` (human-readable)

**Contents:**
- Correlation improvements (R² increase)
- Accuracy metrics
- Key findings
- Areas where enhanced map outperformed
- Business value summary

---

## Presentation Flow

1. Show `01_overview.png`: "Here's the problem - static vs dynamic"
2. Show `02_change_detection.png`: "We detected these changes"
3. Show `03_prediction.png`: "We predicted high fuel here"
4. Show `04_validation.png`: "The fire proved us right"
5. Show `05_summary.png`: "X% more accurate, free data, scales globally"

---

# PATH 2: INTERACTIVE WEB APP APPROACH
**Total Time: 6-8 hours**

## Overview
Build a web application with interactive map showing layer overlays. Users can toggle between datasets, compare side-by-side, and explore spatial patterns.

## Technology Stack
- **Backend:** Python Flask (lightweight web server)
- **Frontend:** Folium (Python → Leaflet.js maps)
- **Alternative:** React + Leaflet (if comfortable with JS)
- **Tiles:** GeoTIFF → COG (Cloud Optimized GeoTIFF) → TileServer

## File Structure
```
hackathon/
├── webapp/
│   ├── app.py                           # Flask web server
│   ├── templates/
│   │   └── index.html                   # Main map interface
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── map_controls.js
│   └── utils/
│       ├── tiler.py                     # Convert GeoTIFFs to tiles
│       └── data_processor.py            # Pre-process data for web
├── tiles/                               # Map tiles (generated)
│   ├── landfire/
│   ├── sentinel_pre/
│   ├── sentinel_post/
│   ├── enhanced_fuel/
│   └── burn_severity/
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
```

## Step-by-Step Implementation

### STEP 1: Do the Analysis First (2-3 hours)
**Same as Path 1, Steps 1-4**

Run all analysis scripts to generate:
- Change detection maps
- Burn severity
- Enhanced fuel map
- Validation results

**Why:** Even the web app needs the analysis done first!

---

### STEP 2: Convert GeoTIFFs to Web Format (1-1.5 hours)
**File:** `webapp/utils/tiler.py`

**Process:**
1. Convert GeoTIFFs to Cloud Optimized GeoTIFF (COG)
2. Generate XYZ map tiles (zoom levels 8-15)
3. Create lightweight PNGs for web serving

**Libraries:**
- `rio-cogeo` (for COG conversion)
- `gdal2tiles.py` (for tile generation)
- OR use `titiler` for on-the-fly tiling

**Commands:**
```bash
# Convert to COG
rio cogeo create input.tif output_cog.tif

# Generate tiles
gdal2tiles.py -z 8-15 output_cog.tif tiles/layer_name/

# Or use TiTiler (easier, on-the-fly)
# Just serve COGs directly
```

**Outputs:**
- `tiles/landfire/{z}/{x}/{y}.png`
- `tiles/sentinel_pre/{z}/{x}/{y}.png`
- etc.

---

### STEP 3: Build Flask Backend (1-2 hours)
**File:** `webapp/app.py`

```python
from flask import Flask, render_template, jsonify
import rasterio
import folium

app = Flask(__name__)

@app.route('/')
def index():
    # Create base map centered on Hermits Peak
    m = folium.Map(
        location=[35.8, -105.6],
        zoom_start=11,
        tiles='OpenStreetMap'
    )

    # Add layer controls
    # Add GeoTIFF overlays
    # Add legend

    return m._repr_html_()

@app.route('/api/layer/<layer_name>')
def get_layer(layer_name):
    # Return layer metadata
    # Or serve tiles
    pass

@app.route('/api/stats')
def get_stats():
    # Return validation statistics
    # Load from analysis_summary.json
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Features:**
- Basemap (OpenStreetMap or Mapbox)
- Layer switcher for all datasets
- Opacity controls
- Click to get pixel values
- Legend for each layer
- Summary statistics panel

---

### STEP 4: Build Frontend Interface (2-3 hours)
**File:** `webapp/templates/index.html`

**Components:**

1. **Map Container**
   - Full-screen Leaflet map
   - Layer control (checkbox toggles)

2. **Layer Panel** (sidebar)
   ```
   ☐ LANDFIRE 2020 Baseline
   ☐ Enhanced Fuel Map 2022
   ☐ Sentinel-2 Pre-Fire (RGB)
   ☐ Sentinel-2 Post-Fire (RGB)
   ☐ NDVI Change 2020→2022
   ☐ Burn Severity (Actual)
   ```

3. **Comparison Mode**
   - Split-screen: LANDFIRE vs Enhanced
   - Slider to swipe between layers

4. **Info Panel**
   - Click on map → show values at that location
   - Display: Fuel type, NDVI, Burn severity, etc.

5. **Statistics Dashboard**
   - Show validation metrics
   - Correlation plots
   - Summary text

**Libraries:**
- Leaflet.js (core mapping)
- Leaflet.Control.Layers (layer switcher)
- Leaflet-side-by-side (comparison slider)
- Chart.js (for inline statistics)

---

### STEP 5: Docker Setup (Optional, 30 min)
**File:** `docker/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install GDAL and dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 5000

CMD ["python", "webapp/app.py"]
```

**File:** `docker/docker-compose.yml`

```yaml
version: '3.8'

services:
  webapp:
    build: ./docker
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./tiles:/app/tiles
    environment:
      - FLASK_ENV=development
```

**Commands:**
```bash
docker-compose up --build
# Access at http://localhost:5000
```

---

## Web App Features (Prioritized)

### Must Have (MVP):
- [x] Interactive map with basemap
- [x] Toggle layers on/off
- [x] Legend for each layer
- [x] Basic layer opacity control
- [x] Display validation statistics

### Nice to Have:
- [ ] Split-screen comparison mode
- [ ] Click for pixel-level info
- [ ] Time slider (if multiple time points)
- [ ] Export current view as image

### Stretch Goals:
- [ ] User can upload their own AOI
- [ ] Real-time tile generation
- [ ] 3D terrain visualization
- [ ] Animation of changes over time

---

## Implementation Timeline (Web App)

**Hour 1-2:** Run analysis scripts (Path 1, Steps 1-4)
**Hour 3:** Convert GeoTIFFs to web-friendly format
**Hour 4:** Build basic Flask app with one layer
**Hour 5:** Add all layers and controls
**Hour 6:** Build frontend UI and styling
**Hour 7:** Add statistics dashboard
**Hour 8:** Testing, debugging, deployment prep

---

# DECISION MATRIX

## Choose Path 1 If:
- ✅ Time is limited (< 6 hours)
- ✅ Focus is on analysis quality
- ✅ Presentation is via slides/screen share
- ✅ Want to minimize technical risk
- ✅ Judges care about scientific rigor

## Choose Path 2 If:
- ✅ Have 8+ hours available
- ✅ Comfortable with web development
- ✅ Live demo is required
- ✅ Want portfolio piece
- ✅ Judges value interactivity/polish

## Hybrid Approach:
1. Start with Path 1 (analysis)
2. If time remains, build simple Folium map
3. Folium can be created in 30-60 min
4. Embed in Jupyter notebook for quick demo

---

# RECOMMENDED: START WITH PATH 1

Get the science right first. If you have extra time, layer on the web interface.

**Reason:** A great analysis with static images beats a pretty UI with weak analysis every time.

---

# Quick Start Commands

## Path 1 (Pragmatic):
```bash
# Create analysis directory
mkdir -p analysis outputs/{change_maps,burn_severity,enhanced_fuel,validation,presentation}

# Run analysis pipeline
python analysis/01_change_detection.py
python analysis/02_burn_severity.py
python analysis/03_enhanced_fuel_map.py
python analysis/04_validation.py
python analysis/05_visualization.py

# Generate summary
python generate_summary.py

# Outputs ready in outputs/presentation/
```

## Path 2 (Web App):
```bash
# Run analysis first
python analysis/01_change_detection.py
# ... (all analysis steps)

# Convert to web format
python webapp/utils/tiler.py

# Start web server
cd webapp
python app.py

# Access at http://localhost:5000
```

---

# Success Criteria

## Path 1:
- [ ] 5 presentation-ready PNG images
- [ ] Correlation R² shows improvement
- [ ] Clear spatial patterns visible
- [ ] Story is compelling and backed by data
- [ ] Can present in 5 minutes

## Path 2:
- [ ] Web app loads without errors
- [ ] Can toggle between all layers
- [ ] Comparison mode works
- [ ] Statistics display correctly
- [ ] Runs on localhost reliably

---

# NEXT STEP

**Decision Required:** Which path?

**Recommendation:** Path 1 → Hybrid if time permits

**To start Path 1:**
```bash
mkdir -p analysis outputs/{change_maps,burn_severity,enhanced_fuel,validation,presentation}
```

Then I'll write `analysis/01_change_detection.py` as the first script.

Ready to begin?
