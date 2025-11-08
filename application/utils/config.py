"""
Configuration management for the project
"""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Config:
    """Project configuration"""

    # Root directory
    ROOT_DIR: Path = Path(__file__).parent.parent.parent

    # Data directories
    DATA_DIR: Path = ROOT_DIR / 'data'
    LANDFIRE_DIR: Path = DATA_DIR / 'landfire'
    SENTINEL_DIR: Path = DATA_DIR / 'satellite' / 'sentinel2'
    MODIS_DIR: Path = DATA_DIR / 'satellite' / 'modis'
    FIRE_PERIMETER_DIR: Path = DATA_DIR / 'fire_perimeters'
    PROCESSED_DIR: Path = DATA_DIR / 'processed'
    RESULTS_DIR: Path = DATA_DIR / 'results'

    # Output directories
    OUTPUTS_DIR: Path = ROOT_DIR / 'outputs'
    FIGURES_DIR: Path = OUTPUTS_DIR / 'figures'
    MAPS_DIR: Path = OUTPUTS_DIR / 'maps'
    REPORTS_DIR: Path = OUTPUTS_DIR / 'reports'

    # Config directory
    CONFIG_DIR: Path = ROOT_DIR / 'config'

    # File paths
    FIRE_AOI_PATH: Path = FIRE_PERIMETER_DIR / 'hermits_peak_area_of_interest.geojson'

    # Coordinate Reference System
    TARGET_CRS: str = 'EPSG:32613'  # UTM Zone 13N

    # Fire metadata
    FIRE_NAME: str = 'Hermits Peak-Calf Canyon Fire'
    FIRE_YEAR: int = 2022
    FIRE_START_DATE: str = '2022-04-06'
    FIRE_END_DATE: str = '2022-08-21'
    FIRE_SIZE_ACRES: int = 341735
    FIRE_DAMAGE_USD: int = 4_000_000_000

    # Bounding box (lat/lon)
    BBOX_MINX: float = -105.9
    BBOX_MINY: float = 35.6
    BBOX_MAXX: float = -105.3
    BBOX_MAXY: float = 36.0

    # Thresholds
    NDVI_LOSS_THRESHOLD: float = -0.1
    NBR_LOSS_THRESHOLD: float = -0.1
    CLOUD_COVER_MAX: int = 20

    def __post_init__(self):
        """Create directories if they don't exist"""
        self.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        self.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        self.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        self.MAPS_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)


# Singleton instance
config = Config()
