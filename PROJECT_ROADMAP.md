# Wildfire Fuel Mapping - Project Roadmap

## Your Current Status: Data Downloaded ✅

You have all the pieces. Now you need to build the model!

---

## The Story You're Telling

**Hook:** "LANDFIRE fuel maps update every 2-3 years, but conditions change constantly"

**Problem:** "The 2022 Hermits Peak fire burned areas that LANDFIRE 2020 didn't flag as high risk"

**Solution:** "We fuse satellite data to update fuel maps weekly, catching changes LANDFIRE misses"

**Proof:** "Our enhanced map showed higher fuel in areas that burned most severely"

---

## Step-by-Step Build Plan

### STEP 1: Detect Vegetation Changes (2020 → 2022 pre-fire)
**What:** Compare satellite data from 2020 vs early 2022 (before fire)

**How:**
- Calculate NDVI change (vegetation health decline = more fuel)
- Calculate NBR change (shows fuel accumulation)
- Calculate NDMI change (moisture stress = fire risk)
- Identify areas where vegetation declined or stress increased

**Output:** Change map showing where conditions got worse 2020→2022

**Why:** This shows what LANDFIRE missed!

---

### STEP 2: Create Enhanced Fuel Map
**What:** Update LANDFIRE 2020 with detected changes

**How:**
- Start with LANDFIRE 2020 fuel classifications
- Where satellite shows vegetation decline → increase fuel load estimate
- Where satellite shows moisture stress → increase fire risk
- Use Sentinel-2 (10m detail) + MODIS (frequent updates)

**Output:** Enhanced fuel map (LANDFIRE 2020 + satellite updates)

**Why:** This is your prediction of actual conditions in April 2022

---

### STEP 3: Validation (Prove It Works!)
**What:** Compare your enhanced map vs LANDFIRE vs actual burn severity

**How:**
- Get actual burn severity data from post-fire imagery
- Calculate: Did high fuel areas burn more intensely?
- Show correlation: Enhanced map vs actual fire
- Show correlation: LANDFIRE 2020 vs actual fire
- Prove your map is better!

**Output:**
- Scatter plots showing correlation
- Side-by-side maps: "LANDFIRE said X, we said Y, fire did Y"
- Quantitative improvement metrics

**Why:** This is your proof that the approach works!

---

### STEP 4: Demo/Visualization
**What:** Make it compelling for presentation

**How:**
- Before/after fuel maps
- "LANDFIRE missed this" highlights
- Fire overlay showing you were right
- Interactive map if time permits

**Output:** Clear, visual demonstration of value

---

## What Data You Have & How You'll Use It

| Data | Resolution | What It Does |
|------|-----------|-------------|
| **LANDFIRE 2020** | 30m | Baseline fuel map (your starting point) |
| **Sentinel-2 Pre-Fire** | 10m | High-res vegetation health before fire |
| **Sentinel-2 Post-Fire** | 10m | Shows actual burn severity (for validation!) |
| **MODIS Pre/Post** | 250m | Broader changes, frequent updates |
| **Landsat Thermal** | 30m | Temperature = stress detection |

---

## The Technical Approach (Simplified)

```
STEP 1: CHANGE DETECTION
  LANDFIRE 2020 fuel map (static)
  + Sentinel-2 NDVI drop 2020→2022 (vegetation decline)
  + MODIS stress indicators
  = "Fuel probably increased here"

STEP 2: FUSION
  LANDFIRE fuel type + Detected changes = Enhanced fuel map

STEP 3: VALIDATION
  Enhanced map vs Actual burn severity
  LANDFIRE 2020 vs Actual burn severity
  Show improvement!
```

---

## Next Actions (In Order)

1. **Build change detection** (detect fuel changes 2020→2022)
2. **Create enhanced fuel map** (LANDFIRE + changes)
3. **Calculate burn severity** from post-fire data
4. **Validate your map** against actual fire
5. **Create visualizations** for demo

---

## Simple Version (Minimum Viable Demo)

If you're short on time, do this:

1. **Show NDVI change map** (2020 vs 2022 pre-fire)
   - "Red areas = vegetation declined = more fuel"

2. **Overlay with actual fire** (post-fire data)
   - "Red areas burned more intensely - we detected it!"

3. **Compare to LANDFIRE**
   - "LANDFIRE said fuel was stable here, but we detected changes"

4. **Tell the story**
   - "Free satellite data can update fuel maps weekly"
   - "Helps fire managers prepare for changing conditions"

---

## Questions to Answer in Your Demo

✅ "What problem are you solving?"
→ LANDFIRE fuel maps get outdated, missing dangerous changes

✅ "How does your solution work?"
→ Fuse satellite data to detect vegetation/fuel changes weekly

✅ "Does it actually work?"
→ Yes! Our enhanced map correlated better with actual fire severity

✅ "Can this scale?"
→ Yes! All data is free, automated, works anywhere

✅ "Who would use this?"
→ Fire managers, forest service, emergency planning

---

## Your Advantage for Hackathon

- **Real fire validation** (not just a concept!)
- **Quantitative proof** (correlation metrics)
- **Free data** (scalable, sustainable)
- **Clear business value** (pre-season planning tool)
- **Compelling visuals** (before/after, fire overlay)

---

## What Makes This Different from Real-Time Fire Detection

**NOT:** Real-time fire spread prediction during active fire
**YES:** Pre-season fuel mapping to plan before fire season

This is about **preparation**, not **response**.
Fire managers use this in March to decide:
- Where to do fuel reduction
- Where to pre-position resources
- Which communities to prepare

---

## Current Status

✅ Environment set up
✅ Data downloaded (all 5 datasets)
✅ Fire boundary defined
✅ Data visualized and validated

**NEXT:** Build the change detection and fusion model!

---

Ready to start coding the model?
