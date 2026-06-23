# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added (2026-06-23)
- ✅ Initial project structure setup
- ✅ Created folder structure:
  - `data/` (raw, processed, external)
  - `docs/` (methodology, meetings, literature-review, project-plan)
  - `scripts/` (01-05 workflow folders)
  - `src/` (reusable code modules)
  - `output/` (reports, maps, charts, presentations, datasets)
  - `assets/` (logos, templates, icons)
  - `Infografis/` (draft, final)
  - `tools/` (utility scripts)
  - `ref/` (existing - references)

- ✅ Created core Python modules:
  - `src/__init__.py`
  - `src/gis_utils.py` - GIS processing functions
  - `src/solar_calc.py` - Solar capacity & production calculations
  - `src/financial.py` - Financial modeling (NPV, IRR, LCOE, etc.)
  - `src/visualization.py` - Visualization functions

- ✅ Created configuration files:
  - `.gitignore` - Git ignore rules
  - `requirements.txt` - Python dependencies
  - `.env.example` - Environment variables template
  - `README.md` - Project documentation
  - `CHANGELOG.md` - This file

- ✅ Created README documentation for:
  - `data/README.md` - Data directory guide
  - `scripts/README.md` - Scripts workflow guide
  - `docs/README.md` - Documentation standards

- ✅ Created research framework documents:
  - `ref/Paper Teduhi Ruang Kota Kami.pdf` - Original brief paper (PDF)
  - `docs/Paper Teduhi Ruang Kota Kami.md` - Brief paper working version (converted from PDF)
  - `docs/project-plan/Framework Awal - Feedback & Analisis.md` - Comprehensive feedback & framework (65 pages)

- ✅ File organization & disposition:
  - Organized reference files by type and purpose
  - Created `ref/README.md` for reference management guide

- ✅ Created comprehensive data acquisition plan:
  - `docs/DATA-ACQUISITION-PLAN.md` - Master log untuk 43 sumber data
  - 10 kategori data: Pemerintah, BUMN, Spasial, Solar, Finansial, dll.
  - Priority framework: Critical (Week 1-2), High (Week 3-4), Medium (Week 5-8)
  - Contact information untuk stakeholder requests
  - SOP data collection & documentation standards

- ✅ Created Streamlit dashboard structure:
  - `.streamlit/config.toml` - Solar-themed configuration (orange primary color #FF6B35)
  - `Dashboard.py` - Main entry page with hero metrics
  - `src/components/sidebar.py` - Shared navigation component
  - `src/utils/styling.py` - Shared CSS styling utilities
  - Created all 8 pages in `pages/` folder:
    - `0_Overview.py` - Overview dashboard (placeholder)
    - `1_Pemetaan_Potensi.py` - Mapping & identification (placeholder)
    - `2_Analisis_Kapasitas.py` - Capacity analysis (placeholder)
    - `3_Analisis_Ekonomi.py` - Economic analysis (placeholder)
    - `4_Manfaat_Lingkungan.py` - Environmental benefits (placeholder)
    - `5_Manfaat_Sosial.py` - Social benefits (placeholder)
    - `6_Studi_Komparasi.py` - Comparative studies (placeholder)
    - `8_Dokumentasi_Riset.py` - **FULLY FUNCTIONAL** - Displays 2 markdown docs

- ✅ **Halaman Dokumentasi Riset (Fully Functional)**:
  - Display 2 research documents: 
    - DATA-ACQUISITION-PLAN.md (43 sumber data)
    - Framework Awal - Feedback & Analisis.md (65 pages)
  - Document selector with radio buttons
  - Custom styled markdown rendering
  - Download button for each document
  - Emoji stripping for stable rendering

- ✅ Updated `requirements.txt`:
  - Enabled streamlit dependency
  - All visualization & dashboard dependencies ready

### 📋 Next Steps (Priority)
- [ ] Test dashboard: Run `streamlit run Dashboard.py` to verify functionality
- [ ] Add logo file: `assets/logos/Duniahub Logo putih.png` (referenced in sidebar)
- [ ] Data collection: Download TransJakarta halte data
- [ ] Data collection: Request data dari PT KAI (stasiun KRL)
- [ ] Data collection: Download OpenStreetMap data untuk Jabodetabek
- [ ] Setup QGIS project untuk GIS analysis
- [ ] Create first analysis script: `scripts/01_data_collection/download_osm_data.py`
- [ ] Literature review: Search & summarize comparative studies (France, Japan, India)
- [ ] Methodology documentation: Write detailed GIS approach
- [ ] Stakeholder engagement: Contact TransJakarta, KAI, MRT for data request

---

## [0.1.0] - 2026-06-23

### Summary
Initial project setup completed. Folder structure, core modules, and documentation framework established. Ready to begin data collection phase.

### Statistics
- Folders created: 30+
- Python modules: 4
- Documentation files: 7
- Total lines of code: ~500

---

**Legend**:
- ✅ Completed
- 🚧 In Progress
- ⏳ Planned
- ❌ Cancelled
- 🔴 Blocked
