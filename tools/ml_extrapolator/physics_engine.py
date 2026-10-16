"""
Physics Engine: Deterministic 4 Bento Metrics Generator
Mengimplementasikan formula baku fotogrametri surya dan standar IEC 61724-1:
1. Luas Atap Efektif (m²) -> Input langsung dari estimasi fisik / ML Quantile
2. Kapasitas Terpasang (kWp) -> floor(Luas / 1.785 m²) * 400 Wp / 1000
3. Produksi Listrik AC Bersih (MWh/th) -> kWp * Jam_Surya * 0.80 (PR 80%) / 1000
4. Reduksi Emisi GRK (Ton CO₂/th) -> MWh * 808.99 kg/MWh / 1000
"""

import numpy as np
import pandas as pd
from typing import Dict, Union
from .config import (
    PANEL_WP,
    PANEL_AREA_M2,
    PERFORMANCE_RATIO,
    GRID_EMISSION_FACTOR,
    ANNUAL_SUNSHINE_DEFAULT
)


def compute_metrics_single(
    roof_area_m2: float,
    sunshine_hours: float = ANNUAL_SUNSHINE_DEFAULT
) -> Dict[str, float]:
    """
    Menghitung 4 Bento Metrics deterministik untuk nilai tunggal luas atap.
    """
    if roof_area_m2 <= 0 or np.isnan(roof_area_m2):
        return {
            "roof_area_m2": 0.0,
            "max_panels_count": 0,
            "installed_capacity_kwp": 0.0,
            "annual_generation_mwh": 0.0,
            "ghg_reduction_tons_co2": 0.0
        }

    panels = int(np.floor(roof_area_m2 / PANEL_AREA_M2))
    kwp = (panels * PANEL_WP) / 1000.0
    mwh = (kwp * sunshine_hours * PERFORMANCE_RATIO) / 1000.0
    co2_tons = (mwh * GRID_EMISSION_FACTOR) / 1000.0

    return {
        "roof_area_m2": round(float(roof_area_m2), 2),
        "max_panels_count": int(panels),
        "installed_capacity_kwp": round(float(kwp), 2),
        "annual_generation_mwh": round(float(mwh), 2),
        "ghg_reduction_tons_co2": round(float(co2_tons), 2)
    }


def compute_metrics_dataframe(
    df: pd.DataFrame,
    area_col: str,
    prefix: str,
    sunshine_col: Union[str, None] = None
) -> pd.DataFrame:
    """
    Menghitung 4 Bento Metrics deterministik secara tervektorisasi pada pandas DataFrame.
    
    Args:
        df: DataFrame target
        area_col: Nama kolom luas atap efektif (m²)
        prefix: Prefix nama kolom output (misal: 'p10', 'p50', 'p90')
        sunshine_col: Kolom jam surya tahunan (opsional, fallback ke ANNUAL_SUNSHINE_DEFAULT)
    
    Returns:
        DataFrame baru dengan kolom metrik lengkap
    """
    res = df.copy()
    
    # Ambil luas atap dan clipping minimum 0
    area = np.maximum(res[area_col].fillna(0.0).to_numpy(), 0.0)
    
    # Ambil sunshine hours
    if sunshine_col and sunshine_col in res.columns:
        sunshine = res[sunshine_col].fillna(ANNUAL_SUNSHINE_DEFAULT).to_numpy()
    else:
        sunshine = np.full_like(area, ANNUAL_SUNSHINE_DEFAULT)
    
    # 1. Jumlah Panel (floor)
    panels = np.floor(area / PANEL_AREA_M2).astype(int)
    
    # 2. Kapasitas Terpasang (kWp)
    kwp = (panels * PANEL_WP) / 1000.0
    
    # 3. Produksi Listrik AC Bersih (MWh/th)
    mwh = (kwp * sunshine * PERFORMANCE_RATIO) / 1000.0
    
    # 4. Reduksi Emisi GRK (Ton CO2/th)
    co2 = (mwh * GRID_EMISSION_FACTOR) / 1000.0
    
    # Simpan ke kolom sesuai prefix
    res[f"{prefix}_roof_area_m2"] = np.round(area, 2)
    res[f"{prefix}_panels_count"] = panels
    res[f"{prefix}_installed_capacity_kwp"] = np.round(kwp, 2)
    res[f"{prefix}_annual_generation_mwh"] = np.round(mwh, 2)
    res[f"{prefix}_ghg_reduction_tons_co2"] = np.round(co2, 2)
    
    return res
