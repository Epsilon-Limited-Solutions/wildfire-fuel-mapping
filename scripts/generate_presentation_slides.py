#!/usr/bin/env python3
"""
Generate presentation slides as PNG images
Creates professional slides for the hackathon pitch
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import numpy as np
from pathlib import Path
from PIL import Image

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / 'outputs'
SLIDES_DIR = OUTPUT_DIR / 'slides'
SLIDES_DIR.mkdir(exist_ok=True)
MAPS_DIR = OUTPUT_DIR / 'maps_only'
PRESENTATION_DIR = OUTPUT_DIR / 'presentation'

# Color palette
FIRE_RED = '#d62728'
ORANGE = '#e6550d'
DARK_BG = '#1a1a2e'
LIGHT_BG = '#f8f9fa'
TEXT_DARK = '#212529'
TEXT_LIGHT = '#ffffff'

def create_title_slide():
    """Slide 1: Title and Introduction"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Background gradient
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(gradient, extent=[0, 1, 0, 1], aspect='auto',
              cmap='Reds', alpha=0.2)

    # Title
    ax.text(0.5, 0.75, 'FUELWATCH',
            ha='center', va='center', fontsize=72,
            fontweight='bold', color=FIRE_RED)

    ax.text(0.5, 0.67, 'Real-Time Wildfire Fuel Intelligence',
            ha='center', va='center', fontsize=28, color=TEXT_DARK)

    # Divider
    ax.plot([0.2, 0.8], [0.6, 0.6], 'k-', linewidth=2, alpha=0.3)

    # Industry/Audience
    ax.text(0.5, 0.52, 'Industry/Audience:',
            ha='center', va='center', fontsize=22,
            fontweight='bold', color=TEXT_DARK)
    ax.text(0.5, 0.47, 'Wildfire Management & Emergency Response',
            ha='center', va='center', fontsize=20, color=TEXT_DARK)
    ax.text(0.5, 0.43, 'USFS • State Fire Agencies • Insurance Companies',
            ha='center', va='center', fontsize=18,
            color=TEXT_DARK, alpha=0.8)

    # Solution Summary
    solution_text = """We update wildfire fuel maps WEEKLY using free satellite data
instead of every 2-3 years, helping fire managers identify high-risk
areas before fire season starts.

Validated on a $4B wildfire: 43% improvement over government standards."""

    ax.text(0.5, 0.28, solution_text,
            ha='center', va='center', fontsize=18,
            color=TEXT_DARK, linespacing=1.6,
            bbox=dict(boxstyle='round,pad=1', facecolor=LIGHT_BG,
                     edgecolor=FIRE_RED, linewidth=2))

    # Impact
    ax.text(0.5, 0.10, 'Better planning → Targeted treatments → Fewer fires → Lives saved',
            ha='center', va='center', fontsize=20,
            fontweight='bold', color=FIRE_RED)

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_01_title.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 1: Title")

def create_problem_slide():
    """Slide 2: The Problem"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')

    # Try to load before/after image
    before_after = MAPS_DIR / 'before_after_true_color.png'

    if before_after.exists():
        img = Image.open(before_after)
        ax = fig.add_subplot(111)
        ax.imshow(img)
        ax.axis('off')

        # Add title overlay
        ax.text(0.5, 0.95, 'WILDFIRE FUEL MAPS ARE DANGEROUSLY OUT OF DATE',
                transform=ax.transAxes, ha='center', va='top',
                fontsize=32, fontweight='bold', color='white',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=FIRE_RED, alpha=0.9))

        # Add stats overlay
        stats_text = """Hermits Peak Fire, New Mexico
• 341,735 acres burned
• $4 billion damage
• 2-year-old fuel map"""

        ax.text(0.05, 0.05, stats_text,
                transform=ax.transAxes, ha='left', va='bottom',
                fontsize=20, color='white', linespacing=1.5,
                bbox=dict(boxstyle='round,pad=0.8', facecolor='black', alpha=0.8))
    else:
        # Text-only version
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

        ax.text(0.5, 0.9, 'WILDFIRE FUEL MAPS ARE',
                ha='center', va='center', fontsize=44, fontweight='bold')
        ax.text(0.5, 0.8, 'DANGEROUSLY OUT OF DATE',
                ha='center', va='center', fontsize=44,
                fontweight='bold', color=FIRE_RED)

        problems = [
            "✗ LANDFIRE updates every 2-3 YEARS",
            "✗ Vegetation changes RAPIDLY (drought, disease, stress)",
            "✗ Managers make BILLION-DOLLAR decisions on stale data",
            "",
            "Result: Hermits Peak Fire",
            "• 341,735 acres burned",
            "• $4 billion in damage",
            "• Could have been prevented with better data"
        ]

        y_pos = 0.6
        for problem in problems:
            if problem:
                size = 28 if '✗' in problem else 24
                weight = 'bold' if '✗' in problem or '•' in problem else 'normal'
                color = FIRE_RED if '✗' in problem else TEXT_DARK
                ax.text(0.5, y_pos, problem, ha='center', va='center',
                       fontsize=size, fontweight=weight, color=color)
            y_pos -= 0.08

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_02_problem.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 2: Problem")

def create_solution_slide():
    """Slide 4: Our Solution"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.92, 'WEEKLY FUEL UPDATES VIA SATELLITE FUSION',
            ha='center', va='center', fontsize=40,
            fontweight='bold', color=FIRE_RED)

    # Workflow boxes
    boxes = [
        ("1. LANDFIRE\nBaseline", 0.15, 0.65),
        ("2. Weekly\nSatellites", 0.35, 0.65),
        ("3. Change\nDetection", 0.55, 0.65),
        ("4. Updated\nFuel Maps", 0.75, 0.65),
    ]

    for text, x, y in boxes:
        # Box
        rect = patches.FancyBboxPatch((x-0.08, y-0.08), 0.16, 0.16,
                                     boxstyle="round,pad=0.01",
                                     facecolor=LIGHT_BG,
                                     edgecolor=FIRE_RED, linewidth=3)
        ax.add_patch(rect)

        # Text
        ax.text(x, y, text, ha='center', va='center',
               fontsize=18, fontweight='bold', color=TEXT_DARK)

        # Arrows
        if x < 0.7:
            ax.annotate('', xy=(x+0.12, y), xytext=(x+0.08, y),
                       arrowprops=dict(arrowstyle='->', lw=3, color=ORANGE))

    # Key Advantages
    ax.text(0.5, 0.44, 'KEY ADVANTAGES', ha='center', va='center',
           fontsize=28, fontweight='bold', color=TEXT_DARK)

    advantages = [
        "✓ Builds on proven LANDFIRE methodology",
        "✓ Uses FREE, public satellite data (Sentinel-2, MODIS)",
        "✓ Automated pipeline - no manual updates",
        "✓ Weekly updates during fire season",
        "✓ Scales to entire US",
        "✓ VALIDATED: +43% improvement"
    ]

    y_pos = 0.35
    for adv in advantages:
        color = FIRE_RED if '43%' in adv else TEXT_DARK
        weight = 'bold' if '43%' in adv else 'normal'
        ax.text(0.5, y_pos, adv, ha='center', va='center',
               fontsize=20, fontweight=weight, color=color)
        y_pos -= 0.06

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_04_solution.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 4: Solution")

def create_validation_slide():
    """Slide 5: Validation Results - THE MONEY SLIDE"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.92, 'PROVEN ON REAL WILDFIRE',
            ha='center', va='center', fontsize=44,
            fontweight='bold', color=FIRE_RED)

    # The big number
    ax.text(0.5, 0.75, '+43.1%',
            ha='center', va='center', fontsize=120,
            fontweight='bold', color=FIRE_RED)

    ax.text(0.5, 0.68, 'IMPROVEMENT',
            ha='center', va='center', fontsize=32,
            fontweight='bold', color=TEXT_DARK)

    # Comparison bars
    bar_y = 0.55

    # LANDFIRE bar
    rect1 = patches.Rectangle((0.2, bar_y-0.05), 0.25, 0.08,
                              facecolor='gray', alpha=0.6)
    ax.add_patch(rect1)
    ax.text(0.15, bar_y-0.01, 'LANDFIRE 2020', ha='right', va='center',
           fontsize=18, fontweight='bold')
    ax.text(0.47, bar_y-0.01, 'R² = 0.0965', ha='left', va='center',
           fontsize=18)

    # FuelWatch bar
    bar_y = 0.42
    rect2 = patches.Rectangle((0.2, bar_y-0.05), 0.36, 0.08,
                              facecolor=FIRE_RED, alpha=0.8)
    ax.add_patch(rect2)
    ax.text(0.15, bar_y-0.01, 'FuelWatch', ha='right', va='center',
           fontsize=18, fontweight='bold', color=FIRE_RED)
    ax.text(0.58, bar_y-0.01, 'R² = 0.1382', ha='left', va='center',
           fontsize=18, fontweight='bold')

    # Details
    details = [
        "Hermits Peak Fire: 341,735 acres",
        "Sample: 2.5 million pixels",
        "Significance: p < 0.001"
    ]

    y_pos = 0.28
    for detail in details:
        ax.text(0.5, y_pos, detail, ha='center', va='center',
               fontsize=20, color=TEXT_DARK)
        y_pos -= 0.06

    # Bottom line
    ax.text(0.5, 0.08, 'Better predictions = Better preparedness',
            ha='center', va='center', fontsize=28,
            fontweight='bold', color=FIRE_RED,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=LIGHT_BG,
                     edgecolor=FIRE_RED, linewidth=2))

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_05_validation.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 5: Validation (MONEY SLIDE)")

def create_impact_slide():
    """Slide 6: Impact & Use Cases"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.92, 'OPERATIONAL IMPACT',
            ha='center', va='center', fontsize=44,
            fontweight='bold', color=FIRE_RED)

    # Use cases in grid
    use_cases = [
        ("📋", "Pre-Season Planning", "Identify high-risk areas\nbefore fire season"),
        ("🎯", "Resource Allocation", "Prioritize fuel treatments\nwhere they matter most"),
        ("🏘️", "Community Protection", "Target wildland-urban\ninterface preparedness"),
        ("💰", "Insurance", "Accurate risk assessment\nfor premiums"),
    ]

    x_positions = [0.25, 0.75]
    y_positions = [0.68, 0.45]

    i = 0
    for y in y_positions:
        for x in x_positions:
            if i < len(use_cases):
                emoji, title, desc = use_cases[i]

                # Box
                rect = patches.FancyBboxPatch((x-0.18, y-0.12), 0.36, 0.18,
                                             boxstyle="round,pad=0.01",
                                             facecolor=LIGHT_BG,
                                             edgecolor=FIRE_RED, linewidth=2)
                ax.add_patch(rect)

                # Content
                ax.text(x, y+0.05, emoji, ha='center', va='center', fontsize=40)
                ax.text(x, y-0.02, title, ha='center', va='center',
                       fontsize=18, fontweight='bold', color=TEXT_DARK)
                ax.text(x, y-0.08, desc, ha='center', va='center',
                       fontsize=14, color=TEXT_DARK, linespacing=1.3)
                i += 1

    # By the numbers
    ax.text(0.5, 0.24, 'BY THE NUMBERS', ha='center', va='center',
           fontsize=24, fontweight='bold', color=TEXT_DARK)

    numbers = [
        "50,000+ wildfires annually in US",
        "$80 billion in annual wildfire costs",
        "10-20% better targeting = BILLIONS saved"
    ]

    y_pos = 0.16
    for num in numbers:
        ax.text(0.5, y_pos, num, ha='center', va='center',
               fontsize=20, color=TEXT_DARK)
        y_pos -= 0.06

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_06_impact.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 6: Impact")

def create_tech_slide():
    """Slide 7: Technology Stack"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.92, 'BUILT ON FREE, PROVEN INFRASTRUCTURE',
            ha='center', va='center', fontsize=38,
            fontweight='bold', color=FIRE_RED)

    # Data sources
    ax.text(0.5, 0.78, 'DATA SOURCES (All FREE & Public)',
            ha='center', va='center', fontsize=26,
            fontweight='bold', color=TEXT_DARK)

    sources = [
        "✓ LANDFIRE → Baseline fuel models (30m)",
        "✓ Sentinel-2 → 10m resolution, 5-day revisit",
        "✓ MODIS → Daily vegetation indices (250m)",
        "✓ Fire perimeters → NIFC real-time data"
    ]

    y_pos = 0.68
    for source in sources:
        ax.text(0.5, y_pos, source, ha='center', va='center',
               fontsize=22, color=TEXT_DARK)
        y_pos -= 0.08

    # Processing
    ax.text(0.5, 0.38, 'PROCESSING',
            ha='center', va='center', fontsize=26,
            fontweight='bold', color=TEXT_DARK)

    processing = [
        "✓ Google Earth Engine → Cloud processing (free tier)",
        "✓ Python/GDAL → Geospatial analysis",
        "✓ Open source → Scalable, reproducible"
    ]

    y_pos = 0.30
    for proc in processing:
        ax.text(0.5, y_pos, proc, ha='center', va='center',
               fontsize=22, color=TEXT_DARK)
        y_pos -= 0.07

    # Why this matters
    matters = [
        "ZERO data acquisition costs",
        "Proven, operational satellites (15+ years)",
        "Scales to entire US",
        "Operational cost: < $1,000/year"
    ]

    y_pos = 0.12
    for matter in matters:
        ax.text(0.5, y_pos, f"→ {matter}", ha='center', va='center',
               fontsize=20, color=FIRE_RED, fontweight='bold')
        y_pos -= 0.06

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_07_tech.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 7: Technology")

def create_demo_slide():
    """Slide 8: Demo placeholder"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.85, 'LIVE SYSTEM DEMO',
            ha='center', va='center', fontsize=48,
            fontweight='bold', color=FIRE_RED)

    # URL prominently
    ax.text(0.5, 0.68, 'hackathon-wildfire-epsilon.limited',
            ha='center', va='center', fontsize=28,
            fontweight='bold', color=TEXT_DARK,
            bbox=dict(boxstyle='round,pad=0.8', facecolor=LIGHT_BG,
                     edgecolor=FIRE_RED, linewidth=3))

    ax.text(0.5, 0.60, '.s3-website-us-east-1.amazonaws.com',
            ha='center', va='center', fontsize=20, color=TEXT_DARK)

    # What to show
    ax.text(0.5, 0.48, 'DEMO WALKTHROUGH:',
            ha='center', va='center', fontsize=26,
            fontweight='bold', color=TEXT_DARK)

    demo_points = [
        "1. Dashboard overview → Real-time stats",
        "2. Before/After satellite imagery → Visual fire impact",
        "3. Change detection maps → Vegetation stress",
        "4. Enhanced fuel maps → Updated predictions",
        "5. Validation results → 43% improvement proof"
    ]

    y_pos = 0.38
    for point in demo_points:
        ax.text(0.5, y_pos, point, ha='center', va='center',
               fontsize=22, color=TEXT_DARK)
        y_pos -= 0.08

    # Features
    ax.text(0.5, 0.06, '✓ Deployed on AWS  ✓ Real satellite data  ✓ Interactive visualizations',
            ha='center', va='center', fontsize=20,
            fontweight='bold', color=FIRE_RED)

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_08_demo.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 8: Demo")

def create_next_steps_slide():
    """Slide 9: Next Steps & Scaling"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.92, 'PATH TO DEPLOYMENT',
            ha='center', va='center', fontsize=44,
            fontweight='bold', color=FIRE_RED)

    # Timeline sections
    sections = [
        ("IMMEDIATE (3 months)", [
            "✓ Partner with one state fire agency (pilot)",
            "✓ Expand to 5 high-risk western states",
            "✓ Validate on 2023-2024 fire seasons"
        ], 0.75),
        ("6-12 MONTHS", [
            "✓ National coverage (lower 48 states)",
            "✓ Integration with WFDSS (Wildland Fire Decision Support)",
            "✓ Mobile app for field crews"
        ], 0.52),
        ("FUNDING NEEDS", [
            "$250K seed → Product development, pilot deployments",
            "$1M Series A → National scaling, agency partnerships"
        ], 0.29)
    ]

    for title, items, y_start in sections:
        ax.text(0.5, y_start, title, ha='center', va='center',
               fontsize=26, fontweight='bold', color=TEXT_DARK)

        y_pos = y_start - 0.08
        for item in items:
            size = 22 if '$' in item else 20
            weight = 'bold' if '$' in item else 'normal'
            color = FIRE_RED if '$' in item else TEXT_DARK
            ax.text(0.5, y_pos, item, ha='center', va='center',
                   fontsize=size, fontweight=weight, color=color)
            y_pos -= 0.06

    # Bottom line
    ax.text(0.5, 0.06, 'Ready to deploy. Infrastructure exists. Satellites are flying.',
            ha='center', va='center', fontsize=24,
            fontweight='bold', color=FIRE_RED)

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_09_next_steps.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 9: Next Steps")

def create_closing_slide():
    """Slide 10: Call to Action"""
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.88, 'WHY US. WHY NOW.',
            ha='center', va='center', fontsize=48,
            fontweight='bold', color=FIRE_RED)

    # The reality
    reality = """Every year between LANDFIRE updates, conditions change.
Every year, fires get worse.
Every year, we lose lives and billions of dollars."""

    ax.text(0.5, 0.70, reality,
            ha='center', va='center', fontsize=24,
            color=TEXT_DARK, linespacing=1.8)

    # Can't wait
    ax.text(0.5, 0.54, "We Can't Wait 2-3 Years for Better Data.",
            ha='center', va='center', fontsize=32,
            fontweight='bold', color=FIRE_RED)

    # The solution
    solution = """The satellites are overhead RIGHT NOW.
The data is FREE.
The solution is PROVEN.

Let's use it."""

    ax.text(0.5, 0.36, solution,
            ha='center', va='center', fontsize=28,
            fontweight='bold', color=TEXT_DARK, linespacing=1.8)

    # Divider
    ax.plot([0.2, 0.8], [0.20, 0.20], 'k-', linewidth=2, alpha=0.3)

    # Contact
    ax.text(0.5, 0.14, 'FUELWATCH',
            ha='center', va='center', fontsize=40,
            fontweight='bold', color=FIRE_RED)

    ax.text(0.5, 0.08, 'Real-Time Wildfire Fuel Intelligence',
            ha='center', va='center', fontsize=20, color=TEXT_DARK)

    ax.text(0.5, 0.03, '[Your Contact Info]',
            ha='center', va='center', fontsize=16,
            color=TEXT_DARK, style='italic')

    plt.tight_layout()
    fig.savefig(SLIDES_DIR / 'slide_10_closing.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("✓ Slide 10: Closing")

def main():
    """Generate all presentation slides"""
    print("=" * 60)
    print("GENERATING PRESENTATION SLIDES")
    print("=" * 60)
    print()

    create_title_slide()
    create_problem_slide()
    create_solution_slide()
    create_validation_slide()
    create_impact_slide()
    create_tech_slide()
    create_demo_slide()
    create_next_steps_slide()
    create_closing_slide()

    print()
    print("=" * 60)
    print(f"✓ All slides saved to: {SLIDES_DIR}")
    print("=" * 60)
    print()
    print("Slides created (16:9 aspect ratio, 300 DPI):")
    for i, slide_file in enumerate(sorted(SLIDES_DIR.glob('slide_*.png')), 1):
        print(f"  {i}. {slide_file.name}")
    print()
    print("Ready for presentation!")

if __name__ == '__main__':
    main()
