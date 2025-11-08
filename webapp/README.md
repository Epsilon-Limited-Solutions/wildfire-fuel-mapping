# Wildfire Fuel Mapping Web Application

Docker-based web application for visualizing wildfire fuel mapping results.

---

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Completed data processing pipeline (`python run.py --step all` from parent directory)
- Generated interactive maps in `../outputs/maps/`

### Running the Application

```bash
# From the webapp directory
cd webapp

# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

The application will be available at: **http://localhost:5000**

### Stopping the Application

```bash
# Stop the container
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## 📁 Directory Structure

```
webapp/
├── backend/
│   └── app.py              # Flask application
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css   # Styling
│   │   ├── js/
│   │   │   └── main.js     # Client-side JavaScript
│   │   └── maps/           # Mounted from ../outputs/maps/
│   └── templates/
│       └── index.html      # Main HTML template
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🎯 Features

### 📊 Interactive Dashboard
- Real-time statistics and metrics
- Validation results display
- Fire information summary

### 🗺️ Map Viewer
- View interactive HTML maps directly in browser
- Side-by-side comparison maps
- Full pan, zoom, and layer controls

### 📈 Analysis Results
- Correlation metrics
- Detection performance statistics
- Methodology overview
- Data sources information

### 🔄 Multi-Tab Interface
1. **Interactive Maps** - Browse and view generated maps
2. **Comparison View** - LANDFIRE baseline vs Enhanced fuel map
3. **Methodology** - Technical approach and data sources
4. **Data & Analysis** - Validation metrics and use cases

---

## 🔧 Configuration

### Data Mounting

The application mounts data as read-only volumes from the parent directory:

```yaml
volumes:
  - ../data:/app/data:ro              # Input and processed data
  - ../outputs:/app/outputs:ro        # Analysis outputs
  - ../outputs/maps:/app/frontend/static/maps:ro  # Interactive maps
```

### Port Configuration

Default port: `5000`

To change the port, edit `docker-compose.yml`:

```yaml
ports:
  - "8080:5000"  # External:Internal
```

---

## 🌐 API Endpoints

### `GET /`
Main web interface

### `GET /api/stats`
Returns validation statistics and metrics
```json
{
  "fire_name": "Hermits Peak-Calf Canyon Fire",
  "fire_year": 2022,
  "fire_size_acres": 341735,
  "baseline_correlation": 0.42,
  "enhanced_correlation": 0.58,
  "improvement_pct": 38.1,
  "sample_size": 45892,
  "detection_rate": 73.2
}
```

### `GET /api/maps`
List available interactive maps
```json
[
  {
    "name": "hermits_peak_comparison_map",
    "filename": "hermits_peak_comparison_map.html",
    "url": "/maps/hermits_peak_comparison_map.html"
  }
]
```

### `GET /api/raster/<raster_name>`
Get raster metadata and statistics

Supported rasters:
- `ndvi_change`
- `nbr_change`
- `burn_severity`
- `fuel_hazard`
- `fbfm40`

### `GET /maps/<filename>`
Serve interactive HTML maps

### `GET /api/health`
Health check endpoint

---

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs -f

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### No maps showing
1. Ensure you've run the pipeline: `python ../run.py --step all`
2. Generate maps: `python ../run.py --step map`
3. Check `../outputs/maps/` directory contains HTML files
4. Restart container: `docker-compose restart`

### Port already in use
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in docker-compose.yml
```

### Data not loading
1. Verify data directory structure:
   ```bash
   ls -la ../data/processed/
   ls -la ../data/results/
   ls -la ../outputs/reports/
   ```
2. Check file permissions
3. Restart container

---

## 🚀 Production Deployment

### Using Gunicorn

For production, use Gunicorn instead of Flask development server:

```dockerfile
# In Dockerfile, replace CMD with:
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "backend.app:app"]
```

### Environment Variables

Create `.env` file:
```bash
FLASK_ENV=production
FLASK_APP=backend/app.py
```

### Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 📊 Performance

### Resource Requirements
- **CPU**: 1-2 cores
- **RAM**: 2-4 GB
- **Disk**: Minimal (data is mounted read-only)
- **Network**: HTTP/HTTPS

### Optimization Tips
1. Use Gunicorn with multiple workers
2. Enable gzip compression
3. Cache static assets
4. Use CDN for large map files

---

## 🔒 Security

### Best Practices
- Run container as non-root user
- Mount data volumes as read-only (`:ro`)
- Use environment variables for sensitive config
- Enable HTTPS in production
- Implement rate limiting for API endpoints

### Network Isolation
The application uses a dedicated Docker network (`wildfire-network`) for isolation.

---

## 🧪 Development Mode

### Run without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=backend/app.py
export FLASK_ENV=development

# Run development server
cd backend
flask run --host=0.0.0.0 --port=5000
```

### Live Reloading

For development with live reload:

```yaml
# In docker-compose.yml
volumes:
  - ./backend:/app/backend
  - ./frontend:/app/frontend
environment:
  - FLASK_ENV=development
```

---

## 📚 Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Maps**: Leaflet.js (for interactive maps)
- **Containerization**: Docker, Docker Compose
- **Geospatial**: Rasterio, GeoPandas
- **Web Server**: Gunicorn (production)

---

## 🎬 Demo Workflow

1. **Build and start** the container
2. **Open browser** to http://localhost:5000
3. **Navigate tabs**:
   - View interactive maps
   - Explore comparison data
   - Review methodology
   - Check validation results
4. **Click map cards** to load and interact with maps
5. **Pan, zoom, toggle layers** in embedded map viewer

---

## 📝 Notes

- All data is mounted **read-only** to prevent accidental modifications
- Maps are served directly from `outputs/maps/` directory
- Statistics are loaded from `outputs/reports/validation_results.txt`
- Application runs on port 5000 by default
- Health checks run every 30 seconds

---

## 🆘 Support

**Common Issues:**
- Data not found → Run pipeline first: `python ../run.py --step all`
- Maps not loading → Generate maps: `python ../run.py --step map`
- Port conflict → Change port in `docker-compose.yml`
- Build errors → Install Docker and Docker Compose

**Container Commands:**
```bash
# View logs
docker-compose logs -f webapp

# Restart
docker-compose restart

# Shell into container
docker-compose exec webapp /bin/bash

# Check container status
docker-compose ps
```

---

## 🎯 Next Steps

After getting the webapp running:

1. **Customize branding** - Edit `frontend/static/css/style.css`
2. **Add features** - Extend `backend/app.py` with new endpoints
3. **Improve UI** - Modify `frontend/templates/index.html`
4. **Deploy** - Use Gunicorn + Nginx for production
5. **Monitor** - Set up logging and monitoring

---

**Ready to visualize your wildfire fuel maps!** 🔥🗺️
