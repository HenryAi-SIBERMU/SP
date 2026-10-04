"""
fetch_pow_100_points.py
-----------------------
Ekstraktor data mentah Google Solar API untuk 100 titik infrastruktur Jabodetabek lintas 13 kategori.
Membaca target secara dinamis dari data/raw/poi/target_100_titik.csv.

Fitur Kunci:
- Zero Hardcoding: Murni mengonsumsi data/raw/poi/target_100_titik.csv (Single Source of Truth).
- Idempotent Cache: Melewatkan unduhan jika berkas sudah ada di data/raw/ (menghemat kuota GCP & anggaran).
- 13 Titik Pilot Eksisting otomatis di-skip (hanya memanggil API untuk 87 titik baru).
- Robust Retry: Menangani connection reset / timeout dengan exponential backoff.
- Kepatuhan Regulasi Agen: no_hardcoded_data.md, strict_data_folder_boundary.md.
"""

import os
import sys
import json
import time
import argparse
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Safe console encoding for Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = Path(__file__).resolve().parent / ".env"
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


def load_targets_from_csv(csv_path):
    """
    Membaca target titik dari file master CSV target_100_titik.csv.
    Zero hardcoded coordinates in python code!
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"File master target tidak ditemukan: {csv_path}")

    df = pd.read_csv(csv_path)
    required_cols = ["asset_id", "asset_name", "category", "latitude", "longitude", "radius_meters"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Kolom wajib '{col}' tidak ditemukan di {csv_path}")

    targets = []
    for _, row in df.iterrows():
        targets.append({
            "asset_id": str(row["asset_id"]).strip(),
            "asset_name": str(row["asset_name"]).strip(),
            "category": str(row["category"]).strip().lower(),
            "category_display": str(row.get("category_display", row["category"])).strip(),
            "city_regency": str(row.get("city_regency", "")).strip(),
            "lat": float(row["latitude"]),
            "lon": float(row["longitude"]),
            "radius_meters": int(row.get("radius_meters", 60)),
            "source_reference": str(row.get("source_reference", "")).strip()
        })
    return targets


def fetch_building_insights(target, dry_run=False):
    """
    Memanggil Building Insights API (kualitas BASE) dan menyimpan JSON mentah
    ke data/raw/solar/building_insights/{kategori}/{asset_id}_insights.json
    """
    cat = target["category"]
    aid = target["asset_id"].lower()
    cat_dir = RAW_BI_DIR / cat
    cat_dir.mkdir(parents=True, exist_ok=True)
    out_file = cat_dir / f"{aid}_insights.json"

    # Idempotent check: Jika file sudah ada dan valid, langsung pakai cache
    if out_file.exists() and out_file.stat().st_size > 100:
        print(f"   [CACHE HIT] Menggunakan Building Insights eksisting: {out_file.relative_to(PROJECT_ROOT)}")
        with open(out_file, "r", encoding="utf-8") as f:
            return json.load(f), False

    if dry_run:
        print(f"   [DRY-RUN] Melewati panggilan Building Insights untuk {target['asset_name']}")
        return None, False

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
            elif resp.status_code == 404:
                print(f"   [NOT FOUND 404] Bangunan di ({target['lat']:.5f}, {target['lon']:.5f}) tidak ada dalam katalog 3D Google Solar.")
                return None, False
            else:
                print(f"   [ERROR] Building Insights HTTP {resp.status_code}: {resp.text[:200]}")
                return None, False
        except Exception as e:
            print(f"   [RETRY {attempt}/3] Network exception: {e}")
            time.sleep(2 * attempt)

    return None, False


def fetch_data_layers(target, bi_data=None, dry_run=False):
    """
    Memanggil Data Layers API (kualitas BASE) dan mengunduh 4 file GeoTIFF:
    - DSM -> data/raw/solar/data_layers/dsm/{kategori}/{asset_id}_dsm.tif
    - RGB -> data/raw/solar/data_layers/rgb/{kategori}/{asset_id}_rgb.tif
    - Mask -> data/raw/solar/data_layers/mask/{kategori}/{asset_id}_mask.tif
    - Annual Flux -> data/raw/solar/data_layers/annual_flux/{kategori}/{asset_id}_annual_flux.tif
    """
    cat = target["category"]
    aid = target["asset_id"].lower()

    lat = target["lat"]
    lon = target["lon"]
    if bi_data:
        center = bi_data.get("center", {})
        if "latitude" in center and "longitude" in center:
            lat = center["latitude"]
            lon = center["longitude"]

    radius = target.get("radius_meters", 60)

    layer_configs = [
        ("dsm", "dsmUrl", f"{aid}_dsm.tif"),
        ("rgb", "rgbUrl", f"{aid}_rgb.tif"),
        ("mask", "maskUrl", f"{aid}_mask.tif"),
        ("annual_flux", "annualFluxUrl", f"{aid}_annual_flux.tif")
    ]

    # Idempotent check
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

    if dry_run:
        print(f"   [DRY-RUN] Melewati unduhan Data Layers GeoTIFF untuk {target['asset_name']}")
        return None, False

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

    print(f"[2/2] Fetching Data Layers: {target['asset_name']} (radius={radius}m)...")
    meta = None
    for attempt in range(1, 4):
        try:
            resp = HTTP.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                meta = resp.json()
                break
            elif resp.status_code == 404:
                print(f"   [NOT FOUND 404] Data Layers tidak tersedia pada lokasi ini.")
                return None, False
            else:
                print(f"   [ERROR] Data Layers HTTP {resp.status_code}: {resp.text[:200]}")
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
    parser = argparse.ArgumentParser(description="Fetch Google Solar API untuk 100 titik Jabodetabek.")
    parser.add_argument("--input", default="data/raw/poi/target_100_titik.csv", help="Path CSV master target.")
    parser.add_argument("--dry-run", action="store_true", help="Hanya cek ketersediaan cache dan verifikasi tanpa memanggil API.")
    parser.add_argument("--limit", type=int, default=None, help="Batas maksimal titik yang diproses (opsional).")
    args = parser.parse_args()

    csv_path = PROJECT_ROOT / args.input
    targets = load_targets_from_csv(csv_path)

    if args.limit:
        targets = targets[:args.limit]

    print("=" * 75)
    print("STARTING GOOGLE SOLAR API BATCH EXTRACTION (100 TITIK / 13 KATEGORI)")
    print(f"Single Source of Truth: {csv_path.relative_to(PROJECT_ROOT)}")
    print(f"Total Targets Loaded : {len(targets)} titik")
    print(f"Mode                 : {'DRY-RUN (Simulasi)' if args.dry_run else 'LIVE FETCH'}")
    print("=" * 75)

    bi_new_calls = 0
    layers_new_calls = 0
    cache_hits = 0

    for idx, target in enumerate(targets, 1):
        print("\n" + "-" * 75)
        print(f"[{idx}/{len(targets)}] {target['asset_id']}: {target['asset_name']} ({target['category_display']}) - {target['city_regency']}")
        print(f"      Koordinat: {target['lat']:.6f}, {target['lon']:.6f} | Radius: {target['radius_meters']}m")
        print("-" * 75)

        # 1. Building Insights
        bi_data, bi_billed = fetch_building_insights(target, dry_run=args.dry_run)
        if bi_billed:
            bi_new_calls += 1
        elif bi_data:
            cache_hits += 1

        # Jika Building Insights tidak ada (misal 404), lewati Data Layers untuk menghemat kuota
        if not bi_data and not args.dry_run:
            print(f"   [SKIP DATA LAYERS] Dilewati karena Building Insights tidak ditemukan.")
            continue

        time.sleep(0.3)

        # 2. Data Layers (4 GeoTIFF)
        layers_data, layers_billed = fetch_data_layers(target, bi_data=bi_data, dry_run=args.dry_run)
        if layers_billed:
            layers_new_calls += 1

    total_cost_usd = (bi_new_calls * 0.0075) + (layers_new_calls * 0.100)
    print("\n" + "=" * 75)
    print("BATCH EXTRACTION REPORT")
    print("=" * 75)
    print(f"Total Target Diproses   : {len(targets)}")
    print(f"Cache Hits (Eksisting)  : {cache_hits} titik (Termasuk 13 titik pilot lama)")
    print(f"Panggilan Baru Insights : {bi_new_calls} request ($0.0075/call)")
    print(f"Panggilan Baru Layers   : {layers_new_calls} request ($0.100/call)")
    print(f"Estimasi Biaya Tambahan : ${total_cost_usd:.4f} USD (~Rp {total_cost_usd * 16000:,.0f})")
    print("=" * 75)


if __name__ == "__main__":
    main()
