# Wildfire Fuel Mapping - Hermits Peak 2022

**Enhanced fuel prediction via satellite data fusion**

Climate Hackathon Project | Improving wildfire risk assessment using weekly satellite updates

---

## 🎯 Project Goal

Build an enhanced fuel mapping system that updates weekly using satellite data to detect fuel changes (drought-killed trees, beetle infestations, vegetation stress) that traditional LANDFIRE maps miss.

**Case Study:** Hermits Peak-Calf Canyon Fire (2022)
- **Size:** 341,735 acres (largest in New Mexico history)
- **Damage:** $4 billion
- **Challenge:** Could we have detected increased fuel hazard before the fire?

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Authenticate Google Earth Engine (one-time)
earthengine authenticate
```

### 2. Download Data
```bash
# Manual: Download LANDFIRE fuel maps
# Go to: https://www.landfire.gov/viewer/
# See: docs/HOW_TO_DOWNLOAD_LANDFIRE.md

# Automated: Download satellite imagery (requires GEE authentication)
python scripts/download_satellite_gee.py
# Then start export tasks at: https://code.earthengine.google.com/tasks
```

### 3. Run Pipeline
```bash
# Run entire analysis pipeline
python run.py --step all

# Or run individual steps:
python run.py --step preprocess   # Data preprocessing
python run.py --step analysis     # Fuel mapping & validation
python run.py --step visualize    # Generate figures
python run.py --step map          # Create interactive maps
python run.py --step dashboard    # Launch Streamlit dashboard
```

### 4. View Results
```bash
# Open interactive map
open outputs/maps/hermits_peak_comparison_map.html

# Check validation statistics
cat outputs/reports/validation_results.txt

# Launch dashboard
python run.py --step dashboard
```

---

## 📁 Project Structure

```
hackathon/
├── application/          # Main application code
│   ├── preprocessing/    # Data preprocessing
│   ├── analysis/         # Fuel mapping & validation
│   ├── visualization/    # Interactive maps
│   └── utils/           # Configuration & logging
├── scripts/             # Data download scripts
├── data/               # Input data & results
├── outputs/            # Figures, maps, reports
├── docs/               # Documentation
├── config/             # Configuration files
└── run.py             # Main execution script
```

**See [`STRUCTURE.md`](STRUCTURE.md) for detailed layout**

---

## 📊 Methodology

### 1. Baseline Data
- **LANDFIRE 2020** fuel models (30m resolution)
- Pre-fire fuel classification

### 2. Satellite Change Detection
- **Sentinel-2** optical imagery (10m, 2020-2022)
- **MODIS** vegetation indices (250m, 16-day)
- Calculate NDVI, NBR, NDMI changes

### 3. Data Fusion
- Combine LANDFIRE + satellite changes
- Detect vegetation stress and fuel accumulation
- Generate enhanced 2022 fuel hazard map

### 4. Validation
- Compare against actual burn severity (dNBR)
- Calculate correlation improvements
- Identify spatial patterns

---

## 🎯 Key Results

**Validation Metrics:**
- ✅ **+X% improvement** in correlation with burn severity vs LANDFIRE baseline
- ✅ **Y% detection rate** for high-severity burn areas
- ✅ **Z% spatial coverage** where enhanced map outperformed baseline

*(Actual numbers depend on analysis - run pipeline to generate)*

---

## 📚 Documentation

- **[`PROJECT_SPEC.md`](docs/PROJECT_SPEC.md)** - Complete technical specification
- **[`VISUALIZATION_GUIDE.md`](docs/VISUALIZATION_GUIDE.md)** - Demo strategies
- **[`STRUCTURE.md`](STRUCTURE.md)** - Project organization
- **[`DATA_DOWNLOAD_SUMMARY.md`](docs/DATA_DOWNLOAD_SUMMARY.md)** - Data acquisition guide

---

## 🛰️ Data Sources

| Dataset | Source | Resolution | Update Frequency |
|---------|--------|-----------|-----------------|
| LANDFIRE | USGS | 30m | 2-3 years |
| Sentinel-2 | ESA/Copernicus | 10m | 5 days |
| MODIS | NASA | 250m | Daily |
| Fire Perimeters | NIFC | Vector | Real-time |

---

## 💡 Use Cases

1. **Pre-season Planning**: Identify areas of increased fuel hazard
2. **Resource Allocation**: Prioritize fuel reduction treatments
3. **Risk Assessment**: Update wildfire risk maps with current conditions
4. **Community Preparedness**: Target high-risk areas for mitigation
5. **Strategic Planning**: Multi-year fuel management programs

---

## 🎬 Demo Guide

### Option 1: Interactive HTML Map (Recommended)
```bash
python run.py --step map
open outputs/maps/hermits_peak_comparison_map.html
```

**Features:**
- Side-by-side LANDFIRE baseline vs Enhanced fuel map
- Toggle burn severity overlay
- Pan and zoom to explore specific areas
- Show detected changes that correspond to high burn severity

### Option 2: Streamlit Dashboard
```bash
python run.py --step dashboard
# Opens at http://localhost:8501
```

**Features:**
- Multi-page dashboard with metrics
- Interactive charts and statistics
- Live map visualization
- Professional presentation UI

### Option 3: Static Figures
```bash
python run.py --step visualize
# Check outputs/figures/
```

Use for PowerPoint slides and reports.

---

## 🔧 Configuration

Edit `application/utils/config.py` to customize:

- **Target CRS**: Default UTM Zone 13N
- **Detection thresholds**: NDVI/NBR change sensitivity
- **Output paths**: Where to save results
- **Fire metadata**: Study area details

---

## 📦 Requirements

Python 3.9+ with packages:
- **Geospatial**: rasterio, geopandas, pyproj
- **Analysis**: numpy, pandas, scikit-learn, scipy
- **Visualization**: matplotlib, folium, streamlit, plotly
- **Data access**: earthengine-api

See [`requirements.txt`](requirements.txt) for complete list.

---

## 🐛 Troubleshooting

**GEE authentication fails:**
```bash
earthengine authenticate --force
```

**Missing LANDFIRE data:**
- Must be downloaded manually from https://www.landfire.gov/viewer/
- See `docs/HOW_TO_DOWNLOAD_LANDFIRE.md`

**Import errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

**Interactive map won't load:**
- Check file size (should be < 50MB)
- Try downsampling rasters in `config.py`
- Ensure all data preprocessing completed successfully

---

## 🏆 Success Metrics

### Minimum Viable Demo
- ✅ LANDFIRE baseline loaded
- ✅ Sentinel-2 change detection working
- ✅ Visual comparison showing improvements
- ✅ Fire perimeter overlay

### Strong Demo
- ✅ Quantitative validation metrics
- ✅ Multi-source data fusion
- ✅ Spatial analysis of improvements
- ✅ Professional visualizations

### Stretch Goals
- ✅ ML model with feature importance
- ✅ Interactive dashboard
- ✅ Multiple fire validation
- ✅ Operational deployment mockup

---

## 📧 Support

**Documentation:**
- Read `docs/PROJECT_SPEC.md` for technical details
- Check `STRUCTURE.md` for code organization
- See `docs/VISUALIZATION_GUIDE.md` for demo strategies

**Common Issues:**
- GEE approval: Can take 2-4 hours
- LANDFIRE download: Manual process, 15-20 minutes
- Pipeline runtime: 30-60 minutes for full analysis

---

## 🎯 Hackathon Pitch

**Hook:** "In 2022, the Hermits Peak fire became New Mexico's largest wildfire, burning 341,000 acres and causing $4 billion in damage. Fire managers rely on fuel maps to understand risk, but these maps update only every 2-3 years."

**Problem:** "LANDFIRE fuel maps from 2020 couldn't detect the drought-killed trees and vegetation stress that made the 2022 fire so destructive."

**Solution:** "We built a system that updates fuel maps weekly using free satellite data. By fusing Sentinel-2, MODIS, and spatial analysis, we create high-res fuel maps reflecting current conditions."

**Proof:** "Our enhanced fuel map showed [X]% correlation improvement with actual burn severity compared to LANDFIRE. We detected fuel accumulation in areas LANDFIRE marked as stable - and those areas burned most intensively."

**Impact:** "This isn't real-time fire prediction - it's a pre-season planning tool. Fire managers can prioritize fuel reduction, pre-position resources, and prepare communities. Our system uses only free data and scales statewide."

---

## 📝 License

MIT License - Educational/Research Use

---

## 👥 Contributors

Climate Hackathon 2024

---

**Last updated:** November 8, 2024

🔥 Good luck! 🗺️
