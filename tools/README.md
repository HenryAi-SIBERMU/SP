# Data Collection Tools

Tools untuk mining dan download data dari berbagai sumber.

## 📁 Folder Structure

```
tools/
├── osm/              # OpenStreetMap data scraper
├── pvgis/            # PVGIS solar data API
├── regulations/      # Regulations & reports downloader
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install osmnx geopandas requests pandas
```

### 2. Run Tools (in order)

```bash
# Tool 1: Download OSM data (buildings, POI, parking)
python tools/osm/scraper.py

# Tool 2: Download PVGIS solar data
python tools/pvgis/scraper.py

# Tool 3: Download regulations & reports
python tools/regulations/downloader.py
```

---

## 📄 Tool Details

### tools/osm/scraper.py
**Tingkat Kemudahan**: 🟢 SANGAT MUDAH  
**Estimated Time**: 1-2 jam  
**Output**:
- `data/raw/osm/buildings_jabodetabek.gpkg` - Building footprints
- `data/raw/osm/parking_jabodetabek.gpkg` - Parking areas
- `data/raw/osm/hospitals_jabodetabek.gpkg` - Hospitals
- `data/raw/osm/universities_jabodetabek.gpkg` - Universities
- `data/raw/osm/retail_mall_jabodetabek.gpkg` - Malls & retail
- `data/raw/osm/roads_jabodetabek.gpkg` - Road network

**What it does**:
- Downloads OpenStreetMap data untuk Jabodetabek
- Bounding box: lat -5.9 to -6.7, lon 106.4 to 107.2
- Uses OSMnx library (easy to use)
- Saves as GeoPackage format (better than shapefile)

**Requirements**:
- Internet connection
- osmnx, geopandas libraries

---

### tools/pvgis/scraper.py
**Tingkat Kemudahan**: 🟢 SANGAT MUDAH  
**Estimated Time**: 1 jam  
**Output**:
- `data/raw/solar/pvgis_summary_jabodetabek.csv` - Summary per lokasi
- `data/raw/solar/pvgis_monthly_jabodetabek.csv` - Monthly data
- `data/raw/solar/pvgis_full_data.json` - Full API response

**What it does**:
- Fetches solar irradiation data dari PVGIS API (European JRC)
- Covers 9 locations: Jakarta (5 areas), Tangerang, Bekasi, Depok, Bogor
- Calculates:
  - Peak Sun Hours (PSH) - jam efektif matahari per hari
  - Yearly energy production (kWh/kWp)
  - Monthly breakdown
  - Optimal tilt angle

**Key Output**:
- Average PSH Jabodetabek: ~4.5-5.0 hours/day
- Yearly energy: ~1,350-1,450 kWh/kWp

**Requirements**:
- Internet connection
- requests, pandas libraries

---

### tools/regulations/downloader.py
**Tingkat Kemudahan**: 🟢 SANGAT MUDAH  
**Estimated Time**: 30 menit  
**Output**:
- `data/external/regulations/regulations/PERMEN_ESDM_26_2021_PLTS_Atap.pdf`
- `data/external/regulations/irena/*.pdf` - IRENA cost reports
- `data/external/regulations/iea_pvps/*.pdf` - IEA solar carport case studies

**What it does**:
- Downloads regulatory documents
- Downloads international reports (IRENA, IEA PVPS)
- Includes manual download instructions if auto-download fails

**Requirements**:
- Internet connection
- requests library

---

## 📊 Expected Results

After running all 3 scripts, you should have:

### Data Files:
```
data/
├── raw/
│   ├── osm/
│   │   ├── buildings_jabodetabek.gpkg (large file, ~500MB)
│   │   ├── parking_jabodetabek.gpkg
│   │   ├── hospitals_jabodetabek.gpkg
│   │   ├── universities_jabodetabek.gpkg
│   │   └── ...
│   └── solar/
│       ├── pvgis_summary_jabodetabek.csv
│       └── pvgis_monthly_jabodetabek.csv
└── external/
    └── regulations/
        ├── regulations/PERMEN_ESDM_26_2021.pdf
        ├── irena/*.pdf
        └── iea_pvps/*.pdf
```

### Key Metrics Obtained:
- ✅ ~50,000+ buildings di Jabodetabek
- ✅ ~500+ parking locations
- ✅ Peak Sun Hours: 4.5-5.0 h/day
- ✅ Solar production: ~1,400 kWh/kWp/year
- ✅ Regulatory framework documented

---

## 🔍 Troubleshooting

### OSMnx download very slow
- OSM servers kadang lambat, tunggu saja
- Atau gunakan bbox yang lebih kecil (fokus Jakarta only)

### PVGIS API timeout
- Try again, sometimes server busy
- Reduce number of locations

### PDF download failed
- Follow manual download instructions di script output
- Visit URLs manually dan download

---

## 📈 Next Steps

After getting data:

1. **Visualize OSM data** using QGIS:
   ```bash
   # Open QGIS, drag & drop .gpkg files
   ```

2. **Process OSM data**:
   ```bash
   python scripts/02_data_processing/01_process_osm.py
   ```

3. **Calculate solar potential**:
   ```bash
   python scripts/03_analysis/01_calculate_solar_potential.py
   ```

---

## 📞 Support

If scripts fail:
- Check internet connection
- Check Python version (3.9+)
- Install missing libraries: `pip install -r requirements.txt`
- See error messages dan Google them

---

**Last Updated**: 19 Juni 2026  
**Status**: ✅ Ready to use

## 🔥 Adding New Tools

When adding new data source tools, create subfolder per source:

```bash
tools/
├── osm/              # ✅ OpenStreetMap
├── pvgis/            # ✅ PVGIS Solar API
├── regulations/      # ✅ PDF Downloads
├── jakarta_data/     # 🔜 Jakarta Open Data CKAN API
├── google_places/    # 🔜 Google Places API
├── bps_api/          # 🔜 BPS Statistics API
└── nasa_power/       # 🔜 NASA POWER API
```

**Naming Convention**:
- Each folder = one data source
- Main file: `scraper.py` or `downloader.py` or `api_client.py`
- Optional: `README.md`, `config.json`
