// Main JavaScript for Wildfire Fuel Mapping Viewer (Static Version)

// Static data - no API calls needed
const STATIC_DATA = {
    maps: [
        {
            name: '01_overview',
            filename: '01_overview.html',
            url: 'maps/01_overview.html',
            displayName: 'Project Overview',
            description: 'Problem, solution, and key results at a glance'
        },
        {
            name: '02_change_detection',
            filename: '02_change_detection.html',
            url: 'maps/02_change_detection.html',
            displayName: 'Change Detection',
            description: 'Satellite-detected vegetation stress from 2020-2022'
        },
        {
            name: '03_prediction',
            filename: '03_prediction.html',
            url: 'maps/03_prediction.html',
            displayName: 'Prediction Comparison',
            description: 'LANDFIRE baseline vs enhanced fuel map'
        },
        {
            name: '04_validation',
            filename: '04_validation.html',
            url: 'maps/04_validation.html',
            displayName: 'Validation Results',
            description: 'Quantitative proof of 43% improvement'
        },
        {
            name: '05_summary',
            filename: '05_summary.html',
            url: 'maps/05_summary.html',
            displayName: 'Complete Summary',
            description: 'Key takeaways and operational applications'
        }
    ]
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
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

// Load Available Maps (Static)
function loadAvailableMaps() {
    const mapsList = document.getElementById('mapsList');

    if (!STATIC_DATA.maps || STATIC_DATA.maps.length === 0) {
        mapsList.innerHTML = '<div class="loading">No maps available</div>';
        return;
    }

    mapsList.innerHTML = '';

    STATIC_DATA.maps.forEach(map => {
        const mapCard = createMapCard(map);
        mapsList.appendChild(mapCard);
    });
}

function createMapCard(map) {
    const card = document.createElement('div');
    card.className = 'map-card';

    card.innerHTML = `
        <h4>${map.displayName}</h4>
        <p>${map.description}</p>
        <button class="map-card-button" onclick="loadMap('${map.url}')">View</button>
    `;

    return card;
}

async function loadMap(url) {
    const mapViewer = document.getElementById('mapViewer');

    // Show loading state
    mapViewer.innerHTML = '<div class="loading">Loading map...</div>';

    try {
        // Fetch the HTML content
        const response = await fetch(url);
        const html = await response.text();

        // Parse the HTML to extract the content we want
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        // Extract the body content (title, image, description)
        const title = doc.querySelector('.title');
        const img = doc.querySelector('img');
        const description = doc.querySelector('.description');

        // Clear the viewer and add the content directly
        mapViewer.innerHTML = '';

        // Add title
        if (title) {
            const titleDiv = document.createElement('div');
            titleDiv.className = 'map-viewer-title';
            titleDiv.innerHTML = title.innerHTML;
            mapViewer.appendChild(titleDiv);
        }

        // Add image
        if (img) {
            const imgDiv = document.createElement('div');
            imgDiv.className = 'map-viewer-image';
            const newImg = document.createElement('img');
            // Fix the image path to be relative from the main page
            newImg.src = 'presentation/' + img.src.split('/').pop();
            newImg.alt = img.alt;
            imgDiv.appendChild(newImg);
            mapViewer.appendChild(imgDiv);
        }

        // Add description
        if (description) {
            const descDiv = document.createElement('div');
            descDiv.className = 'map-viewer-description';
            descDiv.innerHTML = description.innerHTML;
            mapViewer.appendChild(descDiv);
        }

    } catch (error) {
        console.error('Error loading map:', error);
        mapViewer.innerHTML = '<div class="loading">Error loading map. Please try again.</div>';
    }

    // Scroll to map viewer
    mapViewer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
