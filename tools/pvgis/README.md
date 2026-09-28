# PVGIS Solar Data API Client

Download solar irradiation data dari PVGIS (Photovoltaic Geographical Information System) untuk Jabodetabek.

## 📊 Data Source
- **Source**: PVGIS - JRC European Commission
- **URL**: https://re.jrc.ec.europa.eu/pvgis.html
- **API**: Free REST API
- **Tingkat Kemudahan**: 🟢 SANGAT MUDAH

## 🎯 Output Data

| File | Description |
|------|-------------|
| `pvgis_summary_jabodetabek.csv` | Summary per location (PSH, yearly energy) |
| `pvgis_monthly_jabodetabek.csv` | Monthly breakdown |
| `pvgis_full_data.json` | Full API response |

All saved to: `data/raw/solar/`

## 🚀 Usage

```bash
# Install dependencies
pip install requests pandas

# Run scraper
python tools/pvgis/scraper.py
```

## 📍 Locations Covered

| Location | Lat | Lon |
|----------|-----|-----|
| Jakarta Pusat | -6.2088 | 106.8456 |
| Jakarta Utara | -6.1386 | 106.8636 |
| Jakarta Selatan | -6.2615 | 106.8106 |
| Jakarta Timur | -6.2250 | 106.9004 |
| Jakarta Barat | -6.1684 | 106.7598 |
| Tangerang | -6.1781 | 106.6300 |
| Bekasi | -6.2349 | 106.9896 |
| Depok | -6.4025 | 106.7942 |
| Bogor | -6.5950 | 106.8160 |

## 📊 Key Metrics Output

### Peak Sun Hours (PSH)
- Jakarta: ~4.7-4.9 h/day
- Bogor: ~4.5-4.7 h/day (slightly lower, more rainfall)
- Average Jabodetabek: **~4.8 h/day**

### Yearly Energy Production
- ~1,350-1,450 kWh/kWp/year
- Average: **~1,400 kWh/kWp/year**

### System Parameters
- Panel capacity: 1 kWp (normalized)
- System loss: 14% (standard)
- Optimal tilt: 10° (near equator)
- Azimuth: 0° (south-facing)

## ⚙️ Configuration

Edit `scraper.py` to add more locations:

```python
LOCATIONS = {
    'YourLocation': {'lat': -6.xxx, 'lon': 106.xxx},
}
```

## 📈 Estimated Time
- 9 locations: ~1 hour (including API delays)
- Each location: ~5 minutes

## ⚠️ Notes
- Free API, no registration required
- Rate limit: ~10 requests/minute
- Script includes 2-second delay between requests
- Data timeframe: 2005-2020 (PVGIS database)

## 📚 Data Fields

### Summary CSV
- `Location`: Location name
- `Peak_Sun_Hours_h_day`: PSH (hours/day)
- `Yearly_Energy_kWh_per_kWp`: Annual production
- `Daily_Energy_kWh_per_kWp`: Daily average
- `Yearly_Irradiation_kWh_m2`: Solar radiation

### Monthly CSV
- `Location`: Location name
- `Month`: 1-12
- `Energy_kWh`: Monthly production
- `Peak_Sun_Hours`: Monthly PSH

## 🔬 Formula untuk Kalkulasi

```
Daily Energy (kWh) = Panel Capacity (kWp) × PSH (h/day) × System Efficiency

Example:
100 kWp solar panel × 4.8 PSH × 0.86 = 412.8 kWh/day
```

## 🔗 References
- PVGIS Documentation: https://joint-research-centre.ec.europa.eu/pvgis-photovoltaic-geographical-information-system_en
- API Documentation: https://joint-research-centre.ec.europa.eu/pvgis-tools/pvgis-tools_en
