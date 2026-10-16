"""
Train Ensemble Module: Stacking Multi-Quantile Regression
Mengimplementasikan Heterogeneous Stacking Ensemble (Paper 01 & Paper 10):
- LightGBM Quantile Regressor + Scikit-Learn Gradient Boosting Quantile Regressor
- Quantiles: P10 (Konservatif), P50 (Median), P90 (Optimistis)
- Menjamin kendala monotonisitas (non-crossing quantiles: P10 <= P50 <= P90)
- Menjamin batasan batas fisik atap (roof_area <= building_footprint)
"""

import os
import joblib
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
import lightgbm as lgb

from .config import MODEL_DIR, RANDOM_STATE, QUANTILES

logger = logging.getLogger(__name__)


class RooftopQuantileEnsemble:
    """
    Model Ensemble Heterogen Berbasis Quantile Regression
    untuk memprediksi rentang probabilitas luas atap efektif layak PLTS (P10, P50, P90).
    """

    def __init__(self, random_state: int = RANDOM_STATE):
        self.random_state = random_state
        self.preprocessor = None
        self.lgb_models: Dict[float, lgb.LGBMRegressor] = {}
        self.gbr_models: Dict[float, GradientBoostingRegressor] = {}
        self.feature_columns = [
            "log_building_footprint",
            "sunshine_hours_annual",
            "latitude",
            "longitude",
            "category",
            "city_regency"
        ]

    def _build_preprocessor(self) -> ColumnTransformer:
        numeric_features = ["log_building_footprint", "sunshine_hours_annual", "latitude", "longitude"]
        categorical_features = ["category", "city_regency"]

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), numeric_features),
                ("cat", OneHotEncoder(sparse_output=False, handle_unknown="ignore"), categorical_features)
            ]
        )
        return preprocessor

    def fit(self, df_train: pd.DataFrame, y_area: np.ndarray) -> "RooftopQuantileEnsemble":
        """
        Melatih model ensemble untuk ketiga kuantil (0.10, 0.50, 0.90).
        """
        logger.info(f"Training RooftopQuantileEnsemble on {len(df_train)} ground-truth samples...")
        
        # Ekstraksi matriks fitur
        X_df = df_train[self.feature_columns].copy()
        
        # Fit preprocessor
        self.preprocessor = self._build_preprocessor()
        X_trans = self.preprocessor.fit_transform(X_df)
        
        # Target log-transformed untuk stabilitas distribusi skewness atap
        y_log = np.log1p(np.maximum(y_area, 10.0))

        for q in QUANTILES:
            logger.info(f"Fitting Base Learners for Quantile q={q:.2f}...")
            
            # Base Learner 1: LightGBM Quantile Regressor
            lgb_reg = lgb.LGBMRegressor(
                objective="quantile",
                alpha=q,
                n_estimators=120,
                learning_rate=0.04,
                num_leaves=31,
                min_child_samples=15,
                subsample=0.85,
                colsample_bytree=0.85,
                random_state=self.random_state,
                verbose=-1
            )
            lgb_reg.fit(X_trans, y_log)
            self.lgb_models[q] = lgb_reg
            
            # Base Learner 2: Gradient Boosting Quantile Regressor (Paper 10)
            gbr_reg = GradientBoostingRegressor(
                loss="quantile",
                alpha=q,
                n_estimators=100,
                learning_rate=0.05,
                max_depth=4,
                subsample=0.85,
                random_state=self.random_state
            )
            gbr_reg.fit(X_trans, y_log)
            self.gbr_models[q] = gbr_reg

        logger.info("Ensemble model training completed successfully.")
        return self

    def predict(self, df_target: pd.DataFrame) -> pd.DataFrame:
        """
        Melakukan inferensi probabilistik P10, P50, P90 terhadap dataset target.
        Mengembalikan DataFrame dengan kolom:
        ['p10_roof_area_m2', 'p50_roof_area_m2', 'p90_roof_area_m2']
        """
        if self.preprocessor is None:
            raise RuntimeError("Model belum dilatih! Jalankan .fit() terlebih dahulu.")

        X_df = df_target[self.feature_columns].copy()
        X_trans = self.preprocessor.transform(X_df)
        
        preds_log: Dict[float, np.ndarray] = {}
        for q in QUANTILES:
            pred_lgb = self.lgb_models[q].predict(X_trans)
            pred_gbr = self.gbr_models[q].predict(X_trans)
            
            # Heterogeneous Stacking Ensemble Blending: 60% LGBM + 40% GBR (Paper 10)
            preds_log[q] = 0.60 * pred_lgb + 0.40 * pred_gbr

        # Kembalikan dari log space ke m²
        p10 = np.expm1(preds_log[0.10])
        p50 = np.expm1(preds_log[0.50])
        p90 = np.expm1(preds_log[0.90])

        # Enforce Monotonicity (Non-Crossing Quantiles): P10 <= P50 <= P90
        p10 = np.minimum(p10, p50)
        p90 = np.maximum(p90, p50)
        
        # Enforce Physical Upper Bound: Atap efektif tidak boleh melampaui 95% tapak gedung
        footprints = df_target["building_footprint_m2"].to_numpy()
        upper_limit = np.maximum(footprints * 0.95, 20.0)
        
        p10 = np.clip(p10, 15.0, upper_limit)
        p50 = np.clip(p50, 18.0, upper_limit)
        p90 = np.clip(p90, 20.0, upper_limit)
        
        # Enforce final monotonicity post-clipping
        p10 = np.minimum(p10, p50)
        p90 = np.maximum(p90, p50)

        result_df = pd.DataFrame({
            "p10_roof_area_m2": np.round(p10, 2),
            "p50_roof_area_m2": np.round(p50, 2),
            "p90_roof_area_m2": np.round(p90, 2)
        }, index=df_target.index)

        return result_df

    def save(self, filepath: Path) -> None:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)
        logger.info(f"Model ensemble saved to: {filepath}")

    @classmethod
    def load(cls, filepath: Path) -> "RooftopQuantileEnsemble":
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        model = joblib.load(filepath)
        logger.info(f"Model ensemble loaded from: {filepath}")
        return model
