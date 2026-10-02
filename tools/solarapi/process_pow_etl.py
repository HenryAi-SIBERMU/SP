"""
process_pow_etl.py
------------------
Transformer & Loader (ETL) untuk Proof of Work (POW) Google Solar API 5 Titik Pilot.

Menghasilkan seluruh visualisasi SKU resmi:
1. Citra Satelit Aerial RGB Asli (0.25m/px)
2. Solar Panel Layout on Roof (Visualisasi posisi panel surya di atas atap sesuai UI Google)
3. Digital Surface Model (DSM - Elevasi & Ketinggian 3D)
4. Roof Mask (Binary Mask Atap vs Non-Atap)
5. Annual Solar Flux Heatmap (Radiasi Surya Tahunan kWh/kW/year)

Kepatuhan Aturan:
- strict_data_folder_boundary.md: 100% output tersimpan di data/processed/
- statistical_auditor_role.md: Formula matematis terverifikasi
"""

import os
import sys
import json
import math
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
    2. Solar Panels Layout on Roof (Overlay Biru)
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

    # 1. RGB Image
    rgb_arr = None
    if rgb_tif_path and rgb_tif_path.exists():
        try:
            with rasterio.open(rgb_tif_path) as src:
                rgb_raw = src.read([1, 2, 3])
                rgb_arr = np.transpose(rgb_raw, (1, 2, 0))
                im = Image.fromarray(rgb_arr)
                im.save(rgb_png_path, "PNG")
                out_paths["preview_rgb_png"] = str(rgb_png_path.relative_to(PROJECT_ROOT))
        except Exception as e:
            print(f"      [WARN] Gagal generate RGB PNG: {e}")

    # 2. Solar Panels Layout Overlay on Roof (Accurate Segment Azimuth Rotation & Non-Overlapping Spacing)
    if rgb_arr is not None and rgb_tif_path and rgb_tif_path.exists():
        try:
            sp = bi_data.get("solarPotential", {})
            panels = sp.get("solarPanels", [])
            segs = sp.get("roofSegmentStats", [])
            pw_m = sp.get("panelWidthMeters", 1.045)
            ph_m = sp.get("panelHeightMeters", 1.879)

            with rasterio.open(rgb_tif_path) as src:
                transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
                
                # 0.25m per pixel with 0.88 scale factor to preserve clean spacing between physical modules
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

                    seg_idx = p.get("segmentIndex", 0)
                    seg = segs[seg_idx] if seg_idx < len(segs) else {}
                    az_deg = seg.get("azimuthDegrees", 0.0)

                    # Orient vector along roof ridge & slope matching Google Solar API methodology
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
                out_paths["preview_panels_png"] = str(panels_png_path.relative_to(PROJECT_ROOT))
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
                out_paths["preview_dsm_png"] = str(dsm_png_path.relative_to(PROJECT_ROOT))
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
                out_paths["preview_mask_png"] = str(mask_png_path.relative_to(PROJECT_ROOT))
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
                out_paths["preview_flux_png"] = str(flux_png_path.relative_to(PROJECT_ROOT))
        except Exception as e:
            print(f"      [WARN] Gagal generate Flux Heatmap PNG: {e}")

    # 6. Roof Segmentation Grid Overlay (3D RANSAC Planar Facets with Distinct Colors & Convex Hulls)
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

                # Group panels by segment
                seg_points = {i: [] for i in range(len(segs))}
                for p in panels:
                    s_idx = p.get("segmentIndex", 0)
                    ux, uy = transformer.transform(p["center"]["longitude"], p["center"]["latitude"])
                    py, px = src.index(ux, uy)
                    if s_idx in seg_points:
                        seg_points[s_idx].append((px, py))

                badge_coords = []
                for s_idx, pts in seg_points.items():
                    if not pts:
                        continue
                    color = cmap(s_idx % 20)

                    if len(pts) >= 3:
                        pts_arr = np.array(pts)
                        try:
                            hull = ConvexHull(pts_arr)
                            hull_pts = pts_arr[hull.vertices]
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

                    # Centroid for badge (only from points inside visible canvas)
                    pts_in = [p for p in pts if 0 <= p[0] < src.width and 0 <= p[1] < src.height]
                    if pts_in:
                        pts_in_arr = np.array(pts_in)
                        cx = float(np.median(pts_in_arr[:, 0]))
                        cy = float(np.median(pts_in_arr[:, 1]))
                        badge_coords.append((s_idx, cx, cy, color))

                # Collision avoidance repulsion loop
                for _ in range(3):
                    for i in range(len(badge_coords)):
                        for j in range(i + 1, len(badge_coords)):
                            s_i, xi, yi, c_i = badge_coords[i]
                            s_j, xj, yj, c_j = badge_coords[j]
                            dist = np.hypot(xi - xj, yi - yj)
                            if dist < 26:
                                angle = np.arctan2(yj - yi, xj - xi)
                                if dist == 0:
                                    angle = np.pi / 4
                                nudge = (26 - max(dist, 1)) / 2.0
                                badge_coords[j] = (s_j, xj + np.cos(angle) * nudge, yj + np.sin(angle) * nudge, c_j)
                                badge_coords[i] = (s_i, xi - np.cos(angle) * nudge, yi - np.sin(angle) * nudge, c_i)

                for s_idx, cx, cy, color in badge_coords:
                    seg_num = s_idx + 1
                    ax.text(
                        cx, cy, str(seg_num), fontsize=8.5, fontweight='bold', color='white',
                        bbox=dict(boxstyle='circle,pad=0.22', facecolor='#0B111E', edgecolor=color, linewidth=2.0, alpha=0.92),
                        ha='center', va='center', zorder=10
                    )

                ax.set_xlim(0, src.width)
                ax.set_ylim(src.height, 0)
                ax.axis("off")
                fig.patch.set_facecolor("#0E1117")
                fig.savefig(str(segments_png_path.resolve()), facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0)
                plt.close(fig)
                out_paths["preview_segments_png"] = str(segments_png_path.relative_to(PROJECT_ROOT))
        except Exception as e:
            print(f"      [WARN] Gagal generate Segments Overlay PNG: {e}")

    return out_paths


def process_targets():
    print("=" * 70)
    print("STARTING COMPREHENSIVE MULTI-LAYER ETL PROCESS FOR STAGE 1 POW")
    print("Generating Visualizations for ALL 5 SKUs (Panels, RGB, DSM, Mask, Flux)")
    print("=" * 70)

    targets_info = [
        {
            "asset_id": "MRT-003",
            "asset_name": "Stasiun MRT Cipete Raya",
            "category": "mrt",
            "category_display": "MRT",
            "city_regency": "Jakarta Selatan",
            "source_raw_file": "data/raw/mrt_lrt/mrt_stations.csv",
            "raw_lat": -6.2783417,
            "raw_lon": 106.7973264
        },
        {
            "asset_id": "KRL-032",
            "asset_name": "Stasiun KRL Manggarai Sentral",
            "category": "krl",
            "category_display": "KRL",
            "city_regency": "Jakarta Selatan",
            "source_raw_file": "data/raw/krl/krl_stations.csv",
            "raw_lat": -6.2101704,
            "raw_lon": 106.849935
        },
        {
            "asset_id": "LRT-014",
            "asset_name": "Stasiun LRT Dukuh Atas",
            "category": "lrt",
            "category_display": "LRT",
            "city_regency": "Jakarta Pusat",
            "source_raw_file": "data/raw/mrt_lrt/lrt_jabodebek_stations.geojson",
            "raw_lat": -6.204825,
            "raw_lon": 106.82553
        },
        {
            "asset_id": "RS-007",
            "asset_name": "RSUD Tarakan Jakarta",
            "category": "hospital",
            "category_display": "Rumah Sakit",
            "city_regency": "Jakarta Pusat",
            "source_raw_file": "data/raw/osm/hospitals_jakarta.gpkg",
            "raw_lat": -6.17155,
            "raw_lon": 106.81025
        },
        {
            "asset_id": "PKG-020",
            "asset_name": "Lippo Mall Puri 1 Multilevel Parking",
            "category": "parking",
            "category_display": "Gedung Parkir",
            "city_regency": "Jakarta Barat",
            "source_raw_file": "data/raw/osm/parking_jakarta.gpkg",
            "raw_lat": -6.19028,
            "raw_lon": 106.73937
        }
    ]

    records = []
    segment_records = []

    for t in targets_info:
        aid = t["asset_id"].lower()
        cat = t["category"]
        bi_file = RAW_SOLAR_DIR / "building_insights" / cat / f"{aid}_insights.json"

        print(f"\nProcessing {t['asset_name']} ({t['category_display']})...")

        if not bi_file.exists():
            print(f"   ❌ File insights tidak ditemukan: {bi_file}")
            continue

        with open(bi_file, "r", encoding="utf-8") as f:
            bi_data = json.load(f)

        center = bi_data.get("center", {})
        g_lat = center.get("latitude")
        g_lon = center.get("longitude")

        # Spatial Drift
        drift_m = haversine_distance_meters(t["raw_lat"], t["raw_lon"], g_lat, g_lon)
        drift_status = "VALID (< 30m)" if drift_m < 30.0 else "REVIEW (> 30m)"
        print(f"   Spatial Drift: {drift_m:.2f} meters -> {drift_status}")

        # Imagery Date
        img_date_obj = bi_data.get("imageryDate", {})
        imagery_date = f"{img_date_obj.get('year', 2025)}-{img_date_obj.get('month', 8):02d}-{img_date_obj.get('day', 16):02d}"

        # Solar Metrics
        sp = bi_data.get("solarPotential", {})
        max_panels = int(sp.get("maxArrayPanelsCount", 0))
        max_roof_area = float(sp.get("maxArrayAreaMeters2", 0.0))
        sunshine_hours = float(sp.get("maxSunshineHoursPerYear", 0.0))
        co2_factor = float(sp.get("carbonOffsetFactorKgPerMwh", 808.999))

        # Additional Google Solar API Native Metrics (Maximize RAB return)
        wr = sp.get("wholeRoofStats", {})
        whole_roof_area = float(wr.get("areaMeters2", 0.0))
        suitability_ratio = round((max_roof_area / whole_roof_area * 100), 1) if whole_roof_area > 0 else 0.0
        
        configs = sp.get("solarPanelConfigs", [])
        google_dc_kwh = float(configs[-1].get("yearlyEnergyDcKwh", 0.0)) if configs else 0.0
        google_dc_mwh = round(google_dc_kwh / 1000.0, 2)
        
        bs = sp.get("buildingStats", {})
        building_footprint = float(bs.get("areaMeters2", 0.0))
        postal_code = bi_data.get("postalCode", "")

        # CELIOS Formulas
        panel_wp = 400
        capacity_kwp = (max_panels * panel_wp) / 1000.0
        pr_factor = 0.80
        annual_gen_kwh = capacity_kwp * sunshine_hours * pr_factor
        annual_gen_mwh = annual_gen_kwh / 1000.0
        ghg_reduc_tons = (annual_gen_mwh * co2_factor) / 1000.0

        # GeoTIFF paths
        dsm_tif = RAW_SOLAR_DIR / "data_layers" / "dsm" / cat / f"{aid}_dsm.tif"
        rgb_tif = RAW_SOLAR_DIR / "data_layers" / "rgb" / cat / f"{aid}_rgb.tif"
        mask_tif = RAW_SOLAR_DIR / "data_layers" / "mask" / cat / f"{aid}_mask.tif"
        flux_tif = RAW_SOLAR_DIR / "data_layers" / "annual_flux" / cat / f"{aid}_annual_flux.tif"

        # Generate ALL 5 SKU PREVIEWS
        preview_paths = generate_all_sku_previews(
            aid, cat, t["asset_name"], bi_data, rgb_tif, dsm_tif, mask_tif, flux_tif
        )

        rec = {
            "asset_id": t["asset_id"],
            "asset_name": t["asset_name"],
            "category": cat,
            "category_display": t["category_display"],
            "city_regency": t["city_regency"],
            "postal_code": postal_code,
            "source_raw_file": t["source_raw_file"],
            "raw_lat": t["raw_lat"],
            "raw_lon": t["raw_lon"],
            "google_building_id": bi_data.get("name", ""),
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
            "max_panels_count": max_panels,
            "sunshine_hours_annual": round(sunshine_hours, 2),
            "panel_capacity_wp": panel_wp,
            "installed_capacity_kwp": round(capacity_kwp, 2),
            "google_dc_mwh": google_dc_mwh,
            "annual_generation_kwh": round(annual_gen_kwh, 2),
            "annual_generation_mwh": round(annual_gen_mwh, 2),
            "carbon_offset_factor": round(co2_factor, 2),
            "ghg_reduction_tons_co2": round(ghg_reduc_tons, 2),
            "path_dsm_geotiff": str(dsm_tif.relative_to(PROJECT_ROOT)) if dsm_tif.exists() else None,
            "path_rgb_geotiff": str(rgb_tif.relative_to(PROJECT_ROOT)) if rgb_tif.exists() else None,
            "path_mask_geotiff": str(mask_tif.relative_to(PROJECT_ROOT)) if mask_tif.exists() else None,
            "path_flux_geotiff": str(flux_tif.relative_to(PROJECT_ROOT)) if flux_tif.exists() else None,
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
        sp = bi_data.get("solarPotential", {})
        segs = sp.get("roofSegmentStats", [])
        panels = sp.get("solarPanels", [])
        dirs = ["U (0°)", "TL (45°)", "T (90°)", "TG (135°)", "S (180°)", "BD (225°)", "B (270°)", "BL (315°)"]
        for s_idx, s in enumerate(segs):
            p_cnt = sum(1 for pan in panels if pan.get("segmentIndex") == s_idx)
            p_kwh = sum(pan.get("yearlyEnergyDcKwh", 0) for pan in panels if pan.get("segmentIndex") == s_idx)
            az = s.get("azimuthDegrees", 0.0)
            d_idx = int((az + 22.5) // 45) % 8
            segment_records.append({
                "asset_id": t["asset_id"],
                "asset_name": t["asset_name"],
                "category": cat,
                "category_display": t["category_display"],
                "segment_index": s_idx,
                "pitch_degrees": round(s.get("pitchDegrees", 0.0), 2),
                "azimuth_degrees": round(az, 2),
                "azimuth_direction": dirs[d_idx],
                "plane_height_m": round(s.get("planeHeightAtCenterMeters", 0.0), 2),
                "area_m2": round(s.get("stats", {}).get("areaMeters2", 0.0), 2),
                "ground_area_m2": round(s.get("stats", {}).get("groundAreaMeters2", 0.0), 2),
                "panels_count": p_cnt,
                "capacity_kwp": round(p_cnt * 0.4, 2),
                "annual_generation_mwh": round(p_kwh / 1000.0, 2)
            })

    df = pd.DataFrame(records)
    df_segs = pd.DataFrame(segment_records)

    # 1. Save Summary CSV & Parquet
    csv_out = CALC_OUT_DIR / "pow_solar_5_titik_summary.csv"
    df.to_csv(csv_out, index=False, encoding="utf-8")
    print(f"\n[OK] CSV Summary Saved -> {csv_out.relative_to(PROJECT_ROOT)}")

    parquet_out = CALC_OUT_DIR / "pow_solar_5_titik_summary.parquet"
    df.to_parquet(parquet_out, index=False)
    print(f"[OK] Parquet Summary Saved -> {parquet_out.relative_to(PROJECT_ROOT)}")

    # 2. Save Granular Segments CSV & Parquet
    csv_segs_out = CALC_OUT_DIR / "pow_solar_5_titik_segments.csv"
    df_segs.to_csv(csv_segs_out, index=False, encoding="utf-8")
    print(f"[OK] CSV Segments Saved -> {csv_segs_out.relative_to(PROJECT_ROOT)} ({len(df_segs)} segments)")

    parquet_segs_out = CALC_OUT_DIR / "pow_solar_5_titik_segments.parquet"
    df_segs.to_parquet(parquet_segs_out, index=False)
    print(f"[OK] Parquet Segments Saved -> {parquet_segs_out.relative_to(PROJECT_ROOT)}")

    # 3. Save GeoJSON
    geometry = [Point(xy) for xy in zip(df['google_center_lon'], df['google_center_lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    geojson_out = GIS_OUT_DIR / "pow_solar_5_titik.geojson"
    gdf.to_file(geojson_out, driver="GeoJSON")
    print(f"[OK] GeoJSON Saved -> {geojson_out.relative_to(PROJECT_ROOT)}")

    print("\n" + "=" * 70)
    print("ALL 5 SKU PREVIEWS GENERATED & ETL COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    process_targets()
