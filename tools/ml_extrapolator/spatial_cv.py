"""
Spatial Cross-Validation Module
Mengimplementasikan Spatial Block Cross-Validation (Paper 08 - Kuriyama et al.)
untuk mengevaluasi performa generalisasi model pada wilayah geografis yang belum terlihat
serta mencegah kebocoran autokorelasi spasial (Spatial Autocorrelation Leakage).
"""

import logging
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

logger = logging.getLogger(__name__)


def evaluate_spatial_blocks(
    model_builder_fn,
    X: pd.DataFrame,
    y: np.ndarray,
    groups: np.ndarray,
    n_splits: int = 5
) -> Dict[str, Any]:
    """
    Melakukan evaluasi Spatial Block Cross-Validation.
    
    Args:
        model_builder_fn: Fungsi yang mengembalikan dictionary model {'p10': model, 'p50': model, 'p90': model}
        X: Matriks fitur input
        y: Target aktual (max_roof_area_m2)
        groups: Label grup spasial (misal: city_regency atau spatial grid block)
        n_splits: Jumlah fold validasi spasial
    
    Returns:
        Dictionary metrik evaluasi komprehensif
    """
    gkf = GroupKFold(n_splits=n_splits)
    
    oof_p10 = np.zeros(len(y))
    oof_p50 = np.zeros(len(y))
    oof_p90 = np.zeros(len(y))
    
    fold_r2: List[float] = []
    fold_mae: List[float] = []
    fold_rmse: List[float] = []
    
    for fold, (train_idx, val_idx) in enumerate(gkf.split(X, y, groups=groups)):
        X_train, y_train = X.iloc[train_idx], y[train_idx]
        X_val, y_val = X.iloc[val_idx], y[val_idx]
        
        ensemble = model_builder_fn()
        ensemble.fit(X_train, y_train)
        
        pred_df = ensemble.predict(X_val)
        pred_p10 = pred_df["p10_roof_area_m2"].to_numpy()
        pred_p50 = pred_df["p50_roof_area_m2"].to_numpy()
        pred_p90 = pred_df["p90_roof_area_m2"].to_numpy()
        
        oof_p10[val_idx] = pred_p10
        oof_p50[val_idx] = pred_p50
        oof_p90[val_idx] = pred_p90
        
        r2 = r2_score(y_val, pred_p50)
        mae = mean_absolute_error(y_val, pred_p50)
        rmse = root_mean_squared_error(y_val, pred_p50)
        
        fold_r2.append(float(r2))
        fold_mae.append(float(mae))
        fold_rmse.append(float(rmse))
        
        logger.info(f"Spatial Fold {fold+1}/{n_splits} - R²: {r2:.4f}, MAE: {mae:.2f} m², RMSE: {rmse:.2f} m²")

    # Evaluasi global Out-Of-Fold
    total_r2 = float(r2_score(y, oof_p50))
    total_mae = float(mean_absolute_error(y, oof_p50))
    total_rmse = float(root_mean_squared_error(y, oof_p50))
    
    # Kalibrasi Interval Keyakinan P10 - P90 (Nominal Target: 80% data aktual berada di antara P10 dan P90)
    in_interval = (y >= oof_p10) & (y <= oof_p90)
    empirical_coverage_pct = float(np.mean(in_interval) * 100.0)
    
    # P10 coverage (persentase data aktual >= P10, ideal: ~90%)
    p10_coverage_pct = float(np.mean(y >= oof_p10) * 100.0)
    
    # P90 coverage (persentase data aktual <= P90, ideal: ~90%)
    p90_coverage_pct = float(np.mean(y <= oof_p90) * 100.0)
    
    metrics = {
        "spatial_cv_n_splits": n_splits,
        "mean_fold_r2": float(np.mean(fold_r2)),
        "std_fold_r2": float(np.std(fold_r2)),
        "overall_oof_r2": total_r2,
        "overall_oof_mae_m2": total_mae,
        "overall_oof_rmse_m2": total_rmse,
        "nominal_interval_pct": 80.0,
        "empirical_interval_coverage_pct": empirical_coverage_pct,
        "p10_coverage_pct": p10_coverage_pct,
        "p90_coverage_pct": p90_coverage_pct,
        "fold_details": [
            {"fold": i + 1, "r2": fold_r2[i], "mae_m2": fold_mae[i], "rmse_m2": fold_rmse[i]}
            for i in range(n_splits)
        ]
    }
    
    logger.info(f"=== SPATIAL CV AUDIT SUMMARY ===")
    logger.info(f"Overall OOF R²: {total_r2:.4f}")
    logger.info(f"Overall OOF MAE: {total_mae:.2f} m² | RMSE: {total_rmse:.2f} m²")
    logger.info(f"80% Interval Coverage Rate: {empirical_coverage_pct:.2f}% (P10={p10_coverage_pct:.1f}%, P90={p90_coverage_pct:.1f}%)")
    
    return metrics
