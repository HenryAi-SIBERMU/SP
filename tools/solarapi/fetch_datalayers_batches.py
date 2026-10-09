#!/usr/bin/env python3
"""
fetch_datalayers_batches.py
===========================
Harvester Data Layers Google Solar API Skala Aglomerasi Jabodetabek (Batch 1 s/d 8)
Memenuhi Spesifikasi Dokumen: STRATEGI-EKSEKUSI-5-PILAR-2000-TITIK-JABODETABEK.md (Pilar 3, 4, & 5)

FITUR UTAMA:
1. MODULAR PER BATCH (8 BATCH @ 250 TITIK):
   - Menerima argumen --batch <1..8>
   - Mengambil target secara presisi dari data/raw/poi/target_2000_titik.csv
2. CENTROID SNAPPING & ADAPTIVE ENVELOPE:
   - Membaca koordinat fisik pusat atap (center lat/lon) dari file Building Insights lokal
   - Menghitung radius atap dinamis via adaptive_radius_preprocessor (35m - 95m)
     agar kanopi/gedung tertangkap utuh tanpa terpotong (zero cropped)
3. 4-LAYER GEOTIFF RASTER STREAMING:
   - dsm.tif         -> Digital Surface Model 3D atap
   - rgb.tif         -> Foto udara atap resolusi tinggi
   - mask.tif        -> Masking poligon bidang atap
   - annual_flux.tif -> Heatmap radiasi surya tahunan
4. IDEMPOTENT CACHE & ZERO DOUBLE-BILLING:
   - Melewatkan panggilan API jika ke-4 file GeoTIFF sudah ada di disk lokal
5. PACING & RATE LIMITER AMAN:
   - Dibatasi 3 request/detik dengan exponential backoff retry
6. AUDIT & REPORT GENERATION:
   - Mencatat log hasil penarikan batch ke data/raw/solar/datalayers_batch_report.json
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import pandas as pd
from dotenv import load_dotenv

# Safe console encoding for Windows
try:
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / "tools" / "solarapi" / ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError(f"GOOGLE_API_KEY tidak ditemukan di {ENV_PATH}")

# Directory constants
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
RAW_BI_DIR = RAW_SOLAR_DIR / "building_insights"
RAW_LAYERS_DIR = RAW_SOLAR_DIR / "data_layers"
POI_DIR = PROJECT_ROOT / "data" / "raw" / "poi"

# Ensure all subdirectories exist
LAYER_TYPES = ["dsm", "rgb", "mask", "annual_flux"]
for layer_name in LAYER_TYPES:
    (RAW_LAYERS_DIR / layer_name).mkdir(parents=True, exist_ok=True)

# Import adaptive radius preprocessor if available
try:
    sys.path.append(str(PROJECT_ROOT / "tools" / "solarapi"))
    from adaptive_radius_preprocessor import calculate_adaptive_solar_envelope
    ADAPTIVE_AVAILABLE = True
except Exception as e:
    ADAPTIVE_AVAILABLE = False


def get_http_session() -> requests.Session:
    """Membuat HTTP Session dengan retry exponential backoff."""
    session = requests.Session()
    retries = Retry(
        total=4,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


HTTP = get_http_session()


def resolve_building_geometry(target: Dict[str, Any]) -> Tuple[float, float, int]:
    """
    Mengambil koordinat pusat atap dan radius optimal dari Building Insights lokal.
    Fallback ke target CSV jika file JSON tidak tersedia.
    """
    cat = target["category"].lower()
    aid = target["asset_id"].lower()
    bi_path = RAW_BI_DIR / cat / f"{aid}_insights.json"

    fallback_lat = float(target["latitude"])
    fallback_lon = float(target["longitude"])
    fallback_radius = 60

    if not bi_path.exists():
        return fallback_lat, fallback_lon, fallback_radius

    try:
        with open(bi_path, "r", encoding="utf-8") as f:
            bi_data = json.load(f)

        if ADAPTIVE_AVAILABLE:
            envelope = calculate_adaptive_solar_envelope(bi_data, category=cat)
            lat = envelope.get("google_center_lat", fallback_lat)
            lon = envelope.get("google_center_lon", fallback_lon)
            radius = envelope.get("optimal_radius_meters", fallback_radius)
            radius = max(35, min(radius, 100))
            return lat, lon, radius
        else:
            center = bi_data.get("center", {})
            lat = center.get("latitude", fallback_lat)
            lon = center.get("longitude", fallback_lon)
            radius = max(35, min(fallback_radius, 100))
            return lat, lon, radius
    except Exception:
        return fallback_lat, fallback_lon, min(fallback_radius, 100)


def check_cache_status(asset_id: str, category: str) -> Tuple[bool, Dict[str, str]]:
    """Memeriksa apakah ke-4 file GeoTIFF sudah tersimpan di lokal."""
    aid = asset_id.lower()
    cat = category.lower()
    
    file_map = {
        "dsm": RAW_LAYERS_DIR / "dsm" / cat / f"{aid}_dsm.tif",
        "rgb": RAW_LAYERS_DIR / "rgb" / cat / f"{aid}_rgb.tif",
        "mask": RAW_LAYERS_DIR / "mask" / cat / f"{aid}_mask.tif",
        "annual_flux": RAW_LAYERS_DIR / "annual_flux" / cat / f"{aid}_annual_flux.tif"
    }

    all_exist = True
    for layer, p in file_map.items():
        if not (p.exists() and p.stat().st_size > 100):
            all_exist = False
            break

    rel_map = {k: str(v.relative_to(PROJECT_ROOT)) for k, v in file_map.items()} if all_exist else {}
    return all_exist, rel_map


def fetch_single_point_datalayers(
    target: Dict[str, Any],
    api_key: str,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Menjalankan penarikan Data Layers untuk satu titik:
    1. Cek cache
    2. Panggil API jika belum ada
    3. Unduh 4 file GeoTIFF
    """
    aid = target["asset_id"]
    nm = target["asset_name"]
    cat = target["category"].lower()

    # 1. Cek Cache
    cached, _ = check_cache_status(aid, cat)
    if cached:
        return {
            "status": "CACHE_HIT",
            "asset_id": aid,
            "asset_name": nm,
            "category": cat,
            "bytes_downloaded": 0,
            "layers_count": 4,
            "note": "Semua 4 layer GeoTIFF sudah lengkap di disk lokal."
        }

    if dry_run:
        return {
            "status": "DRY_RUN",
            "asset_id": aid,
            "asset_name": nm,
            "category": cat,
            "bytes_downloaded": 0,
            "layers_count": 0,
            "note": "Dry run, API call dilewati."
        }

    # 2. Resolusi Geometri & Radius
    lat, lon, radius = resolve_building_geometry(target)

    # 3. Panggilan API Metadata Data Layers
    url = "https://solar.googleapis.com/v1/dataLayers:get"
    params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "radiusMeters": radius,
        "view": "FULL_LAYERS",
        "requiredQuality": "BASE",
        "pixelSizeMeters": 0.25,
        "key": api_key
    }

    meta = None
    last_err = ""
    for attempt in range(1, 4):
        try:
            resp = HTTP.get(url, params=params, timeout=30)
            if resp.status_code == 200:
                meta = resp.json()
                break
            elif resp.status_code == 404:
                return {
                    "status": "NOT_FOUND_404",
                    "asset_id": aid,
                    "asset_name": nm,
                    "category": cat,
                    "bytes_downloaded": 0,
                    "layers_count": 0,
                    "note": "Data Layers tidak tersedia di koordinat ini."
                }
            else:
                last_err = f"HTTP {resp.status_code}: {resp.text[:150]}"
        except Exception as e:
            last_err = f"Exception: {e}"
            time.sleep(1.5 * attempt)

    if not meta:
        return {
            "status": "ERROR_API",
            "asset_id": aid,
            "asset_name": nm,
            "category": cat,
            "bytes_downloaded": 0,
            "layers_count": 0,
            "note": last_err
        }

    # 4. Unduh 4 Layer Citra GeoTIFF
    layer_configs = [
        ("dsm", "dsmUrl", f"{aid.lower()}_dsm.tif"),
        ("rgb", "rgbUrl", f"{aid.lower()}_rgb.tif"),
        ("mask", "maskUrl", f"{aid.lower()}_mask.tif"),
        ("annual_flux", "annualFluxUrl", f"{aid.lower()}_annual_flux.tif")
    ]

    total_bytes = 0
    saved_count = 0

    for layer_name, url_key, filename in layer_configs:
        layer_url = meta.get(url_key)
        if not layer_url:
            continue

        target_dir = RAW_LAYERS_DIR / layer_name / cat
        target_dir.mkdir(parents=True, exist_ok=True)
        tif_path = target_dir / filename

        # Lewatkan jika sudah ada
        if tif_path.exists() and tif_path.stat().st_size > 100:
            saved_count += 1
            continue

        download_url = f"{layer_url}&key={api_key}"
        for attempt in range(1, 4):
            try:
                tif_resp = HTTP.get(download_url, timeout=90)
                if tif_resp.status_code == 200:
                    with open(tif_path, "wb") as f:
                        f.write(tif_resp.content)
                    total_bytes += len(tif_resp.content)
                    saved_count += 1
                    break
            except Exception as e:
                time.sleep(2 * attempt)

    return {
        "status": "DOWNLOADED" if saved_count == 4 else "PARTIAL",
        "asset_id": aid,
        "asset_name": nm,
        "category": cat,
        "bytes_downloaded": total_bytes,
        "layers_count": saved_count,
        "radius_meters": radius,
        "note": f"Berhasil mengunduh {saved_count}/4 layer GeoTIFF."
    }


def run_batch(
    batch_no: int,
    limit: Optional[int] = None,
    dry_run: bool = False
):
    """Mengeksekusi penarikan Data Layers untuk satu batch."""
    print("=" * 80)
    print(f"  GOOGLE SOLAR API - DATA LAYERS HARVESTER (BATCH {batch_no})")
    print(f"  Target: 250 Titik Infrastruktur Jabodetabek (Pilar 3, 4, & 5)")
    print("=" * 80)

    # 1. Baca master target
    target_csv = POI_DIR / "target_2000_titik.csv"
    if not target_csv.exists():
        raise FileNotFoundError(f"File target tidak ditemukan: {target_csv}")

    df_all = pd.read_csv(target_csv)
    df_batch = df_all[df_all["batch_no"] == batch_no].copy()

    if limit and limit > 0:
        df_batch = df_batch.head(limit)

    total_pts = len(df_batch)
    print(f"[*] Jumlah titik dalam Batch {batch_no} yang akan diproses: {total_pts} titik")
    print(f"[*] Mode: {'DRY RUN' if dry_run else 'LIVE FETCH'}")
    print("-" * 80)

    start_time = time.time()
    results = []
    cache_cnt = 0
    downloaded_cnt = 0
    not_found_cnt = 0
    err_cnt = 0
    total_bytes = 0

    for idx, (_, row) in enumerate(df_batch.iterrows()):
        target = row.to_dict()
        aid = target["asset_id"]
        nm = target["asset_name"]
        cat = str(target["category"]).lower()

        res = fetch_single_point_datalayers(target, API_KEY, dry_run=dry_run)
        results.append(res)

        status = res["status"]
        b_down = res.get("bytes_downloaded", 0)
        total_bytes += b_down

        if status == "CACHE_HIT":
            cache_cnt += 1
            print(f"[{idx+1:03d}/{total_pts:03d}] [CACHE] {aid} | {nm[:36]:36s} (4 GeoTIFF Lengkap)")
        elif status == "DRY_RUN":
            print(f"[{idx+1:03d}/{total_pts:03d}] [DRY_RUN] {aid} | {nm[:36]:36s} (Simulasi Valid)")
        elif status == "DOWNLOADED":
            downloaded_cnt += 1
            mb = b_down / (1024 * 1024)
            print(f"[{idx+1:03d}/{total_pts:03d}] [FETCH OK] {aid} | {nm[:36]:36s} -> 4 TIF ({mb:.2f} MB)")
            time.sleep(0.35)  # Pacing 3 req/s
        elif status == "NOT_FOUND_404":
            not_found_cnt += 1
            print(f"[{idx+1:03d}/{total_pts:03d}] [404] {aid} | {nm[:36]:36s} (Data Layers Not Found)")
            time.sleep(0.2)
        else:
            err_cnt += 1
            print(f"[{idx+1:03d}/{total_pts:03d}] [ERR] {aid} | {nm[:36]:36s} -> {res.get('note', '')[:40]}")
            time.sleep(0.5)

    elapsed = time.time() - start_time
    total_mb = total_bytes / (1024 * 1024)
    total_gb = total_mb / 1024

    # Hitung total file GeoTIFF di disk lokal untuk batch ini
    disk_tifs = 0
    for _, row in df_batch.iterrows():
        a = row["asset_id"].lower()
        c = str(row["category"]).lower()
        for layer in LAYER_TYPES:
            f = RAW_LAYERS_DIR / layer / c / f"{a}_{layer}.tif"
            if f.exists() and f.stat().st_size > 100:
                disk_tifs += 1

    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "batch_no": batch_no,
        "total_points_evaluated": total_pts,
        "cache_hits": cache_cnt,
        "newly_downloaded": downloaded_cnt,
        "not_found_404": not_found_cnt,
        "errors": err_cnt,
        "total_tifs_on_disk_for_batch": disk_tifs,
        "total_tifs_expected": total_pts * 4,
        "downloaded_mb": round(total_mb, 2),
        "downloaded_gb": round(total_gb, 3),
        "elapsed_seconds": round(elapsed, 1),
        "gcp_api_calls_made": downloaded_cnt + not_found_cnt,
        "dry_run": dry_run
    }

    # Simpan laporan batch
    report_file = RAW_SOLAR_DIR / "datalayers_batch_report.json"
    reports_all = {}
    if report_file.exists():
        try:
            with open(report_file, "r", encoding="utf-8") as rf:
                reports_all = json.load(rf)
        except Exception:
            reports_all = {}

    if "batches" not in reports_all:
        reports_all["batches"] = {}
    reports_all["batches"][f"batch_{batch_no}"] = summary
    reports_all["last_run"] = summary

    with open(report_file, "w", encoding="utf-8") as rf:
        json.dump(reports_all, rf, indent=2, ensure_ascii=False)

    print("=" * 80)
    print(f"  RINGKASAN EKSEKUSI DATA LAYERS (BATCH {batch_no}):")
    print(f"  * Total Titik Dievaluasi          : {total_pts} titik")
    print(f"  * Cache Hit (Sudah Tersimpan)     : {cache_cnt} titik")
    print(f"  * Berhasil Diunduh Baru           : {downloaded_cnt} titik")
    print(f"  * 404 Tidak Tersedia              : {not_found_cnt} titik")
    print(f"  * Error Jaringan / API            : {err_cnt} titik")
    print(f"  * Kelengkapan File GeoTIFF di Disk: {disk_tifs} / {total_pts * 4} file")
    print(f"  * Volume Data Terunduh            : {total_mb:.2f} MB (~{total_gb:.3f} GB)")
    print(f"  * Panggilan API GCP Riil          : {summary['gcp_api_calls_made']} calls")
    print(f"  * Waktu Eksekusi                  : {elapsed:.1f} detik ({elapsed/60:.1f} menit)")
    print("=" * 80)

    return summary


def main():
    parser = argparse.ArgumentParser(description="Google Solar API - Data Layers Harvester Per Batch")
    parser.add_argument("--batch", type=int, required=True, choices=range(1, 9), help="Nomor batch yang dieksekusi (1 s/d 8)")
    parser.add_argument("--limit", type=int, default=None, help="Batas jumlah titik untuk uji coba (opsional)")
    parser.add_argument("--dry-run", action="store_true", help="Uji coba tanpa memanggil API riil")

    args = parser.parse_args()
    run_batch(batch_no=args.batch, limit=args.limit, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
