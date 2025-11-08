# WebApp Overview

**Docker-based visualization platform for wildfire fuel mapping**

---

## 📁 Complete Directory Structure

```
webapp/
├── backend/
│   └── app.py                  # Flask API server
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Modern, responsive styling
│   │   ├── js/
│   │   │   └── main.js         # Client-side interactivity
│   │   └── maps/               # (Mounted from ../outputs/maps/)
│   │
│   └── templates/
│       └── index.html          # Single-page application
│
├── config/                     # (Reserved for future use)
├── data/                       # (Mounted from ../data/)
│
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Container orchestration
├── requirements.txt            # Python dependencies
├── .dockerignore              # Files to exclude from build
│
├── start.sh                   # Quick startup script ⭐
├── QUICKSTART.md              # 2-minute getting started
├── README.md                  # Complete documentation
└── OVERVIEW.md                # This file
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│                     localhost:5000                      │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP/HTTPS
                 │
┌────────────────▼────────────────────────────────────────┐
│                    Docker Container                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Flask Web Server                    │  │
│  │              (Port 5000)                         │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                   │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │            Backend API (Flask)                   │  │
│  │  - /api/stats                                    │  │
│  │  - /api/maps                                     │  │
│  │  - /api/raster/<name>                           │  │
│  │  - /api/health                                   │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                   │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │         Frontend (HTML/CSS/JS)                   │  │
│  │  - Interactive UI                                │  │
│  │  - Map viewer                                    │  │
│  │  - Statistics dashboard                          │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Mounted Volumes (Read-Only)              │  │
│  │  - /app/data          ← ../data/                │  │
│  │  - /app/outputs       ← ../outputs/             │  │
│  │  - /app/frontend/static/maps ← ../outputs/maps/ │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Features

### 🌐 Web Interface
- **Single-page application** - No page reloads
- **Responsive design** - Works on desktop, tablet, mobile
- **Modern UI** - Clean, professional styling
- **Tab navigation** - Easy content organization

### 🗺️ Map Visualization
- **Embedded map viewer** - View HTML maps directly in page
- **Interactive controls** - Pan, zoom, toggle layers
- **Multiple maps** - Switch between different visualizations
- **Full-screen mode** - Maximize map viewing area

### 📊 Data Display
- **Real-time stats** - Load from analysis results
- **Comparison view** - LANDFIRE vs Enhanced side-by-side
- **Methodology docs** - Explain technical approach
- **Use case examples** - Show operational applications

### 🔌 API Endpoints
- **RESTful API** - JSON responses
- **Health checks** - Monitor container status
- **Raster metadata** - Query dataset information
- **Map listing** - Discover available visualizations

---

## 🛠️ Technology Stack

### Backend
- **Flask** - Lightweight web framework
- **Rasterio** - Geospatial raster processing
- **GeoPandas** - Vector data handling
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with variables
- **Vanilla JavaScript** - No framework dependencies
- **Leaflet.js** - Interactive map library (CDN)

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Gunicorn** - Production WSGI server (optional)
- **Nginx** - Reverse proxy (optional)

---

## 🚀 Workflow

### 1. Build Phase
```bash
./start.sh
# OR
docker-compose up --build
```

**What happens:**
1. Reads `Dockerfile` to build image
2. Installs system dependencies (GDAL, etc.)
3. Installs Python packages from `requirements.txt`
4. Copies application code into container
5. Creates necessary directories

### 2. Runtime Phase
```bash
# Container starts automatically
```

**What happens:**
1. Mounts data volumes from parent directory
2. Starts Flask server on port 5000
3. Serves frontend at `/`
4. Exposes API at `/api/*`
5. Health check runs every 30 seconds

### 3. Usage Phase
```bash
# Open browser to http://localhost:5000
```

**User flow:**
1. Homepage loads with statistics
2. Click tab to navigate (Maps, Comparison, Methodology, Data)
3. Select map to view embedded
4. Interact with map (pan, zoom, layers)
5. Review validation metrics

### 4. Shutdown Phase
```bash
docker-compose down
```

**What happens:**
1. Stops running container
2. Preserves data (mounted volumes)
3. Removes container (not image)
4. Releases port 5000

---

## 📈 Data Flow

```
Pipeline Output → Docker Volume → Flask API → JSON → Frontend → User
```

**Detailed:**

1. **Pipeline generates data**
   - `python run.py --step all` creates processed data
   - `python run.py --step map` generates HTML maps
   - Files saved to `data/`, `outputs/`

2. **Docker mounts volumes**
   - `../data/` → `/app/data/` (read-only)
   - `../outputs/` → `/app/outputs/` (read-only)
   - `../outputs/maps/` → `/app/frontend/static/maps/` (read-only)

3. **Flask API reads data**
   - Parses validation results from `outputs/reports/`
   - Loads raster metadata from `data/processed/`, `data/results/`
   - Lists HTML maps from `outputs/maps/`

4. **Frontend requests data**
   - JavaScript calls `/api/stats`
   - Receives JSON response
   - Updates DOM dynamically

5. **User views results**
   - Statistics displayed in dashboard
   - Maps embedded via iframe
   - Interactive controls enabled

---

## 🔒 Security Features

### Read-Only Volumes
All data mounted as `:ro` - cannot be modified from container

### No Persistent State
Container is stateless - all data external

### Network Isolation
Dedicated Docker network (`wildfire-network`)

### Health Monitoring
Automatic health checks every 30 seconds

### Port Binding
Only port 5000 exposed to host

---

## 🎨 Customization

### Change Branding
Edit `frontend/static/css/style.css`:
```css
:root {
    --primary-color: #YOUR_COLOR;
    --secondary-color: #YOUR_COLOR;
}
```

### Add API Endpoint
Edit `backend/app.py`:
```python
@app.route('/api/your-endpoint')
def your_endpoint():
    return jsonify({'data': 'value'})
```

### Modify UI
Edit `frontend/templates/index.html`:
```html
<div class="your-section">
    <!-- Your content -->
</div>
```

### Add JavaScript
Edit `frontend/static/js/main.js`:
```javascript
async function yourFunction() {
    // Your code
}
```

---

## 📦 Deployment Options

### Local Development
```bash
./start.sh
# Access at http://localhost:5000
```

### Production (Docker)
```bash
docker-compose up -d
# Add Nginx reverse proxy
# Configure SSL/TLS
```

### Cloud Deployment
- **AWS ECS** - Elastic Container Service
- **Google Cloud Run** - Serverless containers
- **Azure Container Instances** - Managed containers
- **DigitalOcean Apps** - Platform as a Service

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wildfire-webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wildfire-webapp
  template:
    metadata:
      labels:
        app: wildfire-webapp
    spec:
      containers:
      - name: webapp
        image: wildfire-webapp:latest
        ports:
        - containerPort: 5000
```

---

## 🔍 Monitoring

### Health Checks
```bash
# Manual check
curl http://localhost:5000/api/health

# Docker automatic check
# Defined in Dockerfile HEALTHCHECK
```

### Logs
```bash
# View live logs
docker-compose logs -f

# Export logs
docker-compose logs > webapp.log

# Filter logs
docker-compose logs | grep ERROR
```

### Metrics
```bash
# Container stats
docker stats wildfire-fuel-mapping-webapp

# Resource usage
docker-compose top
```

---

## 🧪 Testing

### Manual Testing
1. Start container: `./start.sh`
2. Open browser: http://localhost:5000
3. Test each tab
4. Click map cards
5. Verify data loads correctly

### API Testing
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test stats endpoint
curl http://localhost:5000/api/stats

# Test maps endpoint
curl http://localhost:5000/api/maps
```

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# Using wrk
wrk -t4 -c100 -d30s http://localhost:5000/
```

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `backend/app.py` | Flask application with API routes |
| `frontend/templates/index.html` | Main HTML template |
| `frontend/static/css/style.css` | All styling and responsive design |
| `frontend/static/js/main.js` | Client-side logic and API calls |
| `Dockerfile` | Container image definition |
| `docker-compose.yml` | Multi-container configuration |
| `requirements.txt` | Python package dependencies |
| `.dockerignore` | Files excluded from Docker build |
| `start.sh` | Quick startup script with checks |
| `QUICKSTART.md` | 2-minute getting started guide |
| `README.md` | Complete documentation |
| `OVERVIEW.md` | This architectural overview |

---

## 🎯 Use Cases

### 1. Hackathon Demo
- Start webapp with one command
- Show interactive maps
- Present validation metrics
- Professional appearance

### 2. Project Presentation
- Embed maps in browser
- Navigate between tabs during talk
- Show methodology and data sources
- Answer questions with live data

### 3. Stakeholder Review
- Share localhost URL in meeting
- Walk through features
- Demonstrate improvement over baseline
- Discuss operational applications

### 4. Production Deployment
- Deploy to cloud
- Share public URL
- Enable remote access
- Production-ready with Gunicorn

---

## 🚀 Quick Commands Reference

```bash
# Start
./start.sh

# Start (alternative)
docker-compose up

# Start in background
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Rebuild
docker-compose up --build

# View logs
docker-compose logs -f

# Shell access
docker-compose exec webapp /bin/bash

# Check status
docker-compose ps

# Remove everything
docker-compose down -v
```

---

## 💡 Pro Tips

1. **Generate maps first** - Run `python ../run.py --step map` before starting webapp
2. **Use start.sh** - Automated checks and cleaner output
3. **Check logs** - If something breaks, logs tell you why
4. **Read-only mounts** - Data is safe from accidental changes
5. **Port conflicts** - Change port in docker-compose.yml if 5000 is taken
6. **Hot reload** - Set FLASK_ENV=development for auto-restart on code changes
7. **Production mode** - Use Gunicorn for production deployments
8. **Cache static files** - Add caching headers for better performance

---

**The webapp is production-ready and demo-ready!** 🔥🗺️

Access your visualization at: **http://localhost:5000**
