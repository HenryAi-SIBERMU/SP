# Celios8: Teduhi Ruang Kota Kami
## Potensi Instalasi Dual-Use Infrastructure PLTS Atap di Jabodetabek

**Status**: 🟡 Research in Progress  
**Start Date**: Juni 2026  
**Lead Researcher**: [Your Name]  
**Organization**: Celios

---

## 📋 Ringkasan Project

Penelitian ini menganalisis potensi instalasi PLTS (Pembangkit Listrik Tenaga Surya) atap sebagai **dual-use infrastructure** di wilayah Jabodetabek. Konsep dual-use infrastructure mengintegrasikan fungsi infrastruktur urban (transportasi publik, parkiran, pedestrian) dengan produksi energi terbarukan.

### 🎯 Tujuan Penelitian

1. Mengidentifikasi infrastruktur urban Jabodetabek yang potensial untuk PLTS atap
2. Mengestimasi luas area potensial
3. Mengestimasi kapasitas terpasang (MWp)
4. Mengestimasi produksi listrik tahunan (MWh/GWh)
5. Menganalisis kelayakan ekonomi dan skenario pembiayaan
6. Mengidentifikasi hambatan regulasi dan rekomendasi kebijakan

### 🏗️ Infrastruktur yang Dikaji

1. Halte TransJakarta
2. Peron Stasiun KRL
3. Stasiun MRT dan LRT Jabodetabek
4. Jembatan Penyeberangan Orang (JPO)
5. Area Pejalan Kaki / Pedestrian Canopy
6. Ruang Parkir Terbuka
7. Atap Gedung Parkir Bertingkat (MSCP)

---

## 📁 Struktur Folder

```
├── ref/                    # Referensi paper, dokumen brief
├── data/                   # Data riset
│   ├── raw/               # Data mentah (original)
│   ├── processed/         # Data yang sudah diproses
│   └── external/          # Data dari API eksternal
├── docs/                   # Dokumentasi metodologi
├── scripts/                # Python scripts (workflow 01-05)
├── src/                    # Reusable code modules
├── output/                 # Hasil akhir (reports, maps, charts)
├── assets/                 # Static assets (logos, templates)
├── Infografis/            # Infografis publikasi
└── tools/                  # Utility scripts
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- QGIS (untuk GIS processing)

### Installation

```bash
# Clone repository
git clone [repository-url]
cd "23. Celios8-solarpanel"

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

```bash
# Copy .env.example to .env and fill in your API keys
cp .env.example .env
```

---

## 📊 Metodologi

### 1. Inventarisasi Area
- **Tools**: QGIS, Google Earth Engine, OpenStreetMap
- **Output**: GIS shapefiles dengan area potensial

### 2. Konversi Area ke Kapasitas
- **Formula**: Kapasitas (kWp) = Usable Area (m²) × 0.18 kWp/m²
- **Asumsi**: Module efficiency 18-22%, usable area 70-85%

### 3. Estimasi Produksi Energi
- **Tool**: PVGIS (Photovoltaic Geographical Information System)
- **Formula**: Production (kWh) = Capacity (kWp) × PSH × 365 × PR
- **Parameter Jabodetabek**: PSH 4.7 kWh/m²/day, PR 77%

### 4. Financial Modeling
- LCOE (Levelized Cost of Energy)
- NPV, IRR, Payback Period
- Scenario analysis (optimistic, moderate, conservative)

---

## 📈 Preliminary Results

> [Will be updated as research progresses]

**Estimasi Awal**:
- Total Potensi: ~857 MWp
- Produksi Tahunan: ~1,105 GWh/tahun
- Kontribusi: ~1.4% kebutuhan listrik Jabodetabek

---

## 👥 Stakeholders

- **Pemerintah**: Pemprov DKI, Pemda Bodetabek, Kementerian ESDM
- **BUMN**: PT TransJakarta, PT KAI, PT MRT Jakarta, PLN
- **Private Sector**: Mall operators, solar EPC contractors
- **Civil Society**: IESR, Greenpeace, academia

---

## 📚 Referensi Utama

1. Siswanto et al. (2023). Spatio-temporal characteristics of urban heat Island of Jakarta metropolitan. *Remote Sensing Applications: Society and Environment*.
2. [Tambahan referensi akan ditambahkan]

---

## 📄 License

© 2026 Celios. All rights reserved.

---

## 📞 Contact

**Lead Researcher**: [Your Name]  
**Email**: [email]  
**Organization**: Celios  
**Website**: [website]

---

## 🔄 Changelog

### [Unreleased]
- Initial project setup
- Folder structure creation
- Framework analysis document

---

**Last Updated**: 23 Juni 2026
