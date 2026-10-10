#!/usr/bin/env python3
"""
generate_renders_full_batch.py
==============================
Batch Image Processor untuk menghasilkan visualisasi fotovoltaik lengkap 7 layer
ke direktori lokal: data/processed/renders_full/

7 Lapisan Visual:
1. rgb      -> Citra Satelit Aerial Asli (0.25 m/px)
2. panels   -> Tata Letak Panel Surya Baseline Google (#2563EB)
3. dsm      -> Model Ketinggian 3D (Colormap Terrain + Colorbar)
4. mask     -> Segmentasi Tapak Atap Biner (Roof vs Off-roof)
5. flux     -> Heatmap Radiasi Surya Tahunan (Colormap Plasma + Colorbar)
6. segments -> Poligon Bidang Kemiringan 3D RANSAC
7. infill   -> Simulasi Rekayasa Celah Atap Skenario Penuh (SNI/NFPA)

Kepatuhan Aturan:
- Folder data/processed/renders_full/ terdaftar di .gitignore (Zero Git Bloat).
- Idempotent: Melewatkan file yang sudah ada di disk.
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull
from scipy.ndimage import binary_erosion

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CALC_DIR = PROCESSED_DIR / "calculations"
RENDERS_DIR = PROCESSED_DIR / "renders_full"

LAYERS = ["rgb", "panels", "dsm", "mask", "flux", "segments", "infill"]
for l in LAYERS:
    (RENDERS_DIR / l).mkdir(parents=True, exist_ok=True)


def render_single_asset(row_dict: dict) -> dict:
    aid = str(row_dict.get("asset_id", "")).strip().lower()
    cat = str(row_dict.get("category", "")).strip().lower()
    nm = str(row_dict.get("asset_name", ""))

    out_files = {
        "rgb": RENDERS_DIR / "rgb" / f"{aid}_rgb.png",
        "panels": RENDERS_DIR / "panels" / f"{aid}_panels_overlay.png",
        "dsm": RENDERS_DIR / "dsm" / f"{aid}_dsm_elevation.png",
        "mask": RENDERS_DIR / "mask" / f"{aid}_roof_mask.png",
        "flux": RENDERS_DIR / "flux" / f"{aid}_flux_heatmap.png",
        "segments": RENDERS_DIR / "segments" / f"{aid}_segments_overlay.png",
        "infill": RENDERS_DIR / "infill" / f"{aid}_infill_panels_overlay.png",
    }

    # Jika semua sudah ada dan valid, lewati
    if all(p.exists() and p.stat().st_size > 100 for p in out_files.values()):
        return {"asset_id": aid, "status": "CACHED", "count": len(out_files)}

    # Path sumber file mentah
    bi_candidates = [
        RAW_SOLAR_DIR / "building_insights" / cat / f"{aid}_insights.json",
        RAW_SOLAR_DIR / "building_insights" / cat.replace("_", "") / f"{aid}_insights.json",
    ]
    bi_path = next((p for p in bi_candidates if p.exists()), None)

    rgb_candidates = [
        RAW_SOLAR_DIR / "data_layers" / "rgb" / cat / f"{aid}_rgb.tif",
        RAW_SOLAR_DIR / "data_layers" / "rgb" / cat.replace("_", "") / f"{aid}_rgb.tif",
    ]
    rgb_path = next((p for p in rgb_candidates if p.exists()), None)

    dsm_candidates = [
        RAW_SOLAR_DIR / "data_layers" / "dsm" / cat / f"{aid}_dsm.tif",
        RAW_SOLAR_DIR / "data_layers" / "dsm" / cat.replace("_", "") / f"{aid}_dsm.tif",
    ]
    dsm_path = next((p for p in dsm_candidates if p.exists()), None)

    mask_candidates = [
        RAW_SOLAR_DIR / "data_layers" / "mask" / cat / f"{aid}_mask.tif",
        RAW_SOLAR_DIR / "data_layers" / "mask" / cat.replace("_", "") / f"{aid}_mask.tif",
    ]
    mask_path = next((p for p in mask_candidates if p.exists()), None)

    flux_candidates = [
        RAW_SOLAR_DIR / "data_layers" / "annual_flux" / cat / f"{aid}_annual_flux.tif",
        RAW_SOLAR_DIR / "data_layers" / "annual_flux" / cat.replace("_", "") / f"{aid}_annual_flux.tif",
    ]
    flux_path = next((p for p in flux_candidates if p.exists()), None)

    if not bi_path or not rgb_path:
        return {"asset_id": aid, "status": "SKIPPED_NO_INPUT", "count": 0}

    try:
        with open(bi_path, "r", encoding="utf-8") as f:
            bi_data = json.load(f)
    except Exception:
        return {"asset_id": aid, "status": "ERROR_JSON", "count": 0}

    sp = bi_data.get("solarPotential", {})
    panels = sp.get("solarPanels", [])
    segs = sp.get("roofSegmentStats", [])
    pw_m = sp.get("panelWidthMeters", 1.045)
    ph_m = sp.get("panelHeightMeters", 1.879)

    rendered = 0

    # 1. RGB
    rgb_arr = None
    if not out_files["rgb"].exists() or out_files["rgb"].stat().st_size <= 100:
        try:
            with rasterio.open(rgb_path) as src:
                rgb_raw = src.read([1, 2, 3])
                rgb_arr = np.transpose(rgb_raw, (1, 2, 0))
                im = Image.fromarray(rgb_arr)
                im.save(out_files["rgb"], "PNG")
                rendered += 1
        except Exception:
            pass
    else:
        # Load rgb_arr if needed for panels/segments
        try:
            with rasterio.open(rgb_path) as src:
                rgb_raw = src.read([1, 2, 3])
                rgb_arr = np.transpose(rgb_raw, (1, 2, 0))
        except Exception:
            pass

    # 2. Panels Overlay
    if rgb_arr is not None and (not out_files["panels"].exists() or out_files["panels"].stat().st_size <= 100):
        try:
            with rasterio.open(rgb_path) as src:
                transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                pw_px = (pw_m / 0.25) * 0.88
                ph_px = (ph_m / 0.25) * 0.88

                fig, ax = plt.subplots(figsize=(7, 7), dpi=140)
                ax.imshow(rgb_arr)

                for p in panels:
                    lon = p["center"]["longitude"]
                    lat = p["center"]["latitude"]
                    ux, uy = transformer.transform(lon, lat)
                    py, px = src.index(ux, uy)
                    if not (0 <= px < src.width and 0 <= py < src.height):
                        continue

                    seg_idx = p.get("segmentIndex", 0)
                    seg = segs[seg_idx] if seg_idx < len(segs) else {}
                    az_deg = seg.get("azimuthDegrees", 0.0)

                    az_rad = math.radians(az_deg)
                    u_ridge = np.array([math.cos(az_rad), math.sin(az_rad)])
                    u_slope = np.array([-math.sin(az_rad), math.cos(az_rad)])

                    if p.get("orientation") == "LANDSCAPE":
                        l_vec = u_ridge * (ph_px / 2.0)
                        w_vec = u_slope * (pw_px / 2.0)
                    else:
                        l_vec = u_slope * (ph_px / 2.0)
                        w_vec = u_ridge * (pw_px / 2.0)

                    c = np.array([px, py])
                    p1 = c + l_vec + w_vec
                    p2 = c + l_vec - w_vec
                    p3 = c - l_vec - w_vec
                    p4 = c - l_vec + w_vec

                    poly = Polygon([p1, p2, p3, p4], closed=True, facecolor="#2563EB", edgecolor="#93C5FD", linewidth=0.5, alpha=0.88)
                    ax.add_patch(poly)

                ax.set_xlim(0, src.width)
                ax.set_ylim(src.height, 0)
                ax.axis("off")
                fig.patch.set_facecolor("#0E1117")
                fig.savefig(out_files["panels"], facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
                plt.close(fig)
                rendered += 1
        except Exception:
            plt.close("all")

    # 3. DSM 3D Elevation
    if dsm_path and dsm_path.exists() and (not out_files["dsm"].exists() or out_files["dsm"].stat().st_size <= 100):
        try:
            with rasterio.open(dsm_path) as src:
                dsm = src.read(1).astype(float)
                dsm[dsm < -100] = np.nan
                fig, ax = plt.subplots(figsize=(6, 6), dpi=140)
                im = ax.imshow(dsm, cmap="terrain")
                cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cbar.set_label("Elevasi Ketinggian Atap (Meter)", fontsize=8)
                ax.set_title(f"DSM Elevasi 3D: {nm[:32]}", fontsize=10, fontweight="bold")
                ax.axis("off")
                fig.tight_layout()
                fig.savefig(out_files["dsm"], bbox_inches="tight")
                plt.close(fig)
                rendered += 1
        except Exception:
            plt.close("all")

    # 4. Roof Mask
    if mask_path and mask_path.exists() and (not out_files["mask"].exists() or out_files["mask"].stat().st_size <= 100):
        try:
            with rasterio.open(mask_path) as src:
                mask = src.read(1)
                fig, ax = plt.subplots(figsize=(6, 6), dpi=140)
                cmap = plt.matplotlib.colors.ListedColormap(["#111927", "#00E676"])
                im = ax.imshow(mask, cmap=cmap)
                ax.set_title(f"Roof Mask Segmentasi: {nm[:32]}", fontsize=10, fontweight="bold")
                ax.axis("off")
                fig.tight_layout()
                fig.savefig(out_files["mask"], bbox_inches="tight")
                plt.close(fig)
                rendered += 1
        except Exception:
            plt.close("all")

    # 5. Annual Flux Heatmap
    if flux_path and flux_path.exists() and (not out_files["flux"].exists() or out_files["flux"].stat().st_size <= 100):
        try:
            with rasterio.open(flux_path) as src:
                flux_arr = src.read(1).astype(float)
                flux_arr[flux_arr <= 0] = np.nan
                fig, ax = plt.subplots(figsize=(6, 6), dpi=140)
                cmap = plt.get_cmap("plasma")
                cmap.set_bad(color="black")
                im = ax.imshow(flux_arr, cmap=cmap)
                cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cbar.set_label("Iradiasi Surya (kWh/kW/tahun)", fontsize=8)
                ax.set_title(f"Annual Solar Flux: {nm[:32]}", fontsize=10, fontweight="bold")
                ax.axis("off")
                fig.tight_layout()
                fig.savefig(out_files["flux"], bbox_inches="tight")
                plt.close(fig)
                rendered += 1
        except Exception:
            plt.close("all")

    # 6. Segments Overlay
    if rgb_arr is not None and (not out_files["segments"].exists() or out_files["segments"].stat().st_size <= 100):
        try:
            with rasterio.open(rgb_path) as src:
                transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                fig, ax = plt.subplots(figsize=(7, 7), dpi=140)
                ax.imshow(rgb_arr)

                seg_colors = ["#EF4444", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#14B8A6", "#F97316"]
                for s_idx, seg in enumerate(segs):
                    seg_panels = [p for p in panels if p.get("segmentIndex") == s_idx]
                    if not seg_panels:
                        continue
                    pts = []
                    for p in seg_panels:
                        lon = p["center"]["longitude"]
                        lat = p["center"]["latitude"]
                        ux, uy = transformer.transform(lon, lat)
                        py, px = src.index(ux, uy)
                        if 0 <= px < src.width and 0 <= py < src.height:
                            pts.append([px, py])
                    if len(pts) >= 3:
                        try:
                            hull = ConvexHull(pts)
                            hull_pts = [pts[i] for i in hull.vertices]
                            col = seg_colors[s_idx % len(seg_colors)]
                            poly = Polygon(hull_pts, closed=True, facecolor=col, edgecolor="#FFFFFF", linewidth=1.5, alpha=0.45)
                            ax.add_patch(poly)
                        except Exception:
                            pass

                ax.set_xlim(0, src.width)
                ax.set_ylim(src.height, 0)
                ax.axis("off")
                fig.patch.set_facecolor("#0E1117")
                fig.savefig(out_files["segments"], facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
                plt.close(fig)
                rendered += 1
        except Exception:
            plt.close("all")

    # 7. Infill Overlay
    if rgb_arr is not None and (not out_files["infill"].exists() or out_files["infill"].stat().st_size <= 100):
        try:
            with rasterio.open(rgb_path) as src:
                transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                pw_px = (pw_m / 0.25) * 0.88
                ph_px = (ph_m / 0.25) * 0.88

                fig, ax = plt.subplots(figsize=(7, 7), dpi=140)
                ax.imshow(rgb_arr)

                # Baseline panels
                for p in panels:
                    lon = p["center"]["longitude"]
                    lat = p["center"]["latitude"]
                    ux, uy = transformer.transform(lon, lat)
                    py, px = src.index(ux, uy)
                    if not (0 <= px < src.width and 0 <= py < src.height):
                        continue
                    seg_idx = p.get("segmentIndex", 0)
                    seg = segs[seg_idx] if seg_idx < len(segs) else {}
                    az_deg = seg.get("azimuthDegrees", 0.0)
                    az_rad = math.radians(az_deg)
                    u_ridge = np.array([math.cos(az_rad), math.sin(az_rad)])
                    u_slope = np.array([-math.sin(az_rad), math.cos(az_rad)])
                    if p.get("orientation") == "LANDSCAPE":
                        l_vec = u_ridge * (ph_px / 2.0)
                        w_vec = u_slope * (pw_px / 2.0)
                    else:
                        l_vec = u_slope * (ph_px / 2.0)
                        w_vec = u_ridge * (pw_px / 2.0)
                    c = np.array([px, py])
                    p1, p2, p3, p4 = c + l_vec + w_vec, c + l_vec - w_vec, c - l_vec - w_vec, c - l_vec + w_vec
                    poly = Polygon([p1, p2, p3, p4], closed=True, facecolor="#2563EB", edgecolor="#93C5FD", linewidth=0.5, alpha=0.88)
                    ax.add_patch(poly)

                # Simulated Infill Panels on Usable Roof Mask
                if mask_path and mask_path.exists():
                    with rasterio.open(mask_path) as src_m:
                        raw_mask = src_m.read(1) > 0
                        eroded_mask = binary_erosion(raw_mask, iterations=2)
                        
                        # Mark occupied by existing panels
                        occupied = np.zeros_like(raw_mask, dtype=bool)
                        for p in panels:
                            lon = p["center"]["longitude"]
                            lat = p["center"]["latitude"]
                            ux, uy = transformer.transform(lon, lat)
                            py, px = src.index(ux, uy)
                            if 0 <= py < src.height and 0 <= px < src.width:
                                occupied[max(0, int(py - ph_px/2)):min(src.height, int(py + ph_px/2 + 1)),
                                         max(0, int(px - pw_px/2)):min(src.width, int(px + pw_px/2 + 1))] = True
                        
                        usable_infill = eroded_mask & (~occupied)
                        ys, xs = np.where(usable_infill)
                        
                        # Sample grid of infill panels (max 150 infill panels for visual realism)
                        step_y = max(int(ph_px * 1.2), 3)
                        step_x = max(int(pw_px * 1.2), 3)
                        sampled_pts = []
                        for y in range(0, src.height, step_y):
                            for x in range(0, src.width, step_x):
                                if 0 <= y < src.height and 0 <= x < src.width and usable_infill[y, x]:
                                    sampled_pts.append((x, y))
                                    if len(sampled_pts) >= 120:
                                        break
                            if len(sampled_pts) >= 120:
                                break
                        
                        az_deg = segs[0].get("azimuthDegrees", 180.0) if segs else 180.0
                        az_rad = math.radians(az_deg)
                        u_ridge = np.array([math.cos(az_rad), math.sin(az_rad)])
                        u_slope = np.array([-math.sin(az_rad), math.cos(az_rad)])
                        l_vec = u_slope * (ph_px / 2.0)
                        w_vec = u_ridge * (pw_px / 2.0)

                        for px, py in sampled_pts:
                            c = np.array([px, py])
                            p1, p2, p3, p4 = c + l_vec + w_vec, c + l_vec - w_vec, c - l_vec - w_vec, c - l_vec + w_vec
                            # Infill panels slightly brighter edge to indicate infill expansion
                            poly_inf = Polygon([p1, p2, p3, p4], closed=True, facecolor="#1D4ED8", edgecolor="#60A5FA", linewidth=0.6, alpha=0.85)
                            ax.add_patch(poly_inf)

                ax.set_xlim(0, src.width)
                ax.set_ylim(src.height, 0)
                ax.axis("off")
                fig.patch.set_facecolor("#0E1117")
                fig.savefig(out_files["infill"], facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
                plt.close(fig)
                rendered += 1
        except Exception:
            plt.close("all")

    return {"asset_id": aid, "status": "RENDERED", "count": rendered}


def run_batch_renders(limit: int = None, workers: int = 4):
    print("=" * 80)
    print("  BATCH IMAGE PROCESSOR: 7-LAYER RENDERS (RENDERS_FULL + INFILL)")
    print("=" * 80)

    summary_csv = CALC_DIR / "pow_solar_kumulatif_summary.csv"
    if not summary_csv.exists():
        raise FileNotFoundError(f"File {summary_csv} tidak ditemukan.")

    df = pd.read_csv(summary_csv)
    # Filter hanya titik yang memiliki GeoTIFF di disk lokal
    df_valid = df[df["path_rgb_geotiff"].notna() & (df["path_rgb_geotiff"] != "")].copy()

    if limit and limit > 0:
        df_valid = df_valid.head(limit)

    total_tasks = len(df_valid)
    print(f"[*] Total aset yang akan di-render: {total_tasks} titik")
    print(f"[*] Jumlah worker multiprocessing : {workers} cores")
    print(f"[*] Output directory              : {RENDERS_DIR}")
    print("-" * 80)

    records = df_valid.to_dict(orient="records")
    success_cnt = 0
    cached_cnt = 0
    err_cnt = 0

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(render_single_asset, r): r["asset_id"] for r in records}
        for i, fut in enumerate(as_completed(futures)):
            aid = futures[fut]
            try:
                res = fut.result()
                st = res["status"]
                cnt = res.get("count", 0)
                if st == "CACHED":
                    cached_cnt += 1
                    if (i + 1) % 50 == 0 or (i + 1) == total_tasks:
                        print(f"[{i+1:04d}/{total_tasks:04d}] [CACHED] {aid}")
                elif st == "RENDERED":
                    success_cnt += 1
                    if (i + 1) % 25 == 0 or (i + 1) == total_tasks:
                        print(f"[{i+1:04d}/{total_tasks:04d}] [RENDERED] {aid} -> {cnt} layer baru")
                else:
                    err_cnt += 1
                    print(f"[{i+1:04d}/{total_tasks:04d}] [{st}] {aid}")
            except Exception as e:
                err_cnt += 1
                print(f"[{i+1:04d}/{total_tasks:04d}] [FAIL] {aid}: {e}")

    print("=" * 80)
    print("  RINGKASAN RENDERING FULL 7 LAYERS:")
    print(f"  * Total Diproses  : {total_tasks} titik")
    print(f"  * Berhasil Render : {success_cnt} titik")
    print(f"  * Sudah Ada (Skip): {cached_cnt} titik")
    print(f"  * Gagal / Dilewati: {err_cnt} titik")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Full 7-layer Batch Renderer to renders_full")
    parser.add_argument("--limit", type=int, default=None, help="Batas titik untuk pengujian")
    parser.add_argument("--workers", type=int, default=4, help="Jumlah worker multiprocessing")
    args = parser.parse_args()
    run_batch_renders(limit=args.limit, workers=args.workers)


if __name__ == "__main__":
    main()
