# Wildfire Fuel Mapping - Data Download Summary

## Project: Hermits Peak 2022 Fire Fuel Prediction
**Location:** Northern New Mexico
**Fire Date:** April 6 - August 21, 2022
**Fire Size:** 341,735 acres (largest in NM history)

---

## ✅ COMPLETED

### 1. Python Environment
- ✅ Virtual environment created (`venv/`)
- ✅ Required packages installed:
  - geopandas, rasterio (GIS processing)
  - requests (data download)
  - numpy, pandas, matplotlib (data analysis)
  - scikit-learn, scipy (ML modeling)

### 2. Fire Perimeter Data
- ✅ Created approximate area of interest boundary
  - **File:** `data/fire_perimeters/hermits_peak_area_of_interest.geojson`
  - **Coverage:** ~40km x 40km box around fire area
  - **Coordinates:** 35.6°N - 36.0°N, 105.3°W - 105.9°W
  - **Purpose:** Use this to download satellite imagery and LANDFIRE data

### 3. Documentation
- ✅ API credentials template created (`credentials_template.env`)
- ✅ Download scripts created
- ✅ Data directory structure set up

---

## ⚠️ MANUAL STEPS REQUIRED (Do These Tonight!)

### Priority 1: Google Earth Engine (CRITICAL - Can Take Hours for Approval)
**DO THIS FIRST - Approval can take 2-4 hours**

1. Go to: https://earthengine.google.com/signup/
2. Sign up with your email (use academic/educational if possible for faster approval)
3. Wait for approval email
4. Once approved, authenticate:
   ```bash
   source venv/bin/activate
   earthengine authenticate
   ```

**Why this matters:** GEE gives you access to Sentinel-2, Landsat, and MODIS in one place - essential for the project.

---

### Priority 2: LANDFIRE Fuel Data (Required for Baseline)
**Estimated time: 15-20 minutes**

This is your baseline "before" data to compare against.

**Steps:**
1. Go to: https://www.landfire.gov/viewer/
2. Click "Get Data"
3. Search for: **"Hermits Peak, New Mexico"** or enter coordinates: **35.8, -105.6**
4. Select these layers:
   - **FBFM40** (40 Scott and Burgan Fire Behavior Fuel Models)
   - **CBD** (Canopy Bulk Density)
   - **CH** (Canopy Height)
5. Choose **"LF 2020"** version (this is before the 2022 fire)
6. Draw rectangle around fire area using our GeoJSON coordinates:
   - NW: 36.0°N, 105.9°W
   - SE: 35.6°N, 105.3°W
7. Select format: **GeoTIFF**
8. Download and save to: `data/landfire/`

**Expected files:**
- `LF20_FBFM40_*.tif` (fuel models)
- `LF20_CBD_*.tif` (canopy density)
- `LF20_CH_*.tif` (canopy height)

---

### Priority 3: Fire Perimeter (Optional - Improves Validation)
**Estimated time: 5 minutes**

The approximate boundary works for now, but the exact perimeter is better for validation.

**Option A (Easiest):**
1. Go to: https://data-nifc.opendata.arcgis.com/
2. Search: **"WFIGS 2022"** or **"Hermits Peak"**
3. Click on "2022 Wildland Fire Perimeters"
4. Download as **GeoJSON** or **Shapefile**
5. Save to: `data/fire_perimeters/hermits_peak_actual.geojson`

**Option B (Alternative):**
1. Go to: https://hermits-peak-calf-canyon-fire-resources-nmhu.hub.arcgis.com/
2. Browse datasets for fire perimeter
3. Download and save to same location

---

## 📊 DATA STATUS

| Data Type | Status | Source | Resolution | Priority |
|-----------|--------|--------|------------|----------|
| **Fire AOI Boundary** | ✅ Created | Manual | ~40km box | HIGH |
| **Fire Actual Perimeter** | ⚠️ Manual needed | NIFC | Exact | MEDIUM |
| **LANDFIRE 2020 Fuel** | ⚠️ Manual needed | LANDFIRE | 30m | **CRITICAL** |
| **Sentinel-2 Imagery** | ⏳ Needs GEE auth | Google Earth Engine | 10m | **CRITICAL** |
| **MODIS Fire/Vegetation** | ⏳ Needs GEE auth | Google Earth Engine | 250m-1km | HIGH |
| **Landsat 8/9** | ⏳ Needs GEE auth | Google Earth Engine | 30m | MEDIUM |
| **Elevation (DEM)** | ⏳ Optional | USGS | 10m | LOW |

---

## 🚀 NEXT STEPS FOR TOMORROW

Once you have GEE access and LANDFIRE data:

### 1. Download Satellite Data via GEE
I'll create a script that will:
- Download Sentinel-2 imagery (2020-2022) for the fire area
- Calculate vegetation indices (NDVI, NBR)
- Detect vegetation stress and changes
- Export as GeoTIFF

### 2. Data Preprocessing
- Reproject all data to common coordinate system
- Clip to fire area
- Create time series of vegetation health

### 3. Build Fusion Model
- Combine LANDFIRE + Sentinel-2 + MODIS
- Detect fuel load changes 2020→2022
- Generate enhanced fuel map

### 4. Validation
- Compare our enhanced fuel map vs LANDFIRE 2020
- Overlay with actual burn severity
- Calculate correlation improvements

### 5. Visualization
- Create before/after comparison maps
- Show areas where we detected fuel changes
- Demonstrate prediction improvement

---

## 📁 CURRENT DIRECTORY STRUCTURE

```
hackathon/
├── venv/                           # Python environment
├── data/
│   ├── fire_perimeters/
│   │   └── hermits_peak_area_of_interest.geojson  ✅
│   ├── landfire/                   # Download LANDFIRE here
│   ├── satellite/                  # GEE downloads go here
│   └── elevation/                  # Optional DEM data
├── download_data.py                # Main download script
├── download_fire_perimeter.py      # Fire perimeter script
├── requirements.txt                # Python dependencies
└── credentials_template.env        # API keys template
```

---

## ⏰ TIMELINE FOR TONIGHT

**Before you sleep (30-45 minutes):**

1. **[5 min]** Sign up for Google Earth Engine → Wait for approval
2. **[20 min]** Download LANDFIRE data
3. **[5 min]** (Optional) Download exact fire perimeter from NIFC
4. **[5 min]** Test that you can view the GeoJSON file

**Tomorrow morning:**
1. Check email for GEE approval
2. Authenticate GEE
3. Run satellite download scripts (I'll create these)
4. Start building the model

---

## 🔑 API KEYS NEEDED

### Confirmed Needed:
- ✅ **Google Earth Engine** - Sign up tonight!

### Optional (We can work without these):
- NASA EARTHDATA - Only if GEE doesn't work
- USGS EarthExplorer - Only if GEE doesn't work

---

## 💡 TIPS FOR SUCCESS

1. **Don't wait for perfect data** - The approximate boundary is fine for a hackathon demo
2. **LANDFIRE is critical** - This is your baseline, prioritize getting it
3. **GEE approval can be slow** - Sign up NOW, not tomorrow morning
4. **Focus on one fire** - Hermits Peak is perfect (biggest in NM, well-documented)
5. **Save everything** - Keep all downloaded files, even if you're not sure you need them

---

## ❓ TROUBLESHOOTING

**Q: GEE approval is taking too long**
A: We can use alternative sources (USGS EarthExplorer, Sentinel Hub) but GEE is easier

**Q: LANDFIRE download is confusing**
A: Focus on just FBFM40 (fuel models) - that's the most important layer

**Q: I can't find the exact fire perimeter**
A: The approximate boundary works fine - we can refine later

**Q: Do I need elevation data tonight?**
A: No, it's optional. Focus on GEE signup and LANDFIRE first.

---

## 📧 WHAT TO ASK MENTORS TONIGHT

1. "Is anyone familiar with LANDFIRE or wildfire modeling?"
2. "Do you think pre-fire fuel mapping or real-time spread prediction is more compelling?"
3. "Should I focus on one fire (Hermits Peak) or try to validate across multiple fires?"
4. "What would judges find more impressive - technical sophistication or clear business value?"

---

## ✨ YOU'RE 30% DONE!

✅ Environment set up
✅ Fire boundary defined
✅ Scripts created
⏳ Waiting on: GEE approval, LANDFIRE download

**With 3-4 hours of work tomorrow, you'll have a working demo.**

Good luck! 🔥🗺️
