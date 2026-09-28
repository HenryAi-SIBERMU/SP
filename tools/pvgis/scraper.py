"""
Script untuk download solar irradiation data dari PVGIS API
- Peak Sun Hours (PSH)
- Monthly/yearly solar radiation
- Temperature data
- Optimal tilt angle

Source: PVGIS (JRC European Commission)
Tingkat Kemudahan: 🟢 SANGAT MUDAH
Estimated Time: 1 jam
"""

import requests
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Setup directories
OUTPUT_DIR = Path("data/raw/solar")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("PVGIS SOLAR DATA DOWNLOAD - JAKARTA")
print("="*60)

# ============================================================
# Jakarta 5 Areas (DKI Jakarta Only)
# ============================================================
LOCATIONS = {
    'Jakarta_Pusat': {'lat': -6.2088, 'lon': 106.8456},
    'Jakarta_Utara': {'lat': -6.1386, 'lon': 106.8636},
    'Jakarta_Selatan': {'lat': -6.2615, 'lon': 106.8106},
    'Jakarta_Timur': {'lat': -6.2250, 'lon': 106.9004},
    'Jakarta_Barat': {'lat': -6.1684, 'lon': 106.7598},
}

# ============================================================
# Function: Get PVGIS Data
# ============================================================
def get_pvgis_data(lat, lon, location_name):
    """
    Get solar data from PVGIS API
    
    Parameters:
    - lat, lon: coordinates
    - location_name: name for reference
    
    Returns:
    - dict with solar data
    """
    
    # PVGIS API endpoint
    base_url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc"
    
    params = {
        'lat': lat,
        'lon': lon,
        'peakpower': 1,  # 1 kWp untuk normalisasi
        'loss': 14,  # System loss 14% (standard)
        'mountingplace': 'free',  # Free-standing
        'angle': 10,  # Optimal tilt untuk ekuator ~10 derajat
        'aspect': 0,  # South facing (0 derajat)
        'outputformat': 'json'
    }
    
    try:
        print(f"\n[{location_name}] Fetching data...")
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract key metrics
        outputs = data['outputs']
        totals = outputs['totals']
        
        result = {
            'location': location_name,
            'latitude': lat,
            'longitude': lon,
            'yearly_pv_energy_kwh': totals['fixed']['E_y'],  # kWh/year per kWp
            'yearly_solar_irradiation_kwh_m2': totals['fixed']['H(i)_y'],  # kWh/m²/year
            'average_daily_energy_kwh': totals['fixed']['E_d'],  # kWh/day per kWp
            'average_daily_irradiation_kwh_m2': totals['fixed']['H(i)_d'],  # kWh/m²/day
            'peak_sun_hours_h': round(totals['fixed']['H(i)_d'], 2),  # PSH = kWh/m²/day
            'optimal_tilt_deg': 10,
            'system_loss_pct': 14,
        }
        
        # Monthly data
        monthly_data = []
        for month_data in outputs['monthly']['fixed']:
            monthly_data.append({
                'month': month_data['month'],
                'energy_kwh': month_data['E_m'],
                'irradiation_kwh_m2': month_data['H(i)_m'],
                'peak_sun_hours': round(month_data['H(i)_d'], 2)
            })
        
        result['monthly'] = monthly_data
        
        print(f"   ✅ Peak Sun Hours: {result['peak_sun_hours_h']} h/day")
        print(f"   ✅ Yearly Energy: {result['yearly_pv_energy_kwh']:.0f} kWh/kWp")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

# ============================================================
# Download data for all locations
# ============================================================
all_results = []

for loc_name, coords in LOCATIONS.items():
    result = get_pvgis_data(coords['lat'], coords['lon'], loc_name)
    if result:
        all_results.append(result)

# ============================================================
# Save Results
# ============================================================
if all_results:
    # 1. Save summary as CSV
    summary_data = []
    for r in all_results:
        summary_data.append({
            'Location': r['location'],
            'Latitude': r['latitude'],
            'Longitude': r['longitude'],
            'Peak_Sun_Hours_h_day': r['peak_sun_hours_h'],
            'Yearly_Energy_kWh_per_kWp': r['yearly_pv_energy_kwh'],
            'Yearly_Irradiation_kWh_m2': r['yearly_solar_irradiation_kwh_m2'],
            'Daily_Energy_kWh_per_kWp': r['average_daily_energy_kwh'],
            'Daily_Irradiation_kWh_m2': r['average_daily_irradiation_kwh_m2'],
        })
    
    df_summary = pd.DataFrame(summary_data)
    summary_file = OUTPUT_DIR / "pvgis_jakarta.csv"
    df_summary.to_csv(summary_file, index=False)
    
    print("\n" + "="*60)
    print("SUMMARY TABLE:")
    print("="*60)
    print(df_summary.to_string(index=False))
    
    # 2. Save monthly data
    monthly_data_all = []
    for r in all_results:
        for m in r['monthly']:
            monthly_data_all.append({
                'Location': r['location'],
                'Month': m['month'],
                'Energy_kWh': m['energy_kwh'],
                'Irradiation_kWh_m2': m['irradiation_kwh_m2'],
                'Peak_Sun_Hours': m['peak_sun_hours']
            })
    
    df_monthly = pd.DataFrame(monthly_data_all)
    monthly_file = OUTPUT_DIR / "pvgis_jakarta_monthly.csv"
    df_monthly.to_csv(monthly_file, index=False)
    
    # 3. Save full JSON
    json_file = OUTPUT_DIR / "pvgis_full_data.json"
    with open(json_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # ============================================================
    # Summary Statistics
    # ============================================================
    print("\n" + "="*60)
    print("KEY FINDINGS:")
    print("="*60)
    
    avg_psh = df_summary['Peak_Sun_Hours_h_day'].mean()
    min_psh = df_summary['Peak_Sun_Hours_h_day'].min()
    max_psh = df_summary['Peak_Sun_Hours_h_day'].max()
    
    print(f"\n🌞 Peak Sun Hours (PSH):")
    print(f"   - Average: {avg_psh:.2f} hours/day")
    print(f"   - Min: {min_psh:.2f} hours/day ({df_summary.loc[df_summary['Peak_Sun_Hours_h_day'].idxmin(), 'Location']})")
    print(f"   - Max: {max_psh:.2f} hours/day ({df_summary.loc[df_summary['Peak_Sun_Hours_h_day'].idxmax(), 'Location']})")
    
    avg_yearly = df_summary['Yearly_Energy_kWh_per_kWp'].mean()
    print(f"\n⚡ Energy Production:")
    print(f"   - Average: {avg_yearly:.0f} kWh/kWp/year")
    print(f"   - Range: {df_summary['Yearly_Energy_kWh_per_kWp'].min():.0f} - {df_summary['Yearly_Energy_kWh_per_kWp'].max():.0f} kWh/kWp/year")
    
    print("\n" + "="*60)
    print("FILES SAVED:")
    print("="*60)
    print(f"   📄 {summary_file.name}")
    print(f"   📄 {monthly_file.name}")
    print(f"   📄 {json_file.name}")
    print(f"\n📁 Location: {OUTPUT_DIR.absolute()}")
    
    print("\n✅ Next steps:")
    print("   1. Use PSH value untuk kalkulasi kapasitas solar panel")
    print("   2. Average PSH Jakarta: ~{:.2f} hours/day".format(avg_psh))
    print("   3. Formula: Daily Energy (kWh) = Panel Capacity (kWp) × PSH × System Efficiency")

else:
    print("\n❌ No data retrieved. Check internet connection.")
