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
from scipy.ndimage import binary_erosion
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
    mask_file = RAW_SOLAR_DIR / "data_layers" / "mask" / cat / f"{aid}_mask.tif"
    flux_file = RAW_SOLAR_DIR / "data_layers" / "annual_flux" / cat / f"{aid}_annual_flux.tif"

    if not bi_file.exists() or not rgb_file.exists():
        return None

    try:
        with open(bi_file, "r", encoding="utf-8") as f:
            insights = json.load(f)

        solar_pot = insights.get("solarPotential", {})
        existing_panels = solar_pot.get("solarPanels", [])
        segs = solar_pot.get("roofSegmentStats", [])
        bbox = insights.get("boundingBox", {})

        ph_m = solar_pot.get("panelHeightMeters", 1.722)
        pw_m = solar_pot.get("panelWidthMeters", 1.134)

        with rasterio.open(rgb_file) as src:
            res_m = abs(src.transform[0])
            ph_px = ph_m / res_m
            pw_px = pw_m / res_m
            width, height = src.width, src.height

            trans = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)

            # Pixel bounding box of the building to prevent leaking onto adjacent buildings
            if bbox and "sw" in bbox and "ne" in bbox:
                sw_x, sw_y = trans.transform(bbox["sw"]["longitude"], bbox["sw"]["latitude"])
                ne_x, ne_y = trans.transform(bbox["ne"]["longitude"], bbox["ne"]["latitude"])
                py_sw, px_sw = src.index(sw_x, sw_y)
                py_ne, px_ne = src.index(ne_x, ne_y)
                min_bx = max(0, min(px_sw, px_ne))
                max_bx = min(width - 1, max(px_sw, px_ne))
                min_by = max(0, min(py_sw, py_ne))
                max_by = min(height - 1, max(py_sw, py_ne))
            else:
                min_bx, max_bx = 0, width - 1
                min_by, max_by = 0, height - 1

            coords = []
            for p in existing_panels:
                ux, uy = trans.transform(p["center"]["longitude"], p["center"]["latitude"])
                py, px = src.index(ux, uy)
                if 0 <= px < width and 0 <= py < height:
                    coords.append(np.array([px, py]))

            coords = np.array(coords) if len(coords) > 0 else np.empty((0, 2))

            # Load roof mask to enforce structural boundary
            if mask_file.exists():
                with rasterio.open(mask_file) as src_m:
                    raw_mask = src_m.read(1) > 0
            else:
                raw_mask = np.ones((height, width), dtype=bool)

            flux_arr = None
            if flux_file.exists():
                with rasterio.open(flux_file) as src_f:
                    flux_arr = src_f.read(1).astype(float)

            # Build strictly bounded building roof mask
            bld_mask = np.zeros_like(raw_mask, dtype=bool)
            bld_mask[min_by:max_by+1, min_bx:max_bx+1] = raw_mask[min_by:max_by+1, min_bx:max_bx+1]

            # Fire safety setback from edges (2 px ~ 0.5m)
            eroded_bld_mask = binary_erosion(bld_mask, iterations=2)
            if eroded_bld_mask.sum() == 0:
                eroded_bld_mask = bld_mask

            # Occupied area of existing baseline panels
            occupied = np.zeros_like(raw_mask, dtype=bool)
            for px, py in coords:
                if 0 <= py < height and 0 <= px < width:
                    occupied[max(0, int(py - ph_px/2)):min(height, int(py + ph_px/2 + 1)),
                             max(0, int(px - pw_px/2)):min(width, int(px + pw_px/2 + 1))] = True

            usable_mask = eroded_bld_mask & (~occupied)

            # Azimuth and orientation (dominant facet)
            az_deg = 180.0
            if len(segs) > 0:
                largest_seg = max(segs, key=lambda s: s.get("stats", {}).get("areaMeters2", 0.0), default=segs[0])
                az_deg = largest_seg.get("azimuthDegrees", 180.0)
            az_rad = math.radians(az_deg)
            u_ridge = np.array([math.cos(az_rad), math.sin(az_rad)])
            u_slope = np.array([-math.sin(az_rad), math.cos(az_rad)])

            col_step = pw_px * 1.05
            row_step = ph_px * 1.05
            l_vec = u_slope * (ph_px / 2.0)
            w_vec = u_ridge * (pw_px / 2.0)

            # Candidate infill panels placement
            infill_coords = []
            if infill_target_panels > 0 and usable_mask.sum() > 0:
                anchor = coords.mean(axis=0) if len(coords) > 0 else np.array([(min_bx+max_bx)/2, (min_by+max_by)/2])
                diag = math.sqrt((max_bx - min_bx)**2 + (max_by - min_by)**2)
                n_col = int(diag / col_step) + 8
                n_row = int(diag / row_step) + 8

                ii, jj = np.meshgrid(np.arange(-n_col, n_col + 1), np.arange(-n_row, n_row + 1))
                grid_cand = anchor + ii.ravel()[:, None] * (u_ridge * col_step) + jj.ravel()[:, None] * (u_slope * row_step)

                in_bounds = (
                    (grid_cand[:, 0] >= min_bx + 1) & (grid_cand[:, 0] <= max_bx - 1) &
                    (grid_cand[:, 1] >= min_by + 1) & (grid_cand[:, 1] <= max_by - 1)
                )
                cand_in = grid_cand[in_bounds]

                tree_exist = cKDTree(coords) if len(coords) > 0 else None
                min_clearance = min(ph_px, pw_px) * 0.80

                valid_infill = []
                flux_scores = []
                for pt in cand_in:
                    cx, cy = int(pt[0]), int(pt[1])
                    if not (0 <= cx < width and 0 <= cy < height and usable_mask[cy, cx]):
                        continue
                    if tree_exist is not None:
                        d_exist, _ = tree_exist.query(pt)
                        if d_exist < min_clearance:
                            continue
                    valid_infill.append(pt)
                    flux_val = flux_arr[cy, cx] if flux_arr is not None else 1000.0
                    flux_scores.append(flux_val)

                valid_infill = np.array(valid_infill) if len(valid_infill) > 0 else np.empty((0, 2))
                flux_scores = np.array(flux_scores) if len(flux_scores) > 0 else np.empty(0)

                if len(valid_infill) > 0:
                    tree_cand = cKDTree(valid_infill)
                    densities = np.array([len(tree_cand.query_ball_point(pt, r=row_step * 2.5)) for pt in valid_infill])
                    # Rank by cluster density (contiguous arrays) and solar irradiance
                    scores = densities * 1000.0 + flux_scores
                    top_idx = np.argsort(scores)[::-1][:infill_target_panels]
                    infill_coords = valid_infill[top_idx]

            # Render Matplotlib Figure
            rgb_arr = src.read([1, 2, 3]).transpose(1, 2, 0)
            fig, ax = plt.subplots(figsize=(10, 10), dpi=200)
            ax.imshow(rgb_arr)

            def draw_poly(center_pt):
                # Standard blue Google Solar API panel style (SAME COLOR AS REQUESTED)
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
