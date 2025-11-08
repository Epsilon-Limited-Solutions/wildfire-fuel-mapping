# WebApp Quick Start

**Get your visualization running in 2 minutes**

---

## ✅ Prerequisites

1. **Docker installed** - https://docs.docker.com/get-docker/
2. **Pipeline completed** - Run `python run.py --step all` from parent directory
3. **Maps generated** - Run `python run.py --step map` from parent directory

---

## 🚀 Start the WebApp

### Option 1: Using the Startup Script (Easiest)

```bash
cd webapp
./start.sh
```

### Option 2: Using Docker Compose

```bash
cd webapp
docker-compose up --build
```

### Option 3: Run in Background

```bash
cd webapp
docker-compose up -d --build
```

---

## 🌐 Access the Application

Open your browser to: **http://localhost:5000**

---

## 🎯 What You'll See

### Tab 1: Interactive Maps
- Browse available HTML maps
- Click to view embedded in page
- Full pan/zoom/layer controls

### Tab 2: Comparison View
- LANDFIRE baseline vs Enhanced fuel map
- Correlation metrics
- Improvement percentage

### Tab 3: Methodology
- 4-step process explanation
- Data sources table
- Technical approach

### Tab 4: Data & Analysis
- Validation statistics
- Detection performance
- Use cases

---

## 🛑 Stop the WebApp

```bash
cd webapp
docker-compose down
```

---

## 🐛 Troubleshooting

### Port 5000 already in use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8080:5000"  # Use port 8080 instead
```

### No maps showing
```bash
# Generate maps first
cd ..
python run.py --step map

# Restart webapp
cd webapp
docker-compose restart
```

### Container won't start
```bash
# Check logs
docker-compose logs -f

# Rebuild
docker-compose down
docker-compose up --build
```

### Data not found
```bash
# Verify pipeline ran
ls -la ../data/processed/
ls -la ../outputs/maps/

# Run if missing
cd ..
python run.py --step all
```

---

## 📊 Quick Commands

```bash
# Start
./start.sh

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Stop
docker-compose down

# Rebuild
docker-compose up --build

# Shell into container
docker-compose exec webapp /bin/bash

# Check status
docker-compose ps
```

---

## 🎬 Demo Flow

1. Start webapp: `./start.sh`
2. Open browser: http://localhost:5000
3. Navigate to "Interactive Maps" tab
4. Click "Hermits Peak Comparison Map"
5. Explore side-by-side LANDFIRE vs Enhanced view
6. Toggle layers to show vegetation changes
7. Zoom to areas of interest
8. Switch to "Comparison View" for metrics
9. Check "Data & Analysis" for validation results

---

## ✨ Tips

- Maps are **read-only** - can't accidentally modify data
- All tabs load data from API dynamically
- Health check runs every 30 seconds
- Container restarts automatically unless stopped
- Hot reload enabled in development mode

---

## 🚀 Next Steps

After webapp is running:

1. **Customize** - Edit CSS in `frontend/static/css/style.css`
2. **Add API endpoints** - Extend `backend/app.py`
3. **Deploy** - See README.md for production setup
4. **Share** - Deploy to cloud and share URL

---

**Total time: 2 minutes from `./start.sh` to viewing maps!** 🔥🗺️
