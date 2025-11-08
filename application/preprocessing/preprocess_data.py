"""
Data Preprocessing Pipeline
Loads, reprojects, clips, and normalizes all datasets
"""

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
import numpy as np
import geopandas as gpd
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DataPreprocessor:
    """Handles all data preprocessing tasks"""

    def __init__(self, config: Config):
        self.config = config
        self.target_crs = config.TARGET_CRS

    def reproject_and_clip(self, input_path: Path, output_path: Path,
                          bounds=None, aoi_geometry=None):
        """
        Reproject raster to target CRS and optionally clip to AOI

        Args:
            input_path: Path to input raster
            output_path: Path to output raster
            bounds: Optional bounding box (minx, miny, maxx, maxy)
            aoi_geometry: Optional GeoDataFrame geometry for masking
        """
        logger.info(f"Processing {input_path.name}...")

        with rasterio.open(input_path) as src:
            # Calculate transform for reprojection
            transform, width, height = calculate_default_transform(
                src.crs, self.target_crs, src.width, src.height, *src.bounds
            )

            # Update metadata
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': self.target_crs,
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
                        dst_crs=self.target_crs,
                        resampling=Resampling.nearest
                    )

        # Clip if geometry provided
        if aoi_geometry is not None:
            self._clip_to_geometry(output_path, aoi_geometry)

        logger.info(f"  ✓ Saved to {output_path}")

    def _clip_to_geometry(self, raster_path: Path, geometry):
        """Clip raster to geometry in-place"""
        with rasterio.open(raster_path, 'r+') as src:
            out_image, out_transform = mask(src, geometry, crop=True)
            src.write(out_image)

    def calculate_vegetation_indices(self):
        """Calculate NDVI, NBR, NDMI from Sentinel-2 bands"""
        logger.info("Calculating vegetation indices...")

        # NDVI change
        ndvi_2020 = self._load_raster(self.config.PROCESSED_DIR / 'ndvi_2020_processed.tif')
        ndvi_2022 = self._load_raster(self.config.PROCESSED_DIR / 'ndvi_2022_processed.tif')
        ndvi_change = ndvi_2022 - ndvi_2020

        self._save_raster(
            ndvi_change,
            self.config.PROCESSED_DIR / 'ndvi_change.tif',
            reference_path=self.config.PROCESSED_DIR / 'ndvi_2020_processed.tif'
        )

        # NBR change
        nbr_2020 = self._load_raster(self.config.PROCESSED_DIR / 'nbr_2020_processed.tif')
        nbr_2022 = self._load_raster(self.config.PROCESSED_DIR / 'nbr_2022_processed.tif')
        nbr_change = nbr_2022 - nbr_2020

        self._save_raster(
            nbr_change,
            self.config.PROCESSED_DIR / 'nbr_change.tif',
            reference_path=self.config.PROCESSED_DIR / 'nbr_2020_processed.tif'
        )

        logger.info("  ✓ Vegetation indices calculated")

    def calculate_burn_severity(self):
        """Calculate dNBR and classify burn severity"""
        logger.info("Calculating burn severity...")

        nbr_prefire = self._load_raster(self.config.PROCESSED_DIR / 'nbr_2022_processed.tif')
        nbr_postfire = self._load_raster(self.config.PROCESSED_DIR / 'nbr_postfire_processed.tif')

        # dNBR = pre - post
        dnbr = nbr_prefire - nbr_postfire

        self._save_raster(
            dnbr,
            self.config.PROCESSED_DIR / 'dnbr.tif',
            reference_path=self.config.PROCESSED_DIR / 'nbr_2022_processed.tif'
        )

        # Classify
        burn_severity = np.zeros_like(dnbr, dtype='uint8')
        burn_severity[dnbr < 0.1] = 0  # Unburned
        burn_severity[(dnbr >= 0.1) & (dnbr < 0.27)] = 1  # Low
        burn_severity[(dnbr >= 0.27) & (dnbr < 0.66)] = 2  # Moderate-low
        burn_severity[(dnbr >= 0.66) & (dnbr < 1.3)] = 3  # Moderate-high
        burn_severity[dnbr >= 1.3] = 4  # High

        self._save_raster(
            burn_severity,
            self.config.PROCESSED_DIR / 'burn_severity_classified.tif',
            reference_path=self.config.PROCESSED_DIR / 'nbr_2022_processed.tif',
            dtype='uint8'
        )

        logger.info("  ✓ Burn severity calculated")

    def _load_raster(self, path: Path) -> np.ndarray:
        """Load raster as numpy array"""
        with rasterio.open(path) as src:
            return src.read(1).astype('float32')

    def _save_raster(self, data: np.ndarray, output_path: Path,
                     reference_path: Path, dtype='float32'):
        """Save numpy array as raster using reference metadata"""
        with rasterio.open(reference_path) as src:
            profile = src.profile.copy()
            profile.update(dtype=dtype, nodata=np.nan if dtype == 'float32' else 255)

        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data, 1)


def main():
    """Run preprocessing pipeline"""
    config = Config()
    preprocessor = DataPreprocessor(config)

    # Load AOI
    fire_aoi = gpd.read_file(config.FIRE_AOI_PATH)
    fire_aoi_utm = fire_aoi.to_crs(config.TARGET_CRS)

    # Process all datasets
    datasets = {
        'fbfm40': config.LANDFIRE_DIR / 'LF2020_FBFM40_200_CONUS.tif',
        'cbd': config.LANDFIRE_DIR / 'LF2020_CBD_200_CONUS.tif',
        'ch': config.LANDFIRE_DIR / 'LF2020_CH_200_CONUS.tif',
        'ndvi_2020': config.SENTINEL_DIR / 'ndvi_2020.tif',
        'ndvi_2022': config.SENTINEL_DIR / 'ndvi_2022.tif',
        'nbr_2020': config.SENTINEL_DIR / 'nbr_2020.tif',
        'nbr_2022': config.SENTINEL_DIR / 'nbr_2022.tif',
        'nbr_postfire': config.SENTINEL_DIR / 'nbr_postfire_2022.tif',
    }

    for name, input_path in datasets.items():
        if input_path.exists():
            output_path = config.PROCESSED_DIR / f'{name}_processed.tif'
            preprocessor.reproject_and_clip(
                input_path,
                output_path,
                aoi_geometry=fire_aoi_utm.geometry
            )
        else:
            logger.warning(f"  ⚠ {input_path.name} not found, skipping")

    # Calculate derived products
    preprocessor.calculate_vegetation_indices()
    preprocessor.calculate_burn_severity()

    logger.info("✅ Preprocessing complete!")


if __name__ == '__main__':
    main()
