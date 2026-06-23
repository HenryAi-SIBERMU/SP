"""
Financial Analysis Module

Functions untuk analisis kelayakan ekonomi PLTS.
"""

import numpy as np
from typing import List, Dict, Tuple

def calculate_npv(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Net Present Value.
    
    Parameters:
    -----------
    cash_flows : List[float]
        List of cash flows for each year (year 0 = initial investment as negative)
    discount_rate : float
        Discount rate (e.g., 0.08 for 8%)
        
    Returns:
    --------
    float : NPV in currency units
    """
    npv = sum(cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows))
    return npv

def calculate_irr(cash_flows: List[float], initial_guess: float = 0.1) -> float:
    """
    Calculate Internal Rate of Return.
    
    Parameters:
    -----------
    cash_flows : List[float]
        List of cash flows for each year
    initial_guess : float
        Initial guess for IRR
        
    Returns:
    --------
    float : IRR as decimal (e.g., 0.12 for 12%)
    """
    return np.irr(cash_flows)

def calculate_payback_period(cash_flows: List[float]) -> float:
    """
    Calculate simple payback period.
    
    Parameters:
    -----------
    cash_flows : List[float]
        List of cash flows for each year
        
    Returns:
    --------
    float : Payback period in years
    """
    cumulative = np.cumsum(cash_flows)
    payback_years = np.where(cumulative > 0)[0]
    
    if len(payback_years) == 0:
        return float('inf')  # Never pays back
    
    return payback_years[0]

def lcoe(capex: float, 
         annual_production_kwh: float,
         opex_annual: float,
         lifetime_years: int = 25,
         discount_rate: float = 0.08) -> float:
    """
    Calculate Levelized Cost of Energy.
    
    Parameters:
    -----------
    capex : float
        Capital expenditure (initial investment)
    annual_production_kwh : float
        Annual energy production in kWh
    opex_annual : float
        Annual operational expenditure
    lifetime_years : int
        System lifetime in years (default: 25)
    discount_rate : float
        Discount rate (default: 0.08)
        
    Returns:
    --------
    float : LCOE in currency per kWh
    """
    # Present value of costs
    pv_capex = capex
    pv_opex = sum(opex_annual / (1 + discount_rate)**t for t in range(1, lifetime_years + 1))
    total_pv_cost = pv_capex + pv_opex
    
    # Present value of energy production
    pv_energy = sum(annual_production_kwh / (1 + discount_rate)**t for t in range(1, lifetime_years + 1))
    
    lcoe_value = total_pv_cost / pv_energy
    return lcoe_value

def solar_financial_analysis(capacity_kwp: float,
                             annual_production_kwh: float,
                             capex_per_kwp: float = 18_000_000,  # Rp 18 juta/kWp for carport
                             electricity_tariff: float = 1_467,  # Rp 1,467/kWh (PLN tariff)
                             opex_percent: float = 0.02,  # 2% of CAPEX per year
                             lifetime_years: int = 25,
                             discount_rate: float = 0.08) -> Dict:
    """
    Comprehensive financial analysis for solar PV system.
    
    Parameters:
    -----------
    capacity_kwp : float
        System capacity in kWp
    annual_production_kwh : float
        Annual energy production
    capex_per_kwp : float
        Capital cost per kWp (default: Rp 18 million for carport)
    electricity_tariff : float
        Electricity tariff in Rp/kWh (default: Rp 1,467)
    opex_percent : float
        OPEX as percentage of CAPEX (default: 2%)
    lifetime_years : int
        System lifetime (default: 25 years)
    discount_rate : float
        Discount rate (default: 8%)
        
    Returns:
    --------
    Dict : Financial metrics
    """
    # Calculate costs
    capex = capacity_kwp * capex_per_kwp
    opex_annual = capex * opex_percent
    
    # Calculate revenues (energy savings)
    annual_savings = annual_production_kwh * electricity_tariff
    
    # Cash flows (Year 0 = -CAPEX, Year 1-25 = Savings - OPEX)
    cash_flows = [-capex] + [(annual_savings - opex_annual) for _ in range(lifetime_years)]
    
    # Calculate metrics
    npv_value = calculate_npv(cash_flows, discount_rate)
    irr_value = calculate_irr(cash_flows)
    payback = calculate_payback_period(cash_flows)
    lcoe_value = lcoe(capex, annual_production_kwh, opex_annual, lifetime_years, discount_rate)
    
    return {
        'capacity_kwp': capacity_kwp,
        'capex': capex,
        'capex_per_kwp': capex_per_kwp,
        'opex_annual': opex_annual,
        'annual_production_kwh': annual_production_kwh,
        'annual_savings': annual_savings,
        'npv': npv_value,
        'irr': irr_value,
        'payback_period_years': payback,
        'lcoe_per_kwh': lcoe_value,
        'lifetime_years': lifetime_years,
        'discount_rate': discount_rate
    }

# Add more financial functions here
