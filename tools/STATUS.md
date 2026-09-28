# Tools Status - Phase 1 Focus

**Updated**: 19 Juni 2026

---

## 📁 Current Structure

```
tools/
├── osm/                    ✅ READY (need bbox adjustment)
│   ├── scraper.py
│   └── README.md
│
├── pvgis/                  ✅ READY (need location adjustment)
│   ├── scraper.py
│   └── README.md
│
├── README.md
└── STATUS.md
```

**Total**: 2 working tools (focused, no bloat)

---

## ✅ Tools Ready

### 1. **OSM Scraper** 
**Status**: ✅ Ready (need adjustment)  
**Purpose**: Jakarta parking, buildings, hospitals, universities, stations  
**Action Needed**: Change bbox dari Jabodetabek → Jakarta only  
**Priority**: 🔴 CRITICAL

### 2. **PVGIS Scraper**
**Status**: ✅ Ready (need adjustment)  
**Purpose**: Peak Sun Hours Jakarta  
**Action Needed**: Remove Bogor, Tangerang, Bekasi, Depok → Jakarta 5 areas only  
**Priority**: 🔴 CRITICAL

---

## 🔨 Tools to Build (Phase 1)

### 3. **Jakarta Open Data Scraper** 
**Status**: 🔨 TO BUILD  
**Purpose**: Halte TransJakarta (284), JPO data  
**Source**: data.jakarta.go.id (CKAN API)  
**Priority**: 🔴 CRITICAL  
**Estimated Time**: 2-3 jam

### 4. **Google Places Scraper**
**Status**: 🔨 TO BUILD  
**Purpose**: Mall, office, hospital POI Jakarta  
**Source**: Google Places API (free quota)  
**Priority**: 🔴 CRITICAL  
**Estimated Time**: 3-4 jam

---

## ❌ Tools Removed (Not Urgent)

- ~~Regulations Downloader~~ - Defer to Phase 2
- ~~BPS API~~ - Not built, not urgent
- ~~NASA POWER~~ - Not built, redundant with PVGIS

---

## 🎯 Phase 1 Goal

**Build 4 tools total**:
- ✅ OSM (adjust)
- ✅ PVGIS (adjust)
- 🔨 Jakarta Open Data (build)
- 🔨 Google Places (build)

**Get 5 critical datasets**:
1. Halte TransJakarta (284)
2. Parking POI Jakarta (500+)
3. Peak Sun Hours (4.8 h/day)
4. KRL/MRT/LRT stations (60+)
5. Mall/office/RS/kampus POI (200-500)

**Timeline**: 1 week (17-21 jam total)

---

## 📋 Next Actions

1. Adjust `osm/scraper.py` → Jakarta bbox
2. Adjust `pvgis/scraper.py` → 5 Jakarta locations
3. Build `jakarta_opendata/scraper.py`
4. Build `google_places/scraper.py`

See: `URGENT-DATASETS.md` for detailed action plan
