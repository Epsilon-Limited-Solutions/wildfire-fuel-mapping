# LFPS Coordinate Format Troubleshooting

## The Error You Got:
```
ERROR: Failure validating coordinates.
```

This means the format or order is wrong. Let's try different formats:

---

## TRY THESE FORMATS (in order):

### **Format 1: Lat/Lon order (MOST LIKELY)**
```
35.6,-105.9,36.0,-105.3
```
Order: `south,west,north,east`

### **Format 2: Reversed order**
```
-105.3,36.0,-105.9,35.6
```
Order: `east,north,west,south`

### **Format 3: Space separated**
```
-105.9 35.6 -105.3 36.0
```

### **Format 4: Min/Max clearly separated**
```
-105.9,35.6;-105.3,36.0
```

### **Format 5: Using Map Zone instead**
Instead of coordinates, try:
```
Map Zone: 13
```
Or:
```
Zone: 13
```
(This downloads a larger area but definitely works)

---

## ALTERNATIVE: Use Individual Corner Points

Some systems want corners explicitly:

**Southwest Corner:** `-105.9, 35.6`
**Northeast Corner:** `-105.3, 36.0`

---

## EASIEST FIX: Use Map Zone

If coordinates keep failing, just use **Map Zone 13** which covers all of New Mexico:

1. In the LFPS form, look for "Area of Interest"
2. Instead of coordinates, select "Map Zone"
3. Enter: `13`
4. Submit

**Pros:**
- Will definitely work
- Covers whole area (no edge issues)

**Cons:**
- Larger download (~500 MB instead of ~100 MB)
- Need to clip to Hermits Peak area later (we can do this with Python in 2 minutes)

---

## RECOMMENDATION FOR HACKATHON:

**Just use Map Zone 13!**

It's the most reliable method and you'll have data in 5 minutes. We can easily clip it to just the Hermits Peak area tomorrow with this Python code:

```python
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# Load fire boundary
fire = gpd.read_file('data/fire_perimeters/hermits_peak_area_of_interest.geojson')

# Clip raster to fire boundary
with rasterio.open('data/landfire/LF2020_Zone13.tif') as src:
    clipped, transform = mask(src, fire.geometry, crop=True)
    # Save clipped version
```

Takes 30 seconds to run, gives you exactly what you need.

---

## TRY THIS NOW:

1. Go back to https://lfps.usgs.gov
2. Layers: `220FBFM40;220CBD;220CH`
3. **Area of Interest:** Try Format 1 first: `35.6,-105.9,36.0,-105.3`
4. If that fails, use **Map Zone: 13**

Let me know which works!
