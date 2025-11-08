// Main JavaScript for Wildfire Fuel Mapping Viewer

// API Base URL
const API_URL = window.location.origin;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    loadStatistics();
    loadAvailableMaps();
});

// Tab Navigation
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.dataset.tab;

            // Remove active class from all tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked tab
            button.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

// Load Statistics from API
async function loadStatistics() {
    try {
        const response = await fetch(`${API_URL}/api/stats`);
        const stats = await response.json();

        // Update header stats
        updateHeaderStats(stats);

        // Update comparison tab
        updateComparisonStats(stats);

        // Update data tab
        updateDataStats(stats);

        // Update fire info
        updateFireInfo(stats);

    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

function updateHeaderStats(stats) {
    const headerStats = document.getElementById('headerStats');

    headerStats.innerHTML = `
        <div class="stat-card">
            <div class="stat-value">+${stats.improvement_pct.toFixed(1)}%</div>
            <div class="stat-label">Improvement</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stats.enhanced_correlation.toFixed(2)}</div>
            <div class="stat-label">Correlation</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${stats.detection_rate.toFixed(0)}%</div>
            <div class="stat-label">Detection Rate</div>
        </div>
    `;
}

function updateComparisonStats(stats) {
    document.getElementById('baselineCorr').textContent = stats.baseline_correlation.toFixed(2);
    document.getElementById('enhancedCorr').textContent = stats.enhanced_correlation.toFixed(2);
    document.getElementById('improvementValue').textContent = `+${stats.improvement_pct.toFixed(1)}%`;
}

function updateDataStats(stats) {
    document.getElementById('sampleSize').textContent = stats.sample_size.toLocaleString() + ' pixels';
    document.getElementById('baselineCorr2').textContent = stats.baseline_correlation.toFixed(2);
    document.getElementById('enhancedCorr2').textContent = stats.enhanced_correlation.toFixed(2);
    document.getElementById('improvement').textContent = `+${stats.improvement_pct.toFixed(1)}%`;
    document.getElementById('detectionRate').textContent = `${stats.detection_rate.toFixed(0)}%`;
}

function updateFireInfo(stats) {
    document.getElementById('fireSize').textContent = stats.fire_size_acres.toLocaleString() + ' acres';
    document.getElementById('fireDamage').textContent = '$' + stats.fire_damage_usd;
}

// Load Available Maps
async function loadAvailableMaps() {
    try {
        const response = await fetch(`${API_URL}/api/maps`);
        const maps = await response.json();

        const mapsList = document.getElementById('mapsList');

        if (maps.length === 0) {
            mapsList.innerHTML = '<div class="loading">No maps available yet. Run the pipeline to generate maps.</div>';
            return;
        }

        mapsList.innerHTML = '';

        maps.forEach(map => {
            const mapCard = createMapCard(map);
            mapsList.appendChild(mapCard);
        });

    } catch (error) {
        console.error('Error loading maps:', error);
        document.getElementById('mapsList').innerHTML = '<div class="loading">Error loading maps</div>';
    }
}

function createMapCard(map) {
    const card = document.createElement('div');
    card.className = 'map-card';

    // Format map name
    const displayName = formatMapName(map.name);
    const description = getMapDescription(map.name);

    card.innerHTML = `
        <h4>${displayName}</h4>
        <p>${description}</p>
        <button class="map-card-button" onclick="loadMap('${map.url}')">View Map</button>
    `;

    return card;
}

function formatMapName(name) {
    // Convert filename to readable name
    return name
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

function getMapDescription(name) {
    const descriptions = {
        'hermits_peak_interactive_map': 'Full interactive map with all layers and controls',
        'hermits_peak_comparison_map': 'Side-by-side comparison of LANDFIRE baseline vs Enhanced fuel map'
    };

    return descriptions[name] || 'Interactive map visualization';
}

function loadMap(url) {
    const mapViewer = document.getElementById('mapViewer');

    mapViewer.innerHTML = `
        <iframe src="${url}" style="width: 100%; height: 600px; border: none;"></iframe>
    `;

    // Scroll to map viewer
    mapViewer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch(`${API_URL}/api/health`);
        const health = await response.json();
        console.log('Health check:', health);
        return health.status === 'healthy';
    } catch (error) {
        console.error('Health check failed:', error);
        return false;
    }
}

// Run health check on load
checkHealth();
