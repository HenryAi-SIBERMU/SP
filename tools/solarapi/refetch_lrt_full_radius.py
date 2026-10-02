"""
refetch_lrt_full_radius.py
--------------------------
Menarik ulang 4 GeoTIFF data layers untuk Stasiun LRT Dukuh Atas (lrt-014)
dengan parameter radiusMeters=115 dan koordinat center Google (-6.2048629, 106.8256039)
agar 100% bentang atap stasiun dan seluruh 777 modul panel (termasuk Segmen 1 di sayap timur)
tertangkap utuh di dalam kanvas citra tanpa terpotong (cropped).

Biaya: Tepat 1 panggilan Data Layers API ($0.075 / ~Rp 1.200).
"""

import os
import sys
import json
import time
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from pathlib import Path
from dotenv import load_dotenv

# Safe console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / "tools" / "solarapi" / ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError(f"GOOGLE_API_KEY tidak ditemukan di {ENV_PATH}")

RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
RAW_LAYERS_DIR = RAW_SOLAR_DIR / "data_layers"


def get_http_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


HTTP = get_http_session()


def refetch_lrt_dukuh_atas():
    print("=" * 70)
    print("REFETCHING FULL-RADIUS DATA LAYERS FOR STASIUN LRT DUKUH ATAS")
    print("Target Radius: 115 meters | Center: -6.2048629, 106.8256039 | Resolution: 0.25 m/px")
    print("=" * 70)

    url = "https://solar.googleapis.com/v1/dataLayers:get"
    params = {
        "location.latitude": -6.2048629,
        "location.longitude": 106.8256039,
        "radiusMeters": 115,
        "view": "FULL_LAYERS",
        "requiredQuality": "BASE",
        "pixelSizeMeters": 0.25,
        "key": API_KEY
    }

    print("\n[1/2] Memanggil Google Solar API dataLayers:get...")
    resp = HTTP.get(url, params=params, timeout=30)
    if resp.status_code != 200:
        print(f"❌ Error calling dataLayers API (HTTP {resp.status_code}): {resp.text}")
        sys.exit(1)

    meta = resp.json()
    print("   [OK] Metadata Data Layers diterima.")

    layer_configs = [
        ("dsm", "dsmUrl", "lrt-014_dsm.tif"),
        ("rgb", "rgbUrl", "lrt-014_rgb.tif"),
        ("mask", "maskUrl", "lrt-014_mask.tif"),
        ("annual_flux", "annualFluxUrl", "lrt-014_annual_flux.tif")
    ]

    print("\n[2/2] Mengunduh 4 file GeoTIFF radius 115m (menimpa versi lama radius 60m)...")
    for layer_name, url_key, filename in layer_configs:
        layer_url = meta.get(url_key)
        if not layer_url:
            print(f"   [WARN] URL {url_key} tidak ditemukan pada respons API.")
            continue

        target_dir = RAW_LAYERS_DIR / layer_name / "lrt"
        target_dir.mkdir(parents=True, exist_ok=True)
        tif_path = target_dir / filename

        download_url = f"{layer_url}&key={API_KEY}"
        print(f"   Downloading [{layer_name.upper()}] -> {tif_path.relative_to(PROJECT_ROOT)}...")
        
        tif_resp = HTTP.get(download_url, timeout=90)
        if tif_resp.status_code == 200:
            with open(tif_path, "wb") as f:
                f.write(tif_resp.content)
            print(f"   [SAVED] {filename} ({len(tif_resp.content) / 1024:.1f} KB)")
        else:
            print(f"   [ERROR] Gagal download {layer_name}: HTTP {tif_resp.status_code}")
            sys.exit(1)

    print("\n" + "=" * 70)
    print("SELURUH 4 GEOTIFF RADIUS 115M STASIUN LRT DUKUH ATAS BERHASIL DIUNDUH!")
    print("Menjalankan ETL Transformer untuk sinkronisasi seluruh visualisasi & tabel kalkulasi...")
    print("=" * 70)

    # Re-run ETL transformer to synchronize all preview PNGs and processed tables
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    from tools.solarapi.process_pow_etl import process_targets
    process_targets()


if __name__ == "__main__":
    refetch_lrt_dukuh_atas()
