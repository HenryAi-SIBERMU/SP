# Dashboard Guide
## CELIOS8 Solar Dashboard — Getting Started

### Status Update (23 Juni 2026)
✅ **Dashboard structure COMPLETE**
- Main dashboard (`Dashboard.py`) created
- All 8 pages created in `pages/` folder
- **Fully functional**: Halaman Dokumentasi Riset
- **Placeholders**: 7 pages lainnya (akan dikembangkan seiring data collection)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Dashboard

```bash
streamlit run Dashboard.py
```

Dashboard akan terbuka di browser: `http://localhost:8501`

---

## 📂 Dashboard Structure

```
Dashboard.py                    # Main entry page
├── src/
│   ├── components/
│   │   └── sidebar.py         # Shared navigation
│   └── utils/
│       └── styling.py         # CSS theme
└── pages/
    ├── 0_Overview.py          # 🚧 Placeholder
    ├── 1_Pemetaan_Potensi.py  # 🚧 Placeholder
    ├── 2_Analisis_Kapasitas.py # 🚧 Placeholder
    ├── 3_Analisis_Ekonomi.py   # 🚧 Placeholder
    ├── 4_Manfaat_Lingkungan.py # 🚧 Placeholder
    ├── 5_Manfaat_Sosial.py     # 🚧 Placeholder
    ├── 6_Studi_Komparasi.py    # 🚧 Placeholder
    └── 8_Dokumentasi_Riset.py  # ✅ FUNCTIONAL
```

---

## 🎨 Theme

**Solar Orange Theme** (#FF6B35)
- Primary color: Orange (representing solar energy)
- Dark background for comfortable viewing
- Gradient accents for solar/energy vibe
- High contrast for readability

Theme configured in:
- `.streamlit/config.toml` - Streamlit app configuration
- `src/utils/styling.py` - Custom CSS styling

---

## 📖 Halaman Dokumentasi Riset (FULLY FUNCTIONAL)

**What it displays:**
1. **Data Acquisition Plan** (`docs/DATA-ACQUISITION-PLAN.md`)
   - 43 data sources identified
   - Organized by 10 categories
   - Priority framework (Critical/High/Medium)
   - Contact information for stakeholders

2. **Framework Awal - Feedback & Analisis** (`docs/project-plan/Framework Awal - Feedback & Analisis.md`)
   - 65-page comprehensive feedback
   - Framework analysis
   - Methodology deep dive
   - Comparative studies notes
   - Recommendations roadmap

**Features:**
- Document selector (radio buttons)
- Clean markdown rendering (emoji stripped for stability)
- Download button for each document
- Custom styled with solar theme
- Responsive layout

---

## 🚧 Placeholder Pages

All other pages show development placeholder with:
- Page title & subtitle
- "Sedang dalam pengembangan" message
- List of planned features
- Consistent theming

These will be populated as data collection progresses.

---

## 🎯 Next Development Steps

### Short-term (Dashboard improvements)
1. ✅ **Add logo file**: Place `Duniahub Logo putih.png` in `assets/logos/`
2. Test dashboard on different screen sizes
3. Add more metrics to main dashboard as data becomes available

### Medium-term (Data & Analysis)
1. Collect GIS data (OSM, satellite)
2. Create analysis scripts
3. Populate `1_Pemetaan_Potensi.py` with interactive maps
4. Populate `2_Analisis_Kapasitas.py` with calculations

### Long-term (Full Dashboard)
1. Complete all placeholder pages
2. Add interactive visualizations (Plotly, Folium maps)
3. Connect to live data sources
4. Add filtering & scenario comparison

---

## 🔧 Troubleshooting

### Dashboard won't start
- Check if streamlit is installed: `pip list | grep streamlit`
- Reinstall: `pip install --upgrade streamlit`
- Check Python version (3.8+ required)

### Pages not showing
- Streamlit auto-discovers files in `pages/` folder
- Make sure files are named correctly: `[number]_[Name].py`
- Restart streamlit server

### Styling looks broken
- Clear browser cache
- Check `.streamlit/config.toml` exists
- Verify `get_solar_css()` is called in each page

### Documents not displaying
- Check file paths in `8_Dokumentasi_Riset.py`
- Verify markdown files exist:
  - `docs/DATA-ACQUISITION-PLAN.md`
  - `docs/project-plan/Framework Awal - Feedback & Analisis.md`

---

## 📝 Adding New Pages

Template for new page:
```python
"""
CELIOS8: [Page Name]
"""
import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css

st.set_page_config(
    page_title="[Page Name] — CELIOS Solar Dashboard",
    page_icon="[emoji]",
    layout="wide",
)

render_sidebar()
st.markdown(get_solar_css(), unsafe_allow_html=True)

st.markdown('<div class="page-title">[Page Name]</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">[Subtitle]</div>', unsafe_allow_html=True)

# Your content here
```

---

## 📚 Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Docs**: https://plotly.com/python/
- **Folium Maps**: https://python-visualization.github.io/folium/

---

**Last Updated**: 23 Juni 2026  
**Status**: Dashboard structure complete, ready for data population  
**Contact**: CELIOS Research Division
