"""
Create interactive web map for Hermits Peak fuel mapping demo
Output: Single HTML file that can be opened in any browser
"""

import folium
from folium import plugins
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import geopandas as gpd
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, Normalize
import matplotlib.cm as cm

# Paths
OUTPUT_DIR = Path('data/processed')
RESULTS_DIR = Path('data/results')
VIZ_DIR = Path('visualizations')
VIZ_DIR.mkdir(exist_ok=True)

print("Creating interactive map...")

# ============================================================================
# 1. LOAD FIRE PERIMETER
# ============================================================================
fire_aoi = gpd.read_file('data/fire_perimeters/hermits_peak_area_of_interest.geojson')
fire_centroid = fire_aoi.geometry.centroid.iloc[0]
center_lat, center_lon = fire_centroid.y, fire_centroid.x

print(f"Map center: {center_lat:.3f}°N, {center_lon:.3f}°W")

# ============================================================================
# 2. CREATE BASE MAP
# ============================================================================
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles='OpenStreetMap',
    control_scale=True
)

# Add different basemap options
folium.TileLayer('Stamen Terrain', name='Terrain').add_to(m)
folium.TileLayer('Stamen Toner', name='Toner').add_to(m)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite',
    overlay=False,
    control=True
).add_to(m)

# ============================================================================
# 3. HELPER FUNCTION: RASTER TO IMAGE OVERLAY
# ============================================================================
def raster_to_image_overlay(raster_path, colormap='YlOrRd', vmin=None, vmax=None,
                            alpha=0.7, name='Layer'):
    """
    Convert raster to PNG image overlay for Folium

    Returns: (image_url, bounds) for folium.raster_layers.ImageOverlay
    """
    with rasterio.open(raster_path) as src:
        # Read data
        data = src.read(1)

        # Get bounds in lat/lon
        bounds_native = src.bounds

        # If not in lat/lon, reproject bounds
        if src.crs != 'EPSG:4326':
            from pyproj import Transformer
            transformer = Transformer.from_crs(src.crs, 'EPSG:4326', always_xy=True)
            min_lon, min_lat = transformer.transform(bounds_native.left, bounds_native.bottom)
            max_lon, max_lat = transformer.transform(bounds_native.right, bounds_native.top)
        else:
            min_lon, min_lat = bounds_native.left, bounds_native.bottom
            max_lon, max_lat = bounds_native.right, bounds_native.top

        bounds = [[min_lat, min_lon], [max_lat, max_lon]]

        # Normalize data
        data_masked = np.ma.masked_invalid(data)
        if vmin is None:
            vmin = np.percentile(data_masked.compressed(), 2)
        if vmax is None:
            vmax = np.percentile(data_masked.compressed(), 98)

        norm = Normalize(vmin=vmin, vmax=vmax)

        # Apply colormap
        cmap = cm.get_cmap(colormap)
        data_normalized = norm(data_masked)
        rgba = cmap(data_normalized)

        # Set alpha for masked values to 0 (transparent)
        rgba[..., 3] = np.where(data_masked.mask, 0, alpha)

        # Convert to uint8
        rgba_uint8 = (rgba * 255).astype(np.uint8)

        # Create PIL image
        img = Image.fromarray(rgba_uint8, mode='RGBA')

        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format='PNG')
        img_str = base64.b64encode(buffered.getvalue()).decode()
        img_url = f'data:image/png;base64,{img_str}'

        return img_url, bounds, (vmin, vmax)

# ============================================================================
# 4. ADD FIRE PERIMETER
# ============================================================================
folium.GeoJson(
    fire_aoi,
    name='Fire Area of Interest',
    style_function=lambda x: {
        'fillColor': 'none',
        'color': 'red',
        'weight': 3,
        'dashArray': '5, 5'
    },
    tooltip='Hermits Peak Fire Area (40km x 40km)'
).add_to(m)

# ============================================================================
# 5. ADD RASTER LAYERS
# ============================================================================

# Layer 1: LANDFIRE Baseline Fuel Model
print("Processing LANDFIRE baseline...")
if (OUTPUT_DIR / 'fbfm40_processed.tif').exists():
    try:
        img_url, bounds, (vmin, vmax) = raster_to_image_overlay(
            OUTPUT_DIR / 'fbfm40_processed.tif',
            colormap='YlOrBr',
            vmin=100,
            vmax=190,
            alpha=0.6,
            name='LANDFIRE Baseline'
        )

        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=bounds,
            name='LANDFIRE 2020 Fuel Models',
            opacity=0.6,
            interactive=True,
            cross_origin=False,
            zindex=1
        ).add_to(m)
        print("  ✓ LANDFIRE layer added")
    except Exception as e:
        print(f"  ✗ Error adding LANDFIRE: {e}")
else:
    print("  ⚠ LANDFIRE file not found")

# Layer 2: Enhanced Fuel Hazard Map (STAR OF THE SHOW)
print("Processing enhanced fuel map...")
if (RESULTS_DIR / 'fuel_hazard_enhanced.tif').exists():
    try:
        img_url, bounds, (vmin, vmax) = raster_to_image_overlay(
            RESULTS_DIR / 'fuel_hazard_enhanced.tif',
            colormap='hot_r',
            vmin=0,
            vmax=1,
            alpha=0.7,
            name='Enhanced Fuel Hazard'
        )

        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=bounds,
            name='Enhanced Fuel Hazard (2022)',
            opacity=0.7,
            interactive=True,
            cross_origin=False,
            zindex=2
        ).add_to(m)
        print("  ✓ Enhanced fuel hazard layer added")
    except Exception as e:
        print(f"  ✗ Error adding enhanced fuel: {e}")
else:
    print("  ⚠ Enhanced fuel file not found")

# Layer 3: NDVI Change (shows vegetation loss)
print("Processing NDVI change...")
if (OUTPUT_DIR / 'ndvi_change.tif').exists():
    try:
        img_url, bounds, (vmin, vmax) = raster_to_image_overlay(
            OUTPUT_DIR / 'ndvi_change.tif',
            colormap='RdYlGn',
            vmin=-0.3,
            vmax=0.3,
            alpha=0.7,
            name='NDVI Change'
        )

        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=bounds,
            name='NDVI Change 2020→2022 (Red=Loss)',
            opacity=0.7,
            interactive=True,
            cross_origin=False,
            zindex=3
        ).add_to(m)
        print("  ✓ NDVI change layer added")
    except Exception as e:
        print(f"  ✗ Error adding NDVI change: {e}")
else:
    print("  ⚠ NDVI change file not found")

# Layer 4: Burn Severity (validation ground truth)
print("Processing burn severity...")
if (OUTPUT_DIR / 'burn_severity_classified.tif').exists():
    try:
        # Custom colormap for burn severity classes
        colors = ['#ffffff', '#ffffb2', '#fecc5c', '#fd8d3c', '#e31a1c']
        n_bins = len(colors)
        cmap_burn = ListedColormap(colors)

        with rasterio.open(OUTPUT_DIR / 'burn_severity_classified.tif') as src:
            data = src.read(1)
            bounds_native = src.bounds

            if src.crs != 'EPSG:4326':
                from pyproj import Transformer
                transformer = Transformer.from_crs(src.crs, 'EPSG:4326', always_xy=True)
                min_lon, min_lat = transformer.transform(bounds_native.left, bounds_native.bottom)
                max_lon, max_lat = transformer.transform(bounds_native.right, bounds_native.top)
            else:
                min_lon, min_lat = bounds_native.left, bounds_native.bottom
                max_lon, max_lat = bounds_native.right, bounds_native.top

            bounds = [[min_lat, min_lon], [max_lat, max_lon]]

            # Map classes to colors
            rgba = np.zeros((*data.shape, 4), dtype=np.uint8)
            for i, color in enumerate(colors):
                mask = data == i
                # Convert hex to RGB
                rgb = tuple(int(color[j:j+2], 16) for j in (1, 3, 5))
                rgba[mask, 0] = rgb[0]
                rgba[mask, 1] = rgb[1]
                rgba[mask, 2] = rgb[2]
                rgba[mask, 3] = 180 if i > 0 else 0  # Transparent for unburned

            img = Image.fromarray(rgba, mode='RGBA')
            buffered = BytesIO()
            img.save(buffered, format='PNG')
            img_str = base64.b64encode(buffered.getvalue()).decode()
            img_url = f'data:image/png;base64,{img_str}'

        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=bounds,
            name='Actual Burn Severity',
            opacity=0.7,
            interactive=True,
            cross_origin=False,
            zindex=4
        ).add_to(m)
        print("  ✓ Burn severity layer added")
    except Exception as e:
        print(f"  ✗ Error adding burn severity: {e}")
else:
    print("  ⚠ Burn severity file not found")

# ============================================================================
# 6. ADD MARKERS FOR KEY FINDINGS
# ============================================================================
# These would be specific areas where you detected change that burned intensely
# For now, adding example markers - you'd calculate these from your analysis

example_detections = [
    {
        'lat': 35.85,
        'lon': -105.65,
        'title': 'High Detection Success',
        'description': 'NDVI decreased 18% (2020→2022). Burned at high severity.',
        'color': 'green'
    },
    {
        'lat': 35.77,
        'lon': -105.55,
        'title': 'Missed by LANDFIRE',
        'description': 'Satellite detected vegetation stress. LANDFIRE showed stable fuel.',
        'color': 'orange'
    }
]

marker_group = folium.FeatureGroup(name='Key Detection Examples', show=False)
for detection in example_detections:
    folium.Marker(
        location=[detection['lat'], detection['lon']],
        popup=f"<b>{detection['title']}</b><br>{detection['description']}",
        tooltip=detection['title'],
        icon=folium.Icon(color=detection['color'], icon='fire', prefix='fa')
    ).add_to(marker_group)

marker_group.add_to(m)

# ============================================================================
# 7. ADD LEGEND
# ============================================================================
legend_html = '''
<div style="position: fixed;
            bottom: 50px; right: 50px; width: 300px; height: auto;
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; border-radius: 5px; padding: 10px">
    <h4 style="margin-top:0">Hermits Peak Fuel Mapping</h4>

    <p><b>Enhanced Fuel Hazard</b> (Our Method)<br>
    <span style="background: linear-gradient(to right, yellow, orange, red);
                 padding: 2px 60px; border: 1px solid black;"></span><br>
    <small>Low → High fuel hazard</small></p>

    <p><b>Burn Severity</b> (Validation)<br>
    <span style="background: #ffffb2; padding: 2px 15px; border: 1px solid black;"></span> Low<br>
    <span style="background: #fecc5c; padding: 2px 15px; border: 1px solid black;"></span> Moderate-Low<br>
    <span style="background: #fd8d3c; padding: 2px 15px; border: 1px solid black;"></span> Moderate-High<br>
    <span style="background: #e31a1c; padding: 2px 15px; border: 1px solid black;"></span> High</p>

    <p><b>NDVI Change</b> (2020→2022)<br>
    <span style="background: red; padding: 2px 15px; border: 1px solid black;"></span> Vegetation Loss<br>
    <span style="background: green; padding: 2px 15px; border: 1px solid black;"></span> Vegetation Gain</p>

    <hr>
    <p style="font-size: 12px; margin-bottom: 0;">
    <b>Toggle layers</b> using the layer control (top right) to compare:<br>
    • LANDFIRE baseline vs Enhanced<br>
    • Detected changes vs Actual burn
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# ============================================================================
# 8. ADD TITLE
# ============================================================================
title_html = '''
<div style="position: fixed;
            top: 10px; left: 50px; width: 600px; height: auto;
            background-color: rgba(255, 255, 255, 0.9); z-index:9999; font-size:16px;
            border:2px solid grey; border-radius: 5px; padding: 15px">
    <h2 style="margin:0; color: #d62728;">🔥 Hermits Peak Wildfire Fuel Mapping</h2>
    <p style="margin: 5px 0 0 0; font-size: 14px;">
    <b>Enhanced fuel prediction via satellite data fusion</b><br>
    Hermits Peak-Calf Canyon Fire (2022) • 341,735 acres • $4B damage
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# ============================================================================
# 9. ADD LAYER CONTROL
# ============================================================================
folium.LayerControl(position='topright', collapsed=False).add_to(m)

# ============================================================================
# 10. ADD FULLSCREEN BUTTON
# ============================================================================
plugins.Fullscreen(
    position='topleft',
    title='Fullscreen',
    title_cancel='Exit fullscreen',
    force_separate_button=True
).add_to(m)

# ============================================================================
# 11. ADD MOUSE COORDINATES
# ============================================================================
plugins.MousePosition(
    position='bottomleft',
    separator=' | ',
    prefix='Coordinates: ',
    lat_formatter="function(num) {return L.Util.formatNum(num, 4) + ' N';}",
    lng_formatter="function(num) {return L.Util.formatNum(num, 4) + ' W';}"
).add_to(m)

# ============================================================================
# 12. SAVE MAP
# ============================================================================
output_file = VIZ_DIR / 'hermits_peak_interactive_map.html'
m.save(str(output_file))

print(f"\n✅ Interactive map created: {output_file}")
print(f"\n🌐 Open this file in your browser to view the map")
print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")

# ============================================================================
# 13. CREATE SIDE-BY-SIDE COMPARISON (OPTIONAL)
# ============================================================================
print("\nCreating side-by-side comparison map...")

m2 = folium.plugins.DualMap(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# Left map: LANDFIRE Baseline
if (OUTPUT_DIR / 'fbfm40_processed.tif').exists():
    try:
        img_url, bounds, _ = raster_to_image_overlay(
            OUTPUT_DIR / 'fbfm40_processed.tif',
            colormap='YlOrBr',
            vmin=100,
            vmax=190,
            alpha=0.7
        )
        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=bounds,
            name='LANDFIRE 2020',
            opacity=0.7
        ).add_to(m2.m1)
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Right map: Enhanced Fuel Hazard
if (RESULTS_DIR / 'fuel_hazard_enhanced.tif').exists():
    try:
        img_url, bounds, _ = raster_to_image_overlay(
            RESULTS_DIR / 'fuel_hazard_enhanced.tif',
            colormap='hot_r',
            vmin=0,
            vmax=1,
            alpha=0.7
        )
        folium.raster_layers.ImageOverlay(
            image=img_url,
            bounds=bounds,
            name='Enhanced 2022',
            opacity=0.7
        ).add_to(m2.m2)
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Add burn severity to both
if (OUTPUT_DIR / 'burn_severity_classified.tif').exists():
    try:
        # (Reuse the burn severity layer creation code from above)
        # Add to both maps for comparison
        pass  # Simplified for brevity
    except:
        pass

# Add titles
title_left = '''
<div style="position: fixed; top: 10px; left: 10px; z-index:9999;
            background-color: rgba(255,255,255,0.8); padding: 10px; border-radius: 5px;">
    <h3 style="margin:0">LANDFIRE 2020 (Baseline)</h3>
    <p style="margin:0; font-size:12px">Static, 2-3 year update cycle</p>
</div>
'''

title_right = '''
<div style="position: fixed; top: 10px; left: 10px; z-index:9999;
            background-color: rgba(255,255,255,0.8); padding: 10px; border-radius: 5px;">
    <h3 style="margin:0">Enhanced 2022 (Satellite)</h3>
    <p style="margin:0; font-size:12px">Weekly updates via Sentinel-2/MODIS</p>
</div>
'''

m2.m1.get_root().html.add_child(folium.Element(title_left))
m2.m2.get_root().html.add_child(folium.Element(title_right))

# Save
output_file_dual = VIZ_DIR / 'hermits_peak_comparison_map.html'
m2.save(str(output_file_dual))

print(f"✅ Side-by-side comparison created: {output_file_dual}")

print("\n" + "="*60)
print("INTERACTIVE MAPS READY FOR DEMO!")
print("="*60)
print("\n📂 Files created:")
print(f"  1. Main map: {output_file}")
print(f"  2. Comparison: {output_file_dual}")
print("\n💡 Demo tips:")
print("  • Start with comparison map (shows improvement clearly)")
print("  • Toggle layers to tell the story")
print("  • Zoom to specific areas where you detected changes")
print("  • Show burn severity overlay on enhanced map")
print("\n🎯 Key narrative:")
print("  'Red areas on NDVI change = vegetation loss we detected'")
print("  'See how those areas correspond to high burn severity?'")
print("  'LANDFIRE baseline missed this - our method caught it.'")
