"""
Visualize downloaded satellite data to verify quality
"""

import rasterio
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("data/satellite")

def visualize_sentinel2(filepath, title):
    """
    Visualize Sentinel-2 data with RGB composite and vegetation indices
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath.name}")
    print('='*60)

    with rasterio.open(filepath) as src:
        print(f"  Dimensions: {src.width} x {src.height} pixels")
        print(f"  Bands: {src.count}")
        print(f"  CRS: {src.crs}")
        print(f"  Bounds: {src.bounds}")

        # Band names from our export
        # B2 (Blue), B3 (Green), B4 (Red), B8 (NIR), B11 (SWIR1), B12 (SWIR2), NDVI, NBR, NDMI

        # Read bands
        b2 = src.read(1)  # Blue
        b3 = src.read(2)  # Green
        b4 = src.read(3)  # Red
        b8 = src.read(4)  # NIR
        ndvi = src.read(7)  # NDVI
        nbr = src.read(8)  # NBR
        ndmi = src.read(9)  # NDMI

        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(title, fontsize=16)

        # RGB composite (True color)
        rgb = np.dstack([b4, b3, b2])
        rgb_normalized = np.clip(rgb / 3000, 0, 1)  # Sentinel-2 typical range
        axes[0, 0].imshow(rgb_normalized)
        axes[0, 0].set_title('True Color RGB')
        axes[0, 0].axis('off')

        # False color (NIR, Red, Green) - vegetation shows red
        false_color = np.dstack([b8, b4, b3])
        false_color_normalized = np.clip(false_color / 3000, 0, 1)
        axes[0, 1].imshow(false_color_normalized)
        axes[0, 1].set_title('False Color (NIR-R-G)\nHealthy vegetation = Red')
        axes[0, 1].axis('off')

        # NDVI (vegetation health)
        ndvi_plot = axes[0, 2].imshow(ndvi, cmap='RdYlGn', vmin=-0.5, vmax=1)
        axes[0, 2].set_title('NDVI (Vegetation Index)\nGreen = Healthy vegetation')
        axes[0, 2].axis('off')
        plt.colorbar(ndvi_plot, ax=axes[0, 2], fraction=0.046)

        # NBR (burn ratio - sensitive to fire)
        nbr_plot = axes[1, 0].imshow(nbr, cmap='RdYlGn', vmin=-1, vmax=1)
        axes[1, 0].set_title('NBR (Normalized Burn Ratio)\nGreen = Unburned, Red = Burned')
        axes[1, 0].axis('off')
        plt.colorbar(nbr_plot, ax=axes[1, 0], fraction=0.046)

        # NDMI (moisture)
        ndmi_plot = axes[1, 1].imshow(ndmi, cmap='Blues', vmin=-1, vmax=1)
        axes[1, 1].set_title('NDMI (Moisture Index)\nDark blue = Dry, Light blue = Moist')
        axes[1, 1].axis('off')
        plt.colorbar(ndmi_plot, ax=axes[1, 1], fraction=0.046)

        # Statistics
        stats_text = f"""
Statistics:
NDVI: {np.nanmean(ndvi):.3f} (mean)
      {np.nanmin(ndvi):.3f} to {np.nanmax(ndvi):.3f} (range)

NBR:  {np.nanmean(nbr):.3f} (mean)
      {np.nanmin(nbr):.3f} to {np.nanmax(nbr):.3f} (range)

NDMI: {np.nanmean(ndmi):.3f} (mean)
      {np.nanmin(ndmi):.3f} to {np.nanmax(ndmi):.3f} (range)
        """
        axes[1, 2].text(0.1, 0.5, stats_text, fontsize=11,
                       verticalalignment='center', family='monospace')
        axes[1, 2].axis('off')

        plt.tight_layout()
        output_path = filepath.parent / f"{filepath.stem}_visualization.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  ✓ Visualization saved to: {output_path}")
        plt.close(fig)

def visualize_modis(filepath, title):
    """
    Visualize MODIS vegetation indices
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath.name}")
    print('='*60)

    with rasterio.open(filepath) as src:
        print(f"  Dimensions: {src.width} x {src.height} pixels")
        print(f"  Bands: {src.count}")
        print(f"  CRS: {src.crs}")

        # MODIS MOD13Q1 has NDVI and EVI
        ndvi = src.read(1) * 0.0001  # MODIS NDVI scale factor
        evi = src.read(2) * 0.0001   # MODIS EVI scale factor

        # Create figure
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(title, fontsize=16)

        # NDVI
        ndvi_plot = axes[0].imshow(ndvi, cmap='RdYlGn', vmin=-0.2, vmax=1)
        axes[0].set_title('MODIS NDVI\n(250m resolution)')
        axes[0].axis('off')
        plt.colorbar(ndvi_plot, ax=axes[0], fraction=0.046)

        # EVI
        evi_plot = axes[1].imshow(evi, cmap='RdYlGn', vmin=-0.2, vmax=1)
        axes[1].set_title('MODIS EVI\n(Enhanced Vegetation Index)')
        axes[1].axis('off')
        plt.colorbar(evi_plot, ax=axes[1], fraction=0.046)

        print(f"  NDVI: {np.nanmean(ndvi):.3f} (mean), {np.nanmin(ndvi):.3f} to {np.nanmax(ndvi):.3f}")
        print(f"  EVI:  {np.nanmean(evi):.3f} (mean), {np.nanmin(evi):.3f} to {np.nanmax(evi):.3f}")

        plt.tight_layout()
        output_path = filepath.parent / f"{filepath.stem}_visualization.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  ✓ Visualization saved to: {output_path}")
        plt.close(fig)

def visualize_landsat(filepath, title):
    """
    Visualize Landsat 8 data
    """
    print(f"\n{'='*60}")
    print(f"Analyzing: {filepath.name}")
    print('='*60)

    with rasterio.open(filepath) as src:
        print(f"  Dimensions: {src.width} x {src.height} pixels")
        print(f"  Bands: {src.count}")
        print(f"  CRS: {src.crs}")

        # Landsat bands: SR_B4 (Red), SR_B5 (NIR), ST_B10 (Thermal)
        red = src.read(1) * 0.0000275 - 0.2  # Landsat scaling
        nir = src.read(2) * 0.0000275 - 0.2
        thermal = src.read(3) * 0.00341802 + 149.0 - 273.15  # Convert to Celsius

        # Calculate NDVI
        ndvi = (nir - red) / (nir + red + 1e-10)

        # Create figure
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        fig.suptitle(title, fontsize=16)

        # False color
        false_color = np.dstack([nir, red, red])
        false_color_normalized = np.clip(false_color, 0, 0.3) / 0.3
        axes[0].imshow(false_color_normalized)
        axes[0].set_title('False Color (NIR-R-R)')
        axes[0].axis('off')

        # NDVI
        ndvi_plot = axes[1].imshow(ndvi, cmap='RdYlGn', vmin=-0.2, vmax=1)
        axes[1].set_title('NDVI from Landsat')
        axes[1].axis('off')
        plt.colorbar(ndvi_plot, ax=axes[1], fraction=0.046)

        # Thermal
        thermal_plot = axes[2].imshow(thermal, cmap='hot', vmin=0, vmax=40)
        axes[2].set_title('Surface Temperature (°C)')
        axes[2].axis('off')
        plt.colorbar(thermal_plot, ax=axes[2], fraction=0.046)

        print(f"  NDVI: {np.nanmean(ndvi):.3f} (mean)")
        print(f"  Temp: {np.nanmean(thermal):.1f}°C (mean), {np.nanmin(thermal):.1f}°C to {np.nanmax(thermal):.1f}°C")

        plt.tight_layout()
        output_path = filepath.parent / f"{filepath.stem}_visualization.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"  ✓ Visualization saved to: {output_path}")
        plt.close(fig)

def main():
    """
    Main visualization function
    """
    print("="*60)
    print("SATELLITE DATA VISUALIZATION")
    print("="*60)

    # Check for Sentinel-2 pre-fire
    prefire_s2 = DATA_DIR / "hermits_peak_prefire_2020_2022.tif"
    if prefire_s2.exists():
        visualize_sentinel2(prefire_s2, "Sentinel-2 Pre-Fire (2020-2022)")
    else:
        print(f"  Missing: {prefire_s2.name}")

    # Check for Sentinel-2 post-fire
    postfire_s2 = DATA_DIR / "hermits_peak_postfire_2022.tif"
    if postfire_s2.exists():
        visualize_sentinel2(postfire_s2, "Sentinel-2 Post-Fire (Aug-Dec 2022)")
    else:
        print(f"  Missing: {postfire_s2.name}")

    # Check for MODIS pre-fire
    prefire_modis = DATA_DIR / "hermits_peak_modis_prefire.tif"
    if prefire_modis.exists():
        visualize_modis(prefire_modis, "MODIS Pre-Fire Vegetation (2020-2022)")
    else:
        print(f"  Missing: {prefire_modis.name}")

    # Check for MODIS post-fire
    postfire_modis = DATA_DIR / "hermits_peak_modis_postfire.tif"
    if postfire_modis.exists():
        visualize_modis(postfire_modis, "MODIS Post-Fire Vegetation (Aug-Dec 2022)")
    else:
        print(f"  Missing: {postfire_modis.name}")

    # Check for Landsat
    landsat = DATA_DIR / "hermits_peak_landsat8_prefire.tif"
    if landsat.exists():
        visualize_landsat(landsat, "Landsat 8 Pre-Fire (2020-2022)")
    else:
        print(f"  Missing: {landsat.name}")

    print("\n" + "="*60)
    print("VISUALIZATION COMPLETE!")
    print("="*60)
    print("\nCheck the data/satellite/ folder for visualization PNGs")

if __name__ == "__main__":
    main()
