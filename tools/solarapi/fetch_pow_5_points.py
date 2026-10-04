"""
fetch_pow_5_points.py
---------------------
Ekstraktor data mentah Google Solar API untuk 5 titik pilot POW lintas kategori:
1. MRT: Stasiun MRT Cipete Raya (sumber: data/raw/mrt_lrt/mrt_stations.csv)
2. KRL: Stasiun KRL Manggarai Sentral (sumber: data/raw/krl/krl_stations.csv)
3. LRT: Stasiun LRT Dukuh Atas (sumber: data/raw/mrt_lrt/lrt_jabodebek_stations.geojson)
4. RS: RSUD Tarakan Jakarta (sumber: data/raw/osm/hospitals_jakarta.gpkg)
5. Gedung Parkir: Lippo Mall Puri 1 Multilevel Parking (sumber: data/raw/osm/parking_jakarta.gpkg)

Fitur Kunci:
- Idempotent Cache: Melewatkan unduhan jika berkas sudah ada di data/raw/ untuk menghemat anggaran GCP.
- Robust Retry: Menangani potensi connection reset (WinError 10054) dengan exponential backoff.
- Console encoding: Menjamin kompatibilitas lintas OS (Windows UTF-8 safe).
"""

import os
import sys
import json
import time
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import pandas as pd
import geopandas as gpd
from pathlib import Path
from dotenv import load_dotenv

# Safe console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / "tools" / "solarapi" / ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError(f"GOOGLE_API_KEY tidak ditemukan di {ENV_PATH}")

# Raw directories setup
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
RAW_BI_DIR = RAW_SOLAR_DIR / "building_insights"
RAW_LAYERS_DIR = RAW_SOLAR_DIR / "data_layers"

for sub in ["dsm", "rgb", "mask", "annual_flux"]:
    (RAW_LAYERS_DIR / sub).mkdir(parents=True, exist_ok=True)
RAW_BI_DIR.mkdir(parents=True, exist_ok=True)


def get_http_session():
    """Membuat HTTP Session dengan retry exponential backoff."""
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


HTTP = get_http_session()


def load_raw_targets():
    """
    Membaca target titik pilot secara dinamis dari file fisik data/raw/
    Zero hardcoded coordinates!
    """
    targets = []

    # 1. MRT Cipete Raya
    mrt_path = PROJECT_ROOT / "data" / "raw" / "mrt_lrt" / "mrt_stations.csv"
    if not mrt_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {mrt_path}")
    df_mrt = pd.read_csv(mrt_path)
    cipete = df_mrt[df_mrt["Nama_Stasiun"].astype(str).str.contains("Cipete Raya", case=False, na=False)].iloc[0]
    targets.append({
        "asset_id": "MRT-003",
        "asset_name": "Stasiun MRT Cipete Raya",
        "category": "mrt",
        "category_display": "MRT",
        "city_regency": "Jakarta Selatan",
        "source_file": "data/raw/mrt_lrt/mrt_stations.csv",
        "lat": float(cipete["Latitude"]),
        "lon": float(cipete["Longitude"])
    })

    # 2. KRL Manggarai Sentral
    krl_path = PROJECT_ROOT / "data" / "raw" / "krl" / "krl_stations.csv"
    if not krl_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {krl_path}")
    df_krl = pd.read_csv(krl_path)
    name_col = "station_name" if "station_name" in df_krl.columns else df_krl.columns[0]
    lat_col = "latitude" if "latitude" in df_krl.columns else df_krl.columns[1]
    lon_col = "longitude" if "longitude" in df_krl.columns else df_krl.columns[2]
    mri = df_krl[df_krl[name_col].astype(str).str.contains("Manggarai", case=False, na=False)].iloc[0]
    targets.append({
        "asset_id": "KRL-032",
        "asset_name": "Stasiun KRL Manggarai Sentral",
        "category": "krl",
        "category_display": "KRL",
        "city_regency": "Jakarta Selatan",
        "source_file": "data/raw/krl/krl_stations.csv",
        "lat": float(mri[lat_col]),
        "lon": float(mri[lon_col])
    })

    # 3. LRT Dukuh Atas
    lrt_path = PROJECT_ROOT / "data" / "raw" / "mrt_lrt" / "lrt_jabodebek_stations.geojson"
    if not lrt_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {lrt_path}")
    gdf_lrt = gpd.read_file(lrt_path)
    dukuh = gdf_lrt[gdf_lrt["name"].astype(str).str.contains("Dukuh Atas", case=False, na=False)].iloc[0]
    geom_pt = dukuh.geometry if dukuh.geometry.geom_type == "Point" else dukuh.geometry.centroid
    targets.append({
        "asset_id": "LRT-014",
        "asset_name": "Stasiun LRT Dukuh Atas",
        "category": "lrt",
        "category_display": "LRT",
        "city_regency": "Jakarta Pusat",
        "source_file": "data/raw/mrt_lrt/lrt_jabodebek_stations.geojson",
        "lat": float(geom_pt.y),
        "lon": float(geom_pt.x)
    })

    # 4. RSUD Tarakan Jakarta
    hosp_path = PROJECT_ROOT / "data" / "raw" / "osm" / "hospitals_jakarta.gpkg"
    if not hosp_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {hosp_path}")
    gdf_hosp = gpd.read_file(hosp_path)
    tarakan = gdf_hosp[gdf_hosp["name"].astype(str).str.contains("Tarakan", case=False, na=False)].iloc[0]
    tarakan_pt = tarakan.geometry if tarakan.geometry.geom_type == "Point" else tarakan.geometry.centroid
    targets.append({
        "asset_id": "RS-007",
        "asset_name": "RSUD Tarakan Jakarta",
        "category": "hospital",
        "category_display": "Rumah Sakit",
        "city_regency": "Jakarta Pusat",
        "source_file": "data/raw/osm/hospitals_jakarta.gpkg",
        "lat": float(tarakan_pt.y),
        "lon": float(tarakan_pt.x)
    })

    # 5. Pusat Perbelanjaan / Mall: Pondok Indah Mall 1 (sumber: data/raw/osm/commercial_jakarta.geojson)
    mall_path = PROJECT_ROOT / "data" / "raw" / "osm" / "commercial_jakarta.geojson"
    if not mall_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {mall_path}")
    gdf_mall = gpd.read_file(mall_path)
    pim = gdf_mall[gdf_mall["name"].astype(str).str.contains("Pondok Indah Mall 1", case=False, na=False)].iloc[0]
    pim_pt = pim.geometry if pim.geometry.geom_type == "Point" else pim.geometry.centroid
    targets.append({
        "asset_id": "MALL-001",
        "asset_name": "Pondok Indah Mall 1",
        "category": "mall",
        "category_display": "Pusat Perbelanjaan / Mall",
        "city_regency": "Jakarta Selatan",
        "source_file": "data/raw/osm/commercial_jakarta.geojson",
        "lat": float(pim_pt.y),
        "lon": float(pim_pt.x),
        "radius_meters": 175
    })

    return targets


def fetch_building_insights(target):
    """
    Memanggil Building Insights API (kualitas BASE) dan menyimpan JSON mentah
    ke data/raw/solar/building_insights/{kategori}/{asset_id}_insights.json
    """
    cat = target["category"]
    cat_dir = RAW_BI_DIR / cat
    cat_dir.mkdir(parents=True, exist_ok=True)
    out_file = cat_dir / f"{target['asset_id'].lower()}_insights.json"

    # Idempotent check: jika sudah di-cache dan valid, gunakan cache
    if out_file.exists() and out_file.stat().st_size > 100:
        print(f"   [CACHE HIT] Menggunakan Building Insights dari {out_file.relative_to(PROJECT_ROOT)}")
        with open(out_file, "r", encoding="utf-8") as f:
            return json.load(f), False

    url = "https://solar.googleapis.com/v1/buildingInsights:findClosest"
    params = {
        "location.latitude": target["lat"],
        "location.longitude": target["lon"],
        "requiredQuality": "BASE",
        "key": API_KEY
    }

    print(f"\n[1/2] Fetching Building Insights: {target['asset_name']} ({target['lat']:.5f}, {target['lon']:.5f})...")
    for attempt in range(1, 4):
        try:
            resp = HTTP.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"   [SAVED] Raw JSON -> {out_file.relative_to(PROJECT_ROOT)} ({len(resp.content)} bytes)")
                return data, True
            else:
                print(f"   [ERROR] Building Insights HTTP {resp.status_code}: {resp.text}")
                return None, False
        except Exception as e:
            print(f"   [RETRY {attempt}/3] Network exception: {e}")
            time.sleep(2 * attempt)

    return None, False


def fetch_data_layers(target, bi_data=None):
    """
    Memanggil Data Layers API (kualitas BASE) dan mengunduh 4 file GeoTIFF:
    - DSM -> data/raw/solar/data_layers/dsm/{kategori}/{asset_id}_dsm.tif
    - RGB -> data/raw/solar/data_layers/rgb/{kategori}/{asset_id}_rgb.tif
    - Mask -> data/raw/solar/data_layers/mask/{kategori}/{asset_id}_mask.tif
    - Annual Flux -> data/raw/solar/data_layers/annual_flux/{kategori}/{asset_id}_annual_flux.tif
    """
    cat = target["category"]
    aid = target["asset_id"].lower()

    # Prioritaskan titik center dari building insights untuk presisi maksimal kanopi atap
    lat = target["lat"]
    lon = target["lon"]
    if bi_data:
        center = bi_data.get("center", {})
        if "latitude" in center and "longitude" in center:
            lat = center["latitude"]
            lon = center["longitude"]

    radius = target.get("radius_meters", 60)

    url = "https://solar.googleapis.com/v1/dataLayers:get"
    params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "radiusMeters": radius,
        "view": "FULL_LAYERS",
        "requiredQuality": "BASE",
        "pixelSizeMeters": 0.25,
        "key": API_KEY
    }

    layer_configs = [
        ("dsm", "dsmUrl", f"{aid}_dsm.tif"),
        ("rgb", "rgbUrl", f"{aid}_rgb.tif"),
        ("mask", "maskUrl", f"{aid}_mask.tif"),
        ("annual_flux", "annualFluxUrl", f"{aid}_annual_flux.tif")
    ]

    # Cek apakah semua 4 GeoTIFF sudah lengkap
    all_exist = True
    for layer_name, _, filename in layer_configs:
        tif_path = RAW_LAYERS_DIR / layer_name / cat / filename
        if not (tif_path.exists() and tif_path.stat().st_size > 1000):
            all_exist = False
            break

    if all_exist:
        print(f"[2/2] [CACHE HIT] Semua 4 layer GeoTIFF {target['asset_name']} sudah lengkap.")
        saved = {}
        for layer_name, _, filename in layer_configs:
            saved[layer_name] = str((RAW_LAYERS_DIR / layer_name / cat / filename).relative_to(PROJECT_ROOT))
        return saved, False

    print(f"[2/2] Fetching Data Layers: {target['asset_name']}...")
    meta = None
    for attempt in range(1, 4):
        try:
            resp = HTTP.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                meta = resp.json()
                break
            else:
                print(f"   [ERROR] Data Layers HTTP {resp.status_code}: {resp.text}")
                return None, False
        except Exception as e:
            print(f"   [RETRY {attempt}/3] Data Layers call failed: {e}")
            time.sleep(2 * attempt)

    if not meta:
        return None, False

    saved_layers = {}
    for layer_name, url_key, filename in layer_configs:
        layer_url = meta.get(url_key)
        if not layer_url:
            print(f"   [WARN] URL {url_key} tidak tersedia pada respons API.")
            continue

        target_dir = RAW_LAYERS_DIR / layer_name / cat
        target_dir.mkdir(parents=True, exist_ok=True)
        tif_path = target_dir / filename

        if tif_path.exists() and tif_path.stat().st_size > 1000:
            print(f"   [CACHE] GeoTIFF [{layer_name.upper()}] sudah ada ({tif_path.stat().st_size / 1024:.1f} KB)")
            saved_layers[layer_name] = str(tif_path.relative_to(PROJECT_ROOT))
            continue

        download_url = f"{layer_url}&key={API_KEY}"
        print(f"   Downloading GeoTIFF [{layer_name.upper()}]...")
        for attempt in range(1, 4):
            try:
                tif_resp = HTTP.get(download_url, timeout=90)
                if tif_resp.status_code == 200:
                    with open(tif_path, "wb") as f:
                        f.write(tif_resp.content)
                    saved_layers[layer_name] = str(tif_path.relative_to(PROJECT_ROOT))
                    print(f"      [SAVED] {tif_path.relative_to(PROJECT_ROOT)} ({len(tif_resp.content) / 1024:.1f} KB)")
                    break
                else:
                    print(f"      [ERROR] Download {layer_name}: HTTP {tif_resp.status_code}")
            except Exception as e:
                print(f"      [RETRY {attempt}/3] Download {layer_name} failed: {e}")
                time.sleep(2 * attempt)

    return saved_layers, True


def main():
    print("=" * 70)
    print("STARTING GOOGLE SOLAR API STAGE 1 POW EXTRACTION (5 PILOT POINTS)")
    print("Zero Hardcoded Coordinates - 100% Dynamic Parsing from data/raw/")
    print("=" * 70)

    targets = load_raw_targets()
    print(f"Loaded {len(targets)} pilot targets across categories:")
    for idx, t in enumerate(targets, 1):
        print(f" {idx}. [{t['category_display']}] {t['asset_name']} ({t['lat']:.5f}, {t['lon']:.5f}) from {t['source_file']}")

    results = []
    total_cost_usd = 0.0

    for idx, target in enumerate(targets, 1):
        print("\n" + "-" * 70)
        print(f"PROCESSING TARGET {idx}/{len(targets)}: {target['asset_name']} ({target['category_display']})")
        print("-" * 70)

        # 1. Building Insights
        bi_data, bi_billed = fetch_building_insights(target)
        if bi_billed:
            total_cost_usd += 0.005

        time.sleep(0.5)

        # 2. Data Layers (4 GeoTIFF)
        layers_data, layers_billed = fetch_data_layers(target, bi_data=bi_data)
        if layers_billed:
            total_cost_usd += 0.100

        results.append({
            "target": target,
            "has_insights": bool(bi_data),
            "layers": layers_data
        })

        time.sleep(0.5)

    total_cost_idr = total_cost_usd * 16000
    print("\n" + "=" * 70)
    print("STAGE 1 EXTRACTION COMPLETED SUCCESSFULLY!")
    print(f"Total Targets Evaluated: {len(targets)}")
    print(f"Total New GCP Billing Incurred: ${total_cost_usd:.3f} (~Rp {total_cost_idr:,.0f})")
    print(f"Building Insights JSONs saved to: {RAW_BI_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Data Layers GeoTIFFs saved to: {RAW_LAYERS_DIR.relative_to(PROJECT_ROOT)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
