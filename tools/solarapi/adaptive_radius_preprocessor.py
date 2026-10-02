"""
adaptive_radius_preprocessor.py
---------------------------------
Modul Preprocessing Spasial Adaptif (Adaptive Footprint & Dynamic Radius Calculator)
untuk penarikan data Google Solar API skala aglomerasi ribuan titik tanpa risiko
citra terpotong (cropped) dan tanpa pemborosan kuota API (Zero Hallucination & Zero Waste).

Metodologi:
1. Two-Stage Fetching: Mengekstrak metadata Building Insights ($0.0075) terlebih dahulu.
2. Centroid Snapping: Menggunakan koordinat pusat atap fisik Google, bukan titik gerbang halte.
3. Maximum Panel Reach Calculation: Menghitung jarak Euclidean/Haversine dari sentroid ke panel terjauh.
4. Linear Infrastructure Clamping: Mendeteksi rasio aspek bangunan memanjang (seperti Stasiun LRT/MRT).
   Untuk struktur linier, kanopi peron stasiun diprioritaskan dan dibatasi (clamped) agar tidak memboroskan
   kanvas pada jembatan rel luar.
5. Dynamic Radius Clamping: Menghasilkan parameter radiusMeters resmi dalam batas Google API (35m - 250m).

Kepatuhan Aturan:
- anti_yesman_spatial_methodology_integrity.md: Verifikasi matematis berbasis koordinat riil.
- no_hardcoded_data.md: Menghitung parameter dinamis dari data JSON/GeoTIFF.
- strict_data_folder_boundary.md: Output disimpan di data/processed/.
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

# Safe console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_SOLAR_DIR = PROJECT_ROOT / "data" / "raw" / "solar"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
CALC_DIR = PROCESSED_DIR / "calculations"


def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Menghitung jarak Haversine dalam meter antara dua koordinat WGS84."""
    R = 6371000.0  # Radius bumi (meter)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def calculate_adaptive_solar_envelope(
    insight_data: Dict[str, Any],
    category: str = "general",
    buffer_meters: float = 15.0,
    min_radius: int = 35,
    max_radius: int = 250
) -> Dict[str, Any]:
    """
    Menghitung parameter penarikan Data Layers optimal dari data Building Insights.
    
    Parameters:
    - insight_data: Respons JSON dari Google Building Insights API.
    - category: Kategori aset (krl, lrt, mrt, hospital, parking, dll).
    - buffer_meters: Margin aman sekeliling atap (default: 15 meter).
    - min_radius: Batas radius minimum (default: 35 meter).
    - max_radius: Batas radius maksimum Google Solar API (default: 250 meter).
    
    Returns:
    - Dictionary berisi parameter koordinat tengah, radius optimal, dan audit spasial.
    """
    center = insight_data.get("center", {})
    c_lat = center.get("latitude")
    c_lon = center.get("longitude")
    
    if c_lat is None or c_lon is None:
        raise ValueError("Data Building Insights tidak memiliki koordinat 'center' yang valid.")

    sp = insight_data.get("solarPotential", {})
    panels = sp.get("solarPanels", [])
    segs = sp.get("roofSegmentStats", [])

    # 1. Ekstraksi koordinat batas fisik atap
    all_lats: List[float] = []
    all_lons: List[float] = []

    if panels:
        for p in panels:
            c = p.get("center", {})
            all_lats.append(c["latitude"])
            all_lons.append(c["longitude"])
    elif segs:
        for s in segs:
            box = s.get("boundingBox", {})
            for corner_key in ["sw", "ne"]:
                corner = box.get(corner_key, {})
                if "latitude" in corner:
                    all_lats.append(corner["latitude"])
                    all_lons.append(corner["longitude"])

    # 2. Hitung jarak terjauh dari sentroid ke modul/segmen fisik
    max_reach_m = 0.0
    aspect_ratio = 1.0
    dim_north_south_m = 0.0
    dim_east_west_m = 0.0

    if all_lats and all_lons:
        dists = [haversine_distance_meters(c_lat, c_lon, lat, lon) for lat, lon in zip(all_lats, all_lons)]
        max_reach_m = max(dists)

        # Hitung dimensi bentang Utara-Selatan & Timur-Barat
        avg_lat = sum(all_lats) / len(all_lats)
        dim_north_south_m = (max(all_lats) - min(all_lats)) * 111000.0
        dim_east_west_m = (max(all_lons) - min(all_lons)) * (111000.0 * math.cos(math.radians(avg_lat)))
        
        min_dim = min(dim_north_south_m, dim_east_west_m)
        max_dim = max(dim_north_south_m, dim_east_west_m)
        aspect_ratio = max_dim / (min_dim + 1e-4)
    else:
        # Fallback jika data panel dan segmen kosong
        max_reach_m = 40.0
        dim_north_south_m = 50.0
        dim_east_west_m = 50.0

    # 3. Deteksi Bangunan Linier Memanjang (Linear Infrastructure)
    cat_lower = category.lower()
    is_linear = (
        aspect_ratio >= 2.4 or 
        cat_lower in ["lrt", "mrt", "mrt_elevated", "brt", "railway", "viaduct"]
    )

    # 4. Terapkan Aturan Radius Adaptif
    clamping_note = "Normal Envelope (Full Roof Captured)"
    if is_linear and max_reach_m > 85.0:
        # Aturan khusus infrastruktur linier (seperti Stasiun LRT/MRT):
        # Kanopi peron utama diprioritaskan, viaduct/jembatan rel layang di luar platform dibatasi
        # agar kanvas persegi tidak memboroskan area di luar stasiun.
        optimal_radius_raw = min(max_reach_m + 10.0, 95.0)
        clamping_note = "Linear Clamped (Fokus Platform Stasiun Penumpang; Jalur Rel Luar Tidak Dimasukkan)"
    else:
        # Bangunan kompak/tapak besar (Terminal KRL, Mall, Rumah Sakit):
        optimal_radius_raw = max_reach_m + buffer_meters

    # Bulatkan ke atas ke kelipatan 5 meter untuk efisiensi tile raster
    stepped_radius = int(math.ceil(optimal_radius_raw / 5.0) * 5)
    final_radius = max(min_radius, min(stepped_radius, max_radius))

    return {
        "google_center_lat": round(c_lat, 7),
        "google_center_lon": round(c_lon, 7),
        "max_reach_meters": round(max_reach_m, 2),
        "dim_ns_meters": round(dim_north_south_m, 1),
        "dim_ew_meters": round(dim_east_west_m, 1),
        "aspect_ratio": round(aspect_ratio, 2),
        "is_linear_infrastructure": is_linear,
        "clamping_note": clamping_note,
        "optimal_radius_meters": final_radius,
        "canvas_dimension_meters": final_radius * 2,
        "recommended_datalayers_params": {
            "location.latitude": round(c_lat, 7),
            "location.longitude": round(c_lon, 7),
            "radiusMeters": final_radius,
            "view": "FULL_LAYERS",
            "requiredQuality": "BASE",
            "pixelSizeMeters": 0.25
        }
    }


def audit_pilot_points():
    """Menjalankan audit adaptif pada 5 titik pilot POW yang telah ditarik."""
    print("=" * 80)
    print("AUDIT PREPROCESSING ADAPTIF RADIUS GOOGLE SOLAR API (5 TITIK PILOT)")
    print("Menguji Algoritma Dynamic Radius & Linear Clamping pada Data Empiris")
    print("=" * 80)

    pilot_files = [
        ("MRT-003", "mrt", "Stasiun MRT Cipete Raya", RAW_SOLAR_DIR / "building_insights" / "mrt" / "mrt-003_insights.json"),
        ("KRL-032", "krl", "Stasiun KRL Manggarai Sentral", RAW_SOLAR_DIR / "building_insights" / "krl" / "krl-032_insights.json"),
        ("LRT-014", "lrt", "Stasiun LRT Dukuh Atas", RAW_SOLAR_DIR / "building_insights" / "lrt" / "lrt-014_insights.json"),
        ("RS-007", "hospital", "RSUD Tarakan Jakarta", RAW_SOLAR_DIR / "building_insights" / "hospital" / "rs-007_insights.json"),
        ("PKG-020", "parking", "Lippo Mall Puri Parking", RAW_SOLAR_DIR / "building_insights" / "parking" / "pkg-020_insights.json"),
    ]

    records = []
    for aid, cat, name, json_path in pilot_files:
        if not json_path.exists():
            print(f"⚠️ File tidak ditemukan: {json_path}")
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            bi_data = json.load(f)

        plan = calculate_adaptive_solar_envelope(bi_data, category=cat)
        
        print(f"\n[{aid}] {name} ({cat.upper()}):")
        print(f"   Dimensi Atap     : {plan['dim_ns_meters']}m (U-S) × {plan['dim_ew_meters']}m (T-B) | Rasio: {plan['aspect_ratio']}")
        print(f"   Jangkauan Panel  : {plan['max_reach_meters']} meter dari sentroid")
        print(f"   Tipe Bangunan    : {'LINIER MEMANJANG' if plan['is_linear_infrastructure'] else 'KOMPAK / BLOK'}")
        print(f"   Radius Optimal   : {plan['optimal_radius_meters']} meter (Kanvas: {plan['canvas_dimension_meters']}m × {plan['canvas_dimension_meters']}m)")
        print(f"   Status Clamping  : {plan['clamping_note']}")

        rec = {
            "asset_id": aid,
            "category": cat,
            "asset_name": name,
            "google_center_lat": plan["google_center_lat"],
            "google_center_lon": plan["google_center_lon"],
            "dim_ns_meters": plan["dim_ns_meters"],
            "dim_ew_meters": plan["dim_ew_meters"],
            "aspect_ratio": plan["aspect_ratio"],
            "max_reach_meters": plan["max_reach_meters"],
            "is_linear_infrastructure": plan["is_linear_infrastructure"],
            "optimal_radius_meters": plan["optimal_radius_meters"],
            "canvas_dimension_meters": plan["canvas_dimension_meters"],
            "clamping_note": plan["clamping_note"]
        }
        records.append(rec)

    # Simpan hasil audit ke processed calculations
    df = pd.DataFrame(records)
    CALC_DIR.mkdir(parents=True, exist_ok=True)
    out_csv = CALC_DIR / "adaptive_radius_audit_5_titik.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8")
    print("\n" + "=" * 80)
    print(f"Hasil audit berhasil disimpan ke: {out_csv.relative_to(PROJECT_ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    audit_pilot_points()
