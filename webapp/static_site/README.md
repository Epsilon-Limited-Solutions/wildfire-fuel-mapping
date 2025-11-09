# Wildfire Fuel Mapping - Static Site

This is a pure static version of the Wildfire Fuel Mapping viewer, ready for deployment to S3, GitHub Pages, Netlify, or any static hosting service.

## Features

- ✅ No backend required - all data is embedded
- ✅ Pure HTML/CSS/JavaScript
- ✅ Interactive map viewer with iframe embedding
- ✅ Responsive design
- ✅ Real validation results: 43.1% improvement
- ✅ All presentation images included

## Quick Start

### Local Testing

```bash
# Option 1: Python simple server
cd static_site
python3 -m http.server 8000

# Option 2: Node.js http-server (if installed)
npx http-server -p 8000

# Then open: http://localhost:8000
```

### Deploy to S3 (Easiest)

```bash
cd static_site
./deploy_to_s3.sh

# Or with custom bucket name:
./deploy_to_s3.sh my-wildfire-mapping-site
```

See [S3_DEPLOYMENT_GUIDE.md](S3_DEPLOYMENT_GUIDE.md) for detailed instructions.

### Deploy to Other Platforms

**Netlify (Drag & Drop):**
1. Go to https://app.netlify.com/drop
2. Drag the `static_site` folder
3. Done! You'll get a URL like `https://random-name.netlify.app`

**GitHub Pages:**
```bash
# Create a new repo, then:
cd static_site
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/wildfire-maps.git
git push -u origin main

# Enable GitHub Pages in repo settings → Pages → Source: main branch
```

**Vercel:**
```bash
cd static_site
npx vercel
```

## File Structure

```
static_site/
├── index.html              # Main dashboard
├── css/
│   └── style.css          # Styles
├── js/
│   └── main.js            # Static data, no API calls
├── maps/                   # Individual visualizations
│   ├── 01_overview.html
│   ├── 02_change_detection.html
│   ├── 03_prediction.html
│   ├── 04_validation.html
│   └── 05_summary.html
└── presentation/           # PNG images
    ├── 01_overview.png
    ├── 02_change_detection.png
    ├── 03_prediction.png
    ├── 04_validation.png
    └── 05_summary.png
```

## Key Results Embedded

- **Improvement**: +43.1%
- **Enhanced R²**: 0.1382 (vs 0.0965 baseline)
- **Sample Size**: 2,522,864 pixels
- **Fire**: Hermits Peak-Calf Canyon (341,735 acres, $4B damage)
- **High Stress Areas Detected**: 25.6%
- **Moderate Stress**: 47.6%
- **Mean Fuel Load Increase**: 46%

## Customization

To update statistics, edit `js/main.js`:

```javascript
const STATIC_DATA = {
    maps: [
        // Add or modify map entries here
    ]
};
```

To update text content, edit `index.html`.

## Cost

**S3 hosting**: < $0.01/month for low traffic
**Netlify/Vercel**: Free tier available
**GitHub Pages**: Free for public repos

## Support

- S3 Deployment: See [S3_DEPLOYMENT_GUIDE.md](S3_DEPLOYMENT_GUIDE.md)
- Issues: Check browser console for errors
- Updates: Re-run `./deploy_to_s3.sh [bucket-name]`

## License

Open source - use for any purpose.
