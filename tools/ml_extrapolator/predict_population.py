"""
Predict Population Module
Mengorkestrasi inferensi skala penuh ke seluruh populasi ~20.000 titik target Jabodetabek:
1. Memuat model Ensemble Quantile Regression yang telah dilatih
2. Menghasilkan selang keyakinan P10, P50, P90 untuk luas atap efektif
3. Menerapkan Physics Engine untuk menghasilkan 4 Bento Metrics lengkap
4. Menyimpan output ke Parquet dan CSV di data/processed/calculations/
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd

from .config import (
    MODEL_DIR,
    OUTPUT_PARQUET_FILE,
    OUTPUT_CSV_FILE,
    OUTPUT_METRICS_LOG
)
from .feature_extractor import (
    load_ground_truth_dataset,
    assemble_population_dataset,
    enrich_population_features
)
from .train_ensemble import RooftopQuantileEnsemble
from .physics_engine import compute_metrics_dataframe
from .spatial_cv import evaluate_spatial_blocks

logger = logging.getLogger(__name__)


def run_full_extrapolation(save_model: bool = True) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Menjalankan alur inferensi dan ekstrapolasi penuh.
    
    Returns:
        Tuple (df_extrapolated_population, audit_metrics)
    """
    logger.info("=== MEMULAI PIPELINE ML EKSTRAPOLASI 20.000 TITIK JABODETABEK ===")

    # 1. Muat Data Latih Ground-Truth (2.100 Titik)
    df_gt = load_ground_truth_dataset()
    y_gt = df_gt["max_roof_area_m2"].to_numpy()

    # 2. Evaluasi Spatial Block Cross-Validation (Paper 08)
    logger.info("Menjalankan Spatial Block Cross-Validation...")
    groups = df_gt["city_regency"].to_numpy()
    
    cv_cols = [
        "log_building_footprint", "building_footprint_m2",
        "sunshine_hours_annual", "latitude", "longitude",
        "category", "city_regency"
    ]

    cv_metrics = evaluate_spatial_blocks(
        model_builder_fn=lambda: RooftopQuantileEnsemble(),
        X=df_gt[cv_cols],
        y=y_gt,
        groups=groups,
        n_splits=5
    )

    # Simpan metrik audit ke JSON
    OUTPUT_METRICS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_METRICS_LOG, "w", encoding="utf-8") as f:
        json.dump(cv_metrics, f, indent=2)
    logger.info(f"Metrik audit Spatial CV disimpan di: {OUTPUT_METRICS_LOG}")

    # 3. Latih Ensemble Model Penuh pada Seluruh 2.100 Titik
    ensemble = RooftopQuantileEnsemble()
    ensemble.fit(df_gt, y_gt)
    
    model_save_path = MODEL_DIR / "rooftop_quantile_ensemble.joblib"
    if save_model:
        ensemble.save(model_save_path)

    # 4. Rakit Populasi Target Riil (~20.000 Titik)
    logger.info("Mengompilasi populasi target riil dari bank data OSM dan dataset resmi...")
    df_pop_raw = assemble_population_dataset(dedup_radius_meters=18.0)
    
    logger.info("Memperkaya fitur populasi target (Spatial Sunshine & Footprint Distribution)...")
    df_pop = enrich_population_features(df_pop_raw, df_gt)

    # 5. Lakukan Inferensi Prediksi Ensemble (P10, P50, P90)
    logger.info(f"Menjalankan inferensi Ensemble Multi-Quantile pada {len(df_pop)} titik...")
    pred_quantiles = ensemble.predict(df_pop)
    
    df_result = pd.concat([df_pop, pred_quantiles], axis=1)

    # 6. Terapkan Physics Engine (IEC 61724 PR 80% & Jamali Factor)
    logger.info("Menerapkan Deterministic Physics Engine pada seluruh skenario probabilitas...")
    df_result = compute_metrics_dataframe(df_result, area_col="p10_roof_area_m2", prefix="p10", sunshine_col="sunshine_hours_annual")
    df_result = compute_metrics_dataframe(df_result, area_col="p50_roof_area_m2", prefix="p50", sunshine_col="sunshine_hours_annual")
    df_result = compute_metrics_dataframe(df_result, area_col="p90_roof_area_m2", prefix="p90", sunshine_col="sunshine_hours_annual")

    # 7. Penandaan Tingkat Integritas Sumber Data (Data Lineage)
    df_result["source_tier"] = np.where(
        df_result["is_ground_truth"],
        "GOOGLE_SOLAR_API_GROUND_TRUTH",
        "ML_EXTRAPOLATED_POPULATION"
    )

    # Beri ID formal yang rapi
    asset_ids = []
    ext_counter = 1
    for idx, row in df_result.iterrows():
        if row["is_ground_truth"] and str(row.get("asset_id_seed", "")).startswith("BRT-") or str(row.get("asset_id_seed", "")).startswith("SCH-"):
            asset_ids.append(row["asset_id_seed"])
        else:
            cat_prefix = str(row["category"])[:3].upper()
            asset_ids.append(f"{cat_prefix}-EXT-{ext_counter:05d}")
            ext_counter += 1
            
    df_result["asset_id"] = asset_ids

    # Urutkan kolom agar rapi dan transparan
    primary_cols = [
        "asset_id", "asset_name", "category", "category_display", "city_regency",
        "latitude", "longitude", "source_tier", "is_ground_truth", "building_footprint_m2",
        "sunshine_hours_annual",
        # Skenario Konservatif P10
        "p10_roof_area_m2", "p10_panels_count", "p10_installed_capacity_kwp",
        "p10_annual_generation_mwh", "p10_ghg_reduction_tons_co2",
        # Skenario Median P50 (Baseline Utama)
        "p50_roof_area_m2", "p50_panels_count", "p50_installed_capacity_kwp",
        "p50_annual_generation_mwh", "p50_ghg_reduction_tons_co2",
        # Skenario Optimistis P90
        "p90_roof_area_m2", "p90_panels_count", "p90_installed_capacity_kwp",
        "p90_annual_generation_mwh", "p90_ghg_reduction_tons_co2",
        # Metadata Asal
        "source_origin"
    ]
    
    # Simpan kolom yang ada
    ordered_cols = [c for c in primary_cols if c in df_result.columns]
    remaining_cols = [c for c in df_result.columns if c not in ordered_cols]
    df_final = df_result[ordered_cols + remaining_cols]

    # 8. Simpan ke Format Kolumnar Parquet dan CSV
    OUTPUT_PARQUET_FILE.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(OUTPUT_PARQUET_FILE, index=False)
    logger.info(f"Tersimpan file Parquet: {OUTPUT_PARQUET_FILE} ({len(df_final)} rows)")
    
    df_final.to_csv(OUTPUT_CSV_FILE, index=False)
    logger.info(f"Tersimpan file CSV: {OUTPUT_CSV_FILE} ({len(df_final)} rows)")

    return df_final, cv_metrics
