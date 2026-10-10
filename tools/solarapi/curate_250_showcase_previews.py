"""
curate_250_showcase_previews.py
================================
Skrip kurasi algoritmik 250 titik showcase terbaik untuk dimasukkan ke Git
(data/processed/previews/ dan data/processed/previews/infill/).

Metodologi Seleksi (Composite Stratified Showcase Index - CSSI):
1. Strata Baseline Pilot (100 titik): Dipertahankan 100% untuk kontinuitas historis.
2. Strata Ekspansi Batch 1-4 (150 titik): Dipilih berbasis kuota proporsional 13 kategori
   dengan skor komposit:
     CSSI = 0.40 * Cap_norm + 0.40 * Suitability_norm + 0.20 * Drift_norm
3. Total Showcase = 250 titik persis.

Optimasi Format:
- Mengambil 7 layer dari data/processed/renders_full/
- Dikonversi ke WebP Quality 85 (max dimension 900px)
- Total ukuran folder terkunci ~70-80 MB (Aman untuk GitHub & Streamlit Cloud).
"""

import os
import sys
import shutil
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
import numpy as np
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CALC_DIR = PROJECT_ROOT / "data" / "processed" / "calculations"
RENDERS_FULL_DIR = PROJECT_ROOT / "data" / "processed" / "renders_full"
PREVIEWS_DIR = PROJECT_ROOT / "data" / "processed" / "previews"
PREVIEWS_INFILL_DIR = PREVIEWS_DIR / "infill"

PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
PREVIEWS_INFILL_DIR.mkdir(parents=True, exist_ok=True)

LAYER_SUFFIX_MAP = {
    "rgb": "_rgb",
    "panels": "_panels_overlay",
    "dsm": "_dsm_elevation",
    "mask": "_roof_mask",
    "flux": "_flux_heatmap",
    "segments": "_segments_overlay",
    "infill": "_infill_panels_overlay",
}

CATEGORY_QUOTAS = {
    "brt": 36,
    "krl": 15,
    "mrt_lrt": 10,
    "parking": 25,
    "mall": 20,
    "market": 18,
    "university": 12,
    "stadium": 8,
    "terminal": 6,
}


def select_250_showcase_assets() -> pd.DataFrame:
    summary_p = CALC_DIR / "pow_solar_kumulatif_summary.parquet"
    if not summary_p.exists():
        raise FileNotFoundError(f"File summary tidak ditemukan: {summary_p}")

    df = pd.read_parquet(summary_p)
    df_valid = df[df["path_rgb_geotiff"].notna()].copy()

    # Identifikasi pilot 100 titik awal
    # Pilot ID biasanya berformat 'BRT-001' s/d 'BRT-008' atau terdapat di file 100 summary
    pilot_100_summary = CALC_DIR / "pow_solar_100_titik_summary.csv"
    if pilot_100_summary.exists():
        df_p100 = pd.read_csv(pilot_100_summary)
        pilot_aids = set(df_p100["asset_id"].str.upper().tolist())
    else:
        # Fallback jika file summary tidak ada, ambil dari pola ID digit 3 angka (misal KRL-001)
        pilot_aids = set(df_valid[df_valid["asset_id"].str.len() <= 8]["asset_id"].str.upper().tolist())

    df_pilot = df_valid[df_valid["asset_id"].str.upper().isin(pilot_aids)].copy()
    df_pilot["is_pilot_baseline"] = True
    df_pilot["cssi_score"] = 1.0

    df_candidates = df_valid[~df_valid["asset_id"].str.upper().isin(pilot_aids)].copy()

    selected_new = []
    for cat, quota in CATEGORY_QUOTAS.items():
        cat_df = df_candidates[df_candidates["category"] == cat].copy()
        if cat_df.empty:
            continue

        cap = cat_df["installed_capacity_kwp"].values
        cap_norm = (cap - cap.min()) / (cap.max() - cap.min() + 1e-6)

        suit = cat_df["roof_suitability_ratio_pct"].values
        suit_norm = (suit - suit.min()) / (suit.max() - suit.min() + 1e-6)

        drift = cat_df["spatial_drift_meters"].values
        drift_norm = 1.0 - (drift - drift.min()) / (drift.max() - drift.min() + 1e-6)

        cat_df["cssi_score"] = 0.40 * cap_norm + 0.40 * suit_norm + 0.20 * drift_norm
        cat_df["is_pilot_baseline"] = False

        top = cat_df.sort_values(by="cssi_score", ascending=False).head(quota)
        selected_new.append(top)

    df_selected_new = pd.concat(selected_new, ignore_index=True)
    df_final = pd.concat([df_pilot, df_selected_new], ignore_index=True)

    # Pastikan tepat 250 titik
    if len(df_final) > 250:
        df_final = df_final.head(250)
    elif len(df_final) < 250:
        diff = 250 - len(df_final)
        remaining = df_candidates[~df_candidates["asset_id"].isin(df_final["asset_id"])].head(diff).copy()
        remaining["is_pilot_baseline"] = False
        remaining["cssi_score"] = 0.5
        df_final = pd.concat([df_final, remaining], ignore_index=True)

    return df_final


def process_single_asset_webp(row_dict: dict) -> dict:
    aid = str(row_dict["asset_id"]).strip().lower()
    success_count = 0

    for layer, sfx in LAYER_SUFFIX_MAP.items():
        src_png = RENDERS_FULL_DIR / layer / f"{aid}{sfx}.png"
        if not src_png.exists():
            continue

        if layer == "infill":
            dst_webp = PREVIEWS_INFILL_DIR / f"{aid}{sfx}.webp"
        else:
            dst_webp = PREVIEWS_DIR / f"{aid}{sfx}.webp"

        try:
            with Image.open(src_png) as im:
                w, h = im.size
                # Max dimension 900px
                if max(w, h) > 900:
                    scale = 900.0 / max(w, h)
                    im_resized = im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
                else:
                    im_resized = im

                # Simpan WebP kualitas 85
                im_resized.save(dst_webp, format="WEBP", quality=85, method=6)
                success_count += 1
        except Exception:
            pass

    return {"asset_id": aid, "layers_converted": success_count}


def main():
    print("=" * 80)
    print("  KURASI & EKSPOR 250 TITIK SHOWCASE KE PREVIEWS (WEBP RINGAN ~70 MB)")
    print("=" * 80)
    t0 = time.time()

    # 1. Seleksi 250 titik
    df_250 = select_250_showcase_assets()
    print(f"[*] Berhasil menyeleksi tepat {len(df_250)} titik showcase:")
    print(f"    - Pilot Baseline : {df_250['is_pilot_baseline'].sum()} titik")
    print(f"    - Batch 1-4 Baru : {(~df_250['is_pilot_baseline']).sum()} titik")
    print("\n[*] Distribusi Kategori 250 Titik Showcase:")
    print(df_250["category"].value_counts().to_string())

    # Simpan registry kurasi
    reg_csv = CALC_DIR / "pow_solar_250_showcase_registry.csv"
    reg_parquet = CALC_DIR / "pow_solar_250_showcase_registry.parquet"
    df_250.to_csv(reg_csv, index=False, encoding="utf-8")
    df_250.to_parquet(reg_parquet, index=False)
    print(f"\n[+] Tersimpan Registry 250 Showcase:")
    print(f"    - CSV     : {reg_csv.relative_to(PROJECT_ROOT)}")
    print(f"    - Parquet : {reg_parquet.relative_to(PROJECT_ROOT)}")

    # 2. Konversi 250 titik x 7 layer ke WebP secara paralel
    print("\n[*] Memulai konversi 7 layer ke WebP Quality 85...")
    assets_list = df_250.to_dict("records")
    total_converted = 0

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_single_asset_webp, row): row["asset_id"] for row in assets_list}
        for i, future in enumerate(as_completed(futures), 1):
            res = future.result()
            total_converted += res["layers_converted"]
            if i % 50 == 0 or i == len(assets_list):
                print(f"[{i:03d}/{len(assets_list):03d}] Diproses {i} aset...")

    # 3. Hitung ukuran folder previews
    all_previews = list(PREVIEWS_DIR.glob("**/*.webp"))
    total_bytes = sum(f.stat().st_size for f in all_previews)
    print("=" * 80)
    print(f"  RINGKASAN KURASI SHOWCASE 250 TITIK:")
    print(f"  * Total Aset Dikurasi   : {len(df_250)} titik")
    print(f"  * Total File WebP Dibuat: {len(all_previews)} file")
    print(f"  * Ukuran Total WebP     : {total_bytes / (1024**2):.2f} MB")
    print(f"  * Waktu Eksekusi Total  : {time.time() - t0:.2f} detik")
    print("=" * 80)


if __name__ == "__main__":
    main()
