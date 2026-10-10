#!/usr/bin/env python3
"""
sync_datalayers_to_summary.py
=============================
Menyinkronkan file raster GeoTIFF lokal (Batch 1 s/d 4) ke dalam master database
tabular kumulatif:
- data/processed/calculations/pow_solar_kumulatif_summary.csv
- data/processed/calculations/pow_solar_kumulatif_summary.parquet
- data/processed/gis/pow_solar_kumulatif.geojson
"""

import sys
from pathlib import Path
import pandas as pd
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CALC_DIR = PROJECT_ROOT / "data" / "processed" / "calculations"
GIS_DIR = PROJECT_ROOT / "data" / "processed" / "gis"
RAW_LAYERS_DIR = PROJECT_ROOT / "data" / "raw" / "solar" / "data_layers"

CUMUL_CSV = CALC_DIR / "pow_solar_kumulatif_summary.csv"
CUMUL_PARQ = CALC_DIR / "pow_solar_kumulatif_summary.parquet"
CUMUL_GEOJSON = GIS_DIR / "pow_solar_kumulatif.geojson"


def sync_paths():
    print("=" * 80)
    print("  MENYINKRONKAN PATH GEOTIFF KE MASTER TABULAR KUMULATIF")
    print("=" * 80)

    if not CUMUL_CSV.exists():
        raise FileNotFoundError(f"File {CUMUL_CSV} tidak ditemukan.")

    df = pd.read_csv(CUMUL_CSV)
    print(f"[*] Total baris data: {len(df)} titik")

    # Pindai seluruh file GeoTIFF di disk lokal
    layer_map = {
        "rgb": {},
        "dsm": {},
        "mask": {},
        "annual_flux": {}
    }

    for layer_name in ["rgb", "dsm", "mask", "annual_flux"]:
        lp = RAW_LAYERS_DIR / layer_name
        if lp.exists():
            for f in lp.glob("*/*.tif"):
                # stem format: {aid}_{layer}.tif
                # misalnya: brt-0070_rgb -> brt-0070
                # atau: brt-0070_annual_flux -> brt-0070
                stem = f.stem.lower()
                for suffix in [f"_{layer_name}", "_flux"]:
                    if stem.endswith(suffix):
                        stem = stem[:-len(suffix)]
                        break
                layer_map[layer_name][stem] = str(f.relative_to(PROJECT_ROOT)).replace("\\", "/")

    print(f"[*] Indeks GeoTIFF di disk:")
    for l, d in layer_map.items():
        print(f"    - Layer {l:12s}: {len(d)} file terdeteksi")

    updated_count = 0
    for idx, row in df.iterrows():
        aid = str(row["asset_id"]).strip().lower()

        # Update path jika file ada di disk
        if aid in layer_map["dsm"]:
            df.at[idx, "path_dsm_geotiff"] = layer_map["dsm"][aid]
        if aid in layer_map["rgb"]:
            df.at[idx, "path_rgb_geotiff"] = layer_map["rgb"][aid]
        if aid in layer_map["mask"]:
            df.at[idx, "path_mask_geotiff"] = layer_map["mask"][aid]
        if aid in layer_map["annual_flux"]:
            df.at[idx, "path_flux_geotiff"] = layer_map["annual_flux"][aid]

        if aid in layer_map["rgb"]:
            updated_count += 1

    print(f"[+] Total titik dengan GeoTIFF lengkap: {updated_count} / {len(df)} titik")

    # Simpan kembali CSV & Parquet
    df.to_csv(CUMUL_CSV, index=False, encoding="utf-8")
    df.to_parquet(CUMUL_PARQ, index=False)
    print(f"[+] Berhasil memperbarui {CUMUL_CSV.name} dan {CUMUL_PARQ.name}")

    # Simpan kembali GeoJSON
    if CUMUL_GEOJSON.exists():
        gdf = gpd.read_file(CUMUL_GEOJSON)
        # Gabungkan update kolom path
        for col in ["path_dsm_geotiff", "path_rgb_geotiff", "path_mask_geotiff", "path_flux_geotiff"]:
            gdf[col] = df[col].values
        gdf.to_file(CUMUL_GEOJSON, driver="GeoJSON")
        print(f"[+] Berhasil memperbarui {CUMUL_GEOJSON.name}")

    print("=" * 80)
    print("  SINKRONISASI SELESAI")
    print("=" * 80)


if __name__ == "__main__":
    sync_paths()
