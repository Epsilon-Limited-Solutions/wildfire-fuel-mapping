# LANDFIRE Download Instructions - Quick Guide

**Time Required:** 15-20 minutes
**Difficulty:** Easy (web interface)

---

## 🚀 FASTEST METHOD: LANDFIRE Viewer (RECOMMENDED)

### Step-by-Step Instructions:

**1. Open the LANDFIRE Viewer**
   - Go to: https://www.landfire.gov/viewer/
   - Click "Get Data" button (orange button on right side)

**2. Enter the Area of Interest**

   You have two options - use Option A (easiest):

   **Option A - Search by Name:**
   - In the search box, type: **"Hermits Peak, New Mexico"**
   - Click on the result when it appears

   **Option B - Enter Coordinates:**
   - Enter coordinates: **35.8, -105.6**
   - Click "Search"

**3. Select the Data Version**
   - In the dropdown menu, select: **"LF 2020"**
   - (This is the version BEFORE the 2022 fire - critical for comparison!)

**4. Select the Layers to Download**

   Check these boxes (in order of importance):

   ☑️ **FBFM40** - 40 Scott and Burgan Fire Behavior Fuel Models ← MOST IMPORTANT!
   ☑️ **CBD** - Canopy Bulk Density
   ☑️ **CH** - Canopy Height

   *Note: If you're short on time, just download FBFM40 - it's the critical one*

**5. Define Your Download Area**

   - Click the **"Draw Rectangle"** tool in the map
   - Draw a box around the Hermits Peak area

   **Exact coordinates to use:**
   - Northwest corner: **36.0°N, 105.9°W**
   - Southeast corner: **35.6°N, 105.3°W**

   OR copy/paste these into the coordinate boxes:
   ```
   Min Longitude: -105.9
   Max Longitude: -105.3
   Min Latitude: 35.6
   Max Latitude: 36.0
   ```

**6. Select Output Format**
   - Choose: **GeoTIFF**
   - (This is the standard raster format we'll use)

**7. Enter Your Email**
   - Enter your email address
   - They'll send you a download link (usually arrives in 5-15 minutes)

**8. Submit the Request**
   - Click **"Submit Request"**
   - You'll see a confirmation message

**9. Wait for Email**
   - Check your email (including spam folder!)
   - Email should arrive in 5-15 minutes
   - Subject will be something like: "LANDFIRE Data Request Complete"

**10. Download the Files**
   - Click the download link in the email
   - Save the ZIP file to your Downloads folder
   - Links expire after 24-48 hours, so download promptly!

**11. Extract and Move Files**
   ```bash
   # Extract the ZIP file (double-click on Mac)
   # Then move files to the project:

   cd /Users/thomasduquemin/epsilon/applications/hackathon

   # Move the .tif files to the landfire directory
   # (adjust the path to wherever you extracted the files)
   mv ~/Downloads/LF2020_*.tif data/landfire/
   ```

**12. Verify the Download**
   ```bash
   # Check that files are there
   ls -lh data/landfire/

   # You should see files like:
   # LF2020_FBFM40_*.tif
   # LF2020_CBD_*.tif
   # LF2020_CH_*.tif
   ```

---

## ✅ Expected Files

After download, you should have files approximately this size:

- **LF2020_FBFM40_[numbers].tif** → ~50-100 MB (Fuel models)
- **LF2020_CBD_[numbers].tif** → ~50-100 MB (Canopy density)
- **LF2020_CH_[numbers].tif** → ~50-100 MB (Canopy height)

Total: ~150-300 MB

---

## ⏰ Timeline

- **Step 1-7:** Fill out form (5 minutes)
- **Step 8:** Submit and wait for email (5-15 minutes)
- **Step 9-11:** Download and extract (3-5 minutes)

**Total: 15-25 minutes**

---

## 💡 Tips

1. **Start the request NOW** - Even if you're doing other things, you can submit the request and work on something else while waiting for the email

2. **Check spam folder** - Sometimes the email goes to spam

3. **Use a reliable email** - Gmail/Outlook work best

4. **Download within 24 hours** - The link expires, so don't wait too long

5. **FBFM40 is priority** - If the email takes too long or you're impatient, you can submit a second request for just FBFM40 to get started faster

---

## 🆘 Troubleshooting

**Q: Email not arriving after 20 minutes?**
- Check spam folder
- Try submitting again with different email address
- Contact LANDFIRE help: https://www.landfire.gov/contact.php

**Q: Download link expired?**
- Re-submit the request (takes 2 minutes)

**Q: Files won't open?**
- Make sure you extracted the ZIP file first
- Files should end in .tif (not .tif.zip)

**Q: Not sure if I got the right area?**
- Run this to check the coordinates:
  ```bash
  source venv/bin/activate
  python -c "import rasterio; ds = rasterio.open('data/landfire/LF2020_FBFM40*.tif'); print('Bounds:', ds.bounds)"
  ```
- Should show approximately: (-105.9, 35.6, -105.3, 36.0)

**Q: Can I use a smaller area to download faster?**
- Yes, but make sure it covers the fire perimeter
- Minimum recommended: 35.7°N - 35.9°N, 105.5°W - 105.7°W

---

## 🎯 What You're Downloading

**FBFM40 (Fire Behavior Fuel Model 40):**
- Maps different types of burnable vegetation
- 40 different fuel categories
- Critical for understanding fire behavior
- This is your BASELINE map to improve upon

**CBD (Canopy Bulk Density):**
- Density of forest canopy
- Affects how fire spreads through treetops
- Important but secondary to FBFM40

**CH (Canopy Height):**
- Height of forest canopy
- Affects fire intensity
- Important but secondary to FBFM40

---

## ✨ After Download - Next Steps

Once you have the files:

1. ✅ Verify files are in `data/landfire/`
2. ✅ Sign up for Google Earth Engine (if you haven't already)
3. ✅ Wait for GEE approval email
4. ✅ Get some sleep! Tomorrow you'll download satellite data and build the model

---

## 📞 Need Help?

- **LANDFIRE Help Desk:** https://www.landfire.gov/contact.php
- **User Guides:** https://landfire.gov/tutorials.php
- **Ask me (Claude):** Just describe the issue!

---

**START THIS NOW!** Submit the request, then work on other things while waiting for the email.

Good luck! 🔥🗺️
