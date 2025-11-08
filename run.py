#!/usr/bin/env python3
"""
Main execution script for Hermits Peak Fuel Mapping Pipeline

Usage:
    python run.py --step all              # Run entire pipeline
    python run.py --step preprocess       # Just preprocessing
    python run.py --step analysis         # Just analysis
    python run.py --step visualize        # Just visualization
    python run.py --step dashboard        # Launch dashboard
"""

import argparse
import sys
from pathlib import Path

# Add application to path
sys.path.insert(0, str(Path(__file__).parent / 'application'))

from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


def run_preprocessing():
    """Run data preprocessing pipeline"""
    logger.info("=" * 60)
    logger.info("STEP 1: Data Preprocessing")
    logger.info("=" * 60)

    from preprocessing.preprocess_data import main as preprocess_main
    preprocess_main()


def run_analysis():
    """Run fuel mapping analysis"""
    logger.info("=" * 60)
    logger.info("STEP 2: Fuel Mapping Analysis")
    logger.info("=" * 60)

    from analysis.fuel_mapping import main as analysis_main
    analysis_main()


def run_visualization():
    """Generate static visualizations"""
    logger.info("=" * 60)
    logger.info("STEP 3: Creating Visualizations")
    logger.info("=" * 60)

    # Check if visualization script exists
    viz_script = Path(__file__).parent / 'application' / 'visualization' / 'create_figures.py'

    if viz_script.exists():
        from visualization.create_figures import main as viz_main
        viz_main()
    else:
        logger.warning("Visualization script not found. Generating interactive maps only...")
        run_interactive_map()


def run_interactive_map():
    """Generate interactive HTML maps"""
    logger.info("=" * 60)
    logger.info("Creating Interactive Maps")
    logger.info("=" * 60)

    map_script = Path(__file__).parent / 'application' / 'visualization' / '05_create_interactive_map.py'

    if map_script.exists():
        import subprocess
        subprocess.run([sys.executable, str(map_script)])
    else:
        logger.error(f"Interactive map script not found: {map_script}")


def run_dashboard():
    """Launch Streamlit dashboard"""
    logger.info("=" * 60)
    logger.info("Launching Dashboard")
    logger.info("=" * 60)

    dashboard_script = Path(__file__).parent / 'application' / 'dashboard_app.py'

    if dashboard_script.exists():
        import subprocess
        subprocess.run(['streamlit', 'run', str(dashboard_script)])
    else:
        logger.error(f"Dashboard script not found: {dashboard_script}")


def main():
    parser = argparse.ArgumentParser(
        description='Hermits Peak Wildfire Fuel Mapping Pipeline'
    )
    parser.add_argument(
        '--step',
        choices=['all', 'preprocess', 'analysis', 'visualize', 'map', 'dashboard'],
        default='all',
        help='Which step to run'
    )

    args = parser.parse_args()

    logger.info("🔥 Hermits Peak Wildfire Fuel Mapping Pipeline")
    logger.info("")

    if args.step in ['all', 'preprocess']:
        run_preprocessing()

    if args.step in ['all', 'analysis']:
        run_analysis()

    if args.step in ['all', 'visualize']:
        run_visualization()

    if args.step == 'map':
        run_interactive_map()

    if args.step == 'dashboard':
        run_dashboard()

    if args.step == 'all':
        logger.info("")
        logger.info("=" * 60)
        logger.info("✅ PIPELINE COMPLETE!")
        logger.info("=" * 60)
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Check outputs/ directory for results")
        logger.info("  2. Run: python run.py --step map")
        logger.info("  3. Run: python run.py --step dashboard")


if __name__ == '__main__':
    main()
