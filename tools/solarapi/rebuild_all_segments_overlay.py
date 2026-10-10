"""
rebuild_all_segments_overlay.py
===============================
Membangun ulang seluruh gambar _segments_overlay.png untuk 1.100 titik di:
data/processed/renders_full/segments/
menggunakan algoritma autentik POW 100:
- Colormap tab20
- Klastering BFS 40px + ConvexHull per klaster bidang
- Titik panel fotovoltaik (marker='s', markersize=2)
- Kotak merah putus-putus untuk segmen yang dieliminasi (0 panel)
- Circular badge nomor segmen S0, S1, S2, ...
"""

import os
import sys
import json
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
OUT_SEG_DIR = PROJECT_ROOT / "data" / "processed" / "renders_full" / "segments"
OUT_SEG_DIR.mkdir(parents=True, exist_ok=True)


def render_single_segment(row_dict: dict) -> dict:
    aid = str(row_dict.get("asset_id", "")).strip().lower()
    cat = str(row_dict.get("category", "")).strip().lower()

    out_file = OUT_SEG_DIR / f"{aid}_segments_overlay.png"

    # Cari file building insights dan RGB GeoTIFF
    folder_candidates = [cat, cat.replace("_", "")]
    if "mrt" in aid:
        folder_candidates.extend(["mrt", "mrt_lrt"])
    if "lrt" in aid:
        folder_candidates.extend(["lrt", "mrt_lrt"])

    bi_candidates = [RAW_SOLAR_DIR / "building_insights" / c / f"{aid}_insights.json" for c in folder_candidates]
    bi_path = next((p for p in bi_candidates if p.exists()), None)

    rgb_candidates = [RAW_SOLAR_DIR / "data_layers" / "rgb" / c / f"{aid}_rgb.tif" for c in folder_candidates]
    rgb_path = next((p for p in rgb_candidates if p.exists()), None)

    if not bi_path or not rgb_path:
        return {"asset_id": aid, "status": "SKIPPED_NO_INPUT"}

    try:
        with open(bi_path, "r", encoding="utf-8") as f:
            bi_data = json.load(f)

        sp = bi_data.get("solarPotential", {})
        panels = sp.get("solarPanels", [])
        segs = sp.get("roofSegmentStats", [])

        with rasterio.open(rgb_path) as src:
            rgb_raw = src.read([1, 2, 3])
            rgb_arr = np.transpose(rgb_raw, (1, 2, 0))

            transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
            fig, ax = plt.subplots(figsize=(8, 8), dpi=180)
            ax.imshow(rgb_arr)

            cmap = plt.colormaps['tab20']
            seg_points = {i: [] for i in range(len(segs))}
            for p in panels:
                s_idx = p.get("segmentIndex", 0)
                ux, uy = transformer.transform(p["center"]["longitude"], p["center"]["latitude"])
                py, px = src.index(ux, uy)
                if 0 <= px < src.width and 0 <= py < src.height:
                    if s_idx in seg_points:
                        seg_points[s_idx].append((px, py))

            badge_coords = []
            for s_idx, pts in seg_points.items():
                if not pts:
                    continue
                color = cmap(s_idx % 20)

                # Sub-clustering BFS 40px
                if len(pts) >= 3:
                    sub_clusters = []
                    visited = [False] * len(pts)
                    for i in range(len(pts)):
                        if visited[i]:
                            continue
                        c_pts = [pts[i]]
                        visited[i] = True
                        q = [i]
                        while q:
                            curr = q.pop(0)
                            cx, cy = pts[curr]
                            for j in range(len(pts)):
                                if not visited[j]:
                                    nx, ny = pts[j]
                                    if (cx - nx)**2 + (cy - ny)**2 <= 40**2:
                                        visited[j] = True
                                        c_pts.append(pts[j])
                                        q.append(j)
                        sub_clusters.append(c_pts)

                    for cl_pts in sub_clusters:
                        if len(cl_pts) >= 3:
                            cl_arr = np.array(cl_pts)
                            try:
                                hull = ConvexHull(cl_arr)
                                hull_pts = cl_arr[hull.vertices]
                                poly = Polygon(
                                    hull_pts, closed=True,
                                    facecolor=color, edgecolor=color,
                                    alpha=0.42, linewidth=1.8
                                )
                                ax.add_patch(poly)
                            except Exception:
                                pass

                # Titik panel fotovoltaik
                for px, py in pts:
                    ax.plot(px, py, marker="s", markersize=2, color=color, alpha=0.85)

                pts_in = [p for p in pts if 0 <= p[0] < src.width and 0 <= p[1] < src.height]
                if pts_in:
                    pts_in_arr = np.array(pts_in)
                    cx = float(np.median(pts_in_arr[:, 0]))
                    cy = float(np.median(pts_in_arr[:, 1]))
                    badge_coords.append((s_idx, cx, cy, color))

            # Kotak merah putus-putus untuk segmen 0 panel
            for s_idx, s in enumerate(segs):
                if s_idx in seg_points and len(seg_points[s_idx]) > 0:
                    continue
                box = s.get("boundingBox", {})
                if box and "sw" in box and "ne" in box and transformer:
                    try:
                        sw_ux, sw_uy = transformer.transform(box["sw"]["longitude"], box["sw"]["latitude"])
                        ne_ux, ne_uy = transformer.transform(box["ne"]["longitude"], box["ne"]["latitude"])
                        sw_py, sw_px = src.index(sw_ux, sw_uy)
                        ne_py, ne_px = src.index(ne_ux, ne_uy)
                        min_x = min(sw_px, ne_px)
                        max_x = max(sw_px, ne_px)
                        min_y = min(sw_py, ne_py)
                        max_y = max(sw_py, ne_py)
                        cx = (min_x + max_x) / 2.0
                        cy = (min_y + max_y) / 2.0
                        if 0 <= cx < src.width and 0 <= cy < src.height:
                            rect_w = max(abs(max_x - min_x), 12)
                            rect_h = max(abs(max_y - min_y), 12)
                            rect = plt.Rectangle(
                                (min_x, min_y), rect_w, rect_h,
                                edgecolor="#EF4444", facecolor="#EF4444",
                                alpha=0.25, linestyle="--", linewidth=1.2
                            )
                            ax.add_patch(rect)
                            badge_coords.append((s_idx, cx, cy, "#EF4444"))
                    except Exception:
                        pass

            # Badge penomoran lingkaran S0, S1, S2, ...
            for s_idx, cx, cy, col in badge_coords:
                ax.text(
                    cx, cy, f"S{s_idx}",
                    fontsize=7, fontweight="bold", color="white",
                    ha="center", va="center",
                    bbox=dict(boxstyle="circle,pad=0.25", facecolor="#0F172A", edgecolor=col, linewidth=1.2, alpha=0.92)
                )

            ax.set_xlim(0, src.width)
            ax.set_ylim(src.height, 0)
            ax.axis("off")
            fig.patch.set_facecolor("#0E1117")
            fig.savefig(out_file, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
            plt.close(fig)

        return {"asset_id": aid, "status": "RENDERED"}
    except Exception as e:
        plt.close("all")
        return {"asset_id": aid, "status": f"ERROR: {e}"}


def main():
    print("=" * 80)
    print("  REBUILD AUTENTIK SEGMENTS OVERLAY (PENOMORAN BADGE S0, S1, S2, ...)")
    print("=" * 80)

    summary_file = PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_kumulatif_summary.parquet"
    df = pd.read_parquet(summary_file)

    # Hanya proses 1.100 titik yang memiliki data layers
    df_valid = df[df["path_rgb_geotiff"].notna()].copy()
    print(f"[*] Total titik yang akan dibangun segmennya: {len(df_valid)} titik")

    # Identifikasi 101 titik pilot yang sudah direstore dari previews agar tidak perlu render ulang jika sudah ada
    preview_dir = PROJECT_ROOT / "data" / "processed" / "previews"
    existing_previews = set(f.stem.replace("_segments_overlay", "").lower() for f in preview_dir.glob("*_segments_overlay.png"))
    print(f"[*] Titik pilot original terdeteksi: {len(existing_previews)} titik")

    rows_to_process = []
    for _, r in df_valid.iterrows():
        aid = str(r["asset_id"]).strip().lower()
        # Jika bukan pilot yang sudah ada dari previews, masukkan antrean render
        if aid not in existing_previews:
            rows_to_process.append(r.to_dict())

    print(f"[*] Titik yang memerlukan rendering ulang autentik: {len(rows_to_process)} titik")

    t0 = time.time()
    rendered_cnt = 0
    err_cnt = 0

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(render_single_segment, row): row["asset_id"] for row in rows_to_process}
        for i, future in enumerate(as_completed(futures), 1):
            res = future.result()
            if res["status"] == "RENDERED":
                rendered_cnt += 1
            else:
                err_cnt += 1

            if i % 100 == 0 or i == len(rows_to_process):
                elapsed = time.time() - t0
                rate = i / elapsed if elapsed > 0 else 0
                print(f"[{i:04d}/{len(rows_to_process):04d}] Selesai {i} titik ({rate:.1f} titik/detik)")

    print("=" * 80)
    print(f"  RINGKASAN REBUILD SEGMEN:")
    print(f"  * Berhasil dirender ulang : {rendered_cnt} titik")
    print(f"  * Original POW 100 pilot  : {len(existing_previews)} titik")
    print(f"  * Total lengkap di disk   : {rendered_cnt + len(existing_previews)} / {len(df_valid)} titik")
    print(f"  * Error                   : {err_cnt}")
    print(f"  * Waktu eksekusi total    : {time.time() - t0:.2f} detik")
    print("=" * 80)


if __name__ == "__main__":
    main()
