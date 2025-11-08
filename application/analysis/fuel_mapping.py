"""
Fuel Change Detection and Enhanced Mapping
"""

import numpy as np
import rasterio
from pathlib import Path
from scipy.stats import pearsonr
import sys

sys.path.append(str(Path(__file__).parent.parent))
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FuelMapper:
    """Creates enhanced fuel maps from satellite change detection"""

    def __init__(self, config: Config):
        self.config = config

    def detect_fuel_changes(self):
        """Identify areas where fuel conditions changed 2020-2022"""
        logger.info("Detecting fuel changes...")

        # Load change metrics
        with rasterio.open(self.config.PROCESSED_DIR / 'ndvi_change.tif') as src:
            ndvi_change = src.read(1)
            profile = src.profile

        with rasterio.open(self.config.PROCESSED_DIR / 'nbr_change.tif') as src:
            nbr_change = src.read(1)

        # Detect fuel increase areas (negative change = vegetation loss)
        fuel_increase_mask = (
            (ndvi_change < self.config.NDVI_LOSS_THRESHOLD) |
            (nbr_change < self.config.NBR_LOSS_THRESHOLD)
        ).astype('uint8')

        # Save mask
        with rasterio.open(self.config.RESULTS_DIR / 'fuel_increase_areas.tif', 'w', **profile) as dst:
            dst.write(fuel_increase_mask, 1)

        # Calculate change magnitude
        change_magnitude = np.abs(ndvi_change) + np.abs(nbr_change)

        profile.update(dtype='float32')
        with rasterio.open(self.config.RESULTS_DIR / 'change_magnitude.tif', 'w', **profile) as dst:
            dst.write(change_magnitude, 1)

        logger.info("  ✓ Fuel change areas detected")

    def create_enhanced_fuel_map(self):
        """Generate enhanced fuel hazard map"""
        logger.info("Creating enhanced fuel hazard map...")

        # Load baseline
        with rasterio.open(self.config.PROCESSED_DIR / 'fbfm40_processed.tif') as src:
            fbfm40 = src.read(1)
            profile = src.profile

        with rasterio.open(self.config.PROCESSED_DIR / 'cbd_processed.tif') as src:
            cbd = src.read(1).astype('float32')

        with rasterio.open(self.config.PROCESSED_DIR / 'ndvi_change.tif') as src:
            ndvi_change = src.read(1)

        with rasterio.open(self.config.PROCESSED_DIR / 'nbr_change.tif') as src:
            nbr_change = src.read(1)

        # Create fuel hazard increase layer
        fuel_hazard = np.zeros_like(fbfm40, dtype='float32')

        # Combine signals
        significant_ndvi_loss = ndvi_change < -0.15
        significant_nbr_loss = nbr_change < -0.15
        high_canopy = cbd > 5

        fuel_hazard[significant_ndvi_loss] += 1.0
        fuel_hazard[significant_nbr_loss] += 1.0
        fuel_hazard[high_canopy] += 0.5

        # Normalize to 0-1
        if fuel_hazard.max() > 0:
            fuel_hazard = np.clip(fuel_hazard / fuel_hazard.max(), 0, 1)

        # Save
        profile.update(dtype='float32')
        with rasterio.open(self.config.RESULTS_DIR / 'fuel_hazard_enhanced.tif', 'w', **profile) as dst:
            dst.write(fuel_hazard, 1)

        logger.info("  ✓ Enhanced fuel hazard map created")

    def validate_against_burn_severity(self):
        """Calculate validation metrics"""
        logger.info("Validating against burn severity...")

        # Load actual burn severity
        with rasterio.open(self.config.PROCESSED_DIR / 'dnbr.tif') as src:
            actual_severity = src.read(1).flatten()

        # Load LANDFIRE baseline (convert to continuous hazard)
        with rasterio.open(self.config.PROCESSED_DIR / 'fbfm40_processed.tif') as src:
            fbfm40 = src.read(1).flatten()

        baseline_hazard = self._fbfm_to_hazard(fbfm40)

        # Load enhanced
        with rasterio.open(self.config.RESULTS_DIR / 'fuel_hazard_enhanced.tif') as src:
            enhanced_hazard = src.read(1).flatten()

        # Filter to burned areas
        burned_mask = (actual_severity > 0.1) & ~np.isnan(actual_severity) & ~np.isnan(enhanced_hazard)

        actual_valid = actual_severity[burned_mask]
        baseline_valid = baseline_hazard[burned_mask]
        enhanced_valid = enhanced_hazard[burned_mask]

        # Calculate correlations
        corr_baseline, p_baseline = pearsonr(baseline_valid, actual_valid)
        corr_enhanced, p_enhanced = pearsonr(enhanced_valid, actual_valid)

        # Calculate improvement
        improvement = corr_enhanced - corr_baseline
        improvement_pct = (improvement / corr_baseline) * 100

        # Save results
        results = {
            'sample_size': len(actual_valid),
            'baseline_correlation': corr_baseline,
            'enhanced_correlation': corr_enhanced,
            'improvement': improvement,
            'improvement_pct': improvement_pct,
            'p_value_baseline': p_baseline,
            'p_value_enhanced': p_enhanced
        }

        # Write to file
        with open(self.config.REPORTS_DIR / 'validation_results.txt', 'w') as f:
            f.write("VALIDATION RESULTS\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Sample Size (burned pixels): {results['sample_size']:,}\n")
            f.write(f"Baseline Correlation (Pearson): {results['baseline_correlation']:.4f}\n")
            f.write(f"Enhanced Correlation (Pearson): {results['enhanced_correlation']:.4f}\n")
            f.write(f"Absolute Improvement: {results['improvement']:.4f}\n")
            f.write(f"Relative Improvement: {results['improvement_pct']:.2f}%\n")
            f.write(f"P-value (baseline): {results['p_value_baseline']:.6f}\n")
            f.write(f"P-value (enhanced): {results['p_value_enhanced']:.6f}\n")

        logger.info(f"  Baseline correlation: {corr_baseline:.3f}")
        logger.info(f"  Enhanced correlation: {corr_enhanced:.3f}")
        logger.info(f"  Improvement: +{improvement:.3f} ({improvement_pct:+.1f}%)")
        logger.info(f"  ✓ Results saved to {self.config.REPORTS_DIR / 'validation_results.txt'}")

        return results

    def _fbfm_to_hazard(self, fbfm40: np.ndarray) -> np.ndarray:
        """Convert FBFM40 codes to continuous hazard (0-1)"""
        hazard = np.zeros_like(fbfm40, dtype='float32')

        # Simplified mapping (in reality, consult FBFM40 lookup table)
        hazard[(fbfm40 >= 101) & (fbfm40 <= 109)] = 0.3  # Grass
        hazard[(fbfm40 >= 120) & (fbfm40 <= 129)] = 0.5  # Shrub
        hazard[(fbfm40 >= 140) & (fbfm40 <= 149)] = 0.6  # Timber-grass
        hazard[(fbfm40 >= 180) & (fbfm40 <= 189)] = 0.8  # Timber

        return hazard


def main():
    """Run fuel mapping pipeline"""
    config = Config()
    mapper = FuelMapper(config)

    mapper.detect_fuel_changes()
    mapper.create_enhanced_fuel_map()
    results = mapper.validate_against_burn_severity()

    logger.info("✅ Fuel mapping complete!")


if __name__ == '__main__':
    main()
