#!/usr/bin/env python3
"""
fast_probe_2000_points.py
==========================
Modul Fast-Probe Anti-404 & Pre-Validation Building Insights Google Solar API
Memenuhi Spesifikasi Dokumen: STRATEGI-EKSEKUSI-5-PILAR-2000-TITIK-JABODETABEK.md (Pilar 2 & Pilar 3)

FITUR UTAMA:
1. FAST-PROBE & CACHE-FIRST:
   - Melewatkan titik yang sudah memiliki file JSON di data/raw/solar/building_insights/ (0 API calls, $0 cost).
   - Memanggil endpoint buildingInsights:findClosest secara ringan untuk titik baru.
   - JSON hasil probe langsung disimpan ke disk -> 100% data Building Insights langsung aman!
2. FALLBACK BUFFER HOT-SWAP (ANTI-404):
   - Jika koordinat target utama menghasilkan HTTP 404 (di luar mesh 3D fotogrametri Google),
     sistem secara otomatis menukar dengan kandidat cadangan terdekat dari kategori yang sama
     yang berada dalam pool buffer cadangan (10% buffer / 200 titik).
3. PACING & RATE LIMITING AMAN:
   - Dibatasi 3-4 request per detik (jauh di bawah batas Google 10 req/s / 600 QPM).
4. IDEMPOTENT & RESUMABLE:
   - Dapat dihentikan kapan saja (Ctrl+C) dan dilanjutkan kembali tanpa risiko duplikasi panggilan API.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Konfigurasi Encoding Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / "tools" / "solarapi" / ".env"
load_dotenv(ENV_PATH)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError(f"GOOGLE_API_KEY tidak ditemukan di {ENV_PATH}")

POI_DIR = PROJECT_ROOT / "data" / "raw" / "poi"
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
RAW_BI_DIR = RAW_SOLAR_DIR / "building_insights"
RAW_LAYERS_DIR = RAW_SOLAR_DIR / "data_layers"

CATEGORIES = [
    "airport", "brt", "hospital", "krl", "mrt_lrt", "mall",
    "market", "parking", "school", "stadium", "terminal", "university", "jpo"
]

for cat in CATEGORIES:
    (RAW_BI_DIR / cat).mkdir(parents=True, exist_ok=True)
    for sub in ["dsm", "rgb", "mask", "annual_flux"]:
        (RAW_LAYERS_DIR / sub / cat).mkdir(parents=True, exist_ok=True)


def get_http_session():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def probe_single_point(session, lat: float, lon: float, api_key: str):
    """
    Melakukan panggilan verifikasi ke Building Insights.
    Returns: (status_code, data_json_or_None, error_msg)
    """
    url = "https://solar.googleapis.com/v1/buildingInsights:findClosest"
    params = {
        "location.latitude": lat,
        "location.longitude": lon,
        "requiredQuality": "BASE",
        "key": api_key
    }
    try:
        r = session.get(url, params=params, timeout=15)
        if r.status_code == 200:
            return 200, r.json(), ""
        elif r.status_code == 404:
            return 404, None, "NOT_FOUND"
        elif r.status_code == 400:
            return 400, None, r.text[:100]
        else:
            return r.status_code, None, f"HTTP {r.status_code}: {r.text[:100]}"
    except Exception as e:
        return 0, None, str(e)


def run_fast_probe(batch_target=None, limit=None):
    print("=" * 80)
    print("  FAST-PROBE ANTI-404 & BUILDING INSIGHTS HARVESTER (2.000 TITIK)")
    print("  Dokumen: STRATEGI-EKSEKUSI-5-PILAR-2000-TITIK-JABODETABEK.md (Pilar 2 & 3)")
    print("=" * 80)
    print(f"[*] API Key Status: Terdeteksi ({len(API_KEY)} karakter)")
    print(f"[*] Target Batch  : {batch_target if batch_target else 'SEMUA (Batch 1 - 8)'}")
    print(f"[*] Limit Titik   : {limit if limit else 'Tidak Terbatas'}")
    print("-" * 80)

    cand_file = POI_DIR / "candidates_2200_titik.csv"
    if not cand_file.exists():
        raise FileNotFoundError(f"File kandidat tidak ditemukan: {cand_file}")

    df_cand = pd.read_csv(cand_file)
    df_main = df_cand[~df_cand["is_buffer"]].copy().reset_index(drop=True)
    df_buffer = df_cand[df_cand["is_buffer"]].copy().reset_index(drop=True)

    print(f"[i] Total Target Utama   : {len(df_main)} titik")
    print(f"[i] Total Pool Cadangan : {len(df_buffer)} titik")

    # Filter batch jika ditentukan
    if batch_target is not None and batch_target != "all":
        b_num = int(batch_target)
        df_target_work = df_main[df_main["batch_no"] == b_num].copy()
    else:
        df_target_work = df_main.copy()

    if limit is not None:
        df_target_work = df_target_work.head(int(limit))

    print(f"[i] Titik yang akan dievaluasi dalam sesi ini: {len(df_target_work)} titik")
    print("-" * 80)

    session = get_http_session()

    valid_cached_cnt = 0
    valid_probed_cnt = 0
    swapped_404_cnt = 0
    failed_cnt = 0

    used_buffer_ids = set()
    swap_log = []

    # Map buffer by category
    buffer_by_cat = {}
    for cat in df_buffer["category"].unique():
        buffer_by_cat[cat] = df_buffer[df_buffer["category"] == cat].copy()

    start_time = time.time()

    for idx, (target_idx, row) in enumerate(df_target_work.iterrows()):
        aid = str(row["asset_id"]).strip()
        cat = str(row["category"]).strip().lower()
        nm = str(row["asset_name"]).strip()
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        b_no = int(row.get("batch_no", 1))

        out_json = RAW_BI_DIR / cat / f"{aid.lower()}_insights.json"

        # 1. Cek Caching Lokal (Zero API Call)
        if out_json.exists():
            valid_cached_cnt += 1
            print(f"[{idx+1}/{len(df_target_work)}] [CACHED] {aid} | {nm[:35]:35s} -> Tersedia Lokal")
            continue

        # 2. Panggilan API Ringan
        code, data, err = probe_single_point(session, lat, lon, API_KEY)
        time.sleep(0.3)  # Pacing: ~3 req/detik aman

        if code == 200 and data:
            # Simpan JSON langsung
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            valid_probed_cnt += 1
            roof_m2 = data.get("solarPotential", {}).get("wholeRoofStats", {}).get("areaMeters2", 0)
            panels = data.get("solarPotential", {}).get("maxArrayPanelsCount", 0)
            print(f"[{idx+1}/{len(df_target_work)}] [OK 200]  {aid} | {nm[:35]:35s} -> Atap: {roof_m2:,.0f} m² | {panels} Panel")

        elif code == 404:
            print(f"[{idx+1}/{len(df_target_work)}] [404]     {aid} | {nm[:35]:35s} -> Kena 404! Memulai Hot-Swap Fallback...")
            # 3. Hot-Swap dengan Cadangan Buffer Kategori Sama
            swapped = False
            cat_buf = buffer_by_cat.get(cat, pd.DataFrame())

            if not cat_buf.empty:
                for b_idx, b_row in cat_buf.iterrows():
                    buf_id = str(b_row["asset_id"])
                    if buf_id in used_buffer_ids:
                        continue

                    b_lat = float(b_row["latitude"])
                    b_lon = float(b_row["longitude"])
                    b_nm = str(b_row["asset_name"]).strip()

                    # Probe kandidat buffer
                    b_code, b_data, b_err = probe_single_point(session, b_lat, b_lon, API_KEY)
                    time.sleep(0.3)

                    if b_code == 200 and b_data:
                        # Kandidat buffer valid! Lakukan swap
                        used_buffer_ids.add(buf_id)
                        swapped = True
                        swapped_404_cnt += 1

                        # Simpan JSON menggunakan ID asli target agar konsisten
                        with open(out_json, "w", encoding="utf-8") as f:
                            json.dump(b_data, f, indent=2, ensure_ascii=False)

                        # Update data di df_main
                        replacement_dict = dict(b_row)
                        replacement_dict["asset_id"] = aid  # Tetap pertahankan ID utama
                        replacement_dict["batch_no"] = b_no
                        replacement_dict["is_buffer"] = False
                        replacement_dict["notes"] = f"Hot-Swapped dari buffer {buf_id} (pengganti {nm} 404)"

                        for k, v in replacement_dict.items():
                            if k in df_main.columns:
                                df_main.at[target_idx, k] = v

                        swap_log.append({
                            "original_asset_id": aid,
                            "original_name": nm,
                            "original_lat": lat,
                            "original_lon": lon,
                            "replacement_buffer_id": buf_id,
                            "replacement_name": b_nm,
                            "replacement_lat": b_lat,
                            "replacement_lon": b_lon,
                            "category": cat
                        })

                        print(f"         [SWAP OK] Berhasil digantikan oleh: {b_nm} ({buf_id})")
                        break
                    else:
                        used_buffer_ids.add(buf_id)
                        print(f"         [BUF 404] Cadangan {buf_id} ({b_nm[:25]}) juga 404, mencari berikutnya...")

            if not swapped:
                failed_cnt += 1
                print(f"         [GAGAL] Tidak ada cadangan valid tersisa untuk kategori {cat}!")

        else:
            failed_cnt += 1
            print(f"[{idx+1}/{len(df_target_work)}] [ERR {code}] {aid} | {nm[:35]:35s} -> {err}")

    elapsed = time.time() - start_time

    # 4. Simpan Ulang Master Target 2.000 jika ada swap
    if swapped_404_cnt > 0:
        out_target_csv = POI_DIR / "target_2000_titik.csv"
        out_target_parquet = POI_DIR / "target_2000_titik.parquet"
        out_target_geojson = POI_DIR / "target_2000_titik.geojson"

        df_main.to_csv(out_target_csv, index=False, encoding="utf-8")
        df_main.to_parquet(out_target_parquet, index=False)

        geometry = [Point(xy) for xy in zip(df_main["longitude"], df_main["latitude"])]
        gdf_main = gpd.GeoDataFrame(df_main, geometry=geometry, crs="EPSG:4326")
        gdf_main.to_file(out_target_geojson, driver="GeoJSON")
        print(f"[+] Master target {out_target_csv.name} & GeoJSON berhasil diperbarui dengan hasil swap!")

    # 5. Simpan Laporan Audit Probe
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_evaluated": len(df_target_work),
        "valid_cached": valid_cached_cnt,
        "valid_probed_200": valid_probed_cnt,
        "swapped_404": swapped_404_cnt,
        "failed_unresolved": failed_cnt,
        "elapsed_seconds": round(elapsed, 1),
        "swaps_detail": swap_log
    }

    report_path = POI_DIR / "probe_report_2000.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print("RINGKASAN EKSEKUTIF FAST-PROBE & HARVESTING:")
    print(f"  * Total Titik Dievaluasi : {len(df_target_work)}")
    print(f"  * Valid dari Cache Lokal : {valid_cached_cnt} titik (Zero Cost)")
    print(f"  * Valid Berhasil Ditarik : {valid_probed_cnt} titik (HTTP 200)")
    print(f"  * Kena 404 & Sukses Swap : {swapped_404_cnt} titik")
    print(f"  * Gagal / Belum Berhasil : {failed_cnt} titik")
    print(f"  * Total Waktu Pengerjaan : {elapsed:.1f} detik ({elapsed/60:.1f} menit)")
    print(f"  * Laporan Audit Tercatat : {report_path.name}")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Fast-Probe Anti-404 & Building Insights Harvester (2.000 Titik)")
    parser.add_argument("--batch", type=str, default=None, help="Batch nomor yang akan diproses (1-8 atau all)")
    parser.add_argument("--limit", type=int, default=None, help="Batas jumlah titik yang diproses (opsional)")
    args = parser.parse_args()

    run_fast_probe(batch_target=args.batch, limit=args.limit)


if __name__ == "__main__":
    main()
