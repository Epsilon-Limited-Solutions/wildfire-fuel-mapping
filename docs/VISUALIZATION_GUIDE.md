# Visualization Guide
## Hermits Peak Wildfire Fuel Mapping Demo

---

## 🎯 The Goal

Your MVP needs to **visually demonstrate** that your satellite-enhanced fuel map predicts burn severity better than the LANDFIRE baseline. You need to tell this story in 2-3 minutes to judges who may not be technical.

---

## 📊 Three Visualization Options (Choose Based on Time)

### Option 1: Static High-Res Figures (Fastest - 1 hour)
**Use when:** Time-constrained, need something guaranteed to work

**Script:** `04_visualizations.py` (in PROJECT_SPEC.md)

**Output:**
- 4-panel comparison figure (PNG)
- Validation scatter plots (PNG)
- Detection results map (PNG)
- Presentation summary figure (PNG)

**Pros:**
- Fast to create
- No dependencies on external services
- High-resolution for slides
- Easy to include in PDF/PowerPoint

**Cons:**
- Not interactive
- Can't explore specific areas during demo

**Demo approach:** Show slides with annotations

---

### Option 2: Interactive HTML Map (Recommended - 2 hours)
**Use when:** Want to impress judges with interactivity

**Script:** `05_create_interactive_map.py`

**Output:**
- `hermits_peak_interactive_map.html` - Single file with all layers
- `hermits_peak_comparison_map.html` - Side-by-side LANDFIRE vs Enhanced

**Features:**
✅ Toggle layers on/off (LANDFIRE, Enhanced, NDVI change, Burn severity)
✅ Pan and zoom to specific areas
✅ Hover tooltips with data values
✅ Multiple basemaps (terrain, satellite, street)
✅ Legend and scale bar
✅ No server needed - just open HTML file

**Pros:**
- Very engaging for judges
- Tells story visually
- Can explore during Q&A
- Single file, portable
- Works offline

**Cons:**
- File size can be large (10-50 MB)
- Rendering large rasters can be slow
- Limited to 2D visualization

**Demo approach:**
1. Open `hermits_peak_comparison_map.html`
2. Show side-by-side LANDFIRE vs Enhanced
3. Toggle burn severity overlay: "See how our red areas match the actual burn?"
4. Zoom to specific area: "Here we detected 18% NDVI loss - LANDFIRE missed it"
5. Switch to main map for layer-by-layer storytelling

---

### Option 3: Live Dashboard (Most Impressive - 3 hours)
**Use when:** Want a professional-looking demo, have time to polish

**Script:** `dashboard_app.py`

**Run with:**
```bash
streamlit run dashboard_app.py
```

**Features:**
✅ Multi-page dashboard (Overview, Map, Analysis, About)
✅ Live metrics (correlation, improvement %, detection rate)
✅ Interactive charts (Plotly)
✅ Map with layer controls
✅ Statistical analysis page
✅ Professional UI with custom styling

**Pros:**
- Most professional appearance
- Real-time interactivity
- Can switch between views during demo
- Shows technical sophistication
- Easy to update numbers on the fly

**Cons:**
- Requires running server during demo
- Depends on internet (or local server)
- More complex setup
- Potential for technical issues during presentation

**Demo approach:**
1. Start on Dashboard Overview - show big numbers
2. Navigate to Interactive Map - zoom and explore
3. Show Validation Analysis - scatter plots and statistics
4. Return to Overview for final impact statement

---

## 🏆 Recommended Approach (2-Track Strategy)

### Track 1: Safe Backup (30 min)
Create static figures first:
- Run `04_visualizations.py`
- Export to high-res PNGs
- Create PowerPoint with 5-6 slides
- **This is your fallback if everything else fails**

### Track 2: Interactive Demo (1.5 hours)
Once backup is ready, create interactive map:
- Run `05_create_interactive_map.py`
- Test both HTML files thoroughly
- Practice narrative with map toggling
- **This is your primary demo**

### Track 3: Dashboard (If Time Permits)
After interactive map works:
- Install streamlit: `pip install streamlit streamlit-folium plotly`
- Update `dashboard_app.py` with real data paths
- Test locally: `streamlit run dashboard_app.py`
- **Use this if you want to wow judges**

---

## 🎬 Demo Narrative (2 minutes)

### Opening (15 seconds)
**[Show comparison map side-by-side]**

> "In April 2022, the Hermits Peak fire became New Mexico's largest wildfire - 341,000 acres, $4 billion in damage. Fire managers rely on LANDFIRE fuel maps to assess risk, but these maps update every 2-3 years."

### Problem (15 seconds)
**[Point to LANDFIRE baseline map]**

> "This is the LANDFIRE 2020 fuel map - the latest available before the fire. It couldn't detect the drought stress and vegetation changes that made this fire so destructive."

### Solution (30 seconds)
**[Toggle to enhanced map, then NDVI change layer]**

> "We built a system that updates fuel maps weekly using free satellite data. See these red areas? That's where Sentinel-2 detected significant vegetation loss between 2020 and 2022. LANDFIRE marked these as stable."

### Proof (45 seconds)
**[Overlay burn severity]**

> "Now watch what happened. [Toggle burn severity overlay] These areas we flagged burned at high severity. Our enhanced map showed 38% better correlation with actual burn severity compared to LANDFIRE."

**[Zoom to specific area]**

> "Here's a specific example: We detected 18% NDVI decline in this area. LANDFIRE fuel model stayed the same. It burned at the highest severity class."

### Impact (15 seconds)
**[Show dashboard metrics if using Streamlit, or summary figure]**

> "This isn't real-time fire prediction - it's a pre-season planning tool. Fire managers can prioritize fuel reduction, pre-position resources, and prepare communities. Our system uses only free data and scales statewide."

---

## 📁 File Organization

Create this structure:
```
visualizations/
├── static_figures/           # From 04_visualizations.py
│   ├── figure_main_comparison.png
│   ├── figure_validation_scatter.png
│   ├── figure_detection_results.png
│   └── PRESENTATION_SUMMARY.png
├── interactive_maps/         # From 05_create_interactive_map.py
│   ├── hermits_peak_interactive_map.html
│   └── hermits_peak_comparison_map.html
├── dashboard/               # From dashboard_app.py
│   └── (dashboard runs as web app)
└── presentation/            # For demo day
    ├── slides.pptx
    ├── demo_map.html (copy of comparison map)
    └── backup_figures/ (copies of PNGs)
```

---

## 🎨 Visual Design Principles

### 1. Color Scheme (Consistent Across All Outputs)
- **LANDFIRE baseline:** Blues (#3182bd)
- **Enhanced fuel hazard:** Red-Orange-Yellow (hot_r, YlOrRd)
- **NDVI change:** Red (loss) to Green (gain) - RdYlGn
- **Burn severity:** Yellow → Orange → Red (MTBS standard)
- **Improvement metrics:** Orange (#e6550d)

### 2. Essential Elements Every Visualization Must Have
✅ **Title** - Clear, descriptive
✅ **Legend** - What do colors mean?
✅ **Scale bar** - For maps
✅ **Labels** - Axis labels, units
✅ **Context** - Fire perimeter, study area
✅ **Call-out** - Key finding highlighted

### 3. Story Hierarchy
1. **Main message:** Enhanced > Baseline
2. **Visual evidence:** Red areas = vegetation loss
3. **Validation:** Those areas burned
4. **Quantification:** 38% improvement (or your actual number)
5. **Impact:** Saves lives, protects property

---

## ⚡ Quick Start Commands

### Static Figures
```bash
python 04_visualizations.py
# Output: visualizations/figure_*.png
```

### Interactive Map
```bash
python 05_create_interactive_map.py
# Output: visualizations/hermits_peak_*.html
# Open in browser: open visualizations/hermits_peak_comparison_map.html
```

### Dashboard
```bash
pip install streamlit streamlit-folium plotly
streamlit run dashboard_app.py
# Opens in browser automatically at http://localhost:8501
```

---

## 🐛 Troubleshooting

### "Large raster won't display in HTML"
**Solution:** Downsample before creating image overlay
```python
# In 05_create_interactive_map.py
with rasterio.open(raster_path) as src:
    data = src.read(1, out_shape=(src.height // 4, src.width // 4))
```

### "Map is blank/not showing layers"
**Solution:**
- Check CRS - must reproject to EPSG:4326 for web maps
- Check bounds - verify lat/lon are in correct order
- Check data range - normalize values to 0-1 or use proper vmin/vmax

### "Streamlit won't start"
**Solution:**
```bash
# Install dependencies
pip install streamlit streamlit-folium plotly

# Clear cache
streamlit cache clear

# Run with specific port
streamlit run dashboard_app.py --server.port 8502
```

### "File size too large (>50 MB)"
**Solution:**
- Reduce raster resolution (downsample)
- Compress images (reduce PNG quality)
- Use tiles instead of full image overlay
- Clip to smaller area of interest

---

## 📊 What Judges Want to See

### Technical Judges:
✅ Correlation statistics (r-value)
✅ Methodology diagram
✅ Data sources and processing pipeline
✅ Code quality and reproducibility

### Business Judges:
✅ Clear problem statement
✅ Operational impact (cost, lives saved)
✅ Scalability (works statewide)
✅ Implementation path (what's next?)

### General Audience:
✅ Visual before/after comparison
✅ Specific examples ("We detected THIS, it burned HERE")
✅ Simple metrics ("38% improvement")
✅ Real-world impact ($4B fire, could we prevent next one?)

### All Judges:
✅ Professional presentation
✅ Working demo (no crashes!)
✅ Clear narrative
✅ Enthusiasm and confidence

---

## 🎯 Final Checklist Before Demo

### Technical
- [ ] All HTML files open correctly
- [ ] Layers toggle on/off without errors
- [ ] Map loads in <5 seconds
- [ ] Numbers in dashboard are accurate
- [ ] Backup static figures ready

### Presentation
- [ ] Practiced 2-minute pitch 3+ times
- [ ] Know where to click during demo
- [ ] Prepared answers to "How accurate is this?"
- [ ] Prepared answers to "How much does this cost?"
- [ ] Have backup laptop or second browser tab open

### Story
- [ ] Opens with fire impact ($4B, 341k acres)
- [ ] Shows problem (LANDFIRE outdated)
- [ ] Shows solution (satellite weekly updates)
- [ ] Shows proof (correlation improvement)
- [ ] Shows impact (operational use cases)
- [ ] Closes with next steps

---

## 🚀 Pro Tips

1. **Practice the toggle sequence** - Know exactly which layers to turn on/off when
2. **Zoom to pre-selected areas** - Have 2-3 "hero spots" ready to show
3. **Have numbers memorized** - Don't read from slides
4. **Use "we" not "I"** - Sounds more collaborative
5. **Show, don't tell** - Let the visual do the talking
6. **End with question** - "How can we help fire managers in YOUR region?"

---

## 📚 Resources

**Color Palettes:**
- ColorBrewer: https://colorbrewer2.org/
- Matplotlib colormaps: https://matplotlib.org/stable/tutorials/colors/colormaps.html

**Inspiration:**
- MTBS Viewer: https://www.mtbs.gov/viewer/
- LANDFIRE Viewer: https://www.landfire.gov/viewer/
- NASA Worldview: https://worldview.earthdata.nasa.gov/

**Tutorials:**
- Folium docs: https://python-visualization.github.io/folium/
- Streamlit gallery: https://streamlit.io/gallery
- Plotly examples: https://plotly.com/python/

---

**Good luck! You've got this!** 🔥🗺️✨
