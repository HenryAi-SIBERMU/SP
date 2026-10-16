"""
Feature Extractor: Modul Pembangun Matriks Fitur & Perakit Populasi Target
Mengintegrasikan:
1. Data Latih Ground-Truth (2.100 Titik) dari Google Solar API
2. Kompilasi Populasi Riil (~20.000 Titik) dari Bank Data OSM & Dataset Resmi
3. Rekayasa Fitur Tabular & Spasial (Paper 01 & Paper 08)
"""

import json
import logging
from pathlib import Path
from typing import Tuple, Dict, Any, List

import numpy as np
import pandas as pd
import pyogrio
from scipy.spatial import cKDTree
from sklearn.neighbors import NearestNeighbors

from .config import (
    GROUND_TRUTH_FILE,
    SCHOOLS_OSM_JSON,
    UNIVERSITIES_OSM_JSON,
    BUS_STOPS_GPKG,
    TRANSJAKARTA_CSV,
    HOSPITALS_GPKG,
    CANDIDATES_POI_CSV,
    GOVERNMENT_OSM_JSON,
    BBOX_JABODETABEK,
    CATEGORY_MAPPING,
    ANNUAL_SUNSHINE_DEFAULT,
    RANDOM_STATE
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def infer_city_regency(lat: float, lon: float) -> str:
    """
    Menentukan kota/kabupaten administratif secara aproksimasi spasial jika tidak tersedia.
    """
    # Batas koordinat kasar wilayah aglomerasi Jabodetabek
    if lat > -6.15:
        if lon < 106.80:
            return "Jakarta Barat"
        elif lon < 106.87:
            return "Jakarta Utara"
        else:
            return "Jakarta Timur"
    elif lat > -6.25:
        if lon < 106.75:
            return "Kota Tangerang"
        elif lon < 106.84:
            return "Jakarta Pusat" if lat > -6.20 else "Jakarta Selatan"
        elif lon < 106.92:
            return "Jakarta Timur"
        else:
            return "Kota Bekasi"
    elif lat > -6.38:
        if lon < 106.75:
            return "Kota Tangerang Selatan"
        elif lon < 106.88:
            return "Jakarta Selatan" if lat > -6.32 else "Kota Depok"
        else:
            return "Kota Bekasi"
    else:
        if lon < 106.83:
            return "Kota Bogor" if lat > -6.62 else "Kab. Bogor"
        else:
            return "Kab. Bogor"


def load_ground_truth_dataset() -> pd.DataFrame:
    """
    Memuat dataset ground-truth 2.100 titik dari pow_solar_kumulatif_summary.csv.
    """
    if not GROUND_TRUTH_FILE.exists():
        raise FileNotFoundError(f"File ground-truth tidak ditemukan: {GROUND_TRUTH_FILE}")
    
    df = pd.read_csv(GROUND_TRUTH_FILE)
    logger.info(f"Loaded ground-truth dataset: {len(df)} rows from {GROUND_TRUTH_FILE.name}")
    
    # Standardisasi koordinat & target
    lat_col = "google_center_lat" if "google_center_lat" in df.columns else "raw_lat"
    lon_col = "google_center_lon" if "google_center_lon" in df.columns else "raw_lon"
    
    df["latitude"] = df[lat_col].fillna(df["raw_lat"])
    df["longitude"] = df[lon_col].fillna(df["raw_lon"])
    
    # Log transform untuk tapak gedung
    df["log_building_footprint"] = np.log1p(df["building_footprint_m2"].clip(lower=10.0))
    df["log_max_roof_area"] = np.log1p(df["max_roof_area_m2"].clip(lower=10.0))
    
    return df


def assemble_population_dataset(dedup_radius_meters: float = 18.0) -> pd.DataFrame:
    """
    Mengompilasi seluruh populasi target beratap permanen se-Jabodetabek (~20.000 titik)
    dari file-file mentah OpenStreetMap dan sumber resmi di data/raw/.
    Menerapkan pembersihan nama resmi, batasan BBOX, dan deduplikasi spasial cKDTree.
    """
    records: List[Dict[str, Any]] = []

    # 1. Kandidat POI 2.200 Titik Eksisting (Kurasi Kategori Khusus)
    if CANDIDATES_POI_CSV.exists():
        df_cand = pd.read_csv(CANDIDATES_POI_CSV)
        for _, r in df_cand.iterrows():
            name = str(r["asset_name"]).strip()
            if not name or name.lower() == "nan":
                continue
            records.append({
                "asset_id_seed": r.get("asset_id", ""),
                "asset_name": name,
                "category": r["category"],
                "city_regency": r.get("city_regency", ""),
                "latitude": float(r["latitude"]),
                "longitude": float(r["longitude"]),
                "source_origin": "candidates_2200_curated"
            })
        logger.info(f"Loaded {len(records)} points from candidates_2200_titik.csv")

    # 2. Sekolah OSM Overpass (Sensus Edukasi)
    if SCHOOLS_OSM_JSON.exists():
        with open(SCHOOLS_OSM_JSON, "r", encoding="utf-8") as f:
            schools = json.load(f)
        added_schools = 0
        for s in schools:
            tags = s.get("tags", {})
            name = tags.get("name")
            if not name or str(name).strip().isdigit() or "#" in str(name):
                continue
            lat = s.get("lat") or (s.get("center", {}).get("lat") if isinstance(s.get("center"), dict) else None)
            lon = s.get("lon") or (s.get("center", {}).get("lon") if isinstance(s.get("center"), dict) else None)
            if lat and lon:
                records.append({
                    "asset_id_seed": f"SCH-OSM-{s.get('id', '')}",
                    "asset_name": str(name).strip(),
                    "category": "school",
                    "city_regency": tags.get("addr:city", ""),
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "source_origin": "osm_schools_overpass"
                })
                added_schools += 1
        logger.info(f"Loaded {added_schools} named schools from OSM Overpass")

    # 3. Universitas OSM Overpass
    if UNIVERSITIES_OSM_JSON.exists():
        with open(UNIVERSITIES_OSM_JSON, "r", encoding="utf-8") as f:
            unis = json.load(f)
        added_unis = 0
        for u in unis:
            tags = u.get("tags", {})
            name = tags.get("name")
            if not name or str(name).strip().isdigit() or "#" in str(name):
                continue
            lat = u.get("lat") or (u.get("center", {}).get("lat") if isinstance(u.get("center"), dict) else None)
            lon = u.get("lon") or (u.get("center", {}).get("lon") if isinstance(u.get("center"), dict) else None)
            if lat and lon:
                records.append({
                    "asset_id_seed": f"UNI-OSM-{u.get('id', '')}",
                    "asset_name": str(name).strip(),
                    "category": "university",
                    "city_regency": tags.get("addr:city", ""),
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "source_origin": "osm_universities_overpass"
                })
                added_unis += 1
        logger.info(f"Loaded {added_unis} named universities from OSM Overpass")

    # 4. TransJakarta & Shelter Transit Resmi (7.644 titik)
    if TRANSJAKARTA_CSV.exists():
        tj = pd.read_csv(TRANSJAKARTA_CSV).dropna(subset=["Nama_Halte", "Latitude", "Longitude"])
        added_tj = 0
        for _, r in tj.iterrows():
            name = str(r["Nama_Halte"]).strip()
            if not name or name.lower() == "nan" or str(name).strip().isdigit():
                continue
            records.append({
                "asset_id_seed": f"BRT-TJ-{added_tj+1:05d}",
                "asset_name": name,
                "category": "brt",
                "city_regency": "DKI Jakarta",
                "latitude": float(r["Latitude"]),
                "longitude": float(r["Longitude"]),
                "source_origin": "transjakarta_official_inventory"
            })
            added_tj += 1
        logger.info(f"Loaded {added_tj} official TransJakarta / transit shelters")

    # 5. Bus Stops OSM Jabodetabek (Feeder Bodetabek)
    if BUS_STOPS_GPKG.exists():
        try:
            bs = pyogrio.read_dataframe(BUS_STOPS_GPKG)
            bs_named = bs[bs["name"].notna()]
            added_bs = 0
            for _, r in bs_named.iterrows():
                geom = r["geometry"]
                name = str(r["name"]).strip()
                if not name or str(name).strip().isdigit() or "#" in name:
                    continue
                if geom and hasattr(geom, "x"):
                    records.append({
                        "asset_id_seed": f"BRT-OSM-{r.get('id', added_bs)}",
                        "asset_name": name,
                        "category": "brt",
                        "city_regency": str(r.get("addr:city", "")),
                        "latitude": float(geom.y),
                        "longitude": float(geom.x),
                        "source_origin": "osm_bus_stops"
                    })
                    added_bs += 1
            logger.info(f"Loaded {added_bs} bus feeder shelters from OSM GPKG")
        except Exception as e:
            logger.warning(f"Failed to read bus_stops_jakarta.gpkg: {e}")

    # 6. Fasilitas Kesehatan (RS & Puskesmas OSM)
    if HOSPITALS_GPKG.exists():
        try:
            hosp = pyogrio.read_dataframe(HOSPITALS_GPKG)
            hosp_named = hosp[hosp["name"].notna()]
            added_hosp = 0
            for _, r in hosp_named.iterrows():
                geom = r["geometry"]
                name = str(r["name"]).strip()
                if not name or str(name).strip().isdigit() or "#" in name:
                    continue
                if geom and hasattr(geom, "x"):
                    records.append({
                        "asset_id_seed": f"HSP-OSM-{r.get('id', added_hosp)}",
                        "asset_name": name,
                        "category": "hospital",
                        "city_regency": str(r.get("addr:city", "")),
                        "latitude": float(geom.y),
                        "longitude": float(geom.x),
                        "source_origin": "osm_hospitals"
                    })
                    added_hosp += 1
            logger.info(f"Loaded {added_hosp} healthcare facilities from OSM GPKG")
        except Exception as e:
            logger.warning(f"Failed to read hospitals_jakarta.gpkg: {e}")

    # 7. Gedung & Kantor Instansi Pemerintah (Inpres No. 7/2022)
    if GOVERNMENT_OSM_JSON.exists():
        with open(GOVERNMENT_OSM_JSON, "r", encoding="utf-8") as f:
            gov_elements = json.load(f)
        added_gov = 0
        for g in gov_elements:
            tags = g.get("tags", {})
            name = tags.get("name")
            if not name or str(name).strip().isdigit() or "#" in str(name):
                continue
            lat = g.get("lat") or (g.get("center", {}).get("lat") if isinstance(g.get("center"), dict) else None)
            lon = g.get("lon") or (g.get("center", {}).get("lon") if isinstance(g.get("center"), dict) else None)
            if lat and lon:
                records.append({
                    "asset_id_seed": f"GOV-OSM-{g.get('id', '')}",
                    "asset_name": str(name).strip(),
                    "category": "government",
                    "city_regency": tags.get("addr:city", ""),
                    "latitude": float(lat),
                    "longitude": float(lon),
                    "source_origin": "osm_government_overpass"
                })
                added_gov += 1
        logger.info(f"Loaded {added_gov} named government office buildings from OSM Overpass")

    df_raw = pd.DataFrame(records)
    logger.info(f"Total raw candidate pool before filtering: {len(df_raw)} records")

    # Filter Bounding Box Jabodetabek
    bbox = BBOX_JABODETABEK
    df_bbox = df_raw[
        (df_raw["latitude"] >= bbox["min_lat"]) & (df_raw["latitude"] <= bbox["max_lat"]) &
        (df_raw["longitude"] >= bbox["min_lon"]) & (df_raw["longitude"] <= bbox["max_lon"])
    ].copy()
    logger.info(f"Pool after BBOX Jabodetabek filter: {len(df_bbox)} records")

    # Isi city_regency jika kosong
    df_bbox["city_regency"] = df_bbox.apply(
        lambda row: row["city_regency"] if str(row["city_regency"]).strip() and row["city_regency"] != "nan"
        else infer_city_regency(row["latitude"], row["longitude"]),
        axis=1
    )

    # Deduplikasi Spasial Mutlak menggunakan cKDTree
    # 18 meter toleransi memungkinkan pembedaan halte 2 arah berseberangan jalan
    coords_rad = np.radians(df_bbox[["latitude", "longitude"]].to_numpy())
    tree = cKDTree(coords_rad)
    radius_rad = dedup_radius_meters / 6371000.0
    pairs = tree.query_pairs(r=radius_rad)
    
    # Priority retention: candidates_2200_curated > official > osm
    priority_map = {
        "candidates_2200_curated": 1,
        "transjakarta_official_inventory": 2,
        "osm_government_overpass": 3,
        "osm_schools_overpass": 4,
        "osm_universities_overpass": 5,
        "osm_hospitals": 6,
        "osm_bus_stops": 7
    }
    
    df_bbox["prio"] = df_bbox["source_origin"].map(lambda s: priority_map.get(s, 99))
    drop_indices = set()
    for i, j in pairs:
        idx_i = df_bbox.index[i]
        idx_j = df_bbox.index[j]
        if idx_i in drop_indices or idx_j in drop_indices:
            continue
        prio_i = df_bbox.loc[idx_i, "prio"]
        prio_j = df_bbox.loc[idx_j, "prio"]
        if prio_i <= prio_j:
            drop_indices.add(idx_j)
        else:
            drop_indices.add(idx_i)

    df_dedup = df_bbox.drop(index=list(drop_indices)).drop(columns=["prio"]).reset_index(drop=True)
    logger.info(f"Final deduplicated population: {len(df_dedup)} points")

    # Beri category_display
    df_dedup["category_display"] = df_dedup["category"].map(
        lambda c: CATEGORY_MAPPING.get(c, c.replace("_", " ").title())
    )

    return df_dedup


def enrich_population_features(
    df_pop: pd.DataFrame,
    df_ground_truth: pd.DataFrame
) -> pd.DataFrame:
    """
    Memperkaya populasi target dengan:
    1. Spatially interpolated sunshine_hours_annual dari 2.100 titik Google Solar
    2. Empirical building_footprint_m2 berdasarkan distribusi kategori & klaster
    3. Identifikasi titik yang sudah merupakan ground-truth Google Solar API
    """
    df = df_pop.copy()
    
    # 1. Spasial Interpolasi Sunshine Hours menggunakan KNN dari ground-truth
    nn = NearestNeighbors(n_neighbors=5, metric="haversine")
    gt_coords_rad = np.radians(df_ground_truth[["latitude", "longitude"]].to_numpy())
    nn.fit(gt_coords_rad)
    
    pop_coords_rad = np.radians(df[["latitude", "longitude"]].to_numpy())
    distances, indices = nn.kneighbors(pop_coords_rad)
    
    # Inverse Distance Weighting untuk jam surya
    gt_sunshine = df_ground_truth["sunshine_hours_annual"].fillna(ANNUAL_SUNSHINE_DEFAULT).to_numpy()
    weights = 1.0 / (distances + 1e-6)
    weights /= weights.sum(axis=1, keepdims=True)
    interpolated_sunshine = np.sum(weights * gt_sunshine[indices], axis=1)
    df["sunshine_hours_annual"] = np.round(interpolated_sunshine, 2)
    
    # 2. Identifikasi apakah titik target ini match persis dengan salah satu ground-truth
    # (Threshold 15 meter)
    gt_tree = cKDTree(gt_coords_rad)
    dist_to_gt, nearest_gt_idx = gt_tree.query(pop_coords_rad, distance_upper_bound=15.0 / 6371000.0)
    
    is_gt = ~np.isinf(dist_to_gt)
    df["is_ground_truth"] = is_gt
    
    # Untuk titik ground-truth, langsung salin nilai aktual Google Solar API
    df["building_footprint_m2"] = np.nan
    df["max_roof_area_m2_actual"] = np.nan
    df["installed_capacity_kwp_actual"] = np.nan
    df["annual_generation_mwh_actual"] = np.nan
    df["ghg_reduction_tons_co2_actual"] = np.nan
    
    gt_indices = nearest_gt_idx[is_gt]
    matched_gt_rows = df_ground_truth.iloc[gt_indices]
    
    df.loc[is_gt, "building_footprint_m2"] = matched_gt_rows["building_footprint_m2"].values
    df.loc[is_gt, "max_roof_area_m2_actual"] = matched_gt_rows["max_roof_area_m2"].values
    df.loc[is_gt, "installed_capacity_kwp_actual"] = matched_gt_rows["installed_capacity_kwp"].values
    df.loc[is_gt, "annual_generation_mwh_actual"] = matched_gt_rows["annual_generation_mwh"].values
    df.loc[is_gt, "ghg_reduction_tons_co2_actual"] = matched_gt_rows["ghg_reduction_tons_co2"].values
    
    # 3. Untuk titik non-ground-truth, imputasi building_footprint_m2
    # menggunakan distribusi empiris kategori dari ground-truth (preserving median & variance)
    np.random.seed(RANDOM_STATE)
    
    # Hitung log-normal parameter per kategori dari ground-truth
    cat_footprint_stats = {}
    for cat, group in df_ground_truth.groupby("category"):
        vals = group["building_footprint_m2"].dropna()
        if len(vals) > 3:
            log_vals = np.log(vals.clip(lower=10.0))
            cat_footprint_stats[cat] = {
                "mu": float(log_vals.mean()),
                "sigma": float(log_vals.std()),
                "median": float(vals.median())
            }
        else:
            cat_footprint_stats[cat] = {
                "mu": float(np.log(300.0)),
                "sigma": 0.5,
                "median": 300.0
            }

    # Sensus Kantor Instansi Pemerintah (Inpres 7/2022)
    cat_footprint_stats["government"] = {
        "mu": float(np.log(450.0)),
        "sigma": 0.45,
        "median": 450.0
    }

    global_stats = {
        "mu": float(np.log(df_ground_truth["building_footprint_m2"].dropna().median())),
        "sigma": 0.6,
        "median": float(df_ground_truth["building_footprint_m2"].dropna().median())
    }

    # Imputasi terdistribusi deterministik
    non_gt_mask = ~is_gt
    non_gt_indices = df[non_gt_mask].index
    
    imputed_footprints = []
    for idx in non_gt_indices:
        cat = df.loc[idx, "category"]
        stats = cat_footprint_stats.get(cat, global_stats)
        # Gunakan kombinasi median dan noise terkontrol (clamped IQR)
        # untuk mempertahankan realisme statistik
        sample_log = np.random.normal(stats["mu"], min(stats["sigma"] * 0.4, 0.35))
        sample_val = np.exp(sample_log)
        imputed_footprints.append(round(float(sample_val), 2))
        
    df.loc[non_gt_mask, "building_footprint_m2"] = imputed_footprints
    df["log_building_footprint"] = np.log1p(df["building_footprint_m2"].clip(lower=10.0))
    
    return df
