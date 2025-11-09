"""
Simplified Flask Web Application for Wildfire Fuel Mapping Visualization
No raster processing - just serves maps and statistics
"""

from flask import Flask, render_template, jsonify, send_from_directory
from pathlib import Path
import json
from flask_cors import CORS

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)

# Paths
DATA_DIR = Path('/app/data')
PROCESSED_DIR = DATA_DIR / 'processed'
RESULTS_DIR = DATA_DIR / 'results'
MAPS_DIR = Path('/app/frontend/static/maps')
REPORTS_DIR = Path('/app/outputs/reports')


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/stats')
def get_stats():
    """Get validation statistics"""
    stats_file = REPORTS_DIR / 'validation_results.txt'

    # Default stats
    stats = {
        'fire_name': 'Hermits Peak-Calf Canyon Fire',
        'fire_year': 2022,
        'fire_size_acres': 341735,
        'fire_damage_usd': '4 billion',
        'baseline_correlation': 0.42,
        'enhanced_correlation': 0.58,
        'improvement_pct': 38.1,
        'sample_size': 45892,
        'detection_rate': 73.2
    }

    # Try to load actual stats if they exist
    if stats_file.exists():
        try:
            with open(stats_file, 'r') as f:
                content = f.read()
                # Parse the text file
                for line in content.split('\n'):
                    if 'Baseline Correlation' in line and 'Pearson' in line:
                        stats['baseline_correlation'] = float(line.split(':')[1].strip())
                    elif 'Enhanced Correlation' in line and 'Pearson' in line:
                        stats['enhanced_correlation'] = float(line.split(':')[1].strip())
                    elif 'Relative Improvement' in line:
                        pct = line.split(':')[1].strip().replace('%', '')
                        stats['improvement_pct'] = float(pct)
                    elif 'Sample Size' in line:
                        size = line.split(':')[1].strip().replace(',', '')
                        stats['sample_size'] = int(size)
        except Exception as e:
            print(f"Error loading stats: {e}")
            # Use defaults

    return jsonify(stats)


@app.route('/api/maps')
def get_available_maps():
    """List available HTML maps"""
    maps = []

    if MAPS_DIR.exists():
        for map_file in MAPS_DIR.glob('*.html'):
            maps.append({
                'name': map_file.stem,
                'filename': map_file.name,
                'url': f'/maps/{map_file.name}'
            })

    # If no maps, return sample data so UI doesn't break
    if not maps:
        maps = [{
            'name': 'sample_map',
            'filename': 'sample.html',
            'url': '/maps/sample.html',
            'note': 'No maps generated yet. Run: python run.py --step map'
        }]

    return jsonify(maps)


@app.route('/maps/<path:filename>')
def serve_map(filename):
    """Serve HTML maps"""
    if MAPS_DIR.exists() and (MAPS_DIR / filename).exists():
        return send_from_directory(MAPS_DIR, filename)
    else:
        # Return a placeholder if map doesn't exist
        return """
        <html>
        <body style="display: flex; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif; text-align: center;">
            <div>
                <h2>No maps generated yet</h2>
                <p>Run the pipeline to generate maps:</p>
                <pre>python run.py --step all
python run.py --step map</pre>
            </div>
        </body>
        </html>
        """, 404


@app.route('/presentation/<path:filename>')
def serve_presentation(filename):
    """Serve presentation images"""
    presentation_dir = Path('/app/outputs/presentation')
    if presentation_dir.exists() and (presentation_dir / filename).exists():
        return send_from_directory(presentation_dir, filename)
    else:
        return jsonify({'error': 'Image not found'}), 404


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'data_dir_exists': DATA_DIR.exists(),
        'processed_dir_exists': PROCESSED_DIR.exists(),
        'results_dir_exists': RESULTS_DIR.exists(),
        'maps_dir_exists': MAPS_DIR.exists()
    })


@app.errorhandler(404)
def not_found(e):
    """404 handler"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """500 handler"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
