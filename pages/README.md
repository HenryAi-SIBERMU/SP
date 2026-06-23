# Pages Directory

This directory contains all Streamlit pages for the CELIOS Solar Dashboard.

## Page Structure

Streamlit automatically discovers pages in this folder and creates navigation based on filename prefixes (numbers).

### Numbering Convention
- `0_` - Overview/landing pages
- `1-7_` - Main content pages organized by section
- `8_` - Documentation & resources

## Current Pages

### Fully Functional
- **`8_Dokumentasi_Riset.py`** ✅
  - Displays 2 markdown research documents
  - Interactive document selector
  - Download functionality
  - Custom styled rendering

### Development Placeholders
All other pages show "🚧 Sedang dalam pengembangan" placeholder:

1. **`0_Overview.py`** - Executive summary dashboard
2. **`1_Pemetaan_Potensi.py`** - Interactive maps & infrastructure inventory
3. **`2_Analisis_Kapasitas.py`** - Capacity calculations & energy production estimates
4. **`3_Analisis_Ekonomi.py`** - Financial modeling (ROI, NPV, payback period)
5. **`4_Manfaat_Lingkungan.py`** - Environmental impact (CO₂ reduction, UHI mitigation)
6. **`5_Manfaat_Sosial.py`** - Social benefits (comfort, mobility, job creation)
7. **`6_Studi_Komparasi.py`** - International & domestic case studies
8. **`7_Rekomendasi_Roadmap.py`** - Implementation phases & policy recommendations

## Technical Notes

### Imports Required
All pages should import:
```python
import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css
```

### Page Config
Each page should set:
```python
st.set_page_config(
    page_title="[Page Name] — CELIOS Solar Dashboard",
    page_icon="[emoji]",
    layout="wide",
)
```

### Styling
Always call:
```python
render_sidebar()  # Consistent navigation
st.markdown(get_solar_css(), unsafe_allow_html=True)  # Solar theme
```

## Future Development

Pages will be populated as data becomes available through the data acquisition plan:
- Pemetaan: After GIS data collection (OSM, satellite imagery)
- Kapasitas: After area measurements & solar calculations
- Ekonomi: After CAPEX/OPEX data collection
- Manfaat: After environmental & social impact modeling
- Komparasi: After literature review & case study compilation
- Roadmap: After scenario analysis & stakeholder consultation

## Running the Dashboard

From project root:
```bash
streamlit run Dashboard.py
```

The dashboard will be accessible at `http://localhost:8501`
