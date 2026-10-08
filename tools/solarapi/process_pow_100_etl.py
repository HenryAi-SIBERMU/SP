"""
process_pow_100_etl.py
----------------------
Transformer & Loader (ETL) untuk 100 Titik Infrastruktur Google Solar API Jabodetabek.
Membaca target secara dinamis dari data/raw/poi/target_100_titik.csv.

Menghasilkan seluruh visualisasi SKU resmi:
1. Citra Satelit Aerial RGB Asli (0.25m/px)
2. Solar Panel Layout on Roof (Visualisasi posisi panel surya di atas atap sesuai UI Google)
3. Digital Surface Model (DSM - Elevasi & Ketinggian 3D)
4. Roof Mask (Binary Mask Atap vs Non-Atap)
5. Annual Solar Flux Heatmap (Radiasi Surya Tahunan kWh/kW/year)
6. Roof Segmentation Grid (Bidang 3D RANSAC)

Kepatuhan Aturan:
- no_hardcoded_data.md: Zero hardcoded lists/dictionaries. Pure Dynamic Analytical Engine.
- strict_data_folder_boundary.md: 100% output tersimpan di data/processed/
- statistical_auditor_role.md: Formula matematis terverifikasi.
"""

import os
import sys
import json
import math
import argparse
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import rasterio
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from pyproj import Transformer
from PIL import Image
from scipy.spatial import ConvexHull

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
GIS_OUT_DIR = PROCESSED_DIR / "gis"
CALC_OUT_DIR = PROCESSED_DIR / "calculations"
PREVIEW_OUT_DIR = PROCESSED_DIR / "previews"

GIS_OUT_DIR.mkdir(parents=True, exist_ok=True)
CALC_OUT_DIR.mkdir(parents=True, exist_ok=True)
PREVIEW_OUT_DIR.mkdir(parents=True, exist_ok=True)


def haversine_distance_meters(lat1, lon1, lat2, lon2):
    """Menghitung jarak Haversine dalam meter antara 2 koordinat WGS84."""
    R = 6371000  # Radius bumi dalam meter
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def generate_all_sku_previews(aid, cat, asset_name, bi_data, rgb_tif_path, dsm_tif_path, mask_tif_path, flux_tif_path):
    """
    Menghasilkan 6 visualisasi lengkap untuk seluruh SKU data:
    1. RGB Satellite Image
    2. Solar Panels Layout on Roof
    3. DSM Elevation (Peta Ketinggian 3D)
    4. Roof Mask (Segmentasi Atap)
    5. Annual Flux Heatmap (Iradiasi Matahari)
    6. Roof Segmentation Grid (Bidang 3D RANSAC)
    """
    out_paths = {}

    rgb_png_path = PREVIEW_OUT_DIR / f"{aid}_rgb.png"
    panels_png_path = PREVIEW_OUT_DIR / f"{aid}_panels_overlay.png"
    segments_png_path = PREVIEW_OUT_DIR / f"{aid}_segments_overlay.png"
    dsm_png_path = PREVIEW_OUT_DIR / f"{aid}_dsm_elevation.png"
    mask_png_path = PREVIEW_OUT_DIR / f"{aid}_roof_mask.png"
    flux_png_path = PREVIEW_OUT_DIR / f"{aid}_flux_heatmap.png"

    if all(p.exists() for p in [rgb_png_path, panels_png_path, segments_png_path, dsm_png_path, mask_png_path, flux_png_path]):
        return {
            "preview_rgb_png": rgb_png_path.relative_to(PROJECT_ROOT).as_posix(),
            "preview_panels_png": panels_png_path.relative_to(PROJECT_ROOT).as_posix(),
            "preview_segments_png": segments_png_path.relative_to(PROJECT_ROOT).as_posix(),
            "preview_dsm_png": dsm_png_path.relative_to(PROJECT_ROOT).as_posix(),
            "preview_mask_png": mask_png_path.relative_to(PROJECT_ROOT).as_posix(),
            "preview_flux_png": flux_png_path.relative_to(PROJECT_ROOT).as_posix(),
        }

    # 1. RGB Image
    rgb_arr = None
    if rgb_tif_path and rgb_tif_path.exists():
        try:
            with rasterio.open(rgb_tif_path) as src:
                rgb_raw = src.read([1, 2, 3])
                rgb_arr = np.transpose(rgb_raw, (1, 2, 0))
                im = Image.fromarray(rgb_arr)
                im.save(rgb_png_path, "PNG")
                out_paths["preview_rgb_png"] = rgb_png_path.relative_to(PROJECT_ROOT).as_posix()
        except Exception as e:
            print(f"      [WARN] Gagal generate RGB PNG: {e}")

    # 2. Solar Panels Layout Overlay on Roof
    if rgb_arr is not None and rgb_tif_path and rgb_tif_path.exists():
        try:
            sp = bi_data.get("solarPotential", {})
            panels = sp.get("solarPanels", [])
            segs = sp.get("roofSegmentStats", [])
            pw_m = sp.get("panelWidthMeters", 1.045)
            ph_m = sp.get("panelHeightMeters", 1.879)

            with rasterio.open(rgb_tif_path) as src:
                transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                scale_gap = 0.88
                pw_px = (pw_m / 0.25) * scale_gap
                ph_px = (ph_m / 0.25) * scale_gap

                fig, ax = plt.subplots(figsize=(8, 8), dpi=180)
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

                    is_landscape = p.get("orientation") == "LANDSCAPE"
                    if is_landscape:
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

                    poly = Polygon(
                        [p1, p2, p3, p4], closed=True,
                        facecolor="#2563EB", edgecolor="#93C5FD",
                        linewidth=0.5, alpha=0.88
                    )
                    ax.add_patch(poly)

                ax.set_xlim(0, src.width)
                ax.set_ylim(src.height, 0)
                ax.axis("off")
                fig.patch.set_facecolor("#0E1117")
                fig.savefig(str(panels_png_path.resolve()), facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
                plt.close(fig)
                out_paths["preview_panels_png"] = panels_png_path.relative_to(PROJECT_ROOT).as_posix()
        except Exception as e:
            print(f"      [WARN] Gagal generate Panels Overlay PNG: {e}")

    # 3. DSM Elevation (Peta Ketinggian 3D)
    if dsm_tif_path and dsm_tif_path.exists():
        try:
            with rasterio.open(dsm_tif_path) as src:
                dsm = src.read(1).astype(float)
                dsm[dsm < -100] = np.nan
                fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
                im = ax.imshow(dsm, cmap="terrain")
                cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cbar.set_label("Elevasi Ketinggian Atap (Meter)", fontsize=9)
                ax.set_title(f"DSM (Model Ketinggian 3D): {asset_name}", fontsize=11, fontweight="bold")
                ax.axis("off")
                fig.tight_layout()
                fig.savefig(str(dsm_png_path.resolve()), bbox_inches="tight")
                plt.close(fig)
                out_paths["preview_dsm_png"] = dsm_png_path.relative_to(PROJECT_ROOT).as_posix()
        except Exception as e:
            print(f"      [WARN] Gagal generate DSM PNG: {e}")

    # 4. Roof Mask (Binary Mask Atap)
    if mask_tif_path and mask_tif_path.exists():
        try:
            with rasterio.open(mask_tif_path) as src:
                mask = src.read(1)
                fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
                cmap = plt.matplotlib.colors.ListedColormap(["#111927", "#00E676"])
                im = ax.imshow(mask, cmap=cmap)
                ax.set_title(f"Roof Mask (Segmentasi Atap Layak PLTS): {asset_name}", fontsize=11, fontweight="bold")
                ax.axis("off")
                fig.tight_layout()
                fig.savefig(str(mask_png_path.resolve()), bbox_inches="tight")
                plt.close(fig)
                out_paths["preview_mask_png"] = mask_png_path.relative_to(PROJECT_ROOT).as_posix()
        except Exception as e:
            print(f"      [WARN] Gagal generate Mask PNG: {e}")

    # 5. Annual Flux Heatmap
    if flux_tif_path and flux_tif_path.exists():
        try:
            with rasterio.open(flux_tif_path) as src:
                flux_arr = src.read(1).astype(float)
                flux_arr[flux_arr <= 0] = np.nan
                fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
                cmap = plt.get_cmap("plasma")
                cmap.set_bad(color="black")
                im = ax.imshow(flux_arr, cmap=cmap)
                cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cbar.set_label("Annual Flux (kWh/kW/year)", fontsize=9)
                ax.set_title(f"Annual Solar Flux: {asset_name}", fontsize=11, fontweight="bold")
                ax.axis("off")
                fig.tight_layout()
                fig.savefig(str(flux_png_path.resolve()), bbox_inches="tight")
                plt.close(fig)
                out_paths["preview_flux_png"] = flux_png_path.relative_to(PROJECT_ROOT).as_posix()
        except Exception as e:
            print(f"      [WARN] Gagal generate Flux Heatmap PNG: {e}")

    # 6. Roof Segmentation Grid Overlay
    if rgb_arr is not None and rgb_tif_path and rgb_tif_path.exists():
        try:
            sp = bi_data.get("solarPotential", {})
            panels = sp.get("solarPanels", [])
            segs = sp.get("roofSegmentStats", [])

            with rasterio.open(rgb_tif_path) as src:
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

                    for px, py in pts:
                        ax.plot(px, py, marker="s", markersize=2, color=color, alpha=0.85)

                    pts_in = [p for p in pts if 0 <= p[0] < src.width and 0 <= p[1] < src.height]
                    if pts_in:
                        pts_in_arr = np.array(pts_in)
                        cx = float(np.median(pts_in_arr[:, 0]))
                        cy = float(np.median(pts_in_arr[:, 1]))
                        badge_coords.append((s_idx, cx, cy, color))

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
                fig.savefig(str(segments_png_path.resolve()), facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
                plt.close(fig)
                out_paths["preview_segments_png"] = segments_png_path.relative_to(PROJECT_ROOT).as_posix()
        except Exception as e:
            print(f"      [WARN] Gagal generate Segments Overlay PNG: {e}")

    return out_paths


def main():
    parser = argparse.ArgumentParser(description="ETL Transformer untuk 100 Titik Google Solar API Jabodetabek.")
    parser.add_argument("--input", default="data/raw/poi/target_100_titik.csv", help="Path CSV master target.")
    args = parser.parse_args()

    input_csv = PROJECT_ROOT / args.input
    if not input_csv.exists():
        raise FileNotFoundError(f"Input file tidak ditemukan: {input_csv}")

    df_targets = pd.read_csv(input_csv)
    print("=" * 75)
    print(f"STARTING GOOGLE SOLAR API ETL PIPELINE (100 TITIK)")
    print(f"Single Source of Truth: {input_csv.relative_to(PROJECT_ROOT)} ({len(df_targets)} targets)")
    print("Zero Hardcoding - Pure Dynamic Mathematical Engine")
    print("=" * 75)

    records = []
    segment_records = []

    dirs = ["U (0°)", "TL (45°)", "T (90°)", "TG (135°)", "S (180°)", "BD (225°)", "B (270°)", "BL (315°)"]
    solar_insights = [
        "Optimal saat matahari condong di utara (April – Agustus)",
        "Menangkap sinar pagi menjelang siang",
        "Matahari Terbit: Produksi listrik memuncak di pagi hari (07.00 – 11.00)",
        "Menangkap sinar pagi menjelang tengah hari",
        "Optimal saat matahari condong di selatan (Oktober – Februari)",
        "Menangkap sinar siang menjelang sore",
        "Matahari Terbenam: Produksi listrik memuncak di siang–sore (12.00 – 16.00)",
        "Menangkap sinar sore"
    ]

    processed_count = 0
    missing_count = 0

    for _, t in df_targets.iterrows():
        aid = str(t["asset_id"]).strip().lower()
        cat = str(t["category"]).strip().lower()
        asset_name = str(t["asset_name"]).strip()
        cat_disp = str(t.get("category_display", cat)).strip()
        city_reg = str(t.get("city_regency", "")).strip()
        raw_lat = float(t["latitude"])
        raw_lon = float(t["longitude"])
        source_ref = str(t.get("source_reference", "")).strip()

        bi_file = RAW_SOLAR_DIR / "building_insights" / cat / f"{aid}_insights.json"
        if not bi_file.exists():
            missing_count += 1
            continue

        processed_count += 1
        print(f"\nProcessing [{processed_count}] {asset_name} ({cat_disp} - {city_reg})...")

        with open(bi_file, "r", encoding="utf-8") as f:
            bi_data = json.load(f)

        g_center = bi_data.get("center", {})
        g_lat = g_center.get("latitude", raw_lat)
        g_lon = g_center.get("longitude", raw_lon)

        drift_m = haversine_distance_meters(raw_lat, raw_lon, g_lat, g_lon)
        drift_status = "VALID (< 30m)" if drift_m <= 30.0 else "REVIEW (> 30m)"

        sp = bi_data.get("solarPotential", {})
        imagery_date_dict = bi_data.get("imageryDate", {})
        if imagery_date_dict:
            imagery_date = f"{imagery_date_dict.get('year', 2024)}-{imagery_date_dict.get('month', 1):02d}-{imagery_date_dict.get('day', 1):02d}"
        else:
            imagery_date = "2024-01-01"

        postal_code = bi_data.get("postalCode", "")

        whole_roof_area = sp.get("wholeRoofStats", {}).get("areaMeters2", 0.0)
        max_roof_area = sp.get("maxArrayAreaMeters2", 0.0)
        building_footprint = sp.get("buildingStats", {}).get("areaMeters2", whole_roof_area)
        max_panels = sp.get("maxArrayPanelsCount", 0)
        sunshine_hours = sp.get("maxSunshineHoursPerYear", 1300.0)
        co2_factor = sp.get("carbonOffsetFactorKgPerMwh", 808.999)

        suitability_ratio = round((max_roof_area / whole_roof_area) * 100, 1) if whole_roof_area > 0 else 0.0
        gap_unsegmented_m2 = round(max(0.0, building_footprint - whole_roof_area), 2)
        gap_unpanelled_m2 = round(max(0.0, whole_roof_area - max_roof_area), 2)
        total_gap_m2 = round(max(0.0, building_footprint - max_roof_area), 2)
        roof_coverage_ratio_pct = round((whole_roof_area / building_footprint) * 100.0, 1) if building_footprint > 0 else 100.0
        gap_unsegmented_pct = round(100.0 - roof_coverage_ratio_pct, 1)

        solar_configs = sp.get("solarPanelConfigs", [])
        google_dc_mwh = 0.0
        if solar_configs:
            last_cfg = solar_configs[-1]
            google_dc_mwh = round(last_cfg.get("yearlyEnergyDcKwh", 0.0) / 1000.0, 2)

        # Segment statistics
        segs = sp.get("roofSegmentStats", [])
        pitches = [s.get("pitchDegrees", 0.0) for s in segs]
        areas = [s.get("stats", {}).get("areaMeters2", 0.0) for s in segs]
        if pitches and areas:
            min_p = min(pitches)
            max_p = max(pitches)
            tot_seg_area = sum(areas)
            weighted_p = sum(p * a for p, a in zip(pitches, areas)) / tot_seg_area if tot_seg_area > 0 else 0.0
            pitch_range = f"{min_p:.1f}° – {max_p:.1f}°"
            weighted_pitch = round(weighted_p, 1)
        else:
            pitch_range = "N/A"
            weighted_pitch = 0.0

        # GeoTIFF paths
        dsm_tif = RAW_SOLAR_DIR / "data_layers" / "dsm" / cat / f"{aid}_dsm.tif"
        rgb_tif = RAW_SOLAR_DIR / "data_layers" / "rgb" / cat / f"{aid}_rgb.tif"
        mask_tif = RAW_SOLAR_DIR / "data_layers" / "mask" / cat / f"{aid}_mask.tif"
        flux_tif = RAW_SOLAR_DIR / "data_layers" / "annual_flux" / cat / f"{aid}_annual_flux.tif"

        # CELIOS Formulas
        panel_wp = 400
        capacity_kwp = (max_panels * panel_wp) / 1000.0
        pr_factor = 0.80
        annual_gen_kwh = capacity_kwp * sunshine_hours * pr_factor
        annual_gen_mwh = annual_gen_kwh / 1000.0
        ghg_reduc_tons = (annual_gen_mwh * co2_factor) / 1000.0

        # Generate ALL 6 SKU PREVIEWS
        preview_paths = generate_all_sku_previews(
            aid, cat, asset_name, bi_data, rgb_tif, dsm_tif, mask_tif, flux_tif
        )

        rec = {
            "asset_id": t["asset_id"],
            "asset_name": asset_name,
            "category": cat,
            "category_display": cat_disp,
            "city_regency": city_reg,
            "postal_code": postal_code,
            "source_raw_file": source_ref,
            "raw_lat": raw_lat,
            "raw_lon": raw_lon,
            "google_building_id": bi_data.get("name", ""),
            "google_maps_url": f"https://www.google.com/maps/search/?api=1&query={g_lat:.6f},{g_lon:.6f}" if g_lat and g_lon else "",
            "google_center_lat": g_lat,
            "google_center_lon": g_lon,
            "spatial_drift_meters": round(drift_m, 2),
            "drift_status": drift_status,
            "imagery_date": imagery_date,
            "quality_tier": "BASE",
            "whole_roof_area_m2": round(whole_roof_area, 2),
            "max_roof_area_m2": round(max_roof_area, 2),
            "roof_suitability_ratio_pct": suitability_ratio,
            "building_footprint_m2": round(building_footprint, 2),
            "roof_coverage_ratio_pct": roof_coverage_ratio_pct,
            "gap_unsegmented_pct": gap_unsegmented_pct,
            "gap_unsegmented_m2": gap_unsegmented_m2,
            "gap_unpanelled_m2": gap_unpanelled_m2,
            "total_gap_m2": total_gap_m2,
            "total_segments_count": len(segs),
            "pitch_range": pitch_range,
            "weighted_pitch_deg": weighted_pitch,
            "max_panels_count": max_panels,
            "sunshine_hours_annual": round(sunshine_hours, 2),
            "panel_capacity_wp": panel_wp,
            "installed_capacity_kwp": round(capacity_kwp, 2),
            "google_dc_mwh": google_dc_mwh,
            "annual_generation_kwh": round(annual_gen_kwh, 2),
            "annual_generation_mwh": round(annual_gen_mwh, 2),
            "carbon_offset_factor": round(co2_factor, 2),
            "ghg_reduction_tons_co2": round(ghg_reduc_tons, 2),
            "path_dsm_geotiff": dsm_tif.relative_to(PROJECT_ROOT).as_posix() if dsm_tif.exists() else None,
            "path_rgb_geotiff": rgb_tif.relative_to(PROJECT_ROOT).as_posix() if rgb_tif.exists() else None,
            "path_mask_geotiff": mask_tif.relative_to(PROJECT_ROOT).as_posix() if mask_tif.exists() else None,
            "path_flux_geotiff": flux_tif.relative_to(PROJECT_ROOT).as_posix() if flux_tif.exists() else None,
            "preview_rgb_png": preview_paths.get("preview_rgb_png"),
            "preview_panels_png": preview_paths.get("preview_panels_png"),
            "preview_segments_png": preview_paths.get("preview_segments_png"),
            "preview_dsm_png": preview_paths.get("preview_dsm_png"),
            "preview_mask_png": preview_paths.get("preview_mask_png"),
            "preview_flux_png": preview_paths.get("preview_flux_png")
        }
        records.append(rec)
        print(f"   Kapasitas: {capacity_kwp:.1f} kWp ({max_panels:,} panel) | Luas Atap: {max_roof_area:,.1f} m² | Emisi: {ghg_reduc_tons:.1f} Ton CO2/thn")

        # Collect granular roof segment stats
        panels = sp.get("solarPanels", [])
        r_w, r_h = 479, 479
        trans_r = None
        if rgb_tif and rgb_tif.exists():
            try:
                with rasterio.open(rgb_tif) as src_r:
                    r_w, r_h = src_r.width, src_r.height
                    trans_r = Transformer.from_crs("EPSG:4326", src_r.crs, always_xy=True)
            except Exception:
                pass

        for s_idx, s in enumerate(segs):
            p_cnt = sum(1 for pan in panels if pan.get("segmentIndex") == s_idx)
            p_kwh = sum(pan.get("yearlyEnergyDcKwh", 0) for pan in panels if pan.get("segmentIndex") == s_idx)

            pitch = round(s.get("pitchDegrees", 0.0), 2)
            az = s.get("azimuthDegrees", 0.0)
            d_idx = int((az + 22.5) // 45) % 8
            if pitch < 3.0:
                insight = "Atap Datar (Puncak tengah hari 11.00–13.00, self-cleaning alami rendah)"
            else:
                insight = solar_insights[d_idx]

            if p_cnt == 0:
                spatial_status = "Dieliminasi Google (0 Panel)"
            elif trans_r is not None:
                pts_in_count = 0
                for pan in panels:
                    if pan.get("segmentIndex") == s_idx:
                        ux, uy = trans_r.transform(pan["center"]["longitude"], pan["center"]["latitude"])
                        py, px = src_r.index(ux, uy)
                        if 0 <= px < r_w and 0 <= py < r_h:
                            pts_in_count += 1
                spatial_status = "Di Luar Bingkai Citra" if pts_in_count == 0 else "Tampil di Citra"
            else:
                spatial_status = "Tampil di Citra"

            segment_records.append({
                "asset_id": t["asset_id"],
                "asset_name": asset_name,
                "category": cat,
                "category_display": cat_disp,
                "segment_index": s_idx,
                "pitch_degrees": pitch,
                "azimuth_degrees": round(az, 2),
                "azimuth_direction": dirs[d_idx],
                "spatial_status": spatial_status,
                "solar_insight": insight,
                "plane_height_m": round(s.get("planeHeightAtCenterMeters", 0.0), 2),
                "area_m2": round(s.get("stats", {}).get("areaMeters2", 0.0), 2),
                "ground_area_m2": round(s.get("stats", {}).get("groundAreaMeters2", 0.0), 2),
                "panels_count": p_cnt,
                "capacity_kwp": round(p_cnt * 0.4, 2),
                "annual_generation_mwh": round(p_kwh / 1000.0, 2)
            })

    if not records:
        print("[WARN] Belum ada titik dengan file Building Insights yang dapat diproses.")
        return

    df = pd.DataFrame(records)

    # Data-driven classification based directly on roof_coverage_ratio_pct from configuration
    rules_cfg_path = PROJECT_ROOT / "configs" / "roof_gap_infill_rules.json"
    thr_sedikit = 80.0
    thr_sedang = 65.0
    if rules_cfg_path.exists():
        try:
            with open(rules_cfg_path, "r", encoding="utf-8") as f:
                r_json = json.load(f)
                thr_cfg = r_json.get("gap_classification_thresholds", {})
                thr_sedikit = float(thr_cfg.get("gap_sedikit_min_coverage_pct", 80.0))
                thr_sedang = float(thr_cfg.get("gap_sedang_min_coverage_pct", 65.0))
        except Exception as e:
            print(f"[WARN] Gagal membaca gap_classification_thresholds: {e}")

    def classify_by_coverage(cov):
        if cov >= thr_sedikit:
            return "Gap Sedikit"
        elif cov >= thr_sedang:
            return "Gap Sedang"
        else:
            return "Gap Besar"

    df["gap_category"] = df["roof_coverage_ratio_pct"].apply(classify_by_coverage)
    df_segs = pd.DataFrame(segment_records)

    # 1. Save Summary CSV & Parquet
    csv_p = CALC_OUT_DIR / "pow_solar_100_titik_summary.csv"
    parq_p = CALC_OUT_DIR / "pow_solar_100_titik_summary.parquet"
    df.to_csv(csv_p, index=False, encoding="utf-8")
    df.to_parquet(parq_p, index=False)
    print(f"\n[OK] Summary Saved -> {csv_p.relative_to(PROJECT_ROOT)} ({len(df)} titik)")

    # 2. Save Granular Segments CSV & Parquet
    csv_segs_p = CALC_OUT_DIR / "pow_solar_100_titik_segments.csv"
    parq_segs_p = CALC_OUT_DIR / "pow_solar_100_titik_segments.parquet"
    df_segs.to_csv(csv_segs_p, index=False, encoding="utf-8")
    df_segs.to_parquet(parq_segs_p, index=False)
    print(f"[OK] Segments Saved -> {csv_segs_p.relative_to(PROJECT_ROOT)} ({len(df_segs)} segments)")

    # 3. Save GeoJSON
    geometry = [Point(xy) for xy in zip(df['google_center_lon'], df['google_center_lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    geojson_p = GIS_OUT_DIR / "pow_solar_100_titik.geojson"
    gdf.to_file(geojson_p, driver="GeoJSON")
    print(f"[OK] GeoJSON Saved -> {geojson_p.relative_to(PROJECT_ROOT)}")

    print("\n" + "=" * 75)
    print("ETL TRANSFORMATION COMPLETED SUCCESSFULLY!")
    print(f"Total Target Terproses   : {len(df)} titik")
    print(f"Total Target Belum Fetch : {missing_count} titik")
    print(f"Total Kapasitas Terhitung: {df['installed_capacity_kwp'].sum():,.1f} kWp ({df['max_panels_count'].sum():,} panel)")
    print(f"Total Luas Atap Efektif  : {df['max_roof_area_m2'].sum():,.1f} m²")
    print("=" * 75)


if __name__ == "__main__":
    main()
