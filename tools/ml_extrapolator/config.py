"""
Konfigurasi Terpusat untuk Pipeline ML Ekstrapolasi 20.000 Titik PLTS Atap
Mengacu pada:
1. docs/STRATEGI-TOOL-ML-EKSTRAPOLASI-20000-TITIK-SLR.md
2. docs/LAPORAN-POTENSI-MAKSIMAL-POPULASI-OSM-13-KATEGORI-JABODETABEK.md
3. Standar IEC 61724-1 (PR 80% Tropis) & Jamali Grid Factor ESDM (808.99 kg/MWh)
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CALCULATIONS_DIR = PROCESSED_DIR / "calculations"
POI_RAW_DIR = RAW_DIR / "poi"
OSM_RAW_DIR = RAW_DIR / "osm"
MODEL_DIR = Path(__file__).resolve().parent / "saved_models"

# Dataset Files
GROUND_TRUTH_FILE = CALCULATIONS_DIR / "pow_solar_kumulatif_summary.csv"
OUTPUT_PARQUET_FILE = CALCULATIONS_DIR / "pow_solar_extrapolasi_20000_summary.parquet"
OUTPUT_CSV_FILE = CALCULATIONS_DIR / "pow_solar_extrapolasi_20000_summary.csv"
OUTPUT_METRICS_LOG = CALCULATIONS_DIR / "ml_extrapolation_audit_metrics.json"

# Raw Source Files for Population Assembly
SCHOOLS_OSM_JSON = OSM_RAW_DIR / "schools_osm_overpass.json"
UNIVERSITIES_OSM_JSON = OSM_RAW_DIR / "universities_osm_overpass.json"
BUS_STOPS_GPKG = OSM_RAW_DIR / "bus_stops_jakarta.gpkg"
TRANSJAKARTA_CSV = RAW_DIR / "transjakarta" / "transjakarta_stations.csv"
HOSPITALS_GPKG = OSM_RAW_DIR / "hospitals_jakarta.gpkg"
BUILDINGS_GPKG = OSM_RAW_DIR / "buildings_jakarta.gpkg"
PARKING_GPKG = OSM_RAW_DIR / "parking_jakarta.gpkg"
STATIONS_GPKG = OSM_RAW_DIR / "stations_jakarta.gpkg"
CANDIDATES_POI_CSV = POI_RAW_DIR / "candidates_2200_titik.csv"
TARGET_2000_CSV = POI_RAW_DIR / "target_2000_titik.csv"

# Bounding Box Jabodetabek (Rule Spatial Integrity)
BBOX_JABODETABEK = {
    "min_lat": -6.65,
    "max_lat": -6.05,
    "min_lon": 106.55,
    "max_lon": 107.15
}

# Technical Standards (Physics Engine)
PANEL_WP = 400.0                       # Modul Monokristalin Tier-1 400 Wp
PANEL_AREA_M2 = 1.785                  # Luas per modul (~1.72m x 1.04m = 1.785 m2)
PERFORMANCE_RATIO = 0.80               # IEC 61724 PR 80% (Cirata IJTech UI Benchmark)
GRID_EMISSION_FACTOR = 808.99          # kg CO2 / MWh (Ditjen Ketenagalistrikan ESDM Jamali)
ANNUAL_SUNSHINE_DEFAULT = 1627.95      # Rata-rata jam surya efektif Jabodetabek (Google Solar)

# Quantiles for Probabilistic Extrapolation
QUANTILES = [0.10, 0.50, 0.90]

# 13 Target Categories Mapping & Display Names
CATEGORY_MAPPING = {
    "school": "Sekolah (SD, SMP, SMA/SMK)",
    "brt": "Halte TransJakarta & Shelter Transit",
    "hospital": "Fasilitas Kesehatan (RS & Puskesmas)",
    "university": "Universitas & Kampus",
    "market": "Pasar Tradisional & Rakyat",
    "parking": "Gedung Parkir (MSCP)",
    "krl": "Stasiun KRL Commuter Line",
    "mall": "Pusat Perbelanjaan / Mall",
    "stadium": "Stadion, GOR & Arena Olahraga",
    "mrt_lrt": "Stasiun MRT & LRT",
    "terminal": "Terminal Bus & Simpul Antarmoda",
    "jpo": "Jembatan Penyeberangan (JPO) Beratap",
    "airport": "Fasilitas Penunjang Bandara",
    "government": "Gedung Instansi Pemerintah (Inpres 7/2022)"
}

# Random Seed for Reproducibility
RANDOM_STATE = 42
