#!/usr/bin/env python3
"""
build_target_2000_poi.py
========================
Skrip Kurasi Master Dataset Target 2.000 Titik Potensi PLTS Atap Jabodetabek
Memenuhi Spesifikasi Dokumen: STRATEGI-EKSEKUSI-5-PILAR-2000-TITIK-JABODETABEK.md

PRINSIP METODOLOGI:
1. PILAR 1: Komposisi 13 Kategori Gabungan (2.000 Titik Utama + 200 Titik Buffer = 2.200 Kandidat).
2. ZERO HARDCODED: Mengekstrak dari dataset lokal terverifikasi (data/raw/) dan Overpass API terkurasi.
3. PILAR 3 BATCH MAPPING: Mengalokasikan 8 Batch @ 250 Titik secara terstruktur.
4. SPATIAL INTEGRITY: WGS84, deduplikasi spasial (jarak > 30m), boundary filter Jabodetabek.
"""

import os
import sys
import json
import time
import math
from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import requests

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

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_HEADERS = {
    "User-Agent": "CeliosSolarResearch/2.0 (contact: admin@celios.co.id; research@celios.org)"
}


def query_overpass(query_str: str, max_retries: int = 3) -> list:
    """Helper untuk mengambil data OSM via Overpass API dengan retry aman."""
    for attempt in range(max_retries):
        try:
            r = requests.post(
                OVERPASS_URL,
                data={"data": query_str},
                headers=OVERPASS_HEADERS,
                timeout=60
            )
            if r.status_code == 200:
                data = r.json()
                return data.get("elements", [])
            elif r.status_code == 429:
                time.sleep(10 * (attempt + 1))
        except Exception as e:
            time.sleep(5 * (attempt + 1))
    return []


def is_in_bbox(lat: float, lon: float) -> bool:
    """Validasi apakah koordinat berada di koridor Aglomerasi Jabodetabek."""
    return (
        BBOX_JABODETABEK["min_lat"] <= lat <= BBOX_JABODETABEK["max_lat"] and
        BBOX_JABODETABEK["min_lon"] <= lon <= BBOX_JABODETABEK["max_lon"]
    )


def determine_city(lat: float, lon: float) -> str:
    """Estimasi wilayah administratif berbasis koordinat lintang/bujur Jabodetabek."""
    # Jakarta bounds rough breakdown
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
            # DKI Jakarta sectors
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
        # Southern Jabodetabek (Depok / Bogor)
        if lat > -6.45:
            return "Kota Depok"
        elif lon < 106.85:
            return "Kota Bogor"
        else:
            return "Kab. Bogor"


def deduplicate_spatial(records: list, min_dist_m: float = 25.0) -> list:
    """Deduplikasi koordinat berdekatan dalam satu kategori agar tidak menumpuk."""
    unique = []
    for r in records:
        lat1, lon1 = r["latitude"], r["longitude"]
        too_close = False
        for u in unique:
            lat2, lon2 = u["latitude"], u["longitude"]
            # Haversine approximation
            dlat = (lat1 - lat2) * 111000
            dlon = (lon1 - lon2) * 111000 * math.cos(math.radians(lat1))
            dist = math.sqrt(dlat*dlat + dlon*dlon)
            if dist < min_dist_m:
                too_close = True
                break
        if not too_close:
            unique.append(r)
    return unique


# ─── 1. EXTRACT PARKING (TARGET 900 + 46 BUFFER = 946) ────────────────────────
def harvest_parking() -> list:
    print("[*] Mengekstrak data Parkir / MSCP dari data/raw/osm/parking_jakarta.gpkg...")
    p_file = RAW_DIR / "osm" / "parking_jakarta.gpkg"
    records = []
    if not p_file.exists():
        print(f"[!] File {p_file} tidak ditemukan!")
        return records

    gdf = gpd.read_file(p_file)
    gdf["centroid"] = gdf.geometry.centroid
    
    # Pisahkan yang punya nama dan unnamed
    named = gdf[gdf["name"].notnull()].copy()
    unnamed = gdf[gdf["name"].isnull()].copy()
    
    idx = 1
    # Proses yang bernama dulu
    for _, row in named.iterrows():
        lat = row["centroid"].y
        lon = row["centroid"].x
        if not is_in_bbox(lat, lon):
            continue
        nm = str(row["name"]).strip()
        records.append({
            "asset_name": nm,
            "category": "parking",
            "category_display": "Gedung & Area Parkir (MSCP)",
            "city_regency": determine_city(lat, lon),
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "source_reference": f"parking_jakarta.gpkg:{row['id']}"
        })
        idx += 1

    # Tambahkan unnamed dengan penamaan lokasional yang rapi
    for _, row in unnamed.iterrows():
        lat = row["centroid"].y
        lon = row["centroid"].x
        if not is_in_bbox(lat, lon):
            continue
        city = determine_city(lat, lon)
        nm = f"Area Parkir Gedung {city} #{row['id']}"
        records.append({
            "asset_name": nm,
            "category": "parking",
            "category_display": "Gedung & Area Parkir (MSCP)",
            "city_regency": city,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "source_reference": f"parking_jakarta.gpkg:{row['id']}"
        })
        idx += 1

    records = deduplicate_spatial(records, min_dist_m=30.0)
    print(f"    -> Berhasil mengekstrak {len(records)} titik Parkir unik.")
    return records[:946]


# ─── 2. EXTRACT TRANSJAKARTA (TARGET 400 + 40 BUFFER = 440) ───────────────────
def harvest_transjakarta() -> list:
    print("[*] Mengekstrak Halte TransJakarta dari data/raw/transjakarta/transjakarta_stations.csv...")
    tj_file = RAW_DIR / "transjakarta" / "transjakarta_stations.csv"
    records = []
    if not tj_file.exists():
        print(f"[!] File {tj_file} tidak ditemukan!")
        return records

    df = pd.read_csv(tj_file).dropna(subset=["Latitude", "Longitude", "Nama_Halte"])
    # Filter duplikasi nama
    df = df.drop_duplicates(subset=["Nama_Halte"]).copy()

    # Prioritaskan halte yang memiliki kata kunci 'Halte', 'Koridor', atau nama stasiun
    df["is_priority"] = df["Nama_Halte"].str.contains(r"Halte|Koridor|Stasiun|Terminal|Simpang|Flyover|Plaza|Mall", case=False, regex=True)
    df = df.sort_values(by="is_priority", ascending=False)

    for _, row in df.iterrows():
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        if not is_in_bbox(lat, lon):
            continue
        nm = str(row["Nama_Halte"]).strip()
        # Standarisasi prefix nama halte
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
        if len(records) >= 600:
            break

    records = deduplicate_spatial(records, min_dist_m=20.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Halte TransJakarta.")
    return records[:440]


# ─── 3. EXTRACT KRL (TARGET 80 + 10 BUFFER = 90) ─────────────────────────────
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
        gdf_st["centroid"] = gdf_st.geometry.centroid
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
    return records[:90]


# ─── 4. EXTRACT MRT & LRT (TARGET 40 + 5 BUFFER = 45) ─────────────────────────
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
            gdf["centroid"] = gdf.geometry.centroid
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
    return records[:45]


# ─── 5. EXTRACT HOSPITALS (TARGET 100 + 15 BUFFER = 115) ─────────────────────
def harvest_hospitals() -> list:
    print("[*] Mengekstrak Rumah Sakit & Fasilitas Medis dari hospitals_jakarta.gpkg...")
    h_file = RAW_DIR / "osm" / "hospitals_jakarta.gpkg"
    records = []
    if not h_file.exists():
        return records

    gdf = gpd.read_file(h_file).dropna(subset=["name"])
    gdf["centroid"] = gdf.geometry.centroid

    for _, row in gdf.iterrows():
        nm = str(row["name"]).strip()
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

    records = deduplicate_spatial(records, min_dist_m=50.0)
    print(f"    -> Berhasil mengekstrak {len(records)} Fasilitas Medis.")
    return records[:115]


# ─── 6. EXTRACT JPO (TARGET 30 + 5 BUFFER = 35) ──────────────────────────────
def harvest_jpo() -> list:
    print("[*] Mengekstrak Jembatan Penyeberangan Orang (JPO)...")
    records = []
    jpo_file = RAW_DIR / "jpo" / "jpo_jakarta.csv"
    if not jpo_file.exists():
        return records

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
        if len(records) >= 100:
            break

    records = deduplicate_spatial(records, min_dist_m=30.0)
    print(f"    -> Berhasil mengekstrak {len(records)} JPO bernama.")
    return records[:35]


# ─── 7. HARVEST OVERPASS CATEGORIES (EDUCATION, MALL, MARKET, STADIUM, TERMINAL, AIRPORT) ───
def harvest_overpass_categories() -> dict:
    print("[*] Menghubungi Overpass API untuk mengekstrak fasilitas pendidikan, mall, pasar, stadion, terminal & bandara...")
    query = """
    [out:json][timeout:90];
    (
      nwr["amenity"="school"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["amenity"="university"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["amenity"="college"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["shop"="mall"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["amenity"="marketplace"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["leisure"="stadium"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["leisure"="sports_centre"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["amenity"="bus_station"]["name"](-6.65, 106.55, -6.05, 107.15);
      nwr["aeroway"~"aerodrome|terminal"]["name"](-6.65, 106.55, -6.05, 107.15);
    );
    out center;
    """
    elements = query_overpass(query)
    print(f"    -> Total elemen mentah diterima dari Overpass: {len(elements)}")

    cat_map = {
        "school": [],
        "university": [],
        "mall": [],
        "market": [],
        "stadium": [],
        "terminal": [],
        "airport": []
    }

    for el in elements:
        tags = el.get("tags", {})
        nm = str(tags.get("name", "")).strip()
        if not nm:
            continue
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        if not lat or not lon or not is_in_bbox(lat, lon):
            continue

        osm_id = f"{el.get('type', 'node')}/{el.get('id', '')}"
        city = determine_city(lat, lon)

        # Kategorisasi
        amenity = tags.get("amenity", "")
        shop = tags.get("shop", "")
        leisure = tags.get("leisure", "")
        aeroway = tags.get("aeroway", "")

        if amenity in ["university", "college"] or "universitas" in nm.lower() or "institut" in nm.lower() or "politeknik" in nm.lower():
            cat_map["university"].append({
                "asset_name": nm,
                "category": "university",
                "category_display": "Universitas & Kampus",
                "city_regency": city,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })
        elif amenity == "school" or "sma" in nm.lower() or "smk" in nm.lower() or "smp" in nm.lower() or "sekolah" in nm.lower():
            cat_map["school"].append({
                "asset_name": nm,
                "category": "school",
                "category_display": "Sekolah Menengah (SMA/SMK/SMP)",
                "city_regency": city,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })
        elif shop == "mall" or "mall" in nm.lower() or "plaza" in nm.lower() or "square" in nm.lower():
            cat_map["mall"].append({
                "asset_name": nm,
                "category": "mall",
                "category_display": "Pusat Perbelanjaan / Mall",
                "city_regency": city,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })
        elif amenity == "marketplace" or "pasar" in nm.lower():
            cat_map["market"].append({
                "asset_name": nm,
                "category": "market",
                "category_display": "Pasar Tradisional",
                "city_regency": city,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })
        elif leisure in ["stadium", "sports_centre"] or "stadion" in nm.lower() or "gor" in nm.lower() or "gelanggang" in nm.lower():
            cat_map["stadium"].append({
                "asset_name": nm,
                "category": "stadium",
                "category_display": "Stadion & Arena Olahraga",
                "city_regency": city,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })
        elif amenity == "bus_station" or "terminal" in nm.lower():
            cat_map["terminal"].append({
                "asset_name": nm,
                "category": "terminal",
                "category_display": "Terminal Bus & Simpul Antarmoda",
                "city_regency": city,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })
        elif aeroway or "bandara" in nm.lower() or "airport" in nm.lower() or "terminal 1" in nm.lower() or "terminal 2" in nm.lower() or "terminal 3" in nm.lower():
            cat_map["airport"].append({
                "asset_name": nm,
                "category": "airport",
                "category_display": "Fasilitas Penunjang Bandara",
                "city_regency": city,
                "latitude": round(lat, 6),
                "longitude": round(lon, 6),
                "source_reference": f"osm_overpass:{osm_id}"
            })

    # Deduplikasi masing-masing
    for k in cat_map:
        cat_map[k] = deduplicate_spatial(cat_map[k], min_dist_m=35.0)
        print(f"    -> Kategori {k}: {len(cat_map[k])} titik terkurasi.")

    return cat_map


# ─── BATCH ASSIGNMENT LOGIC (PILAR 3: 8 BATCH @ 250 TITIK) ────────────────────
def assign_batches(df_main: pd.DataFrame) -> pd.DataFrame:
    """
    Mengalokasikan nomor Batch 1 s.d. Batch 8 (Presisi 250 titik per batch):
    * Batch 1: Klaster Rel & Simpul Transit (KRL 80, MRT/LRT 31, Terminal 30, JPO 30, Bandara 10, Halte 69) = 250 titik
    * Batch 2: Halte TransJakarta Koridor = 250 titik
    * Batch 3: Halte TransJakarta Sisa (81) + Parkir MSCP (169) = 250 titik
    * Batch 4: Gedung Parkir MSCP = 250 titik
    * Batch 5: Gedung Parkir MSCP = 250 titik
    * Batch 6: Pendidikan (Sekolah 165 + Kampus 61) + Parkir MSCP (24) = 250 titik
    * Batch 7: Fasilitas Medis (100) + Pasar Tradisional (80) + Parkir MSCP (70) = 250 titik
    * Batch 8: Mall (70) + Stadion (50) + Parkir MSCP (130) = 250 titik
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
    sch_idx = df[df["category"] == "school"].index.tolist()
    univ_idx = df[df["category"] == "university"].index.tolist()
    hosp_idx = df[df["category"] == "hospital"].index.tolist()
    mkt_idx = df[df["category"] == "market"].index.tolist()
    mall_idx = df[df["category"] == "mall"].index.tolist()
    std_idx = df[df["category"] == "stadium"].index.tolist()

    # Batch 1 (250 titik)
    b1 = krl_idx[:80] + mrt_idx[:31] + term_idx[:30] + jpo_idx[:30] + air_idx[:10] + brt_idx[:69]
    df.loc[b1, "batch_no"] = 1

    # Batch 2 (250 titik Halte TJ)
    b2 = brt_idx[69:319]
    df.loc[b2, "batch_no"] = 2

    # Batch 3 (250 titik: sisa 81 Halte TJ + 169 Parkir)
    b3 = brt_idx[319:400] + pkg_idx[:169]
    df.loc[b3, "batch_no"] = 3

    # Batch 4 (250 titik Parkir)
    b4 = pkg_idx[169:419]
    df.loc[b4, "batch_no"] = 4

    # Batch 5 (250 titik Parkir)
    b5 = pkg_idx[419:669]
    df.loc[b5, "batch_no"] = 5

    # Batch 6 (250 titik: 165 Sekolah + 61 Kampus + 24 Parkir)
    b6 = sch_idx[:165] + univ_idx[:61] + pkg_idx[669:693]
    df.loc[b6, "batch_no"] = 6

    # Batch 7 (250 titik: 100 RS + 80 Pasar + 70 Parkir)
    b7 = hosp_idx[:100] + mkt_idx[:80] + pkg_idx[693:763]
    df.loc[b7, "batch_no"] = 7

    # Batch 8 (250 titik: 70 Mall + 50 Stadion + 130 Parkir)
    b8 = mall_idx[:70] + std_idx[:50] + pkg_idx[763:893]
    df.loc[b8, "batch_no"] = 8

    return df


def main():
    print("=" * 80)
    print("  KURASI DATASET TARGET 2.000 TITIK POTENSI PLTS ATAP JABODETABEK")
    print("  Dokumen: STRATEGI-EKSEKUSI-5-PILAR-2000-TITIK-JABODETABEK.md (Pilar 1)")
    print("=" * 80)

    # 1. Ekstraksi dari Dataset Lokal
    parking_list = harvest_parking()
    brt_list = harvest_transjakarta()
    krl_list = harvest_krl()
    mrt_list = harvest_mrt_lrt()
    hosp_list = harvest_hospitals()
    jpo_list = harvest_jpo()

    # 2. Ekstraksi Kategori Pendukung via Overpass API
    overpass_data = harvest_overpass_categories()
    sch_list = overpass_data["school"]
    univ_list = overpass_data["university"]
    mall_list = overpass_data["mall"]
    mkt_list = overpass_data["market"]
    std_list = overpass_data["stadium"]
    term_list = overpass_data["terminal"]
    air_list = overpass_data["airport"]

    # 3. Alokasi Target Utama & Buffer Cadangan (Presisi 2.000 Target + 200 Buffer = 2.200 Titik)
    targets_config = [
        ("parking", "Gedung & Area Parkir (MSCP)", parking_list, 893, 0, "PKG"),
        ("brt", "Halte TransJakarta & Shelter", brt_list, 400, 25, "BRT"),
        ("school", "Sekolah Menengah (SMA/SMK/SMP)", sch_list, 165, 50, "SCH"),
        ("hospital", "Rumah Sakit & Fasilitas Medis", hosp_list, 100, 15, "RS"),
        ("krl", "Stasiun KRL Commuter Line", krl_list, 80, 2, "KRL"),
        ("market", "Pasar Tradisional", mkt_list, 80, 30, "MKT"),
        ("mall", "Pusat Perbelanjaan / Mall", mall_list, 70, 20, "MALL"),
        ("university", "Universitas & Kampus", univ_list, 61, 20, "UNIV"),
        ("stadium", "Stadion & Arena Olahraga", std_list, 50, 20, "STD"),
        ("mrt_lrt", "Stasiun MRT & LRT", mrt_list, 31, 0, "MRT"),
        ("terminal", "Terminal Bus & Simpul Antarmoda", term_list, 30, 13, "TERM"),
        ("jpo", "Jembatan Penyeberangan Orang (JPO)", jpo_list, 30, 5, "JPO"),
        ("airport", "Fasilitas Penunjang Bandara", air_list, 10, 0, "AIR"),
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
    print("[+] SUKSES: Kurasi Master Dataset 2.000 Titik Berhasil Disimpan!")
    print(f"    - Master Target 2.000 CSV    : {out_target_csv}")
    print(f"    - Master Target 2.000 GeoJSON: {out_target_geojson}")
    print(f"    - Pool Kandidat + Buffer CSV : {out_cand_csv}")
    print("=" * 80)
    print("DISTRIBUSI BATCH EKSEKUSI (8 BATCH @ 250 TITIK):")
    print(df_main["batch_no"].value_counts().sort_index().to_string())
    print("=" * 80)


if __name__ == "__main__":
    main()
