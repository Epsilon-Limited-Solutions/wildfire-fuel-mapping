#!/usr/bin/env python3
"""
Generate individual map visualizations for presentation
Creates clean, presentation-ready maps of each key output
"""

import numpy as np
import matplotlib.pyplot as plt
import rasterio
from pathlib import Path
import json

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / 'outputs'
MAPS_ONLY_DIR = OUTPUT_DIR / 'maps_only'
MAPS_ONLY_DIR.mkdir(exist_ok=True)

# Load fire boundary for context
FIRE_BOUNDARY = OUTPUT_DIR.parent / 'data' / 'fire_boundary.geojson'

def load_geotiff(path):
    """Load a GeoTIFF file"""
    with rasterio.open(path) as src:
        data = src.read(1)
        bounds = src.bounds
        return data, bounds

def create_map_figure(data, title, cmap='RdYlGn_r', vmin=None, vmax=None,
                      cbar_label='', figsize=(12, 10)):
    """Create a clean map figure"""
    fig, ax = plt.subplots(figsize=figsize, facecolor='white')

    # Handle NaN values
    masked_data = np.ma.masked_invalid(data)

    # Plot
    im = ax.imshow(masked_data, cmap=cmap, vmin=vmin, vmax=vmax,
                   interpolation='nearest', aspect='auto')

    # Styling
    ax.set_title(title, fontsize=20, fontweight='bold', pad=20)
    ax.axis('off')

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04,
                       label=cbar_label, shrink=0.8)
    cbar.ax.tick_params(labelsize=12)
    cbar.set_label(cbar_label, size=14, weight='bold')

    plt.tight_layout()
    return fig

def generate_stress_score_map():
    """Generate vegetation stress score map"""
    print("Generating vegetation stress score map...")

    stress_file = OUTPUT_DIR / 'change_maps' / 'stress_score.tif'
    if not stress_file.exists():
        print(f"  Skipping: {stress_file} not found")
        return

    data, bounds = load_geotiff(stress_file)

    fig = create_map_figure(
        data,
        title='Vegetation Stress Score (2020-2022)',
        cmap='RdYlGn_r',
        vmin=0,
        vmax=1,
        cbar_label='Stress Score (0=healthy, 1=severe stress)'
    )

    output_file = MAPS_ONLY_DIR / 'stress_score_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def generate_ndvi_change_map():
    """Generate NDVI change map"""
    print("Generating NDVI change map...")

    ndvi_file = OUTPUT_DIR / 'change_maps' / 'ndvi_change.tif'
    if not ndvi_file.exists():
        print(f"  Skipping: {ndvi_file} not found")
        return

    data, bounds = load_geotiff(ndvi_file)

    fig = create_map_figure(
        data,
        title='NDVI Change (2020-2022)',
        cmap='RdYlGn',
        vmin=-0.3,
        vmax=0.3,
        cbar_label='NDVI Change (negative = vegetation loss)'
    )

    output_file = MAPS_ONLY_DIR / 'ndvi_change_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def generate_fuel_load_map():
    """Generate fuel load factor map"""
    print("Generating fuel load factor map...")

    fuel_file = OUTPUT_DIR / 'enhanced_fuel' / 'fuel_load_factor.tif'
    if not fuel_file.exists():
        print(f"  Skipping: {fuel_file} not found")
        return

    data, bounds = load_geotiff(fuel_file)

    fig = create_map_figure(
        data,
        title='Enhanced Fuel Load Factor',
        cmap='YlOrRd',
        vmin=1.0,
        vmax=2.0,
        cbar_label='Fuel Load Multiplier (1.0 = baseline)'
    )

    output_file = MAPS_ONLY_DIR / 'fuel_load_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def generate_fuel_risk_map():
    """Generate fuel risk score map"""
    print("Generating fuel risk score map...")

    risk_file = OUTPUT_DIR / 'enhanced_fuel' / 'fuel_risk_score.tif'
    if not risk_file.exists():
        print(f"  Skipping: {risk_file} not found")
        return

    data, bounds = load_geotiff(risk_file)

    fig = create_map_figure(
        data,
        title='Fuel Risk Score (Enhanced)',
        cmap='RdYlGn_r',
        vmin=0,
        vmax=10,
        cbar_label='Risk Score (0=low, 10=extreme)'
    )

    output_file = MAPS_ONLY_DIR / 'fuel_risk_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def generate_burn_severity_map():
    """Generate actual burn severity map"""
    print("Generating burn severity map...")

    burn_file = OUTPUT_DIR / 'burn_severity' / 'dnbr.tif'
    if not burn_file.exists():
        print(f"  Skipping: {burn_file} not found")
        return

    data, bounds = load_geotiff(burn_file)

    fig = create_map_figure(
        data,
        title='Actual Burn Severity (dNBR)',
        cmap='hot_r',
        vmin=0,
        vmax=800,
        cbar_label='dNBR (higher = more severe)'
    )

    output_file = MAPS_ONLY_DIR / 'burn_severity_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def generate_burn_severity_classified_map():
    """Generate classified burn severity map"""
    print("Generating classified burn severity map...")

    burn_file = OUTPUT_DIR / 'burn_severity' / 'burn_severity_classified.tif'
    if not burn_file.exists():
        print(f"  Skipping: {burn_file} not found")
        return

    data, bounds = load_geotiff(burn_file)

    # Custom colormap for burn severity classes
    from matplotlib.colors import ListedColormap
    colors = ['#2166ac', '#92c5de', '#fddbc7', '#f4a582', '#d6604d', '#b2182b']
    cmap = ListedColormap(colors)

    fig = create_map_figure(
        data,
        title='Burn Severity Classification',
        cmap=cmap,
        vmin=0,
        vmax=5,
        cbar_label='Severity Class (0=Unburned, 5=Extreme)'
    )

    output_file = MAPS_ONLY_DIR / 'burn_severity_classified_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def generate_nbr_change_map():
    """Generate NBR change map"""
    print("Generating NBR change map...")

    nbr_file = OUTPUT_DIR / 'change_maps' / 'nbr_change.tif'
    if not nbr_file.exists():
        print(f"  Skipping: {nbr_file} not found")
        return

    data, bounds = load_geotiff(nbr_file)

    fig = create_map_figure(
        data,
        title='NBR Change (2020-2022)',
        cmap='RdYlGn',
        vmin=-0.3,
        vmax=0.3,
        cbar_label='NBR Change (negative = fuel accumulation)'
    )

    output_file = MAPS_ONLY_DIR / 'nbr_change_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def generate_ndmi_change_map():
    """Generate NDMI change map"""
    print("Generating NDMI change map...")

    ndmi_file = OUTPUT_DIR / 'change_maps' / 'ndmi_change.tif'
    if not ndmi_file.exists():
        print(f"  Skipping: {ndmi_file} not found")
        return

    data, bounds = load_geotiff(ndmi_file)

    fig = create_map_figure(
        data,
        title='NDMI Change (2020-2022)',
        cmap='RdYlGn',
        vmin=-0.3,
        vmax=0.3,
        cbar_label='NDMI Change (negative = moisture deficit)'
    )

    output_file = MAPS_ONLY_DIR / 'ndmi_change_map.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  Saved: {output_file}")

def main():
    """Generate all individual maps"""
    print("=" * 60)
    print("GENERATING INDIVIDUAL MAPS FOR PRESENTATION")
    print("=" * 60)
    print()

    # Change detection maps
    print("Change Detection Maps:")
    generate_stress_score_map()
    generate_ndvi_change_map()
    generate_nbr_change_map()
    generate_ndmi_change_map()
    print()

    # Enhanced fuel maps
    print("Enhanced Fuel Maps:")
    generate_fuel_load_map()
    generate_fuel_risk_map()
    print()

    # Burn severity maps
    print("Burn Severity Maps:")
    generate_burn_severity_map()
    generate_burn_severity_classified_map()
    print()

    print("=" * 60)
    print(f"✓ All maps saved to: {MAPS_ONLY_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
