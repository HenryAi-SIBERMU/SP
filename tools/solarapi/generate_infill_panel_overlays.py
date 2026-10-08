#!/usr/bin/env python3
"""
generate_infill_panel_overlays.py
=================================
Tool Visualisasi Spasial Rekayasa Celah Atap (Roof Gap Infill Overlay Generator).

PRINSIP METODOLOGI:
1. WARNA IDENTIK DENGAN BASELINE GOOGLE: Panel infill dirender dengan warna biru fotovoltaik
   yang persis sama (#2563EB face, #93C5FD edge) untuk menyajikan simulasi atap yang terisi penuh.
2. STANDALONE & REPRODUCIBLE: Skrip ini membaca data secara read-only dan mengekspor gambar
   pratinjau baru ke folder terpisah: data/processed/previews/infill/
3. GRID ALIGNMENT GEOMETRI: Posisi panel baru mengikuti arah orientasi sumbu kanopi (azimuth)
   dan spasi matriks baris-kolom dari panel yang sudah ada secara vectorized cepat (cKDTree).
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
INFILL_CSV_PATH = PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_gap_infill_extension.csv"
OUT_PREVIEWS_DIR = PROJECT_ROOT / "data" / "processed" / "previews" / "infill"


def generate_single_infill_overlay(row: dict, out_dir: Path) -> str:
    asset_id = str(row.get("asset_id", "")).strip()
    cat = str(row.get("category", "")).strip().lower()
    aid = asset_id.lower()
    infill_target_panels = int(row.get("infill_additional_panels", 0))

    out_file = out_dir / f"{aid}_infill_panels_overlay.png"

    bi_file = RAW_SOLAR_DIR / "building_insights" / cat / f"{aid}_insights.json"
    rgb_file = RAW_SOLAR_DIR / "data_layers" / "rgb" / cat / f"{aid}_rgb.tif"

    if not bi_file.exists() or not rgb_file.exists():
        return None

    try:
        with open(bi_file, "r", encoding="utf-8") as f:
            insights = json.load(f)

        solar_pot = insights.get("solarPotential", {})
        existing_panels = solar_pot.get("solarPanels", [])
        segs = solar_pot.get("roofSegmentStats", [])

        ph_m = solar_pot.get("panelHeightMeters", 1.722)
        pw_m = solar_pot.get("panelWidthMeters", 1.134)

        with rasterio.open(rgb_file) as src:
            res_m = abs(src.transform[0])
            ph_px = ph_m / res_m
            pw_px = pw_m / res_m
            width, height = src.width, src.height

            trans = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)

            coords = []
            for p in existing_panels:
                ux, uy = trans.transform(p["center"]["longitude"], p["center"]["latitude"])
                py, px = src.index(ux, uy)
                if 0 <= px < width and 0 <= py < height:
                    coords.append(np.array([px, py]))

            coords = np.array(coords) if len(coords) > 0 else np.empty((0, 2))

            # Azimuth and orientation
            az_deg = 180.0
            if len(segs) > 0:
                az_deg = segs[0].get("azimuthDegrees", 180.0)
            az_rad = math.radians(az_deg)
            u_ridge = np.array([math.cos(az_rad), math.sin(az_rad)])
            u_slope = np.array([-math.sin(az_rad), math.cos(az_rad)])

            # Estimate grid step basis vectors
            if len(coords) >= 10:
                # Subsample if coords is large for fast neighbor distance
                sample_coords = coords[:min(len(coords), 500)]
                diffs = (sample_coords[:, None, :] - sample_coords[None, :, :]).reshape(-1, 2)
                dists = np.linalg.norm(diffs, axis=1)

                col_cand = diffs[(dists > 3.0) & (dists < 5.5)]
                row_cand = diffs[(dists > 5.5) & (dists < 9.0)]

                if len(col_cand) > 0:
                    col_cand_pos = col_cand[col_cand[:, 0] > 0]
                    v_col = np.median(col_cand_pos if len(col_cand_pos) > 0 else col_cand, axis=0)
                else:
                    v_col = u_ridge * (pw_px * 1.05)

                if len(row_cand) > 0:
                    row_cand_pos = row_cand[row_cand[:, 1] > 0]
                    v_row = np.median(row_cand_pos if len(row_cand_pos) > 0 else row_cand, axis=0)
                else:
                    v_row = u_slope * (ph_px * 1.05)
            else:
                v_col = u_ridge * (pw_px * 1.05)
                v_row = u_slope * (ph_px * 1.05)

            # Ensure valid norms
            if np.linalg.norm(v_col) < 1.0: v_col = u_ridge * 4.2
            if np.linalg.norm(v_row) < 1.0: v_row = u_slope * 7.2

            # Candidate infill panels placement (Fast KDTree)
            infill_coords = []
            if infill_target_panels > 0 and len(coords) > 0:
                tree = cKDTree(coords)
                anchor = coords.mean(axis=0)

                step_col_len = max(np.linalg.norm(v_col), 1.0)
                step_row_len = max(np.linalg.norm(v_row), 1.0)
                max_steps_col = min(int(width / step_col_len) + 5, 40)
                max_steps_row = min(int(height / step_row_len) + 5, 40)

                ii, jj = np.meshgrid(
                    np.arange(-max_steps_col, max_steps_col + 1),
                    np.arange(-max_steps_row, max_steps_row + 1)
                )
                grid_pts = anchor + ii.ravel()[:, None] * v_col + jj.ravel()[:, None] * v_row

                # Filter within image bounds
                valid_mask = (
                    (grid_pts[:, 0] >= 15) & (grid_pts[:, 0] < width - 15) &
                    (grid_pts[:, 1] >= 15) & (grid_pts[:, 1] < height - 15)
                )
                valid_grid = grid_pts[valid_mask]

                if len(valid_grid) > 0:
                    dists_to_exist, _ = tree.query(valid_grid)
                    # Non-overlapping points
                    cand_pts = valid_grid[dists_to_exist >= 3.2]
                    cand_d = dists_to_exist[dists_to_exist >= 3.2]

                    # Prioritize points close to the existing array (contiguous infill expansion)
                    sorted_order = np.argsort(cand_d)
                    infill_coords = cand_pts[sorted_order][:infill_target_panels]

            # Render Matplotlib Figure
            rgb_arr = src.read([1, 2, 3]).transpose(1, 2, 0)
            fig, ax = plt.subplots(figsize=(10, 10), dpi=200)
            ax.imshow(rgb_arr)

            def draw_poly(center_pt):
                # Standard blue Google Solar API panel style (SAME COLOR AS REQUESTED)
                l_vec = u_slope * (ph_px / 2.0)
                w_vec = u_ridge * (pw_px / 2.0)
                p1 = center_pt + l_vec + w_vec
                p2 = center_pt + l_vec - w_vec
                p3 = center_pt - l_vec - w_vec
                p4 = center_pt - l_vec + w_vec
                poly = Polygon(
                    [p1, p2, p3, p4], closed=True,
                    facecolor="#2563EB", edgecolor="#93C5FD",
                    linewidth=0.5, alpha=0.90
                )
                ax.add_patch(poly)

            # Draw baseline Google panels
            for c in coords:
                draw_poly(c)

            # Draw infill panels (EXACT SAME COLOR)
            for c in infill_coords:
                draw_poly(c)

            ax.set_xlim(0, width)
            ax.set_ylim(height, 0)
            ax.axis("off")
            fig.patch.set_facecolor("#0E1117")

            fig.savefig(str(out_file.resolve()), facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
            plt.close(fig)

            return out_file.relative_to(PROJECT_ROOT).as_posix()

    except Exception as e:
        print(f"    [WARN] Gagal membuat overlay infill untuk {asset_id}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate Solar Panel Infill Layout Overlay Images (Same Blue Color)"
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(INFILL_CSV_PATH),
        help="Path ke file CSV infill suplemen"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(OUT_PREVIEWS_DIR),
        help="Direktori penyimpanan gambar preview infill"
    )

    args = parser.parse_args()

    infill_csv = Path(args.input)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not infill_csv.exists():
        print(f"[!] File {infill_csv} tidak ditemukan.")
        sys.exit(1)

    df_infill = pd.read_csv(infill_csv)
    print(f"[*] Memproses pembuatan gambar layout infill untuk {len(df_infill)} fasilitas...")

    preview_paths = []
    success_count = 0

    for idx, row in df_infill.iterrows():
        a_id = row.get("asset_id")
        a_name = row.get("asset_name")
        target_pan = int(row.get("infill_additional_panels", 0))

        rel_path = generate_single_infill_overlay(row.to_dict(), out_dir)
        preview_paths.append(rel_path)

        if rel_path:
            success_count += 1
            print(f"  [{idx+1}/{len(df_infill)}] OK: {a_id} - {a_name} (+{target_pan} panel) -> {rel_path}")
        else:
            print(f"  [{idx+1}/{len(df_infill)}] SKIP/GAGAL: {a_id} - {a_name}")

    # Simpan kembali CSV dengan kolom preview_infill_panels_png
    df_infill["preview_infill_panels_png"] = preview_paths
    df_infill.to_csv(infill_csv, index=False, encoding="utf-8")
    
    parquet_path = infill_csv.with_suffix(".parquet")
    df_infill.to_parquet(parquet_path, index=False)

    print("=" * 80)
    print(f"[+] SELESAI: Berhasil membuat {success_count} gambar layout infill atap.")
    print(f"[+] Path preview tercatat di: {infill_csv.name}")
    print("=" * 80)


if __name__ == "__main__":
    main()
