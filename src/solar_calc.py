"""
Solar Calculation Module

Functions untuk menghitung kapasitas PLTS dan produksi energi.
"""

from typing import Dict, Tuple
import numpy as np

# Constants
DEFAULT_MODULE_EFFICIENCY = 0.20  # 20% efficiency
DEFAULT_USABLE_AREA_RATIO = 0.75  # 75% of total area
DEFAULT_KWP_PER_SQM = 0.18  # kWp per m²
DEFAULT_PEAK_SUN_HOURS = 4.7  # PSH for Jabodetabek
DEFAULT_PERFORMANCE_RATIO = 0.77  # 77% PR

def area_to_capacity(area_sqm: float, 
                     kwp_per_sqm: float = DEFAULT_KWP_PER_SQM,
                     usable_ratio: float = DEFAULT_USABLE_AREA_RATIO) -> float:
    """
    Convert area to solar capacity.
    
    Parameters:
    -----------
    area_sqm : float
        Total area in square meters
    kwp_per_sqm : float
        Kilowatt-peak per square meter (default: 0.18)
    usable_ratio : float
        Usable area ratio (default: 0.75)
        
    Returns:
    --------
    float : Capacity in kWp
    """
    usable_area = area_sqm * usable_ratio
    capacity_kwp = usable_area * kwp_per_sqm
    return capacity_kwp

def capacity_to_annual_production(capacity_kwp: float,
                                   psh: float = DEFAULT_PEAK_SUN_HOURS,
                                   pr: float = DEFAULT_PERFORMANCE_RATIO) -> float:
    """
    Calculate annual energy production from capacity.
    
    Parameters:
    -----------
    capacity_kwp : float
        Installed capacity in kWp
    psh : float
        Peak sun hours per day (default: 4.7 for Jabodetabek)
    pr : float
        Performance ratio (default: 0.77)
        
    Returns:
    --------
    float : Annual production in kWh
    """
    daily_production = capacity_kwp * psh * pr
    annual_production = daily_production * 365
    return annual_production

def estimate_full_system(area_sqm: float, 
                         kwp_per_sqm: float = DEFAULT_KWP_PER_SQM,
                         usable_ratio: float = DEFAULT_USABLE_AREA_RATIO,
                         psh: float = DEFAULT_PEAK_SUN_HOURS,
                         pr: float = DEFAULT_PERFORMANCE_RATIO) -> Dict[str, float]:
    """
    Full estimation from area to production.
    
    Parameters:
    -----------
    area_sqm : float
        Total area in square meters
    kwp_per_sqm, usable_ratio, psh, pr : float
        System parameters (use defaults if not specified)
        
    Returns:
    --------
    Dict : {
        'total_area_sqm': float,
        'usable_area_sqm': float,
        'capacity_kwp': float,
        'annual_production_kwh': float,
        'annual_production_mwh': float,
        'parameters': dict
    }
    """
    usable_area = area_sqm * usable_ratio
    capacity = area_to_capacity(area_sqm, kwp_per_sqm, usable_ratio)
    production = capacity_to_annual_production(capacity, psh, pr)
    
    return {
        'total_area_sqm': area_sqm,
        'usable_area_sqm': usable_area,
        'capacity_kwp': capacity,
        'annual_production_kwh': production,
        'annual_production_mwh': production / 1000,
        'parameters': {
            'kwp_per_sqm': kwp_per_sqm,
            'usable_ratio': usable_ratio,
            'psh': psh,
            'pr': pr
        }
    }

def co2_reduction(annual_production_kwh: float, 
                  emission_factor: float = 0.85) -> float:
    """
    Calculate CO2 reduction from solar production.
    
    Parameters:
    -----------
    annual_production_kwh : float
        Annual production in kWh
    emission_factor : float
        Grid emission factor in kg CO2/kWh (default: 0.85 for Indonesia)
        
    Returns:
    --------
    float : CO2 reduction in kg per year
    """
    return annual_production_kwh * emission_factor

# Add more solar calculation functions here
