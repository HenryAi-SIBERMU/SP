"""
PLN Tariff Scraper
Get electricity tariff 2026 for Jakarta

Source: PLN website
Tingkat Kemudahan: MUDAH
Estimated Time: 1 jam
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import json

# Setup
OUTPUT_DIR = Path("data/raw/pln")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("PLN TARIFF SCRAPER - 2026")
print("="*60)

# PLN Tariff 2026 (Manual input from official source)
# Source: https://web.pln.co.id/pelanggan/tarif-tenaga-listrik
TARIFF_2026 = {
    'residential': [
        {'power_va': 450, 'tariff_rp_kwh': 415, 'category': 'R-1/TR', 'subsidy': True},
        {'power_va': 900, 'tariff_rp_kwh': 605, 'category': 'R-1/TR', 'subsidy': True},
        {'power_va': 1300, 'tariff_rp_kwh': 1352, 'category': 'R-1/TR', 'subsidy': False},
        {'power_va': 2200, 'tariff_rp_kwh': 1444.70, 'category': 'R-1/TR', 'subsidy': False},
        {'power_va': 3500, 'tariff_rp_kwh': 1444.70, 'category': 'R-2/TR', 'subsidy': False},
        {'power_va': 6600, 'tariff_rp_kwh': 1444.70, 'category': 'R-3/TR', 'subsidy': False},
    ],
    'commercial': [
        {'power_va': '6-200 kVA', 'tariff_rp_kwh': 1467.28, 'category': 'B-2/TR', 'description': 'Business'},
        {'power_va': '>200 kVA', 'tariff_rp_kwh': 1114.74, 'category': 'B-3/TM', 'description': 'Business Large'},
    ],
    'industrial': [
        {'power_va': '200-30000 kVA', 'tariff_rp_kwh': 1074.39, 'category': 'I-3/TM', 'description': 'Industry Medium'},
        {'power_va': '>30000 kVA', 'tariff_rp_kwh': 996.74, 'category': 'I-4/TT', 'description': 'Industry Large'},
    ],
    'public': [
        {'power_va': '6-200 kVA', 'tariff_rp_kwh': 1467.28, 'category': 'P-1/TR', 'description': 'Public Service'},
        {'power_va': '>200 kVA', 'tariff_rp_kwh': 1044.33, 'category': 'P-2/TM', 'description': 'Public Large'},
    ],
}

print("\n[1/3] Processing tariff data...")

# Convert to DataFrames
all_tariffs = []

for sector, tariffs in TARIFF_2026.items():
    for t in tariffs:
        row = {
            'sector': sector,
            'category': t['category'],
            'power': t['power_va'],
            'tariff_rp_kwh': t['tariff_rp_kwh'],
        }
        if 'subsidy' in t:
            row['subsidy'] = t['subsidy']
        if 'description' in t:
            row['description'] = t['description']
        all_tariffs.append(row)

df = pd.DataFrame(all_tariffs)

print(f"   OK Processed {len(df)} tariff categories")

# Save CSV
csv_file = OUTPUT_DIR / "pln_tariff_2026.csv"
df.to_csv(csv_file, index=False)
print(f"\n[2/3] Saved to: {csv_file}")

# Save JSON (full structure)
json_file = OUTPUT_DIR / "pln_tariff_2026_full.json"
with open(json_file, 'w') as f:
    json.dump(TARIFF_2026, f, indent=2)
print(f"[3/3] Saved to: {json_file}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"\nTariff Categories: {len(df)}")
print(f"\nBy Sector:")
print(df.groupby('sector')['tariff_rp_kwh'].agg(['min', 'max', 'mean']))

print("\n" + "="*60)
print("KEY TARIFFS FOR SOLAR ANALYSIS")
print("="*60)
print(f"\nResidential (R-1, 2200VA): Rp {df[df['power']==2200]['tariff_rp_kwh'].values[0]:,.0f}/kWh")
print(f"Commercial (B-2, 6-200kVA): Rp {df[df['category']=='B-2/TR']['tariff_rp_kwh'].values[0]:,.2f}/kWh")
print(f"Public (P-1, 6-200kVA):     Rp {df[df['category']=='P-1/TR']['tariff_rp_kwh'].values[0]:,.2f}/kWh")

print("\n" + "="*60)
print("FILES SAVED:")
print("="*60)
print(f"   {csv_file.name}")
print(f"   {json_file.name}")
print(f"\nLocation: {OUTPUT_DIR.absolute()}")

print("\nOK Next: Use tariff for ROI calculation")
print("   Formula: Savings = kWh × Tariff")
print("   Example: 1000 kWh × Rp 1,445 = Rp 1,445,000/month")
