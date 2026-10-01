"""
process_pow_etl.py
------------------
Transformer & Loader (ETL) untuk Proof of Work (POW) Google Solar API 5 Titik Pilot.

Alur Kerja:
1. Membaca raw data dari:
   - data/raw/solar/building_insights/{kategori}/{aid}_insights.json
   - data/raw/solar/data_layers/{layer}/{kategori}/{aid}_{layer}.tif
2. Menghitung spatial drift (Haversine formula) antara titik sumber dan centroid Google.
3. Menghitung metrik tekno-ekonomi surya (kWp, kWh/thn, emisi CO2).
4. Menghasilkan PNG preview citra satelit RGB dan heatmap Annual Flux untuk dashboard web.
5. Menyimpan data olahan ke:
   - data/processed/gis/pow_solar_5_titik.geojson
   - data/processed/calculations/pow_solar_5_titik_summary.csv
   - data/processed/calculations/pow_solar_5_titik_summary.parquet
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
from PIL import Image

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


def generate_raster_previews(aid, cat, rgb_tif_path, flux_tif_path):
    """
    Mengonversi GeoTIFF RGB dan Annual Flux menjadi gambar PNG visualisasi web
    yang tersimpan di data/processed/previews/
    """
    rgb_png_path = PREVIEW_OUT_DIR / f"{aid}_rgb.png"
    flux_png_path = PREVIEW_OUT_DIR / f"{aid}_flux_heatmap.png"

    # 1. Generate RGB PNG
    if rgb_tif_path and rgb_tif_path.exists():
        try:
            with rasterio.open(rgb_tif_path) as src:
                # Read bands 1, 2, 3
                rgb_arr = src.read([1, 2, 3])
                # Transpose from (C, H, W) to (H, W, C)
                rgb_img = np.transpose(rgb_arr, (1, 2, 0))
                im = Image.fromarray(rgb_img)
                im.save(rgb_png_path, "PNG")
        except Exception as e:
            print(f"      [WARN] Gagal generate RGB PNG: {e}")

    # 2. Generate Annual Flux Heatmap PNG
    if flux_tif_path and flux_tif_path.exists():
        try:
            with rasterio.open(flux_tif_path) as src:
                flux_arr = src.read(1).astype(float)
                # Filter invalid/nodata
                flux_arr[flux_arr <= 0] = np.nan
                
                fig, ax = plt.subplots(figsize=(6, 6), dpi=150)
                cmap = plt.get_cmap('plasma')
                cmap.set_bad(color='black')
                im = ax.imshow(flux_arr, cmap=cmap)
                plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Annual Flux (kWh/kW/year)")
                ax.set_title(f"Annual Solar Flux: {aid.upper()}", fontsize=11, fontweight='bold')
                ax.axis('off')
                fig.tight_layout()
                fig.savefig(flux_png_path, bbox_inches='tight', transparent=False)
                plt.close(fig)
        except Exception as e:
            print(f"      [WARN] Gagal generate Flux Heatmap PNG: {e}")

    return (
        str(rgb_png_path.relative_to(PROJECT_ROOT)) if rgb_png_path.exists() else None,
        str(flux_png_path.relative_to(PROJECT_ROOT)) if flux_png_path.exists() else None
    )


def process_targets():
    print("=" * 70)
    print("STARTING ETL PROCESS FOR STAGE 1 POW (5 PILOT POINTS)")
    print("Transforming Raw API Data -> data/processed/ Calculations & Web GIS")
    print("=" * 70)

    # Master targets info
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

        # CELIOS Formulas (Standard 400 Wp panel, 0.80 PR)
        panel_wp = 400
        capacity_kwp = (max_panels * panel_wp) / 1000.0
        pr_factor = 0.80  # Performance Ratio standar iklim tropis perkotaan
        annual_gen_kwh = capacity_kwp * sunshine_hours * pr_factor
        annual_gen_mwh = annual_gen_kwh / 1000.0
        ghg_reduc_tons = (annual_gen_mwh * co2_factor) / 1000.0

        # GeoTIFF paths
        dsm_tif = RAW_SOLAR_DIR / "data_layers" / "dsm" / cat / f"{aid}_dsm.tif"
        rgb_tif = RAW_SOLAR_DIR / "data_layers" / "rgb" / cat / f"{aid}_rgb.tif"
        mask_tif = RAW_SOLAR_DIR / "data_layers" / "mask" / cat / f"{aid}_mask.tif"
        flux_tif = RAW_SOLAR_DIR / "data_layers" / "annual_flux" / cat / f"{aid}_annual_flux.tif"

        # Generate Web PNG Previews
        rgb_png, flux_png = generate_raster_previews(aid, cat, rgb_tif, flux_tif)

        rec = {
            "asset_id": t["asset_id"],
            "asset_name": t["asset_name"],
            "category": cat,
            "category_display": t["category_display"],
            "city_regency": t["city_regency"],
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
            "max_panels_count": max_panels,
            "max_roof_area_m2": round(max_roof_area, 2),
            "sunshine_hours_annual": round(sunshine_hours, 2),
            "panel_capacity_wp": panel_wp,
            "installed_capacity_kwp": round(capacity_kwp, 2),
            "annual_generation_kwh": round(annual_gen_kwh, 2),
            "annual_generation_mwh": round(annual_gen_mwh, 2),
            "carbon_offset_factor": round(co2_factor, 2),
            "ghg_reduction_tons_co2": round(ghg_reduc_tons, 2),
            "path_dsm_geotiff": str(dsm_tif.relative_to(PROJECT_ROOT)) if dsm_tif.exists() else None,
            "path_rgb_geotiff": str(rgb_tif.relative_to(PROJECT_ROOT)) if rgb_tif.exists() else None,
            "path_mask_geotiff": str(mask_tif.relative_to(PROJECT_ROOT)) if mask_tif.exists() else None,
            "path_flux_geotiff": str(flux_tif.relative_to(PROJECT_ROOT)) if flux_tif.exists() else None,
            "preview_rgb_png": rgb_png,
            "preview_flux_png": flux_png
        }
        records.append(rec)
        print(f"   Kapasitas: {capacity_kwp:.1f} kWp ({max_panels} panel) | Luas Atap: {max_roof_area:.1f} m² | Emisi: {ghg_reduc_tons:.1f} Ton CO2/thn")

    # Build DataFrame
    df = pd.DataFrame(records)

    # 1. Save CSV
    csv_out = CALC_OUT_DIR / "pow_solar_5_titik_summary.csv"
    df.to_csv(csv_out, index=False, encoding="utf-8")
    print(f"\n[OK] CSV Summary Saved -> {csv_out.relative_to(PROJECT_ROOT)}")

    # 2. Save Parquet
    parquet_out = CALC_OUT_DIR / "pow_solar_5_titik_summary.parquet"
    df.to_parquet(parquet_out, index=False)
    print(f"[OK] Parquet Summary Saved -> {parquet_out.relative_to(PROJECT_ROOT)}")

    # 3. Save GeoJSON
    # Geometry uses Google Building Centroid for optimal spatial accuracy
    geometry = [Point(xy) for xy in zip(df['google_center_lon'], df['google_center_lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    geojson_out = GIS_OUT_DIR / "pow_solar_5_titik.geojson"
    gdf.to_file(geojson_out, driver="GeoJSON")
    print(f"[OK] GeoJSON Saved -> {geojson_out.relative_to(PROJECT_ROOT)}")

    print("\n" + "=" * 70)
    print("ETL TRANSFORMATION COMPLETED SUCCESSFULLY!")
    print(f"Processed: {len(df)} Points")
    print(f"Total Kapasitas: {df['installed_capacity_kwp'].sum():,.1f} kWp")
    print(f"Total Luas Atap Efektif: {df['max_roof_area_m2'].sum():,.1f} m²")
    print(f"Total Reduksi Emisi GRK: {df['ghg_reduction_tons_co2'].sum():,.1f} Ton CO2/tahun")
    print("=" * 70)


if __name__ == "__main__":
    process_targets()
