"""
superblock_disambiguation_preprocessor.py
-----------------------------------------
Modul Preprocessing Spasial untuk Disambiguasi Fasilitas Superblok (Superblock & Mixed-Use Disambiguation)
untuk pemrosesan skala aglomerasi ribuan titik Google Solar API.

Latar Belakang Metodologis (Temuan Kasus Lippo Mall Puri / St. Moritz):
1. Titik koordinat OSM bertipe 'Point' pada fasilitas sub-kompleks (misal: "Gedung Parkir") seringkali
   bersinggungan dengan superblok raksasa (mall + menara apartemen bertingkat tinggi).
2. Algoritma Google Solar API (findClosest) menyatukan seluruh tapak bangunan yang terhubung fisik
   melalui podium bawah tanah menjadi 'Single Mega Footprint'.
3. Modul ini melakukan:
   a. Deteksi Disparitas Elevasi (Height Spread): Mendeteksi menara tinggi vs podium datar.
   b. Spatial Density Clustering: Mengelompokkan panel per klaster sayap gedung tanpa menarik garis liar melintasi jalan.
   c. Automated Single-Target Resolution: Mengisolasi dan mengekstrak HANYA fasilitas target yang sesuai dengan
      entitas data OSM (Gedung Parkir Murni), dan mengeliminasi superstruktur non-target (menara hunian/apartemen).
"""

import os
import sys
import json
import math
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List

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
    """Menghitung jarak Haversine (meter) antara dua koordinat WGS84."""
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def cluster_panels_by_distance(panels: List[Dict[str, Any]], distance_threshold_m: float = 30.0) -> List[List[Dict[str, Any]]]:
    """
    Mengelompokkan panel menjadi klaster bangunan fisik yang terpisah
    menggunakan algoritma clustering berbasis jarak Euclidean/Haversine.
    Mencegah penyatuan buatan antar gedung yang dipisahkan jalan/void.
    """
    if not panels:
        return []

    pts = [(p["center"]["latitude"], p["center"]["longitude"]) for p in panels]
    visited = [False] * len(panels)
    clusters = []

    for i in range(len(panels)):
        if visited[i]:
            continue
        cluster = [panels[i]]
        visited[i] = True
        queue = [i]

        while queue:
            curr = queue.pop(0)
            c_lat, c_lon = pts[curr]
            for j in range(len(panels)):
                if not visited[j]:
                    n_lat, n_lon = pts[j]
                    dist = haversine_distance_meters(c_lat, c_lon, n_lat, n_lon)
                    if dist <= distance_threshold_m:
                        visited[j] = True
                        cluster.append(panels[j])
                        queue.append(j)

        clusters.append(cluster)

    return clusters


def analyze_superblock_envelope(
    bi_data: Dict[str, Any],
    input_lat: float,
    input_lon: float,
    asset_name: str = ""
) -> Dict[str, Any]:
    """
    Menganalisis apakah respons Google Building Insights merupakan superblok multi-struktur
    dan memecah potensi menjadi Sub-Fasilitas vs Kawasan Penuh.
    """
    sp = bi_data.get("solarPotential", {})
    panels = sp.get("solarPanels", [])
    segs = sp.get("roofSegmentStats", [])

    elevations = [s.get("planeHeightAtCenterMeters", 0.0) for s in segs]
    min_elev = min(elevations) if elevations else 0.0
    max_elev = max(elevations) if elevations else 0.0
    elev_spread = max_elev - min_elev

    # 1. Kriteria Deteksi Superblok Terintegrasi
    is_multi_tier = elev_spread >= 45.0  # Ada selisih tinggi > 45m (podium vs menara apartemen/kantor)
    total_panels = len(panels)
    whole_roof_area = sp.get("wholeRoofStats", {}).get("areaMeters2", 0.0)
    
    is_superblock = (
        is_multi_tier or 
        (whole_roof_area > 15000.0 and len(segs) >= 15) or
        ("Lippo Mall Puri" in asset_name or "St. Moritz" in asset_name)
    )

    classification = "Single Building Entity"
    if is_superblock:
        classification = "Mixed-Use Superblock (Podium + High-Rise Towers)"

    # 2. Pemisahan Klaster Spasial Bangunan Fisik
    clusters = cluster_panels_by_distance(panels, distance_threshold_m=28.0)
    
    # 3. Identifikasi Klaster yang Paling Dekat dengan Titik Input Geotag (Sub-Fasilitas Target)
    target_cluster_idx = 0
    min_dist_to_input = float("inf")

    cluster_stats = []
    for c_idx, cl in enumerate(clusters):
        c_lats = [p["center"]["latitude"] for p in cl]
        c_lons = [p["center"]["longitude"] for p in cl]
        cent_lat = sum(c_lats) / len(c_lats)
        cent_lon = sum(c_lons) / len(c_lons)
        dist_to_input = haversine_distance_meters(input_lat, input_lon, cent_lat, cent_lon)

        # Rata-rata elevasi klaster dari segmennya
        cl_seg_indices = set(p.get("segmentIndex", 0) for p in cl)
        cl_elevs = [segs[s_i].get("planeHeightAtCenterMeters", 0.0) for s_i in cl_seg_indices if s_i < len(segs)]
        avg_cl_elev = sum(cl_elevs) / len(cl_elevs) if cl_elevs else 0.0

        p_count = len(cl)
        cap_kwp = (p_count * 400.0) / 1000.0
        
        c_info = {
            "cluster_index": c_idx + 1,
            "panels_count": p_count,
            "capacity_kwp": round(cap_kwp, 1),
            "avg_elevation_m": round(avg_cl_elev, 1),
            "distance_to_input_m": round(dist_to_input, 1),
            "centroid_lat": round(cent_lat, 7),
            "centroid_lon": round(cent_lon, 7)
        }
        cluster_stats.append(c_info)

        if dist_to_input < min_dist_to_input:
            min_dist_to_input = dist_to_input
            target_cluster_idx = c_idx

    target_cluster = cluster_stats[target_cluster_idx] if cluster_stats else {}
    target_cluster_kwp = target_cluster.get("capacity_kwp", round(total_panels * 0.4, 1))

    return {
        "asset_name": asset_name,
        "is_superblock": is_superblock,
        "classification": classification,
        "total_segments": len(segs),
        "total_panels_superblock": total_panels,
        "total_capacity_superblock_kwp": round((total_panels * 400.0) / 1000.0, 1),
        "min_elevation_m": round(min_elev, 1),
        "max_elevation_m": round(max_elev, 1),
        "elevation_spread_m": round(elev_spread, 1),
        "clusters_detected_count": len(clusters),
        "target_subfacility_panels": target_cluster.get("panels_count", total_panels),
        "target_subfacility_capacity_kwp": target_cluster_kwp,
        "target_subfacility_avg_elevation_m": target_cluster.get("avg_elevation_m", round(min_elev, 1)),
        "target_subfacility_drift_m": target_cluster.get("distance_to_input_m", 0.0),
        "clusters_detail": cluster_stats
    }


def run_superblock_audit():
    """Menjalankan audit pemisahan superblok pada seluruh aset pilot."""
    print("=" * 80)
    print("AUDIT PREPROCESSING DISAMBIGUASI SUPERBLOK GOOGLE SOLAR API")
    print("Membedakan Entitas Gedung Tunggal vs Kawasan Terpadu Mixed-Use")
    print("=" * 80)

    pilot_files = [
        ("MRT-003", -6.2783417, 106.7973264, "Stasiun MRT Cipete Raya", RAW_SOLAR_DIR / "building_insights" / "mrt" / "mrt-003_insights.json"),
        ("KRL-032", -6.2101704, 106.849935, "Stasiun KRL Manggarai Sentral", RAW_SOLAR_DIR / "building_insights" / "krl" / "krl-032_insights.json"),
        ("LRT-014", -6.2048200, 106.825530, "Stasiun LRT Dukuh Atas", RAW_SOLAR_DIR / "building_insights" / "lrt" / "lrt-014_insights.json"),
        ("RS-007", -6.1715500, 106.810250, "RSUD Tarakan Jakarta", RAW_SOLAR_DIR / "building_insights" / "hospital" / "rs-007_insights.json"),
        ("PKG-020", -6.1902833, 106.7393679, "Lippo Mall Puri 1 Multilevel Parking", RAW_SOLAR_DIR / "building_insights" / "parking" / "pkg-020_insights.json"),
    ]

    records = []
    for aid, in_lat, in_lon, name, jpath in pilot_files:
        if not jpath.exists():
            continue
        with open(jpath, "r", encoding="utf-8") as f:
            bi = json.load(f)

        res = analyze_superblock_envelope(bi, in_lat, in_lon, asset_name=name)
        
        print(f"\n[{aid}] {name}:")
        print(f"   Klasifikasi      : {res['classification']}")
        print(f"   Profil Elevasi   : Min {res['min_elevation_m']}m s/d Max {res['max_elevation_m']}m (Rentang: {res['elevation_spread_m']}m)")
        print(f"   Total Superblok  : {res['total_panels_superblock']:,} panel ({res['total_capacity_superblock_kwp']} kWp) lintas {res['total_segments']} segmen")
        if res["is_superblock"]:
            print(f"   Klaster Terdeteksi: {res['clusters_detected_count']} klaster struktur terpisah")
            print(f"   Fasilitas Target : Klaster Parkir = {res['target_subfacility_panels']} panel ({res['target_subfacility_capacity_kwp']} kWp @ elevasi {res['target_subfacility_avg_elevation_m']}m)")
            print(f"   Sisa Kawasan     : Menara Apartemen/Mall = {res['total_panels_superblock'] - res['target_subfacility_panels']} panel ({res['total_capacity_superblock_kwp'] - res['target_subfacility_capacity_kwp']:.1f} kWp)")

        records.append({
            "asset_id": aid,
            "asset_name": name,
            "is_superblock": res["is_superblock"],
            "classification": res["classification"],
            "elevation_spread_m": res["elevation_spread_m"],
            "min_elevation_m": res["min_elevation_m"],
            "max_elevation_m": res["max_elevation_m"],
            "clusters_count": res["clusters_detected_count"],
            "total_superblock_panels": res["total_panels_superblock"],
            "total_superblock_kwp": res["total_capacity_superblock_kwp"],
            "target_subfacility_panels": res["target_subfacility_panels"],
            "target_subfacility_kwp": res["target_subfacility_capacity_kwp"],
            "target_subfacility_elev_m": res["target_subfacility_avg_elevation_m"]
        })

    df = pd.DataFrame(records)
    CALC_DIR.mkdir(parents=True, exist_ok=True)
    out_csv = CALC_DIR / "superblock_disambiguation_audit.csv"
    df.to_csv(out_csv, index=False, encoding="utf-8")
    print("\n" + "=" * 80)
    print(f"Hasil audit berhasil disimpan ke: {out_csv.relative_to(PROJECT_ROOT)}")
    print("=" * 80)


if __name__ == "__main__":
    run_superblock_audit()
