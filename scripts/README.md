# Scripts Directory

Folder ini berisi Python scripts untuk data processing dan analysis workflow.

## 📂 Workflow Structure

Scripts dinomori sesuai urutan workflow:

### `01_data_collection/`
Scripts untuk mengumpulkan data dari berbagai sources.

**Contoh**:
- `download_transjakarta_data.py` - Download data halte dari API
- `scrape_station_info.py` - Scrape info stasiun dari website
- `download_osm_data.py` - Download infrastructure data dari OpenStreetMap

### `02_gis_processing/`
Scripts untuk GIS analysis dan spatial processing.

**Contoh**:
- `digitize_infrastructure.py` - Digitize infrastruktur dari satellite imagery
- `calculate_areas.py` - Calculate area dari GIS polygons
- `create_buffers.py` - Create buffer zones
- `spatial_join.py` - Join spatial datasets

### `03_calculation/`
Scripts untuk menghitung kapasitas dan produksi energi.

**Contoh**:
- `estimate_capacity.py` - Area → Capacity conversion
- `query_pvgis.py` - Query PVGIS API untuk production estimates
- `aggregate_results.py` - Aggregate capacity by category

### `04_financial_modeling/`
Scripts untuk analisis ekonomi.

**Contoh**:
- `calculate_npv_irr.py` - Financial metrics calculation
- `scenario_analysis.py` - Multiple scenario comparison
- `sensitivity_analysis.py` - Parameter sensitivity testing

### `05_visualization/`
Scripts untuk generate visualisasi.

**Contoh**:
- `create_potential_maps.py` - Generate interactive maps
- `create_charts.py` - Generate charts & graphs
- `export_to_pdf.py` - Export visualizations to PDF

## 🚀 How to Use

### Run Single Script

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run script
python scripts/01_data_collection/download_transjakarta_data.py
```

### Run Full Workflow

```bash
# Run all scripts in order (to be created)
python run_workflow.py
```

## 📝 Script Template

Setiap script harus mengikuti template ini:

```python
"""
Script Name: [name]
Purpose: [what it does]
Input: [input files/data]
Output: [output files/data]
Author: [name]
Date: [date]
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from src import gis_utils, solar_calc  # Import from src/

def main():
    """Main function"""
    print("Starting script...")
    
    # Your code here
    
    print("Script completed!")

if __name__ == "__main__":
    main()
```

## ⚙️ Configuration

Configuration files (API keys, paths, etc.) harus disimpan di `.env` atau `config/` folder, **TIDAK di-hardcode dalam script**.

## 🐛 Debugging

Untuk debugging, gunakan folder `debug/` (tidak masuk git) atau tambahkan verbose logging.

---

**Last Updated**: 23 Juni 2026
