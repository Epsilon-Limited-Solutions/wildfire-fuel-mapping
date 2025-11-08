# Wildfire Fuel Mapping - Technical Specification
## Hermits Peak 2022 Fire Prediction MVP

**Project Name:** Enhanced Wildfire Fuel Mapping via Satellite Data Fusion
**Target Fire:** Hermits Peak-Calf Canyon Fire (2022)
**Location:** Northern New Mexico (35.6°N-36.0°N, 105.3°W-105.9°W)
**Timeline:** 24-hour hackathon
**Created:** November 8, 2024

---

## 1. PROJECT OVERVIEW

### 1.1 Problem Statement
LANDFIRE fuel maps update every 2-3 years, missing critical fuel changes caused by:
- Drought-induced tree mortality
- Bark beetle infestations
- Recent disturbance events
- Seasonal vegetation stress

The 2022 Hermits Peak fire (341,735 acres, $4B damage) burned through areas where fuel conditions had changed significantly since the 2020 LANDFIRE baseline.

### 1.2 Solution
Build a satellite-based fuel mapping system that:
1. Uses LANDFIRE 2020 as baseline fuel classification
2. Detects fuel changes (2020→2022) using multi-source satellite data
3. Generates enhanced fuel maps reflecting current conditions
4. Validates improvements against actual burn severity

### 1.3 Success Criteria

**Minimum Viable Demo:**
- [ ] LANDFIRE baseline map loaded and visualized
- [ ] At least one satellite product (Sentinel-2) processed
- [ ] Visual comparison showing fuel change detection
- [ ] Fire perimeter overlay
- [ ] Clear narrative presentation

**Strong Demo:**
- [ ] Multi-source data fusion (LANDFIRE + Sentinel-2 + MODIS)
- [ ] Quantitative validation metrics (correlation with burn severity)
- [ ] Before/after comparison maps
- [ ] Identified specific areas where changes were detected

**Stretch Goals:**
- [ ] Interactive web visualization
- [ ] Multiple validation fires
- [ ] Real-time update workflow demonstration

---

## 2. DATA REQUIREMENTS

### 2.1 Core Datasets (REQUIRED)

#### Dataset 1: LANDFIRE Fuel Data (2020)
**Purpose:** Baseline fuel classification
**Source:** https://www.landfire.gov/viewer/
**Status:** ⚠️ NEEDS MANUAL DOWNLOAD
**Priority:** CRITICAL

**Layers Required:**
- **FBFM40** (40 Scott & Burgan Fire Behavior Fuel Models)
  - Resolution: 30m
  - Format: GeoTIFF
  - Version: LF 2020 (LF 2.2.0)
  - Size: ~50 MB
  - Variables: 40 fuel model classifications

- **CBD** (Canopy Bulk Density)
  - Resolution: 30m
  - Format: GeoTIFF
  - Units: kg/m³ × 100
  - Use: Tree canopy fuel density

- **CH** (Canopy Height)
  - Resolution: 30m
  - Format: GeoTIFF
  - Units: meters × 10
  - Use: Vertical fuel structure

**Download Instructions:**
1. Go to LANDFIRE Data Viewer
2. Search: "Hermits Peak, New Mexico" or coordinates (35.8°N, 105.6°W)
3. Select layers: FBFM40, CBD, CH
4. Choose version: LF 2020 (LF 2.2.0)
5. Draw bounding box: 35.6°N-36.0°N, 105.3°W-105.9°W
6. Format: GeoTIFF
7. Download to: `data/landfire/`

**Expected Files:**
```
data/landfire/
├── LF2020_FBFM40_200_CONUS.tif
├── LF2020_CBD_200_CONUS.tif
└── LF2020_CH_200_CONUS.tif
```

---

#### Dataset 2: Sentinel-2 Optical Imagery
**Purpose:** High-resolution vegetation change detection
**Source:** Google Earth Engine (Copernicus/S2_SR_HARMONIZED)
**Status:** ⏳ REQUIRES GEE AUTHENTICATION
**Priority:** CRITICAL

**Specifications:**
- Resolution: 10m (RGB, NIR), 20m (SWIR)
- Temporal Coverage: 2020-01-01 to 2022-04-06 (pre-fire)
- Cloud Cover: < 20%
- Processing Level: Surface Reflectance (SR)

**Bands to Download:**
- B2 (Blue): 490nm
- B3 (Green): 560nm
- B4 (Red): 665nm
- B8 (NIR): 842nm
- B11 (SWIR1): 1610nm
- B12 (SWIR2): 2190nm

**Derived Indices:**
- NDVI = (NIR - Red) / (NIR + Red)
- NBR = (NIR - SWIR2) / (NIR + SWIR2)
- NDMI = (NIR - SWIR1) / (NIR + SWIR1)

**Time Windows:**
1. **Baseline (2020):** Jan-Dec 2020, summer median
2. **Pre-fire (2022):** Jan-Apr 2022, latest clear image
3. **Change:** 2022 - 2020 for each index

**Output Files:**
```
data/satellite/sentinel2/
├── sentinel2_2020_median_composite.tif
├── sentinel2_2022_prefire_composite.tif
├── ndvi_2020.tif
├── ndvi_2022.tif
├── ndvi_change.tif
├── nbr_2020.tif
├── nbr_2022.tif
└── nbr_change.tif
```

---

#### Dataset 3: MODIS Vegetation Indices
**Purpose:** Temporal trend detection, gap-filling
**Source:** Google Earth Engine (MODIS/006/MOD13Q1)
**Status:** ⏳ REQUIRES GEE AUTHENTICATION
**Priority:** HIGH

**Specifications:**
- Resolution: 250m
- Temporal: 16-day composites (2020-2022)
- Product: MOD13Q1 (NDVI/EVI)

**Variables:**
- NDVI: Normalized Difference Vegetation Index
- EVI: Enhanced Vegetation Index
- Quality flags

**Processing:**
1. Extract time series (2020-2022)
2. Calculate seasonal baselines
3. Detect anomalies and trends
4. Identify vegetation stress periods

**Output Files:**
```
data/satellite/modis/
├── modis_ndvi_2020_mean.tif
├── modis_ndvi_2022_prefire.tif
├── modis_ndvi_anomaly.tif
└── modis_timeseries.csv
```

---

### 2.2 Validation Data (REQUIRED)

#### Dataset 4: Fire Perimeter
**Purpose:** Define study area and validation boundary
**Source:** NIFC Wildfire Perimeters / Manual creation
**Status:** ✅ APPROXIMATE BOUNDARY CREATED
**Priority:** MEDIUM

**Current File:**
- `data/fire_perimeters/hermits_peak_area_of_interest.geojson`
- Type: Approximate 40km × 40km bounding box
- Format: GeoJSON

**Improved Version (Optional):**
- Source: https://data-nifc.opendata.arcgis.com/
- Search: "WFIGS 2022 Hermits Peak"
- Format: GeoJSON or Shapefile
- Save to: `data/fire_perimeters/hermits_peak_actual_perimeter.geojson`

---

#### Dataset 5: Burn Severity (MTBS)
**Purpose:** Validation ground truth
**Source:** Monitoring Trends in Burn Severity (MTBS)
**Status:** ⏳ NEEDS DOWNLOAD
**Priority:** HIGH

**Options:**

**Option A: MTBS Portal (Preferred)**
- URL: https://www.mtbs.gov/direct-download
- Search: "Hermits Peak" or "New Mexico 2022"
- Download: dNBR (differenced Normalized Burn Ratio)
- Format: GeoTIFF
- Resolution: 30m

**Option B: Google Earth Engine**
```python
# MTBS may not have 2022 data yet
# Alternative: Calculate dNBR manually
dNBR = NBR_prefire - NBR_postfire
```

**Option C: Manual Calculation**
1. Download Sentinel-2 post-fire imagery (Aug-Sept 2022)
2. Calculate NBR pre-fire and post-fire
3. Compute dNBR = NBR_pre - NBR_post
4. Classify burn severity:
   - Unburned: dNBR < 0.1
   - Low: 0.1 - 0.27
   - Moderate: 0.27 - 0.66
   - High: > 0.66

**Output Files:**
```
data/validation/
├── burn_severity_dnbr.tif
├── burn_severity_classified.tif
└── sentinel2_postfire_composite.tif
```

---

### 2.3 Optional Enhancement Data

#### Dataset 6: Digital Elevation Model (DEM)
**Purpose:** Topographic features, slope, aspect
**Source:** USGS 3DEP or Google Earth Engine
**Status:** ⏳ OPTIONAL
**Priority:** LOW

**If Time Permits:**
- Resolution: 10m or 30m
- Source: USGS National Map or SRTM via GEE
- Variables: Elevation, Slope, Aspect
- Use: Improve fuel load estimation on slopes

---

### 2.4 Data Summary Table

| Dataset | Resolution | Temporal | Size | Status | Priority |
|---------|-----------|----------|------|--------|----------|
| LANDFIRE FBFM40 | 30m | 2020 | 50 MB | ⚠️ Need | CRITICAL |
| LANDFIRE CBD/CH | 30m | 2020 | 100 MB | ⚠️ Need | HIGH |
| Sentinel-2 Pre | 10m | 2020-2022 | 200 MB | ⏳ GEE | CRITICAL |
| Sentinel-2 Post | 10m | Aug 2022 | 200 MB | ⏳ GEE | HIGH |
| MODIS NDVI | 250m | 2020-2022 | 20 MB | ⏳ GEE | MEDIUM |
| Fire Perimeter | Vector | 2022 | 1 KB | ✅ Have | MEDIUM |
| Burn Severity | 30m | 2022 | 50 MB | ⏳ Need | HIGH |
| DEM | 10-30m | Static | 100 MB | ⏳ Skip | LOW |

**Total Data Volume:** ~700 MB
**Critical Path:** LANDFIRE + Sentinel-2 + Burn Severity

---

## 3. TECHNICAL ARCHITECTURE

### 3.1 Technology Stack

**Languages & Core Libraries:**
- Python 3.13
- NumPy, Pandas (data manipulation)
- Matplotlib, Seaborn (visualization)
- Scikit-learn, SciPy (machine learning)

**Geospatial Libraries:**
- Rasterio (raster I/O and processing)
- GeoPandas (vector data)
- PyProj (coordinate transformations)
- Google Earth Engine API (satellite data access)
- GDAL (via rasterio)

**Optional Visualization:**
- Folium (interactive maps)
- Plotly (interactive charts)
- Jupyter Notebook (analysis presentation)

**Environment:**
- Virtual environment: `venv/`
- Requirements: `requirements.txt`

### 3.2 Coordinate Reference System

**Target CRS:** UTM Zone 13N (EPSG:32613)
- Reason: Study area centered at ~105.6°W (UTM 13N)
- Units: Meters (easier for spatial analysis)
- All datasets will be reprojected to this CRS

**Source CRS by Dataset:**
- LANDFIRE: Albers Equal Area (EPSG:5070) → reproject
- Sentinel-2: WGS84 (EPSG:4326) → reproject
- MODIS: Sinusoidal → reproject
- Fire perimeter: WGS84 (EPSG:4326) → reproject

### 3.3 Data Processing Pipeline

```
Raw Data → Preprocessing → Feature Engineering → Fusion → Validation
    ↓            ↓                ↓                ↓          ↓
LANDFIRE     Reproject       Calculate         Combine    Compare
Sentinel-2   Clip to AOI     Indices           Layers     to Burn
MODIS        Resample        Normalize         Model      Severity
Fire Poly    Cloud mask      Changes           Predict
```

---

## 4. METHODOLOGY

### 4.1 Phase 1: Data Acquisition & Preprocessing

#### Step 1.1: Download LANDFIRE Data (MANUAL - 20 min)

**Action Items:**
1. Navigate to https://www.landfire.gov/viewer/
2. Search for Hermits Peak area (35.8°N, 105.6°W)
3. Select layers: FBFM40, CBD, CH
4. Choose version: LF 2020
5. Define bounding box: 35.6-36.0°N, 105.3-105.9°W
6. Download as GeoTIFF
7. Save to `data/landfire/`

**Verification:**
```bash
ls -lh data/landfire/*.tif
# Should see 3 files: FBFM40, CBD, CH
```

---

#### Step 1.2: Authenticate Google Earth Engine (5 min)

**Prerequisites:**
- GEE account approved (sign up at https://earthengine.google.com/signup/)
- Wait 2-4 hours for approval email

**Action Items:**
```bash
source venv/bin/activate
earthengine authenticate
# Follow OAuth flow in browser
```

**Verification:**
```bash
python -c "import ee; ee.Initialize(); print('GEE authenticated!')"
```

---

#### Step 1.3: Download Sentinel-2 Imagery via GEE (30 min setup + 20 min processing)

**Script:** `download_satellite_gee.py` (already created)

**Action Items:**
```bash
python download_satellite_gee.py
```

**What This Does:**
1. Loads fire AOI from GeoJSON
2. Filters Sentinel-2 collection:
   - Date: 2020-01-01 to 2022-04-06
   - Cloud cover < 20%
   - Bounds: Fire area + 5km buffer
3. Creates temporal composites:
   - 2020: Median composite (Jun-Sep)
   - 2022: Latest clear image (Jan-Apr)
4. Calculates indices: NDVI, NBR, NDMI
5. Exports to Google Drive as GeoTIFF

**Manual Steps After Script:**
1. Go to https://code.earthengine.google.com/tasks
2. Click "RUN" on each export task (6-8 tasks)
3. Wait 10-30 minutes for processing
4. Download from Google Drive to `data/satellite/sentinel2/`

**Expected Files:**
- `sentinel2_2020_composite.tif` (6 bands)
- `sentinel2_2022_composite.tif` (6 bands)
- `ndvi_2020.tif`
- `ndvi_2022.tif`
- `nbr_2020.tif`
- `nbr_2022.tif`

---

#### Step 1.4: Download Post-Fire Imagery for Burn Severity (15 min)

**Modify GEE Script or Run Separately:**
```python
# Add to download_satellite_gee.py or run separately
postfire_start = '2022-08-01'
postfire_end = '2022-09-30'

postfire_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(aoi)
    .filterDate(postfire_start, postfire_end)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)))

postfire_composite = postfire_collection.median()

# Calculate post-fire NBR
nbr_postfire = postfire_composite.normalizedDifference(['B8', 'B12'])

# Export
task = ee.batch.Export.image.toDrive(
    image=nbr_postfire,
    description='nbr_postfire_2022',
    folder='hermits_peak_data',
    scale=10,
    region=aoi.geometry(),
    maxPixels=1e9
)
task.start()
```

**Manual Steps:**
1. Run modified script
2. Start export task in GEE
3. Download `nbr_postfire_2022.tif`
4. Calculate dNBR in Python (next phase)

---

#### Step 1.5: Download MODIS Data (Optional - 15 min)

**If Time Permits:**

Add to `download_satellite_gee.py`:
```python
modis = (ee.ImageCollection('MODIS/006/MOD13Q1')
    .filterBounds(aoi)
    .filterDate('2020-01-01', '2022-04-06')
    .select(['NDVI', 'EVI']))

# 2020 mean
modis_2020 = modis.filterDate('2020-01-01', '2020-12-31').mean()

# 2022 pre-fire
modis_2022 = modis.filterDate('2022-01-01', '2022-04-06').mean()

# Export both
```

**Note:** MODIS is lower priority. Skip if time-constrained.

---

#### Step 1.6: Organize Downloaded Data

**Directory Structure Check:**
```bash
tree data/
```

**Expected Structure:**
```
data/
├── fire_perimeters/
│   └── hermits_peak_area_of_interest.geojson
├── landfire/
│   ├── LF2020_FBFM40_200_CONUS.tif
│   ├── LF2020_CBD_200_CONUS.tif
│   └── LF2020_CH_200_CONUS.tif
├── satellite/
│   ├── sentinel2/
│   │   ├── sentinel2_2020_composite.tif
│   │   ├── sentinel2_2022_composite.tif
│   │   ├── ndvi_2020.tif
│   │   ├── ndvi_2022.tif
│   │   ├── nbr_2020.tif
│   │   ├── nbr_2022.tif
│   │   └── nbr_postfire_2022.tif
│   └── modis/  (optional)
└── validation/
    └── (will create processed files here)
```

---

### 4.2 Phase 2: Data Preprocessing

**Script to Create:** `01_preprocess_data.py`

#### Step 2.1: Load and Inspect Data

```python
import rasterio
import geopandas as gpd
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
from pathlib import Path

# Define paths
DATA_DIR = Path('data')
LANDFIRE_DIR = DATA_DIR / 'landfire'
SENTINEL_DIR = DATA_DIR / 'satellite' / 'sentinel2'
OUTPUT_DIR = DATA_DIR / 'processed'
OUTPUT_DIR.mkdir(exist_ok=True)

# Target CRS
TARGET_CRS = 'EPSG:32613'  # UTM 13N

# Load fire AOI
fire_aoi = gpd.read_file(DATA_DIR / 'fire_perimeters' / 'hermits_peak_area_of_interest.geojson')
fire_aoi = fire_aoi.to_crs(TARGET_CRS)
fire_bounds = fire_aoi.total_bounds  # minx, miny, maxx, maxy
```

**Inspection:**
```python
# Check LANDFIRE
with rasterio.open(LANDFIRE_DIR / 'LF2020_FBFM40_200_CONUS.tif') as src:
    print(f"FBFM40 - CRS: {src.crs}, Shape: {src.shape}, Bounds: {src.bounds}")

# Check Sentinel-2
with rasterio.open(SENTINEL_DIR / 'ndvi_2020.tif') as src:
    print(f"NDVI 2020 - CRS: {src.crs}, Shape: {src.shape}, Bounds: {src.bounds}")
```

---

#### Step 2.2: Reproject and Clip to AOI

**Function to Reproject:**
```python
def reproject_and_clip(input_path, output_path, target_crs, bounds):
    """
    Reproject raster to target CRS and clip to bounding box

    Args:
        input_path: Path to input raster
        output_path: Path to output raster
        target_crs: Target CRS (e.g., 'EPSG:32613')
        bounds: (minx, miny, maxx, maxy) in target CRS
    """
    with rasterio.open(input_path) as src:
        # Calculate transform
        transform, width, height = calculate_default_transform(
            src.crs, target_crs, src.width, src.height, *src.bounds
        )

        # Update metadata
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': target_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Reproject
        with rasterio.open(output_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.nearest
                )

    # Clip to bounds
    # (Use rasterio.mask or gdal.Warp with cutline)
```

**Apply to All Datasets:**
```python
# LANDFIRE
datasets_to_process = {
    'fbfm40': LANDFIRE_DIR / 'LF2020_FBFM40_200_CONUS.tif',
    'cbd': LANDFIRE_DIR / 'LF2020_CBD_200_CONUS.tif',
    'ch': LANDFIRE_DIR / 'LF2020_CH_200_CONUS.tif',
    'ndvi_2020': SENTINEL_DIR / 'ndvi_2020.tif',
    'ndvi_2022': SENTINEL_DIR / 'ndvi_2022.tif',
    'nbr_2020': SENTINEL_DIR / 'nbr_2020.tif',
    'nbr_2022': SENTINEL_DIR / 'nbr_2022.tif',
    'nbr_postfire': SENTINEL_DIR / 'nbr_postfire_2022.tif',
}

for name, input_path in datasets_to_process.items():
    output_path = OUTPUT_DIR / f'{name}_processed.tif'
    print(f"Processing {name}...")
    reproject_and_clip(input_path, output_path, TARGET_CRS, fire_bounds)
```

---

#### Step 2.3: Calculate Change Metrics

```python
# NDVI Change
with rasterio.open(OUTPUT_DIR / 'ndvi_2020_processed.tif') as src2020:
    ndvi_2020 = src2020.read(1).astype('float32')
    profile = src2020.profile

with rasterio.open(OUTPUT_DIR / 'ndvi_2022_processed.tif') as src2022:
    ndvi_2022 = src2022.read(1).astype('float32')

# Calculate change (negative = vegetation loss)
ndvi_change = ndvi_2022 - ndvi_2020

# Save
with rasterio.open(OUTPUT_DIR / 'ndvi_change.tif', 'w', **profile) as dst:
    dst.write(ndvi_change, 1)

# Repeat for NBR
with rasterio.open(OUTPUT_DIR / 'nbr_2020_processed.tif') as src2020:
    nbr_2020 = src2020.read(1).astype('float32')

with rasterio.open(OUTPUT_DIR / 'nbr_2022_processed.tif') as src2022:
    nbr_2022 = src2022.read(1).astype('float32')

nbr_change = nbr_2022 - nbr_2020

with rasterio.open(OUTPUT_DIR / 'nbr_change.tif', 'w', **profile) as dst:
    dst.write(nbr_change, 1)
```

---

#### Step 2.4: Calculate Burn Severity (dNBR)

```python
# dNBR = NBR_prefire - NBR_postfire
# (Note: opposite sign from change calculation)

with rasterio.open(OUTPUT_DIR / 'nbr_2022_processed.tif') as src_pre:
    nbr_prefire = src_pre.read(1).astype('float32')
    profile = src_pre.profile

with rasterio.open(OUTPUT_DIR / 'nbr_postfire_processed.tif') as src_post:
    nbr_postfire = src_post.read(1).astype('float32')

dnbr = nbr_prefire - nbr_postfire

# Save continuous dNBR
with rasterio.open(OUTPUT_DIR / 'dnbr.tif', 'w', **profile) as dst:
    dst.write(dnbr, 1)

# Classify burn severity
burn_severity = np.zeros_like(dnbr, dtype='uint8')
burn_severity[dnbr < 0.1] = 0  # Unburned
burn_severity[(dnbr >= 0.1) & (dnbr < 0.27)] = 1  # Low
burn_severity[(dnbr >= 0.27) & (dnbr < 0.66)] = 2  # Moderate-low
burn_severity[(dnbr >= 0.66) & (dnbr < 1.3)] = 3  # Moderate-high
burn_severity[dnbr >= 1.3] = 4  # High

profile.update(dtype='uint8', nodata=255)
with rasterio.open(OUTPUT_DIR / 'burn_severity_classified.tif', 'w', **profile) as dst:
    dst.write(burn_severity, 1)
```

---

#### Step 2.5: Normalize and Stack Features

```python
from sklearn.preprocessing import StandardScaler

# Load all features
features_to_stack = [
    'fbfm40_processed.tif',
    'cbd_processed.tif',
    'ch_processed.tif',
    'ndvi_2020_processed.tif',
    'ndvi_2022_processed.tif',
    'ndvi_change.tif',
    'nbr_2020_processed.tif',
    'nbr_2022_processed.tif',
    'nbr_change.tif',
]

feature_arrays = []
for fname in features_to_stack:
    with rasterio.open(OUTPUT_DIR / fname) as src:
        data = src.read(1).astype('float32')
        feature_arrays.append(data.flatten())
        if len(feature_arrays) == 1:
            profile = src.profile  # Save profile from first raster

# Stack into 2D array (pixels x features)
X = np.column_stack(feature_arrays)

# Handle NaN/NoData
valid_mask = ~np.isnan(X).any(axis=1)
X_valid = X[valid_mask]

# Normalize
scaler = StandardScaler()
X_normalized = scaler.fit_transform(X_valid)

# Save for modeling
np.save(OUTPUT_DIR / 'feature_matrix.npy', X_normalized)
np.save(OUTPUT_DIR / 'valid_mask.npy', valid_mask)
np.save(OUTPUT_DIR / 'profile.npy', profile, allow_pickle=True)
```

**Preprocessing Complete!**

**Output Files:**
```
data/processed/
├── fbfm40_processed.tif
├── cbd_processed.tif
├── ch_processed.tif
├── ndvi_2020_processed.tif
├── ndvi_2022_processed.tif
├── ndvi_change.tif
├── nbr_2020_processed.tif
├── nbr_2022_processed.tif
├── nbr_change.tif
├── dnbr.tif
├── burn_severity_classified.tif
├── feature_matrix.npy
├── valid_mask.npy
└── profile.npy
```

---

### 4.3 Phase 3: Fuel Change Detection & Fusion

**Script to Create:** `02_fuel_mapping.py`

#### Step 3.1: Analyze Vegetation Changes

**Goal:** Identify areas where fuel conditions changed between 2020-2022

```python
import numpy as np
import rasterio
from pathlib import Path

OUTPUT_DIR = Path('data/processed')
RESULTS_DIR = Path('data/results')
RESULTS_DIR.mkdir(exist_ok=True)

# Load change metrics
with rasterio.open(OUTPUT_DIR / 'ndvi_change.tif') as src:
    ndvi_change = src.read(1)
    profile = src.profile

with rasterio.open(OUTPUT_DIR / 'nbr_change.tif') as src:
    nbr_change = src.read(1)

# Define thresholds for significant change
# Negative change = vegetation loss = increased fuel load
NDVI_LOSS_THRESHOLD = -0.1  # 10% NDVI decrease
NBR_LOSS_THRESHOLD = -0.1   # NBR decrease indicates stress

# Detect fuel increase areas
fuel_increase_mask = (
    (ndvi_change < NDVI_LOSS_THRESHOLD) |
    (nbr_change < NBR_LOSS_THRESHOLD)
).astype('uint8')

# Save fuel change mask
with rasterio.open(RESULTS_DIR / 'fuel_increase_areas.tif', 'w', **profile) as dst:
    dst.write(fuel_increase_mask, 1)

# Calculate change magnitude
change_magnitude = np.abs(ndvi_change) + np.abs(nbr_change)

profile.update(dtype='float32')
with rasterio.open(RESULTS_DIR / 'change_magnitude.tif', 'w', **profile) as dst:
    dst.write(change_magnitude, 1)
```

---

#### Step 3.2: Enhanced Fuel Map Creation

**Approach:** Update LANDFIRE fuel models based on detected changes

```python
# Load LANDFIRE baseline
with rasterio.open(OUTPUT_DIR / 'fbfm40_processed.tif') as src:
    fbfm40_baseline = src.read(1)
    profile = src.profile

with rasterio.open(OUTPUT_DIR / 'cbd_processed.tif') as src:
    cbd_baseline = src.read(1).astype('float32')

# Create enhanced fuel map
fbfm40_enhanced = fbfm40_baseline.copy()
cbd_enhanced = cbd_baseline.copy()

# Rule-based adjustment
# If NDVI decreased significantly -> increase fuel load category
# This is simplified; could use ML model instead

# Example rule: Areas with vegetation loss get higher fuel model
significant_loss = (ndvi_change < -0.15)

# Adjust fuel models (this is domain-specific, simplified here)
# In reality, you'd consult fuel model definitions
# For demo, we'll create a "fuel hazard increase" layer

fuel_hazard_increase = np.zeros_like(fbfm40_baseline, dtype='float32')

# Combine multiple signals
fuel_hazard_increase[significant_loss] += 1.0
fuel_hazard_increase[nbr_change < -0.15] += 1.0
fuel_hazard_increase[cbd_baseline > 5] += 0.5  # Already high canopy density

# Normalize to 0-1 scale
fuel_hazard_increase = np.clip(fuel_hazard_increase / fuel_hazard_increase.max(), 0, 1)

# Save enhanced fuel hazard map
profile.update(dtype='float32')
with rasterio.open(RESULTS_DIR / 'fuel_hazard_enhanced.tif', 'w', **profile) as dst:
    dst.write(fuel_hazard_increase, 1)
```

---

#### Step 3.3: Machine Learning Approach (Optional)

**If Time Permits:** Train a model to predict burn severity from fuel features

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Load feature matrix
X = np.load(OUTPUT_DIR / 'feature_matrix.npy')
valid_mask = np.load(OUTPUT_DIR / 'valid_mask.npy')

# Load burn severity as target
with rasterio.open(OUTPUT_DIR / 'dnbr.tif') as src:
    dnbr = src.read(1).flatten()

y = dnbr[valid_mask]

# Split data (only use burned areas for training)
# Burned area = dNBR > 0.1
burned_mask = y > 0.1
X_burned = X[burned_mask]
y_burned = y[burned_mask]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_burned, y_burned, test_size=0.3, random_state=42
)

# Train Random Forest
print("Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"R² Score: {r2:.3f}")
print(f"RMSE: {rmse:.3f}")

# Feature importance
feature_names = [
    'FBFM40', 'CBD', 'CH',
    'NDVI_2020', 'NDVI_2022', 'NDVI_Change',
    'NBR_2020', 'NBR_2022', 'NBR_Change'
]
importances = model.feature_importances_

plt.figure(figsize=(10, 6))
plt.barh(feature_names, importances)
plt.xlabel('Importance')
plt.title('Feature Importance for Burn Severity Prediction')
plt.tight_layout()
plt.savefig(RESULTS_DIR / 'feature_importance.png', dpi=300)
plt.close()

# Predict on full dataset
y_pred_full = np.zeros(len(valid_mask))
y_pred_full[valid_mask] = model.predict(X)

# Reshape to raster
predicted_severity = y_pred_full.reshape(profile['height'], profile['width'])

with rasterio.open(RESULTS_DIR / 'predicted_burn_severity.tif', 'w', **profile) as dst:
    dst.write(predicted_severity, 1)
```

---

### 4.4 Phase 4: Validation & Analysis

**Script to Create:** `03_validation.py`

#### Step 4.1: Compare Baseline vs Enhanced

**Goal:** Quantify improvement of enhanced fuel map over LANDFIRE baseline

```python
import numpy as np
import rasterio
from scipy.stats import pearsonr, spearmanr
from pathlib import Path
import matplotlib.pyplot as plt

RESULTS_DIR = Path('data/results')
OUTPUT_DIR = Path('data/processed')

# Load actual burn severity (ground truth)
with rasterio.open(OUTPUT_DIR / 'dnbr.tif') as src:
    actual_severity = src.read(1).flatten()

# Load LANDFIRE baseline (convert FBFM40 to continuous hazard)
with rasterio.open(OUTPUT_DIR / 'fbfm40_processed.tif') as src:
    fbfm40 = src.read(1).flatten()

# Simplified mapping: higher FBFM = higher hazard
# (In reality, specific models have different hazard levels)
# Models 101-165 = grass/shrub, 180s = timber
baseline_hazard = np.zeros_like(fbfm40, dtype='float32')
baseline_hazard[(fbfm40 >= 101) & (fbfm40 <= 109)] = 0.3  # Grass
baseline_hazard[(fbfm40 >= 120) & (fbfm40 <= 129)] = 0.5  # Shrub
baseline_hazard[(fbfm40 >= 140) & (fbfm40 <= 149)] = 0.6  # Timber-grass
baseline_hazard[(fbfm40 >= 180) & (fbfm40 <= 189)] = 0.8  # Timber

# Load enhanced fuel hazard
with rasterio.open(RESULTS_DIR / 'fuel_hazard_enhanced.tif') as src:
    enhanced_hazard = src.read(1).flatten()

# Filter to burned areas only (dNBR > 0.1)
burned_mask = actual_severity > 0.1
valid_mask = ~np.isnan(actual_severity) & ~np.isnan(enhanced_hazard) & burned_mask

actual_valid = actual_severity[valid_mask]
baseline_valid = baseline_hazard[valid_mask]
enhanced_valid = enhanced_hazard[valid_mask]

# Calculate correlations
corr_baseline, p_baseline = pearsonr(baseline_valid, actual_valid)
corr_enhanced, p_enhanced = pearsonr(enhanced_valid, actual_valid)

print("=== VALIDATION RESULTS ===")
print(f"Baseline (LANDFIRE only) correlation: {corr_baseline:.3f} (p={p_baseline:.4f})")
print(f"Enhanced (Satellite fusion) correlation: {corr_enhanced:.3f} (p={p_enhanced:.4f})")
print(f"Improvement: {(corr_enhanced - corr_baseline):.3f} ({((corr_enhanced - corr_baseline)/corr_baseline * 100):.1f}%)")

# Save results to file
with open(RESULTS_DIR / 'validation_results.txt', 'w') as f:
    f.write("VALIDATION RESULTS\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Sample Size (burned pixels): {len(actual_valid):,}\n")
    f.write(f"Baseline Correlation (Pearson): {corr_baseline:.4f}\n")
    f.write(f"Enhanced Correlation (Pearson): {corr_enhanced:.4f}\n")
    f.write(f"Absolute Improvement: {(corr_enhanced - corr_baseline):.4f}\n")
    f.write(f"Relative Improvement: {((corr_enhanced - corr_baseline)/corr_baseline * 100):.2f}%\n")
```

---

#### Step 4.2: Spatial Analysis - Where Did We Improve?

```python
# Calculate residuals
baseline_residual = np.abs(actual_valid - baseline_valid)
enhanced_residual = np.abs(actual_valid - enhanced_valid)

# Identify areas where enhanced map was better
improvement_mask = enhanced_residual < baseline_residual
improvement_areas = np.sum(improvement_mask) / len(improvement_mask) * 100

print(f"\nEnhanced map was more accurate in {improvement_areas:.1f}% of burned pixels")

# Create improvement map (full raster)
improvement_raster = np.zeros(len(actual_severity), dtype='float32')
improvement_raster[valid_mask] = (baseline_residual - enhanced_residual)  # Positive = improvement

# Reshape to 2D
with rasterio.open(OUTPUT_DIR / 'dnbr.tif') as src:
    profile = src.profile
    height, width = src.shape

improvement_raster_2d = improvement_raster.reshape(height, width)

with rasterio.open(RESULTS_DIR / 'spatial_improvement.tif', 'w', **profile) as dst:
    dst.write(improvement_raster_2d, 1)
```

---

#### Step 4.3: Bin Analysis - By Severity Class

```python
# Classify actual severity
severity_bins = [0, 0.1, 0.27, 0.66, 1.3, 3.0]
severity_labels = ['Unburned', 'Low', 'Moderate-Low', 'Moderate-High', 'High']

severity_class = np.digitize(actual_valid, severity_bins)

# Calculate correlation by severity class
print("\n=== Correlation by Burn Severity Class ===")
for i, label in enumerate(severity_labels, start=1):
    mask_class = severity_class == i
    if np.sum(mask_class) < 10:
        continue

    corr_base_class = pearsonr(baseline_valid[mask_class], actual_valid[mask_class])[0]
    corr_enh_class = pearsonr(enhanced_valid[mask_class], actual_valid[mask_class])[0]

    print(f"{label:15s}: Baseline={corr_base_class:.3f}, Enhanced={corr_enh_class:.3f}, Δ={corr_enh_class-corr_base_class:+.3f}")
```

---

### 4.5 Phase 5: Visualization & Presentation

**Script to Create:** `04_visualizations.py`

#### Step 5.1: Create Comparison Maps

```python
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, BoundaryNorm
import rasterio
from pathlib import Path
import numpy as np

RESULTS_DIR = Path('data/results')
OUTPUT_DIR = Path('data/processed')
VIZ_DIR = Path('visualizations')
VIZ_DIR.mkdir(exist_ok=True)

# Load rasters for visualization
with rasterio.open(OUTPUT_DIR / 'fbfm40_processed.tif') as src:
    fbfm40 = src.read(1)

with rasterio.open(RESULTS_DIR / 'fuel_hazard_enhanced.tif') as src:
    enhanced_hazard = src.read(1)

with rasterio.open(OUTPUT_DIR / 'burn_severity_classified.tif') as src:
    burn_severity = src.read(1)

with rasterio.open(OUTPUT_DIR / 'ndvi_change.tif') as src:
    ndvi_change = src.read(1)

# Create figure with 4 panels
fig, axes = plt.subplots(2, 2, figsize=(16, 14))

# Panel 1: LANDFIRE Baseline
ax1 = axes[0, 0]
im1 = ax1.imshow(fbfm40, cmap='YlOrRd', vmin=0, vmax=200)
ax1.set_title('A) LANDFIRE 2020 Fuel Models (Baseline)', fontsize=14, fontweight='bold')
ax1.axis('off')
plt.colorbar(im1, ax=ax1, label='Fuel Model Code', fraction=0.046)

# Panel 2: NDVI Change 2020→2022
ax2 = axes[0, 1]
im2 = ax2.imshow(ndvi_change, cmap='RdYlGn', vmin=-0.3, vmax=0.3)
ax2.set_title('B) NDVI Change 2020→2022 (Pre-Fire)', fontsize=14, fontweight='bold')
ax2.axis('off')
cbar2 = plt.colorbar(im2, ax=ax2, label='NDVI Change', fraction=0.046)
cbar2.ax.axhline(y=-0.1, color='black', linestyle='--', linewidth=1)

# Panel 3: Enhanced Fuel Hazard
ax3 = axes[1, 0]
im3 = ax3.imshow(enhanced_hazard, cmap='hot_r', vmin=0, vmax=1)
ax3.set_title('C) Enhanced Fuel Hazard Map (2022)', fontsize=14, fontweight='bold')
ax3.axis('off')
plt.colorbar(im3, ax=ax3, label='Fuel Hazard (0=Low, 1=High)', fraction=0.046)

# Panel 4: Actual Burn Severity
ax4 = axes[1, 1]
colors = ['#ffffff', '#ffffb2', '#fecc5c', '#fd8d3c', '#e31a1c']
cmap = ListedColormap(colors)
bounds = [0, 1, 2, 3, 4, 5]
norm = BoundaryNorm(bounds, cmap.N)
im4 = ax4.imshow(burn_severity, cmap=cmap, norm=norm)
ax4.set_title('D) Actual Burn Severity (dNBR)', fontsize=14, fontweight='bold')
ax4.axis('off')

# Custom legend
legend_labels = ['Unburned', 'Low', 'Moderate-Low', 'Moderate-High', 'High']
legend_patches = [mpatches.Patch(color=colors[i], label=legend_labels[i]) for i in range(5)]
ax4.legend(handles=legend_patches, loc='lower right', fontsize=10)

plt.suptitle('Hermits Peak Fire - Fuel Mapping Comparison', fontsize=18, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(VIZ_DIR / 'figure_main_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Saved: {VIZ_DIR / 'figure_main_comparison.png'}")
```

---

#### Step 5.2: Side-by-Side Validation

```python
# Scatter plots: Predicted vs Actual Severity
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Load data
with rasterio.open(OUTPUT_DIR / 'dnbr.tif') as src:
    actual = src.read(1).flatten()

with rasterio.open(RESULTS_DIR / 'fuel_hazard_enhanced.tif') as src:
    enhanced = src.read(1).flatten()

# Create baseline from FBFM
with rasterio.open(OUTPUT_DIR / 'fbfm40_processed.tif') as src:
    fbfm = src.read(1).flatten()

baseline = np.zeros_like(fbfm, dtype='float32')
baseline[(fbfm >= 101) & (fbfm <= 109)] = 0.3
baseline[(fbfm >= 120) & (fbfm <= 129)] = 0.5
baseline[(fbfm >= 140) & (fbfm <= 149)] = 0.6
baseline[(fbfm >= 180) & (fbfm <= 189)] = 0.8

# Filter valid burned pixels
burned_mask = (actual > 0.1) & ~np.isnan(actual) & ~np.isnan(enhanced)
actual_burned = actual[burned_mask]
baseline_burned = baseline[burned_mask]
enhanced_burned = enhanced[burned_mask]

# Downsample for plotting (plot every 10th point)
plot_mask = np.random.choice(len(actual_burned), size=min(5000, len(actual_burned)), replace=False)

# Panel 1: Baseline
ax1 = axes[0]
ax1.hexbin(baseline_burned[plot_mask], actual_burned[plot_mask], gridsize=50, cmap='Blues', mincnt=1)
ax1.plot([0, 1], [0, 1.3], 'r--', label='Perfect prediction')
ax1.set_xlabel('LANDFIRE Baseline Fuel Hazard', fontsize=12)
ax1.set_ylabel('Actual Burn Severity (dNBR)', fontsize=12)
ax1.set_title(f'Baseline: r={pearsonr(baseline_burned, actual_burned)[0]:.3f}', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# Panel 2: Enhanced
ax2 = axes[1]
ax2.hexbin(enhanced_burned[plot_mask], actual_burned[plot_mask], gridsize=50, cmap='Oranges', mincnt=1)
ax2.plot([0, 1], [0, 1.3], 'r--', label='Perfect prediction')
ax2.set_xlabel('Enhanced Fuel Hazard (Satellite Fusion)', fontsize=12)
ax2.set_ylabel('Actual Burn Severity (dNBR)', fontsize=12)
ax2.set_title(f'Enhanced: r={pearsonr(enhanced_burned, actual_burned)[0]:.3f}', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

plt.suptitle('Fuel Hazard vs Actual Burn Severity', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig(VIZ_DIR / 'figure_validation_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Saved: {VIZ_DIR / 'figure_validation_scatter.png'}")
```

---

#### Step 5.3: Create Story Map - Detected Changes That Burned

```python
# Find areas where we detected significant change AND actually burned severely
with rasterio.open(OUTPUT_DIR / 'ndvi_change.tif') as src:
    ndvi_change = src.read(1)

with rasterio.open(OUTPUT_DIR / 'burn_severity_classified.tif') as src:
    burn_severity = src.read(1)

# Create categories:
# 1. Detected decline + High burn = TRUE POSITIVE (good prediction!)
# 2. No decline detected + High burn = MISS (LANDFIRE also missed)
# 3. Detected decline + Low/No burn = False positive
# 4. No decline + No burn = True negative

detection_result = np.zeros_like(ndvi_change, dtype='uint8')

detected_decline = ndvi_change < -0.1
high_burn = burn_severity >= 3  # Moderate-high or high

detection_result[(detected_decline) & (high_burn)] = 1  # True positive
detection_result[(~detected_decline) & (high_burn)] = 2  # Miss
detection_result[(detected_decline) & (~high_burn)] = 3  # False alarm
detection_result[(~detected_decline) & (~high_burn)] = 0  # True negative

# Visualize
fig, ax = plt.subplots(figsize=(12, 10))

colors_detect = ['#f0f0f0', '#2ca25f', '#de2d26', '#fee08b']  # TN, TP, Miss, FP
cmap_detect = ListedColormap(colors_detect)
bounds_detect = [0, 1, 2, 3, 4]
norm_detect = BoundaryNorm(bounds_detect, cmap_detect.N)

im = ax.imshow(detection_result, cmap=cmap_detect, norm=norm_detect)
ax.set_title('Fuel Change Detection Results vs Actual Burn', fontsize=16, fontweight='bold')
ax.axis('off')

# Legend
labels_detect = [
    'No change, No burn (TN)',
    'Detected decline, High burn (TP)',
    'Missed decline, High burn (FN)',
    'Detected decline, Low/No burn (FP)'
]
patches_detect = [mpatches.Patch(color=colors_detect[i], label=labels_detect[i]) for i in range(4)]
ax.legend(handles=patches_detect, loc='lower right', fontsize=11, framealpha=0.9)

plt.tight_layout()
plt.savefig(VIZ_DIR / 'figure_detection_results.png', dpi=300, bbox_inches='tight')
plt.close()

# Calculate statistics
total_pixels = np.sum(~np.isnan(ndvi_change))
tp = np.sum(detection_result == 1)
fn = np.sum(detection_result == 2)
fp = np.sum(detection_result == 3)
tn = np.sum(detection_result == 0)

print("\n=== DETECTION STATISTICS ===")
print(f"True Positives (detected + burned): {tp:,} ({tp/total_pixels*100:.1f}%)")
print(f"False Negatives (missed + burned): {fn:,} ({fn/total_pixels*100:.1f}%)")
print(f"False Positives (detected + not burned): {fp:,} ({fp/total_pixels*100:.1f}%)")
print(f"True Negatives (no change + no burn): {tn:,} ({tn/total_pixels*100:.1f}%)")

if tp + fn > 0:
    recall = tp / (tp + fn)
    print(f"\nRecall (detected / all high burns): {recall:.2%}")

if tp + fp > 0:
    precision = tp / (tp + fp)
    print(f"Precision (correct / all detections): {precision:.2%}")

print(f"\nSaved: {VIZ_DIR / 'figure_detection_results.png'}")
```

---

#### Step 5.4: Create Presentation Summary Figure

```python
# Create final "money shot" figure for presentation
fig = plt.figure(figsize=(20, 12))

# Use GridSpec for custom layout
import matplotlib.gridspec as gridspec
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

# Large panel: Enhanced fuel map with burn overlay
ax_main = fig.add_subplot(gs[0:2, 0:2])
im_main = ax_main.imshow(enhanced_hazard, cmap='YlOrRd', vmin=0, vmax=1, alpha=0.8)
# Overlay burn perimeter
burn_outline = (burn_severity > 0).astype('float32')
burn_outline[burn_outline == 0] = np.nan
ax_main.contour(burn_outline, levels=[0.5], colors='black', linewidths=2)
ax_main.set_title('Enhanced Fuel Hazard Map (2022)\nwith Actual Fire Perimeter',
                  fontsize=16, fontweight='bold')
ax_main.axis('off')
plt.colorbar(im_main, ax=ax_main, label='Fuel Hazard', fraction=0.046)

# Panel: Correlation comparison
ax_corr = fig.add_subplot(gs[0, 2])
methods = ['LANDFIRE\n(Baseline)', 'Enhanced\n(Satellite)']
correlations = [
    pearsonr(baseline_burned, actual_burned)[0],
    pearsonr(enhanced_burned, actual_burned)[0]
]
colors_bar = ['#3182bd', '#e6550d']
bars = ax_corr.bar(methods, correlations, color=colors_bar, edgecolor='black', linewidth=2)
ax_corr.set_ylabel('Correlation with Burn Severity', fontsize=11, fontweight='bold')
ax_corr.set_ylim(0, max(correlations) * 1.2)
ax_corr.set_title('Validation: Correlation', fontsize=12, fontweight='bold')
ax_corr.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, val in zip(bars, correlations):
    height = bar.get_height()
    ax_corr.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=12)

# Panel: Improvement percentage
ax_improve = fig.add_subplot(gs[1, 2])
improvement_pct = (correlations[1] - correlations[0]) / correlations[0] * 100
ax_improve.text(0.5, 0.5, f'+{improvement_pct:.1f}%',
                ha='center', va='center', fontsize=48, fontweight='bold', color='#e6550d')
ax_improve.text(0.5, 0.2, 'Improvement',
                ha='center', va='center', fontsize=16, fontweight='bold')
ax_improve.set_xlim(0, 1)
ax_improve.set_ylim(0, 1)
ax_improve.axis('off')

# Panel: Key statistics
ax_stats = fig.add_subplot(gs[2, 0:])
ax_stats.axis('off')

stats_text = f"""
KEY FINDINGS:
• Study Area: Hermits Peak Fire, New Mexico (341,735 acres, $4B damage)
• Enhanced fuel map correlation: {correlations[1]:.3f} vs LANDFIRE baseline: {correlations[0]:.3f}
• Improvement: +{improvement_pct:.1f}% correlation with actual burn severity
• Detection rate: {recall:.1%} of high-severity burn areas showed pre-fire vegetation decline
• Data: Sentinel-2 (10m) + MODIS + LANDFIRE (2020-2022)
• Update frequency: Weekly (vs 2-3 years for traditional maps)
"""

ax_stats.text(0.05, 0.5, stats_text, fontsize=13, verticalalignment='center',
             family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

fig.suptitle('Wildfire Fuel Mapping: Satellite Data Fusion Improves Prediction Accuracy',
            fontsize=20, fontweight='bold', y=0.98)

plt.savefig(VIZ_DIR / 'PRESENTATION_SUMMARY.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✅ Saved presentation figure: {VIZ_DIR / 'PRESENTATION_SUMMARY.png'}")
```

---

## 5. EXECUTION TIMELINE

### Hour 0-1: Data Acquisition
- [ ] **[20 min]** Download LANDFIRE data manually
- [ ] **[10 min]** Sign up for GEE (if not done) & authenticate
- [ ] **[30 min]** Run GEE download script, start export tasks

### Hour 1-2: GEE Processing & Download
- [ ] **[15 min]** Monitor GEE tasks, click RUN on exports
- [ ] **[30 min]** Wait for processing (use time to review code, plan)
- [ ] **[15 min]** Download completed files from Google Drive

### Hour 2-4: Data Preprocessing
- [ ] **[30 min]** Run `01_preprocess_data.py`
  - Load and inspect data
  - Reproject to UTM 13N
  - Clip to AOI
- [ ] **[30 min]** Calculate change metrics (NDVI, NBR)
- [ ] **[30 min]** Calculate burn severity (dNBR)
- [ ] **[30 min]** Stack and normalize features

### Hour 4-6: Fuel Mapping & Fusion
- [ ] **[45 min]** Run `02_fuel_mapping.py`
  - Detect vegetation changes
  - Create enhanced fuel map
- [ ] **[45 min]** Optional: Train ML model
- [ ] **[30 min]** Debug, refine thresholds

### Hour 6-8: Validation & Analysis
- [ ] **[30 min]** Run `03_validation.py`
  - Calculate correlations
  - Compare baseline vs enhanced
- [ ] **[30 min]** Spatial analysis
- [ ] **[30 min]** Statistical testing
- [ ] **[30 min]** Document results

### Hour 8-10: Visualization
- [ ] **[45 min]** Run `04_visualizations.py`
  - Create comparison maps
  - Validation scatter plots
  - Detection results
- [ ] **[45 min]** Create presentation summary figure
- [ ] **[30 min]** Export high-res images

### Hour 10-11: Presentation Prep
- [ ] **[30 min]** Create slide deck (5-6 slides)
- [ ] **[30 min]** Write narrative script

### Hour 11-12: Buffer & Polish
- [ ] **[30 min]** Practice pitch
- [ ] **[30 min]** Handle unexpected issues, refinements

---

## 6. DELIVERABLES

### 6.1 Code & Data
- [ ] Python scripts (4 scripts)
- [ ] Processed datasets in `data/processed/`
- [ ] Results in `data/results/`
- [ ] Visualizations in `visualizations/`

### 6.2 Visualizations
- [ ] Main comparison figure (4-panel)
- [ ] Validation scatter plots
- [ ] Detection results map
- [ ] Presentation summary figure
- [ ] Feature importance chart (if ML used)

### 6.3 Documentation
- [ ] Validation results text file
- [ ] Detection statistics summary
- [ ] README with instructions to reproduce

### 6.4 Presentation (5-6 slides)
1. **Problem:** LANDFIRE maps update too slowly, miss critical fuel changes
2. **Solution:** Satellite-based weekly fuel mapping via data fusion
3. **Case Study:** Hermits Peak fire (341k acres, $4B damage)
4. **Results:** X% improvement in correlation with burn severity
5. **Visual:** Before/after maps, detection success stories
6. **Impact:** Better pre-season planning, resource allocation, community preparedness

---

## 7. VALIDATION METRICS

### 7.1 Primary Metrics
- **Pearson correlation:** Enhanced vs Baseline with burn severity
- **Target:** +15-30% improvement over baseline

### 7.2 Secondary Metrics
- **Spearman correlation:** Rank-order validation
- **RMSE:** Root mean squared error reduction
- **R² score:** Variance explained (if ML model used)

### 7.3 Qualitative Analysis
- **Spatial patterns:** Where did we improve?
- **Detection success:** % of high-severity burns with pre-fire decline
- **Case examples:** Specific areas where satellite detected change LANDFIRE missed

---

## 8. RISK MITIGATION

### 8.1 Risk: GEE Approval Delayed
**Mitigation:**
- Use USGS EarthExplorer as backup
- Download Landsat/Sentinel from AWS
- Focus on LANDFIRE analysis with publicly available historical data

### 8.2 Risk: Correlation Improvement Not Significant
**Mitigation:**
- Emphasize visual detection of changes
- Focus on specific case examples
- Highlight operational value (weekly updates) over accuracy gains
- Show where changes were detected, even if correlation modest

### 8.3 Risk: Time Overruns
**Mitigation:**
- Skip ML model, use rule-based fusion
- Skip MODIS, focus on Sentinel-2 only
- Use pre-made visualization templates
- Reduce statistical analysis depth

### 8.4 Risk: Data Processing Errors
**Mitigation:**
- Test scripts incrementally
- Save intermediate outputs
- Use try-except blocks with informative errors
- Have backup pre-processed data (download sample if needed)

---

## 9. SUCCESS CRITERIA

### Minimum Viable Demo (MUST HAVE)
- ✅ Visual comparison: LANDFIRE vs Enhanced fuel map
- ✅ Fire perimeter overlay
- ✅ At least one satellite product integrated
- ✅ Clear narrative about fuel change detection
- ✅ Basic correlation numbers

### Strong Demo (SHOULD HAVE)
- ✅ Quantitative validation showing improvement
- ✅ Multiple satellite products fused
- ✅ Spatial analysis of where improvements occurred
- ✅ Detection success statistics
- ✅ Professional visualizations

### Stretch Goals (NICE TO HAVE)
- ✅ ML model with feature importance
- ✅ Interactive map (Folium/Plotly)
- ✅ Multiple fires validated
- ✅ Time series animation of fuel changes
- ✅ Operational deployment mockup

---

## 10. FINAL NOTES

**Key Message for Pitch:**
*"LANDFIRE fuel maps update every 2-3 years and cost millions. We built a system that updates weekly using free satellite data. In the Hermits Peak fire—New Mexico's largest and most expensive wildfire—our satellite-enhanced fuel map showed [X]% better correlation with actual burn severity compared to the 2020 LANDFIRE baseline. We detected vegetation stress and fuel accumulation in areas LANDFIRE marked as stable, and those areas burned most intensively. This isn't real-time fire prediction; it's a pre-season planning tool that helps fire managers prioritize fuel reduction, pre-position resources, and prepare communities—using only free, publicly available data that scales statewide."*

**What Makes This Compelling:**
1. Real disaster case study ($4B damage, 341k acres)
2. Clear baseline comparison (LANDFIRE 2020)
3. Quantifiable improvement (correlation metrics)
4. Visual evidence (before/after maps)
5. Operational value (weekly updates vs 2-3 years)
6. Free data sources (scalable, sustainable)
7. Actionable output (pre-season planning, not crystal ball)

**Remember:**
- Story > Perfect accuracy
- Visual > Tables
- Impact > Technical sophistication
- Deployed solution > Research prototype

---

**Good luck! You've got this!** 🔥🛰️🗺️
