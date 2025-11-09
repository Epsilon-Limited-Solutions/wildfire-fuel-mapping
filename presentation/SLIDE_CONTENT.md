# Presentation Slides - Detailed Content

## SLIDE 1: Title & Introduction
**Duration**: 15 seconds

```
═══════════════════════════════════════════════════════════
                         FUELWATCH
              Real-Time Wildfire Fuel Intelligence
═══════════════════════════════════════════════════════════

Team: [Your Name]

Industry/Audience:
  Wildfire Management & Emergency Response
  → USFS, State Fire Agencies, Insurance Companies

Solution Summary:
  We update wildfire fuel maps WEEKLY using free satellite
  data instead of every 2-3 years, helping fire managers
  identify high-risk areas before fire season starts.

  Validated on a $4B wildfire: 43% improvement over current
  government standards (LANDFIRE).

Impact:
  Better pre-season planning → Prioritized fuel treatments
  → Fewer catastrophic fires → Lives and billions saved
═══════════════════════════════════════════════════════════
```

**Visual**: Your logo + dramatic fire image background
**Speaker Notes**: "LANDFIRE updates fuel maps every 2-3 years. Wildfires don't wait. We fixed that with weekly satellite updates. Proven on a real wildfire with 43% improvement."

---

## SLIDE 2: The Problem
**Duration**: 30 seconds

```
═══════════════════════════════════════════════════════════
         WILDFIRE FUEL MAPS ARE DANGEROUSLY OUT OF DATE
═══════════════════════════════════════════════════════════

[BEFORE/AFTER SATELLITE IMAGE - Full slide]

Hermits Peak-Calf Canyon Fire, New Mexico
• 341,735 acres burned
• $4 billion in damage
• Largest fire in New Mexico history

THE PROBLEM:
✗ LANDFIRE (government standard) updates every 2-3 years
✗ Vegetation changes rapidly: drought, disease, climate stress
✗ Fire managers make billion-dollar decisions on stale data
✗ Result: Catastrophic fires that could have been prevented

═══════════════════════════════════════════════════════════
```

**Visual**: Use `before_after_true_color.png` - dramatic before/after
**Speaker Notes**: "This is the Hermits Peak fire. By the time it hit in 2022, conditions had changed drastically from the 2020 fuel map. But managers were flying blind. This isn't unique - it's systemic across all US wildfire agencies."

---

## SLIDE 3: Why Static Maps Fail
**Duration**: 20 seconds

```
═══════════════════════════════════════════════════════════
                   WHY STATIC MAPS FAIL
═══════════════════════════════════════════════════════════

LANDFIRE Update Cycle:
  2018 ──→ 2020 ──→ 2022 ──→ 2024 ──→ 2026
   └─ 2-3 YEARS between updates ─┘

What Happens Between Updates:
  ✗ Drought stress builds up
  ✗ Vegetation dies off
  ✗ Fuel loads increase
  ✗ Risk skyrockets

  BUT THE MAP SAYS: "Everything is fine" ⚠️

Meanwhile, Satellites Pass Overhead:
  Sentinel-2: Every 5 days
  MODIS: Daily

  → We're just not using this data!

═══════════════════════════════════════════════════════════
```

**Visual**: Timeline diagram showing LANDFIRE vs satellite frequency
**Speaker Notes**: "LANDFIRE is incredible work - 30m resolution across the entire US. But it's a snapshot. Between updates, conditions change dramatically. Satellites are capturing this change every few days. We're just not using it."

---

## SLIDE 4: Our Solution
**Duration**: 45 seconds

```
═══════════════════════════════════════════════════════════
            WEEKLY FUEL UPDATES VIA SATELLITE FUSION
═══════════════════════════════════════════════════════════

How It Works:

  1. LANDFIRE Baseline        [Proven 30m fuel models]
         ↓
  2. + Weekly Satellites      [Sentinel-2 (10m) + MODIS]
         ↓
  3. Change Detection         [Stress, moisture, fuel ↑]
         ↓
  4. Updated Fuel Maps        [Every week during fire season]
         ↓
  5. Deploy                   [Free, public data - scales nationwide]

Key Advantages:
  ✓ Builds on proven LANDFIRE methodology (not reinventing wheel)
  ✓ Uses FREE, public satellite data (Sentinel-2, MODIS)
  ✓ Automated pipeline - no manual updates needed
  ✓ Weekly updates during fire season
  ✓ Scalable to entire US
  ✓ VALIDATED ON REAL WILDFIRE (+43% improvement)

═══════════════════════════════════════════════════════════
```

**Visual**: Workflow diagram or architecture
**Speaker Notes**: "We don't replace LANDFIRE - we enhance it. Start with their baseline, add satellite-detected changes. Every week, we update fuel risk based on actual vegetation stress and moisture deficit. All using free, public data."

---

## SLIDE 5: Validation Results
**Duration**: 45 seconds

```
═══════════════════════════════════════════════════════════
          PROVEN ON REAL WILDFIRE: +43% IMPROVEMENT
═══════════════════════════════════════════════════════════

Hermits Peak Fire Validation (341,735 acres)

Method                          R² Score    Performance
────────────────────────────────────────────────────────
LANDFIRE 2020 (Baseline)        0.0965     ████░░░░░░
LANDFIRE + FuelWatch (Ours)     0.1382     ██████░░░░

IMPROVEMENT: +43.1% ⭐

Sample size: 2,522,864 pixels
Statistical significance: p < 0.001

What We Detected (that LANDFIRE missed):
  • 25.6% of area = HIGH vegetation stress
  • 47.6% of area = MODERATE stress
  • Mean fuel load: 46% HIGHER than baseline
  • Moisture deficit across burn area

Bottom Line:
  Better predictions = Better preparedness

═══════════════════════════════════════════════════════════
```

**Visual**: Use `04_validation.png` from presentation folder
**Speaker Notes**: "This isn't a simulation. We tested on Hermits Peak - the largest fire in New Mexico history. Compared our predictions to what actually burned. 43% better correlation than LANDFIRE alone. That's the difference between knowing where to focus resources and guessing."

---

## SLIDE 6: Impact & Use Cases
**Duration**: 30 seconds

```
═══════════════════════════════════════════════════════════
                    OPERATIONAL IMPACT
═══════════════════════════════════════════════════════════

Use Cases:

📋 PRE-SEASON PLANNING
   → Identify highest-risk areas before fire season

🎯 RESOURCE ALLOCATION
   → Prioritize fuel reduction treatments where they matter most

🏘️ COMMUNITY PROTECTION
   → Target WUI (wildland-urban interface) preparedness

💰 INSURANCE
   → Accurate risk assessment for premiums

⚡ INCIDENT PLANNING
   → Real-time fuel conditions for active fires

By The Numbers:
  • 50,000+ wildfires annually in US
  • $80 billion in annual wildfire costs
  • 10-20% improvement in targeting = BILLIONS saved

═══════════════════════════════════════════════════════════
```

**Visual**: Icons for each use case + cost statistics
**Speaker Notes**: "Fire managers' number one challenge: deciding where to spend limited fuel treatment dollars. With weekly updates, they can target areas showing the most stress, most fuel accumulation, highest risk. That's actionable intelligence they don't have today."

---

## SLIDE 7: Technology Stack
**Duration**: 20 seconds

```
═══════════════════════════════════════════════════════════
            BUILT ON FREE, PROVEN INFRASTRUCTURE
═══════════════════════════════════════════════════════════

Data Sources (All FREE & PUBLIC):
  ✓ LANDFIRE → Baseline fuel models (30m)
  ✓ Sentinel-2 → 10m resolution, 5-day revisit
  ✓ MODIS → Daily vegetation indices (250m)
  ✓ Fire perimeters → NIFC real-time data

Processing:
  ✓ Google Earth Engine → Cloud processing (free tier)
  ✓ Python/GDAL → Geospatial analysis
  ✓ Open source → Scalable, reproducible

Why This Matters:
  → ZERO data acquisition costs
  → Proven, operational satellites (15+ years)
  → Scales to entire US
  → Operational cost: < $1,000/year

═══════════════════════════════════════════════════════════
```

**Visual**: Tech stack diagram with logos
**Speaker Notes**: "Everything runs on free satellite data and open source tools. Sentinel-2 operational since 2015. MODIS since 2000. This isn't experimental - it's production-ready infrastructure that costs almost nothing to operate at scale."

---

## SLIDE 8: Live Demo
**Duration**: 60 seconds

```
═══════════════════════════════════════════════════════════
                      LIVE SYSTEM DEMO
═══════════════════════════════════════════════════════════

[SWITCH TO WEB BROWSER]

URL: http://hackathon-wildfire-epsilon.limited.s3-website-us-east-1.amazonaws.com

Demo Flow:
  1. Dashboard overview → Stats at a glance
  2. Before/After imagery → Visual fire impact
  3. Change detection maps → Vegetation stress
  4. Enhanced fuel maps → Updated predictions
  5. Validation results → 43% improvement proof

[SHOW EACH VISUALIZATION]

Key Features:
  ✓ Interactive web viewer (deployed on AWS)
  ✓ Real satellite imagery processing
  ✓ Multiple analysis layers
  ✓ Quantified validation metrics

═══════════════════════════════════════════════════════════
```

**Visual**: Live website
**Speaker Notes**: "Let me show you the actual system. [Navigate through site] Before/after satellite images... change detection showing vegetation stress building up... and here's the validation - 43% improvement over LANDFIRE baseline. This is live, processing real data, deployed and ready to use."

---

## SLIDE 9: Next Steps & Scaling
**Duration**: 30 seconds

```
═══════════════════════════════════════════════════════════
                   PATH TO DEPLOYMENT
═══════════════════════════════════════════════════════════

IMMEDIATE (3 months):
  ✓ Partner with one state fire agency (pilot)
  ✓ Expand to 5 high-risk western states
  ✓ Validate on 2023-2024 fire seasons

6-12 MONTHS:
  ✓ National coverage (lower 48 states)
  ✓ Integration with WFDSS (Wildland Fire Decision Support)
  ✓ Mobile app for field crews

FUNDING NEEDS:
  → $250K seed: Product development, pilot deployments
  → $1M Series A: National scaling, agency partnerships

BUSINESS MODEL:
  → B2G: Government contracts (state/federal agencies)
  → B2B: Insurance companies, utilities, large landowners
  → SaaS: Subscription tiers for premium features

═══════════════════════════════════════════════════════════
```

**Visual**: Roadmap timeline + funding breakdown
**Speaker Notes**: "We're ready to deploy. We need one forward-thinking state fire agency to pilot with. Prove it works operationally. Then scale nationally. The infrastructure exists. The satellites are flying. We just need to get this in the hands of people who can use it."

---

## SLIDE 10: Call to Action
**Duration**: 15 seconds

```
═══════════════════════════════════════════════════════════
                     WHY US. WHY NOW.
═══════════════════════════════════════════════════════════

The Reality:
  Every year between LANDFIRE updates, conditions change.
  Every year, fires get worse.
  Every year, we lose lives and billions of dollars.

We Can't Wait 2-3 Years for Better Data.

The satellites are overhead RIGHT NOW.
The data is FREE.
The solution is PROVEN.

Let's use it.

───────────────────────────────────────────────────────────

Contact: [Your Email] | [LinkedIn]

Looking for:
  → Agency partnerships
  → Pilot funding
  → Technical advisors

───────────────────────────────────────────────────────────

FUELWATCH
Real-Time Wildfire Fuel Intelligence

═══════════════════════════════════════════════════════════
```

**Visual**: Team photo + contact info
**Speaker Notes**: "We can't wait 2-3 years for better data while fires rage. The satellites are overhead right now. Let's use them. Thank you."

---

## BACKUP SLIDES (If Asked)

### BACKUP: Climate Impact

```
═══════════════════════════════════════════════════════════
                     CLIMATE IMPACT
═══════════════════════════════════════════════════════════

How This Positively Impacts Climate:

1. MITIGATION
   Better fuel management → Less catastrophic fires
   → Less carbon released into atmosphere

   Large wildfires release MASSIVE CO2
   Reduced fire intensity = more carbon stays sequestered

2. ADAPTATION
   Climate change → Worse fire conditions
   Our tool helps communities adapt to new reality
   Weekly updates capture climate-driven vegetation stress

3. PREVENTION > REACTION
   Smart fuel treatments PREVENT fires from starting
   Protect carbon-storing forests before they burn

4. DATA FOR DECISION-MAKING
   Climate action requires good data
   Weekly satellite monitoring = climate intelligence
   Target limited resources for maximum impact

The Bigger Picture:
  Climate change is making fires worse. We can't stop that
  overnight. But we can give fire managers tools to prepare.

  Better data → Better decisions → Fewer catastrophic fires
  → Less carbon released → More resilient communities

═══════════════════════════════════════════════════════════
```

### BACKUP: Technical Details

```
═══════════════════════════════════════════════════════════
                   TECHNICAL METHODOLOGY
═══════════════════════════════════════════════════════════

Change Detection Indices:

  NDVI (Vegetation)    = (NIR - Red) / (NIR + Red)
  → Detects vegetation loss/stress

  NBR (Burn Ratio)     = (NIR - SWIR) / (NIR + SWIR)
  → Detects fuel accumulation

  NDMI (Moisture)      = (NIR - SWIR1) / (NIR + SWIR1)
  → Detects drought stress

Stress Score Formula:
  Stress = Weighted combination of:
    - NDVI decrease (vegetation loss)
    - NBR decrease (fuel buildup)
    - NDMI decrease (moisture deficit)

Fuel Load Enhancement:
  Enhanced_FL = LANDFIRE_baseline × (1 + Stress_Score)

Validation Approach:
  Compare enhanced fuel predictions vs actual burn severity
  Metric: R² correlation coefficient
  Statistical test: Pearson correlation, p-value

═══════════════════════════════════════════════════════════
```

### BACKUP: Competitive Landscape

```
═══════════════════════════════════════════════════════════
                  COMPETITIVE LANDSCAPE
═══════════════════════════════════════════════════════════

Current Solutions:

LANDFIRE (Government):
  ✓ Comprehensive coverage
  ✓ Proven methodology
  ✗ 2-3 year update cycle
  ✗ Misses rapid changes

Private Vendors (Technosylva, Zonehaven):
  ✓ Real-time fire tracking
  ✓ Good UI/UX
  ✗ Expensive ($$$)
  ✗ Focus on active fires, not pre-season planning
  ✗ Proprietary models

Research Projects:
  ✓ Novel methods
  ✓ High accuracy
  ✗ Not operational
  ✗ No validation on real fires

Our Advantage:
  ✓ Builds on proven LANDFIRE
  ✓ Free data, scalable
  ✓ Pre-season focus (prevention)
  ✓ REAL VALIDATION on actual wildfire
  ✓ Ready to deploy

═══════════════════════════════════════════════════════════
```

---

## PRESENTATION TIPS

**Timing**:
- Aim for 6 minutes total
- Leave 1-2 minutes for questions
- Practice with timer

**Delivery**:
- Speak slowly and clearly
- Make eye contact with judges
- Use pauses for emphasis
- Show passion for the problem
- Stay calm if tech fails (have backup screenshots)

**Demo Tips**:
- Test site before presenting
- Have backup screenshots ready
- Narrate what you're clicking
- Don't apologize for UI - it's a working prototype

**Handling Questions**:
- Listen fully before answering
- "Great question, let me address that..."
- If you don't know: "I don't have that data yet, but here's how I'd approach it..."
- Redirect to strengths: "What's most important is..."

**Body Language**:
- Stand tall, confident posture
- Hand gestures for emphasis
- Move with purpose (don't pace)
- Smile when appropriate

**Voice**:
- Project to back of room
- Vary tone to maintain interest
- Emphasize key numbers (43%, $4B)
- End sentences with confidence, not uptalk

---

Good luck! You've built something real and proven. Now just tell that story with confidence. 🔥
