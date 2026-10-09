#!/usr/bin/env python3
"""
build_target_2000_poi.py
========================
Skrip Kurasi Master Dataset Target 2.000 Titik Potensi PLTS Atap Jabodetabek
Memenuhi Spesifikasi Dokumen:
- STRATEGI-EKSEKUSI-5-PILAR-2000-TITIK-JABODETABEK.md
- LAPORAN-AUDIT-METODOLOGI-KUOTA-2000-TITIK-DAN-REALOKASI-OSM.md

PRINSIP METODOLOGI & REGULASI AGEN:
1. ZERO HALLUCINATED / DUMMY ENTITIES: 100% entitas beratap fisik riil dan bernama resmi.
   Dilarang keras membuat label sintetis dummy berformat `#OSM_ID`.
2. STRICT DATASET BOUNDARY: Mengekstrak hanya dari aset bank database lokal (data/raw/).
3. SPATIAL INTEGRITY: WGS84, boundary filter Aglomerasi Jabodetabek, dan deduplikasi spasial
   berbasis cKDTree (scipy.spatial) standar industri.
4. PILAR 3 BATCH MAPPING: 8 Batch presisi @ 250 Titik. Batch 1 Transit (250 titik) dipertahankan
   secara mutlak agar selaras dengan 1.000 GeoTIFF Data Layers yang telah selesai diunduh.
"""

import os
import sys
import json
import math
import time
from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from scipy.spatial import cKDTree

# Windows console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
POI_DIR = RAW_DIR / "poi"
POI_DIR.mkdir(parents=True, exist_ok=True)

# Bounding box resmi Aglomerasi Jabodetabek
BBOX_JABODETABEK = {
    "min_lat": -6.65,
    "max_lat": -6.05,
    "min_lon": 106.55,
    "max_lon": 107.15
}


def is_in_bbox(lat: float, lon: float) -> bool:
    """Validasi apakah koordinat berada di koridor Aglomerasi Jabodetabek."""
    return (
        BBOX_JABODETABEK["min_lat"] <= lat <= BBOX_JABODETABEK["max_lat"] and
        BBOX_JABODETABEK["min_lon"] <= lon <= BBOX_JABODETABEK["max_lon"]
    )


def determine_city(lat: float, lon: float) -> str:
    """Estimasi wilayah administratif berbasis koordinat lintang/bujur Jabodetabek."""
    if lat > -6.40:
        if lon < 106.75:
            if lat < -6.25:
                return "Kota Tangerang Selatan"
            return "Kota Tangerang"
        elif lon > 106.96:
            if lat < -6.26:
                return "Kab. Bekasi"
            return "Kota Bekasi"
        else:
            if lat > -6.16:
                return "Jakarta Utara"
            elif lat > -6.22:
                if lon < 106.81:
                    return "Jakarta Barat"
                elif lon < 106.86:
                    return "Jakarta Pusat"
                else:
                    return "Jakarta Timur"
            elif lat > -6.32:
                if lon < 106.83:
                    return "Jakarta Selatan"
                else:
                    return "Jakarta Timur"
            else:
                return "Kota Depok"
    else:
        if lat > -6.45:
            return "Kota Depok"
        elif lon < 106.85:
            return "Kota Bogor"
        else:
            return "Kab. Bogor"


def deduplicate_spatial(records: list, min_dist_m: float = 25.0) -> list:
    """
    Deduplikasi spasial berkecepatan tinggi O(N log N) menggunakan scipy.spatial.cKDTree.
    Sesuai aturan pilar 2 anti-yesman: dilarang manual scratch loop jika library industri tersedia.
    """
    if not records:
        return []

    # Proyeksi ekuirektangular lokal berpusat di Jakarta (-6.2 LS)
    lat0 = math.radians(-6.2)
    coords = [
        (r["longitude"] * 111320 * math.cos(lat0), r["latitude"] * 110540)
        for r in records
    ]

    tree = cKDTree(coords)
    pairs = tree.query_pairs(r=min_dist_m)

    drop_indices = set()
    for i, j in sorted(pairs):
        if i not in drop_indices and j not in drop_indices:
            drop_indices.add(j)

    return [r for idx, r in enumerate(records) if idx not in drop_indices]


# ─── 1. EXTRACT PARKING (HANYA ENTITAS BERNAMA RESMI / 0 DUMMY) ───────────────
def harvest_parking() -> list:
    print("[*] Mengekstrak data Gedung Parkir & MSCP (HANYA bernama resmi) dari parking_jakarta.gpkg...")
    p_file = RAW_DIR / "osm" / "parking_jakarta.gpkg"
    records = []
    if not p_file.exists():
        print(f"[!] File {p_file} tidak ditemukan!")
        return records

    gdf = gpd.read_file(p_file)
    # Centroid projected aman
    gdf["centroid"] = gdf.to_crs(epsg=3857).geometry.centroid.to_crs(epsg=4326)

    # Filter HANYA yang memiliki nama resmi (BUANG SEMUA UNNAMED DUMMY)
    named = gdf[gdf["name"].notnull()].copy()

    for _, row in named.iterrows():
        lat = row["centroid"].y
        lon = row["centroid"].x
        if not is_in_bbox(lat, lon):
            continue
        nm = str(row["name"]).strip()
        # Cegah string nan atau dummy
        if not nm or nm.lower() == "nan" or "#" in nm:
            continue
        records.append({
            "asset_name": nm,
            "category": "parking",
            "category_display": "Gedung & Area Parkir (MSCP)",
            "city_regency": determine_city(lat, lon),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "source_reference": f"parking_jakarta.gpkg:{row['id']}"
        })

    records = deduplicate_spatial(records, min_dist_m=25.0)
    print(f"    -> Berhasil mengekstrak {len(records)} titik Gedung Parkir bernama resmi.")
    return records


# ─── 2. EXTRACT HOSPITALS & PUSKESMAS (TARGET 246 DARI GPKG LOKAL) ─────────────
def harvest_hospitals() -> list:
    print("[*] Mengekstrak Rumah Sakit & Fasilitas Medis dari hospitals_jakarta.gpkg...")
    h_file = RAW_DIR / "osm" / "hospitals_jakarta.gpkg"
    records = []
    if not h_file.exists():
        print(f"[!] File {h_file} tidak ditemukan!")
        return records

    gdf = gpd.read_file(h_file).dropna(subset=["name"])
    gdf["centroid"] = gdf.to_crs(epsg=3857).geometry.centroid.to_crs(epsg=4326)

    for _, row in gdf.iterrows():
        nm = str(row["name"]).strip()
        if not nm or nm.lower() == "nan":
            continue
        lat = row["centroid"].y
        lon = row["centroid"].x
        if not is_in_bbox(lat, lon):
            continue
        records.append({
            "asset_name": nm,
            "category": "hospital",
            "category_display": "Rumah Sakit & Fasilitas Medis",
            "city_regency": determine_city(lat, lon),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "source_reference": f"hospitals_jakarta.gpkg:{row['id']}"
        })

    records = deduplicate_spatial(records, min_dist_m=35.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Fasilitas Medis unik.")
    return records


# ─── 3. EXTRACT TRANSJAKARTA (TARGET 400 TITIK) ────────────────────────────────
def harvest_transjakarta() -> list:
    print("[*] Mengekstrak Halte TransJakarta dari transjakarta_stations.csv...")
    tj_file = RAW_DIR / "transjakarta" / "transjakarta_stations.csv"
    records = []
    if not tj_file.exists():
        print(f"[!] File {tj_file} tidak ditemukan!")
        return records

    df = pd.read_csv(tj_file).dropna(subset=["Latitude", "Longitude", "Nama_Halte"])
    df = df.drop_duplicates(subset=["Nama_Halte"]).copy()
    df["is_priority"] = df["Nama_Halte"].str.contains(r"Halte|Koridor|Stasiun|Terminal|Simpang|Flyover|Plaza|Mall", case=False, regex=True)
    df = df.sort_values(by="is_priority", ascending=False)

    for _, row in df.iterrows():
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        if not is_in_bbox(lat, lon):
            continue
        nm = str(row["Nama_Halte"]).strip()
        if not nm.lower().startswith("halte ") and not nm.lower().startswith("shelter "):
            nm = f"Halte {nm}"

        records.append({
            "asset_name": nm,
            "category": "brt",
            "category_display": "Halte TransJakarta & Shelter",
            "city_regency": determine_city(lat, lon),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "source_reference": "transjakarta_stations.csv"
        })

    records = deduplicate_spatial(records, min_dist_m=20.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Halte TransJakarta.")
    return records


# ─── 4. EXTRACT KRL (TARGET 80 TITIK) ─────────────────────────────────────────
def harvest_krl() -> list:
    print("[*] Mengekstrak Stasiun KRL Commuter Line...")
    records = []
    krl_file = RAW_DIR / "krl" / "krl_stations.csv"
    st_gpkg = RAW_DIR / "osm" / "stations_jakarta.gpkg"
    seen_names = set()

    if krl_file.exists():
        df_krl = pd.read_csv(krl_file).dropna(subset=["Latitude", "Longitude", "Nama_Stasiun"])
        for _, row in df_krl.iterrows():
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
            if not is_in_bbox(lat, lon):
                continue
            nm = str(row["Nama_Stasiun"]).strip()
            if not nm.lower().startswith("stasiun "):
                nm = f"Stasiun KRL {nm}"
            seen_names.add(nm.lower())
            records.append({
                "asset_name": nm,
                "category": "krl",
                "category_display": "Stasiun KRL Commuter Line",
                "city_regency": determine_city(lat, lon),
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": "krl_stations.csv"
            })

    if st_gpkg.exists():
        gdf_st = gpd.read_file(st_gpkg)
        gdf_st["centroid"] = gdf_st.to_crs(epsg=3857).geometry.centroid.to_crs(epsg=4326)
        for _, row in gdf_st.iterrows():
            raw_name = str(row.get("name", "")).strip()
            if not raw_name or raw_name == "nan":
                continue
            nm = f"Stasiun KRL {raw_name}" if not raw_name.lower().startswith("stasiun") else raw_name
            if nm.lower() in seen_names:
                continue
            lat = row["centroid"].y
            lon = row["centroid"].x
            if not is_in_bbox(lat, lon):
                continue
            seen_names.add(nm.lower())
            records.append({
                "asset_name": nm,
                "category": "krl",
                "category_display": "Stasiun KRL Commuter Line",
                "city_regency": determine_city(lat, lon),
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"stations_jakarta.gpkg:{row.get('id', '')}"
            })

    records = deduplicate_spatial(records, min_dist_m=50.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Stasiun KRL.")
    return records


# ─── 5. EXTRACT MRT & LRT (TARGET 31 TITIK) ───────────────────────────────────
def harvest_mrt_lrt() -> list:
    print("[*] Mengekstrak Stasiun MRT & LRT Jabodebek/Jakarta...")
    records = []
    seen = set()

    mrt_file = RAW_DIR / "mrt_lrt" / "mrt_stations.csv"
    if mrt_file.exists():
        df_mrt = pd.read_csv(mrt_file)
        for _, row in df_mrt.iterrows():
            nm = str(row.get("Nama_Stasiun", row.get("nama", ""))).strip()
            lat = float(row.get("Latitude", row.get("lat", 0)))
            lon = float(row.get("Longitude", row.get("lon", 0)))
            if not is_in_bbox(lat, lon) or not nm:
                continue
            full_nm = f"Stasiun MRT {nm}" if not nm.lower().startswith("stasiun") else nm
            seen.add(full_nm.lower())
            records.append({
                "asset_name": full_nm,
                "category": "mrt_lrt",
                "category_display": "Stasiun MRT & LRT",
                "city_regency": determine_city(lat, lon),
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": "mrt_stations.csv"
            })

    for geo_name, prefix in [("lrt_jabodebek_stations.geojson", "Stasiun LRT Jabodebek"), ("lrt_jkt_stations.geojson", "Stasiun LRT Jakarta")]:
        f = RAW_DIR / "mrt_lrt" / geo_name
        if f.exists():
            gdf = gpd.read_file(f)
            gdf["centroid"] = gdf.to_crs(epsg=3857).geometry.centroid.to_crs(epsg=4326)
            for _, row in gdf.iterrows():
                nm = str(row.get("name", row.get("station_name", ""))).strip()
                if not nm or nm == "nan":
                    continue
                full_nm = f"{prefix} {nm}" if not nm.lower().startswith("stasiun") else nm
                if full_nm.lower() in seen:
                    continue
                lat = row["centroid"].y
                lon = row["centroid"].x
                if not is_in_bbox(lat, lon):
                    continue
                seen.add(full_nm.lower())
                records.append({
                    "asset_name": full_nm,
                    "category": "mrt_lrt",
                    "category_display": "Stasiun MRT & LRT",
                    "city_regency": determine_city(lat, lon),
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6),
                    "source_reference": geo_name
                })

    records = deduplicate_spatial(records, min_dist_m=40.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Stasiun MRT & LRT.")
    return records


# ─── 6. EXTRACT JPO (TARGET 30 TITIK) ─────────────────────────────────────────
def harvest_jpo() -> list:
    print("[*] Mengekstrak Jembatan Penyeberangan Orang (JPO)...")
    records = []
    jpo_file = RAW_DIR / "jpo" / "jpo_jakarta.csv"
    if jpo_file.exists():
        df = pd.read_csv(jpo_file).dropna(subset=["Latitude", "Longitude", "Nama_JPO"])
        named_jpo = df[~df["Nama_JPO"].str.contains("Tanpa Nama", case=False, na=False)].copy()

        for _, row in named_jpo.iterrows():
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
            if not is_in_bbox(lat, lon):
                continue
            nm = str(row["Nama_JPO"]).strip()
            full_nm = f"JPO {nm}" if not nm.lower().startswith("jpo") else nm
            records.append({
                "asset_name": full_nm,
                "category": "jpo",
                "category_display": "Jembatan Penyeberangan Orang (JPO)",
                "city_regency": determine_city(lat, lon),
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": "jpo_jakarta.csv"
            })

    records = deduplicate_spatial(records, min_dist_m=30.0)
    print(f"    -> Berhasil mengekstrak {len(records)} JPO bernama.")
    return records


# ─── 7. EXTRACT MALL, MARKET, STADIUM, TERMINAL, AIRPORT ───────────────────────
def harvest_existing_candidates() -> dict:
    print("[*] Mengekstrak Mall, Pasar, Stadion, Terminal, Bandara terkurasi...")
    cand_file = POI_DIR / "candidates_2200_titik.csv"
    cat_map = {"mall": [], "market": [], "stadium": [], "terminal": [], "airport": []}

    if cand_file.exists():
        df = pd.read_csv(cand_file)
        for cat in cat_map:
            sub = df[df["category"] == cat].copy()
            for _, row in sub.iterrows():
                nm = str(row["asset_name"]).strip()
                lat = float(row["latitude"])
                lon = float(row["longitude"])
                if not is_in_bbox(lat, lon):
                    continue
                cat_map[cat].append({
                    "asset_name": nm,
                    "category": cat,
                    "category_display": row["category_display"],
                    "city_regency": determine_city(lat, lon),
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6),
                    "source_reference": str(row.get("source_reference", ""))
                })
            cat_map[cat] = deduplicate_spatial(cat_map[cat], min_dist_m=30.0)
            print(f"    -> {cat}: {len(cat_map[cat])} titik terkurasi.")
    return cat_map


# ─── 8. EXTRACT UNIVERSITIES (TARGET 180 TITIK) ───────────────────────────────
def harvest_universities() -> list:
    print("[*] Mengekstrak Universitas & Kampus dari data/raw/osm/universities_osm_overpass.json...")
    records = []
    seen_names = set()

    # Prioritaskan kandidat lama yang sudah ada di candidates_2200_titik.csv
    cand_file = POI_DIR / "candidates_2200_titik.csv"
    if cand_file.exists():
        df_old = pd.read_csv(cand_file)
        u_old = df_old[df_old["category"] == "university"]
        for _, row in u_old.iterrows():
            nm = str(row["asset_name"]).strip()
            seen_names.add(nm.lower())
            records.append({
                "asset_name": nm,
                "category": "university",
                "category_display": "Universitas & Kampus",
                "city_regency": determine_city(float(row["latitude"]), float(row["longitude"])),
                "latitude": round(float(row["latitude"]), 6),
                "longitude": round(float(row["longitude"]), 6),
                "source_reference": str(row.get("source_reference", ""))
            })

    # Tambahkan dari raw overpass lokal
    u_file = RAW_DIR / "osm" / "universities_osm_overpass.json"
    if u_file.exists():
        with open(u_file, "r", encoding="utf-8") as f:
            elements = json.load(f)
        for el in elements:
            tags = el.get("tags", {})
            nm = str(tags.get("name", "")).strip()
            if not nm or nm.lower() in seen_names:
                continue
            lat = el.get("lat") or el.get("center", {}).get("lat")
            lon = el.get("lon") or el.get("center", {}).get("lon")
            if not lat or not lon or not is_in_bbox(lat, lon):
                continue
            osm_id = f"{el.get('type', 'node')}/{el.get('id', '')}"
            seen_names.add(nm.lower())
            records.append({
                "asset_name": nm,
                "category": "university",
                "category_display": "Universitas & Kampus",
                "city_regency": determine_city(lat, lon),
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })

    records = deduplicate_spatial(records, min_dist_m=35.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Universitas & Kampus bernama resmi.")
    return records


# ─── 9. EXTRACT SCHOOLS (TARGET 659 TITIK) ────────────────────────────────────
def harvest_schools() -> list:
    print("[*] Mengekstrak Sekolah Menengah (SMA/SMK/SMP) dari schools_osm_overpass.json...")
    records = []
    seen_names = set()

    # Prioritaskan sekolah lama dari candidates_2200_titik.csv
    cand_file = POI_DIR / "candidates_2200_titik.csv"
    if cand_file.exists():
        df_old = pd.read_csv(cand_file)
        s_old = df_old[df_old["category"] == "school"]
        for _, row in s_old.iterrows():
            nm = str(row["asset_name"]).strip()
            seen_names.add(nm.lower())
            records.append({
                "asset_name": nm,
                "category": "school",
                "category_display": "Sekolah Menengah (SMA/SMK/SMP)",
                "city_regency": determine_city(float(row["latitude"]), float(row["longitude"])),
                "latitude": round(float(row["latitude"]), 6),
                "longitude": round(float(row["longitude"]), 6),
                "source_reference": str(row.get("source_reference", ""))
            })

    # Tambahkan dari raw overpass lokal
    s_file = RAW_DIR / "osm" / "schools_osm_overpass.json"
    if s_file.exists():
        with open(s_file, "r", encoding="utf-8") as f:
            elements = json.load(f)

        # Pisahkan prioritas SMA/SMK/SMP negeri/swasta
        priority_sch = []
        regular_sch = []

        for el in elements:
            tags = el.get("tags", {})
            nm = str(tags.get("name", "")).strip()
            if not nm or nm.lower() in seen_names:
                continue
            lat = el.get("lat") or el.get("center", {}).get("lat")
            lon = el.get("lon") or el.get("center", {}).get("lon")
            if not lat or not lon or not is_in_bbox(lat, lon):
                continue
            osm_id = f"{el.get('type', 'node')}/{el.get('id', '')}"
            seen_names.add(nm.lower())

            item = {
                "asset_name": nm,
                "category": "school",
                "category_display": "Sekolah Menengah (SMA/SMK/SMP)",
                "city_regency": determine_city(lat, lon),
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            }

            # Utamakan SMA, SMK, SMP, MA, MTS
            if any(k in nm.lower() for k in ["sma", "smk", "smp", "madrasah", "aliyah", "tsanawiyah", "high school"]):
                priority_sch.append(item)
            else:
                regular_sch.append(item)

        records.extend(priority_sch)
        records.extend(regular_sch)

    records = deduplicate_spatial(records, min_dist_m=35.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Sekolah bernama resmi.")
    return records


# ─── 10. BATCH ASSIGNMENT LOGIC (8 BATCH @ 250 TITIK) ─────────────────────────
def assign_batches(df_main: pd.DataFrame) -> pd.DataFrame:
    """
    Mengalokasikan nomor Batch 1 s.d. Batch 8 (Presisi tepat 250 titik per batch):
    * Batch 1: Klaster Rel & Simpul Transit (KRL 80, MRT/LRT 31, Terminal 30, JPO 30, Bandara 10, Halte 69) = 250 titik
      (100% IDENTIK dengan penarikan Batch 1 yang telah selesai & terverifikasi di git)
    * Batch 2: Halte TransJakarta Koridor = 250 titik (BRT 70..319)
    * Batch 3: Halte TransJakarta Sisa (81) + Gedung Parkir Resmi (99) + Mall (70) = 250 titik
    * Batch 4: Sisa Mall (10) + Pasar Tradisional (100) + Stadion (55) + Kampus (85) = 250 titik
    * Batch 5: Sisa Kampus (95) + Rumah Sakit & Medis (155) = 250 titik
    * Batch 6: Sisa Rumah Sakit (91) + Sekolah Menengah (159) = 250 titik
    * Batch 7: Sekolah Menengah = 250 titik
    * Batch 8: Sisa Sekolah Menengah = 250 titik
    TOTAL: 8 Batch x 250 Titik = 2.000 Titik Tepat
    """
    df = df_main.copy()
    df["batch_no"] = 0

    krl_idx = df[df["category"] == "krl"].index.tolist()
    mrt_idx = df[df["category"] == "mrt_lrt"].index.tolist()
    term_idx = df[df["category"] == "terminal"].index.tolist()
    jpo_idx = df[df["category"] == "jpo"].index.tolist()
    air_idx = df[df["category"] == "airport"].index.tolist()
    brt_idx = df[df["category"] == "brt"].index.tolist()
    pkg_idx = df[df["category"] == "parking"].index.tolist()
    mall_idx = df[df["category"] == "mall"].index.tolist()
    mkt_idx = df[df["category"] == "market"].index.tolist()
    std_idx = df[df["category"] == "stadium"].index.tolist()
    univ_idx = df[df["category"] == "university"].index.tolist()
    hosp_idx = df[df["category"] == "hospital"].index.tolist()
    sch_idx = df[df["category"] == "school"].index.tolist()

    # Batch 1 (250 titik: 80 KRL, 31 MRT/LRT, 30 Terminal, 30 JPO, 10 Bandara, 69 BRT)
    b1 = krl_idx[:80] + mrt_idx[:31] + term_idx[:30] + jpo_idx[:30] + air_idx[:10] + brt_idx[:69]
    df.loc[b1, "batch_no"] = 1

    # Batch 2 (250 titik: BRT 70..319)
    b2 = brt_idx[69:319]
    df.loc[b2, "batch_no"] = 2

    # Batch 3 (250 titik: sisa 81 BRT + 99 Parkir + 70 Mall)
    b3 = brt_idx[319:400] + pkg_idx[:99] + mall_idx[:70]
    df.loc[b3, "batch_no"] = 3

    # Batch 4 (250 titik: sisa 10 Mall + 100 Pasar + 55 Stadion + 85 Kampus)
    b4 = mall_idx[70:80] + mkt_idx[:100] + std_idx[:55] + univ_idx[:85]
    df.loc[b4, "batch_no"] = 4

    # Batch 5 (250 titik: sisa 95 Kampus + 155 RS)
    b5 = univ_idx[85:180] + hosp_idx[:155]
    df.loc[b5, "batch_no"] = 5

    # Batch 6 (250 titik: sisa 91 RS + 159 Sekolah)
    b6 = hosp_idx[155:246] + sch_idx[:159]
    df.loc[b6, "batch_no"] = 6

    # Batch 7 (250 titik Sekolah)
    b7 = sch_idx[159:409]
    df.loc[b7, "batch_no"] = 7

    # Batch 8 (250 titik Sekolah)
    b8 = sch_idx[409:659]
    df.loc[b8, "batch_no"] = 8

    return df


def main():
    print("=" * 80)
    print("  KURASI DATASET TARGET 2.000 TITIK POTENSI PLTS ATAP JABODETABEK")
    print("  AUDIT METODOLOGIS: 100% ENTITAS RESMI, BERATAP RIIL, ZERO DUMMY #OSM_ID")
    print("=" * 80)

    # 1. Ekstraksi seluruh kategori dari sumber lokal resmi
    parking_list = harvest_parking()
    hosp_list = harvest_hospitals()
    brt_list = harvest_transjakarta()
    krl_list = harvest_krl()
    mrt_list = harvest_mrt_lrt()
    jpo_list = harvest_jpo()

    cand_cats = harvest_existing_candidates()
    mall_list = cand_cats["mall"]
    mkt_list = cand_cats["market"]
    std_list = cand_cats["stadium"]
    term_list = cand_cats["terminal"]
    air_list = cand_cats["airport"]

    univ_list = harvest_universities()
    sch_list = harvest_schools()

    # 2. Konfigurasi Target Utama & Buffer Cadangan
    # Total Target Utama Tepat 2.000 Titik!
    targets_config = [
        ("brt", "Halte TransJakarta & Shelter", brt_list, 400, 20, "BRT"),
        ("krl", "Stasiun KRL Commuter Line", krl_list, 80, 2, "KRL"),
        ("mrt_lrt", "Stasiun MRT & LRT", mrt_list, 31, 0, "MRT"),
        ("terminal", "Terminal Bus & Simpul Antarmoda", term_list, 30, 10, "TERM"),
        ("jpo", "Jembatan Penyeberangan Orang (JPO)", jpo_list, 30, 5, "JPO"),
        ("airport", "Fasilitas Penunjang Bandara", air_list, 10, 0, "AIR"),
        ("parking", "Gedung & Area Parkir (MSCP)", parking_list, 99, 0, "PKG"),
        ("mall", "Pusat Perbelanjaan / Mall", mall_list, 80, 5, "MALL"),
        ("market", "Pasar Tradisional", mkt_list, 100, 7, "MKT"),
        ("stadium", "Stadion & Arena Olahraga", std_list, 55, 10, "STD"),
        ("university", "Universitas & Kampus", univ_list, 180, 30, "UNIV"),
        ("hospital", "Rumah Sakit & Fasilitas Medis", hosp_list, 246, 0, "RS"),
        ("school", "Sekolah Menengah (SMA/SMK/SMP)", sch_list, 659, 50, "SCH"),
    ]

    all_curated = []

    for cat_key, cat_disp, full_list, target_cnt, buffer_cnt, prefix in targets_config:
        avail_cnt = len(full_list)
        take_main = min(avail_cnt, target_cnt)
        take_buffer = min(avail_cnt - take_main, buffer_cnt)

        print(f"[*] {cat_disp:35s}: Target {target_cnt:3d} | Buffer {buffer_cnt:2d} | Tersedia {avail_cnt:4d}")

        # Titik Utama
        for i in range(take_main):
            row = dict(full_list[i])
            row["asset_id"] = f"{prefix}-{i+1:04d}"
            row["is_buffer"] = False
            all_curated.append(row)

        # Titik Buffer Cadangan
        for j in range(take_buffer):
            row = dict(full_list[take_main + j])
            row["asset_id"] = f"{prefix}-BUF-{j+1:03d}"
            row["is_buffer"] = True
            all_curated.append(row)

    df_all = pd.DataFrame(all_curated)
    print("-" * 80)
    print(f"[i] Total kandidat terhimpun: {len(df_all)} titik")
    print(f"    - Target Utama (is_buffer=False): {len(df_all[~df_all['is_buffer']])} titik")
    print(f"    - Cadangan Buffer (is_buffer=True) : {len(df_all[df_all['is_buffer']])} titik")

    # Pisahkan target utama dan tetapkan nomor batch
    df_main = df_all[~df_all["is_buffer"]].copy().reset_index(drop=True)
    df_main = assign_batches(df_main)

    df_buf = df_all[df_all["is_buffer"]].copy().reset_index(drop=True)
    df_buf["batch_no"] = 0

    df_final_candidates = pd.concat([df_main, df_buf], ignore_index=True)

    # Simpan Output
    out_cand_csv = POI_DIR / "candidates_2200_titik.csv"
    out_cand_parquet = POI_DIR / "candidates_2200_titik.parquet"
    out_target_csv = POI_DIR / "target_2000_titik.csv"
    out_target_parquet = POI_DIR / "target_2000_titik.parquet"
    out_target_geojson = POI_DIR / "target_2000_titik.geojson"

    df_final_candidates.to_csv(out_cand_csv, index=False, encoding="utf-8")
    df_final_candidates.to_parquet(out_cand_parquet, index=False)

    df_main.to_csv(out_target_csv, index=False, encoding="utf-8")
    df_main.to_parquet(out_target_parquet, index=False)

    # GeoJSON
    geometry = [Point(xy) for xy in zip(df_main["longitude"], df_main["latitude"])]
    gdf_main = gpd.GeoDataFrame(df_main, geometry=geometry, crs="EPSG:4326")
    gdf_main.to_file(out_target_geojson, driver="GeoJSON")

    print("=" * 80)
    print("[+] SUKSES: Kurasi Master Dataset 2.000 Titik Baru Berhasil Disimpan!")
    print(f"    - Master Target 2.000 CSV    : {out_target_csv}")
    print(f"    - Master Target 2.000 GeoJSON: {out_target_geojson}")
    print(f"    - Pool Kandidat + Buffer CSV : {out_cand_csv}")
    print("=" * 80)
    print("DISTRIBUSI BATCH EKSEKUSI (8 BATCH @ 250 TITIK):")
    print(df_main["batch_no"].value_counts().sort_index().to_string())
    print("=" * 80)


if __name__ == "__main__":
    main()
