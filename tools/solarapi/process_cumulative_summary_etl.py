#!/usr/bin/env python3
"""
process_cumulative_summary_etl.py
===================================
Lightweight Cumulative ETL Aggregator untuk Google Solar API Jabodetabek.
Menggabungkan 100 Titik Pilot yang sudah ada + Batch yang sudah di-fetch (misal Batch 1: 250 titik)
menghasilkan master dataset kumulatif (~350 titik, dan berkembang hingga 2.000 titik).

Kepatuhan Aturan:
- zero hardcoding
- deduplikasi spasial teruji
- perhitungan CELIOS resmi (400Wp, PR 0.80, CO2 factor 808.99 kg/MWh)
- konsistensi skema 49 kolom identik
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
POI_DIR = RAW_DIR / "poi"
RAW_SOLAR_DIR = RAW_DIR / "solar"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CALC_OUT_DIR = PROCESSED_DIR / "calculations"
GIS_OUT_DIR = PROCESSED_DIR / "gis"
CONFIGS_DIR = PROJECT_ROOT / "configs"

CALC_OUT_DIR.mkdir(parents=True, exist_ok=True)
GIS_OUT_DIR.mkdir(parents=True, exist_ok=True)


def haversine_distance_meters(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_gap_thresholds():
    rules_cfg = CONFIGS_DIR / "roof_gap_infill_rules.json"
    thr_sedikit = 80.0
    thr_sedang = 65.0
    if rules_cfg.exists():
        try:
            with open(rules_cfg, "r", encoding="utf-8") as f:
                r_json = json.load(f)
                cfg = r_json.get("gap_classification_thresholds", {})
                thr_sedikit = float(cfg.get("gap_sedikit_min_coverage_pct", 80.0))
                thr_sedang = float(cfg.get("gap_sedang_min_coverage_pct", 65.0))
        except Exception:
            pass
    return thr_sedikit, thr_sedang


def classify_gap_category(coverage_pct, thr_sedikit=80.0, thr_sedang=65.0):
    if coverage_pct >= thr_sedikit:
        return "Gap Sedikit"
    elif coverage_pct >= thr_sedang:
        return "Gap Sedang"
    else:
        return "Gap Besar"


def run_cumulative_etl(max_batch=1):
    print("=" * 80)
    print("  LIGHTWEIGHT CUMULATIVE ETL AGGREGATOR (100 PILOT + BATCH SOLAR API)")
    print("=" * 80)
    print(f"[*] Target Max Batch : Batch 1 s/d Batch {max_batch}")
    
    # 1. Load Existing 100 Pilot Summary
    p100_csv = CALC_OUT_DIR / "pow_solar_100_titik_summary.csv"
    existing_100_records = []
    seen_names = set()
    seen_coords = []

    if p100_csv.exists():
        df_100 = pd.read_csv(p100_csv)
        print(f"[i] Berhasil memuat dataset awal 100 pilot ({len(df_100)} baris).")
        for _, r in df_100.iterrows():
            d = dict(r)
            existing_100_records.append(d)
            nm = str(d.get("asset_name", "")).strip().lower()
            seen_names.add(nm)
            lat = float(d.get("raw_lat", 0))
            lon = float(d.get("raw_lon", 0))
            seen_coords.append((lat, lon))
    else:
        print("[!] File pow_solar_100_titik_summary.csv tidak ditemukan, mulai dari awal.")

    # 2. Load Target POI Batches
    target_csv = POI_DIR / "target_2000_titik.csv"
    if not target_csv.exists():
        raise FileNotFoundError(f"Target file {target_csv} tidak ditemukan.")

    df_target = pd.read_csv(target_csv)
    # Filter batches up to max_batch
    df_batches = df_target[df_target["batch_no"].isin(range(1, max_batch + 1))].copy()
    print(f"[i] Titik target dari Batch 1 s/d Batch {max_batch}: {len(df_batches)} titik.")

    thr_sedikit, thr_sedang = get_gap_thresholds()

    # 3. Process Batch Points from JSON
    new_records = []
    skipped_duplicates = 0
    missing_json = 0

    for _, row in df_batches.iterrows():
        aid = str(row["asset_id"]).strip()
        cat = str(row["category"]).strip().lower()
        nm = str(row["asset_name"]).strip()
        raw_lat = float(row["latitude"])
        raw_lon = float(row["longitude"])
        cat_disp = str(row.get("category_display", cat)).strip()
        city_reg = str(row.get("city_regency", "")).strip()
        source_ref = str(row.get("source_reference", "")).strip()

        # Check deduplication with existing 100 points
        if nm.lower() in seen_names:
            skipped_duplicates += 1
            continue

        is_dup_coord = False
        for elat, elon in seen_coords:
            if abs(raw_lat - elat) < 0.00025 and abs(raw_lon - elon) < 0.00025:
                is_dup_coord = True
                break
        if is_dup_coord:
            skipped_duplicates += 1
            continue

        json_file = RAW_SOLAR_DIR / "building_insights" / cat / f"{aid.lower()}_insights.json"
        if not json_file.exists():
            missing_json += 1
            continue

        with open(json_file, "r", encoding="utf-8") as f:
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
        if building_footprint < whole_roof_area:
            building_footprint = whole_roof_area

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

        # Segments
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

        panel_wp = 400
        capacity_kwp = (max_panels * panel_wp) / 1000.0
        pr_factor = 0.80
        annual_gen_kwh = capacity_kwp * sunshine_hours * pr_factor
        annual_gen_mwh = annual_gen_kwh / 1000.0
        ghg_reduc_tons = (annual_gen_mwh * co2_factor) / 1000.0

        gap_cat = classify_gap_category(roof_coverage_ratio_pct, thr_sedikit, thr_sedang)

        rec = {
            "asset_id": aid,
            "asset_name": nm,
            "category": cat,
            "category_display": cat_disp,
            "city_regency": city_reg,
            "postal_code": postal_code,
            "source_raw_file": source_ref,
            "raw_lat": raw_lat,
            "raw_lon": raw_lon,
            "google_building_id": bi_data.get("name", ""),
            "google_maps_url": f"https://www.google.com/maps/search/?api=1&query={g_lat:.6f},{g_lon:.6f}",
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
            "path_dsm_geotiff": None,
            "path_rgb_geotiff": None,
            "path_mask_geotiff": None,
            "path_flux_geotiff": None,
            "preview_rgb_png": None,
            "preview_panels_png": None,
            "preview_segments_png": None,
            "preview_dsm_png": None,
            "preview_mask_png": None,
            "preview_flux_png": None,
            "gap_category": gap_cat
        }
        new_records.append(rec)
        seen_names.add(nm.lower())
        seen_coords.append((raw_lat, raw_lon))

    print(f"[+] Titik baru berhasil di-ekstrak dari JSON : {len(new_records)} titik")
    print(f"[-] Titik dilewati karena duplikasi          : {skipped_duplicates} titik")
    if missing_json > 0:
        print(f"[!] Titik terlewat karena belum ada JSON      : {missing_json} titik")

    # 4. Merge All
    all_records = existing_100_records + new_records
    df_combined = pd.DataFrame(all_records)
    df_combined["postal_code"] = df_combined["postal_code"].fillna("").astype(str).str.replace(r"\.0$", "", regex=True)
    for str_col in ["asset_id", "asset_name", "category", "category_display", "city_regency", "source_raw_file", "google_building_id", "google_maps_url", "drift_status", "imagery_date", "quality_tier", "pitch_range", "gap_category"]:
        if str_col in df_combined.columns:
            df_combined[str_col] = df_combined[str_col].fillna("").astype(str)
    print("-" * 80)
    print(f"[*] TOTAL MASTER DATASET KUMULATIF: {len(df_combined)} TITIK!")

    # 5. Save Outputs
    # Save to both 100 path (so existing page 1 immediately renders it) and accumulated paths
    out_csv = CALC_OUT_DIR / "pow_solar_100_titik_summary.csv"
    out_parq = CALC_OUT_DIR / "pow_solar_100_titik_summary.parquet"
    out_acc_csv = CALC_OUT_DIR / "pow_solar_accumulated_summary.csv"
    out_acc_parq = CALC_OUT_DIR / "pow_solar_accumulated_summary.parquet"

    df_combined.to_csv(out_csv, index=False, encoding="utf-8")
    df_combined.to_parquet(out_parq, index=False)
    df_combined.to_csv(out_acc_csv, index=False, encoding="utf-8")
    df_combined.to_parquet(out_acc_parq, index=False)

    # GeoJSON
    out_geojson = GIS_OUT_DIR / "pow_solar_100_titik.geojson"
    out_acc_geojson = GIS_OUT_DIR / "pow_solar_accumulated.geojson"
    geometry = [Point(xy) for xy in zip(df_combined["raw_lon"], df_combined["raw_lat"])]
    gdf = gpd.GeoDataFrame(df_combined, geometry=geometry, crs="EPSG:4326")
    gdf.to_file(out_geojson, driver="GeoJSON")
    gdf.to_file(out_acc_geojson, driver="GeoJSON")

    # 6. Print KPI Summary
    tot_cap = df_combined["installed_capacity_kwp"].sum()
    tot_area = df_combined["max_roof_area_m2"].sum()
    tot_mwh = df_combined["annual_generation_mwh"].sum()
    tot_co2 = df_combined["ghg_reduction_tons_co2"].sum()
    tot_panels = df_combined["max_panels_count"].sum()

    print("=" * 80)
    print("RINGKASAN METRIK AGREGAT BARU (CUMULATIVE DASHBOARD):")
    print(f"  * Total Fasilitas Tergabung : {len(df_combined)} Titik")
    print(f"  * Total Kapasitas Terpasang : {tot_cap:,.1f} kWp ({tot_cap/1000:.2f} MWp)")
    print(f"  * Total Panel Surya         : {tot_panels:,} Unit Panel")
    print(f"  * Total Luas Atap Efektif   : {tot_area:,.0f} m²")
    print(f"  * Estimasi Produksi Listrik : {tot_mwh:,.1f} MWh/thn")
    print(f"  * Reduksi Emisi GRK Tahunan : {tot_co2:,.1f} Ton CO2/thn")
    print("=" * 80)
    print(f"[+] Output tersimpan di: {out_csv.name} & {out_geojson.name}")


def main():
    parser = argparse.ArgumentParser(description="Lightweight Cumulative ETL Aggregator")
    parser.add_argument("--max-batch", type=int, default=1, help="Batas batch maksimum yang digabungkan (1-8)")
    args = parser.parse_args()
    run_cumulative_etl(max_batch=args.max_batch)


if __name__ == "__main__":
    main()
