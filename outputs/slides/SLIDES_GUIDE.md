# Presentation Slides - Usage Guide

## 📊 Generated Slides

Location: `/outputs/slides/`

**9 Professional PNG Slides (16:9, 300 DPI):**

1. **slide_01_title.png** (418 KB)
   - Team name: FuelWatch
   - Industry/audience
   - Solution summary
   - Impact statement

2. **slide_02_problem.png** (12 MB)
   - Before/after satellite imagery
   - Hermits Peak fire stats
   - Problem statement

3. **slide_04_solution.png** (345 KB)
   - Workflow diagram
   - 4-step process
   - Key advantages

4. **slide_05_validation.png** (277 KB) ⭐ **MONEY SLIDE**
   - **+43.1% improvement**
   - Comparison bars
   - Validation stats

5. **slide_06_impact.png** (321 KB)
   - 4 use cases
   - Market statistics
   - Billions saved

6. **slide_07_tech.png** (481 KB)
   - Data sources (free & public)
   - Processing stack
   - Operational costs

7. **slide_08_demo.png** (387 KB)
   - Demo URL
   - Walkthrough points
   - Key features

8. **slide_09_next_steps.png** (427 KB)
   - Timeline (3 months, 6-12 months)
   - Funding needs
   - Deployment path

9. **slide_10_closing.png** (390 KB)
   - Call to action
   - Why now
   - Contact info

## 📋 Presentation Order & Timing

**Total: 6-7 minutes**

| Slide | Title | Time | Key Point |
|-------|-------|------|-----------|
| 1 | Title | 15s | Weekly updates, 43% better |
| 2 | Problem | 30s | $4B fire, 2-year-old map |
| - | *(Slide 3 skipped - covered verbally)* | - | - |
| 3 | Solution | 45s | LANDFIRE + satellites |
| 4 | Validation | 45s | **43% improvement** ⭐ |
| 5 | Impact | 30s | Billions saved |
| 6 | Tech | 20s | Free data, scalable |
| 7 | Demo | 60s | *Switch to website* |
| 8 | Next Steps | 30s | Pilot, scale, funding |
| 9 | Closing | 15s | Can't wait, let's go |

## 🎤 How to Use These Slides

### Option 1: PowerPoint/Keynote
1. Insert PNG images in order
2. Set to full screen (16:9 aspect ratio)
3. Add slide transitions (simple fade recommended)
4. **For Demo slide**: Switch to browser, then back to slides

### Option 2: PDF Export
```bash
# On Mac, use Preview to combine PNGs into PDF
# Or use ImageMagick:
cd outputs/slides
convert slide_*.png FuelWatch_Presentation.pdf
```

### Option 3: Google Slides
1. Create new presentation (16:9)
2. Insert → Image → Upload each PNG
3. One image per slide, fit to page
4. Share link for backup

## 💡 Presentation Tips

### Slide 2 (Problem)
- **Let the image speak**
- Point to before (left) and after (right)
- Emphasize the scale: "341,735 acres, $4 billion"

### Slide 4 (Validation) - THE MONEY SLIDE
- **Slow down here**
- Point to the bars
- Emphasize: "Forty-three percent better"
- Pause for impact

### Slide 7 (Demo)
- **This is where you switch to browser**
- Have URL ready in browser tab
- If tech fails, stay on this slide and describe

### Slide 9 (Closing)
- **End strong**
- Make eye contact
- Deliver closing line with confidence
- Pause, then "Thank you"

## 🔧 Customization

To update slides with your name/contact:

**Slide 1 (Title)**: No personalization needed yet
**Slide 10 (Closing)**: Replace `[Your Contact Info]` with:
- Your email
- LinkedIn profile
- GitHub (if relevant)

You can edit the PNGs or regenerate with customization by editing:
`scripts/generate_presentation_slides.py`

## 📱 Backup Plan

**If laptop fails:**
1. Have slides on USB drive
2. Have slides in Google Drive/Dropbox
3. Have PDF version
4. Have demo screenshots ready

**If projector aspect ratio is different:**
- 16:9 slides will still work on 4:3 (letterboxed)
- Images are high-res (300 DPI) so they scale well

## ✅ Pre-Presentation Checklist

### Test Your Setup:
- [ ] Slides load correctly
- [ ] Images are sharp/readable
- [ ] Demo URL works
- [ ] Browser tab is ready
- [ ] Backup screenshots ready
- [ ] Clicker/remote works (if using)

### Visual Quality Check:
- [ ] Text readable from back of room
- [ ] Colors display correctly on projector
- [ ] No typos or errors
- [ ] Slide numbers/order correct

### Practice:
- [ ] Run through with slides 3+ times
- [ ] Practice transitions (especially to/from demo)
- [ ] Time yourself with slides
- [ ] Practice with clicker if using one

## 🎯 Key Messages Per Slide

1. **Title**: We update fuel maps weekly, not yearly - 43% better
2. **Problem**: Catastrophic fire, outdated map, systemic issue
3. **Solution**: LANDFIRE baseline + weekly satellites = better maps
4. **Validation**: Real wildfire proof - 43% improvement ⭐
5. **Impact**: Save billions by better targeting
6. **Tech**: Free, proven, scalable infrastructure
7. **Demo**: It works, it's live, see for yourself
8. **Next**: Ready to deploy with pilot partner
9. **Close**: Can't wait - satellites are ready now

## 📊 Notes on Design

**Colors:**
- Fire red (#d62728) - Primary accent
- Orange (#e6550d) - Secondary accent
- Clean white backgrounds - Professional
- Dark text (#212529) - Readable

**Typography:**
- Large text (20-48pt) - Readable from distance
- Bold for emphasis
- Minimal text per slide
- High contrast for readability

**Layout:**
- 16:9 widescreen format
- Centered content
- Visual hierarchy clear
- Consistent styling

## 🚀 Quick Start

**To present right now:**

1. Open `outputs/slides/` folder
2. Load slide_01_title.png
3. Go through in numerical order
4. At slide_08, switch to browser
5. After demo, return to slides
6. Finish with slide_10

**That's it!** You're ready to pitch.

---

Good luck! You've got killer slides and a killer story. 🔥
