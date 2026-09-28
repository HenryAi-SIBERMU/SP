# Product Requirements Document (PRD)
## CELIOS8: Dashboard Potensi Dual-Use Infrastructure PLTS Atap JABODETABEK

**Tanggal**: 4 Juli 2026 (Updated: 24 September 2026)  
**Status**: 🟡 Draft / Planning (Regional Scope: JABODETABEK)  
**Target Output**: Interactive Streamlit Dashboard  
**Target Objek**: 4,000 Titik Regional (Safety Buffer Pagu Anggaran; Catatan: Estimasi Belum Tervalidasi Riil)  

---

## 1. Product Vision
Membangun dashboard interaktif untuk memvisualisasikan potensi infrastruktur publik di kawasan aglomerasi **JABODETABEK** (Halte BRT, Stasiun KRL/MRT/LRT, Kantung Park & Ride Komuter, Terminal, dan Lapangan Parkir Terbuka) sebagai *dual-use infrastructure* untuk pemasangan panel surya. Dashboard ini harus mampu mengkuantifikasi kapasitas energi yang dihasilkan sekaligus membuktikan manfaat *triple-benefits* (ekonomi, sosial, dan mitigasi *Urban Heat Island* regional).

---

## 2. Development Roadmap (Phase per Page) & Dataset Mapping

Pengembangan Streamlit Dashboard akan dieksekusi secara modular berdasarkan **halaman (page)**. Berikut adalah pemetaan detail sumber data ke dalam masing-masing fase:

### 📍 Phase 1: Page "Overview & Data Status"
**Tujuan**: Memberikan konteks riset (Kedaulatan Energi Kawasan Metropolitan) dan transparansi *live-status* akuisisi data (Pagu safety buffer 4,000 titik Jabodetabek).  
**Kebutuhan Fitur**: Narasi pengantar & Live Progress Bar untuk dataset krusial.  
**Dataset yang Dibutuhkan**:

| ID | Sumber Data | Target / Deskripsi | Status / Prioritas | Status Biaya |
|:---|:---|:---|:---|:---|
| `Data #11` | **PT TransJakarta & Dishub Bodetabek** | ~650 halte (TJ koridor + feeder Biskita Bogor, Trans Patriot Bekasi, Tayo Tangerang) | Prioritas #1 | 🟢 Gratis (Request Formal/Open Data) |
| `Data #12` | **PT KAI Commuter (KCI)** | 85 stasiun KRL Commuter Line se-Jabodetabek | Prioritas #2 | 🟢 Gratis (Request Formal) |
| `Data #13` | **PT MRT Jakarta** | 13 stasiun MRT Fase 1 | Tinggi | 🟢 Gratis (Request Formal) |
| `Data #14` | **PT KAI (LRT Jabodebek) & LRT Jkt** | 24 stasiun (18 LRT Jabodebek + 6 LRT Jakarta) | Tinggi | 🟢 Gratis (Request Formal) |
| `Data #15` | **BPTJ, Kemenhub, & Dishub Bodetabek** | ~475 JPO, 25 Terminal Bus Tipe A/B, serta 60+ kantung Park & Ride stasiun | Menengah | 🟢 Gratis (PPID/Portal) |

### 🗺️ Phase 2: Page "Inventarisasi Spasial"
**Tujuan**: Memetakan titik infrastruktur se-Jabodetabek secara interaktif.  
**Kebutuhan Fitur**: Peta interaktif (Folium/PyDeck) & Kalkulator agregat luas area potensial (m²).  
**Dataset yang Dibutuhkan**:

| ID | Sumber Data | Kegunaan / Target | Status Biaya |
|:---|:---|:---|:---|
| `Data #16` | **OpenStreetMap (OSM)** | Ekstraksi koordinat (POI) dan *building footprints* via OSMnx (BBOX Jabodetabek) | 🟢 Gratis |
| `Data #20` | **Google Maps API** | Geocoding & Places API (validasi 1,350+ lokasi parkir komersial/publik & Park and Ride) | 💰 Berbayar (API) |
| `Data #6` | **Portal Satu Data (Jabar, Banten, DKI)** | Data simpul transportasi dan fasilitas publik terpadu | 🟢 Gratis |
| `Data #4` | **One Map Indonesia / BIG** | Peta dasar Jabodetabek & batas administrasi provinsi/kabupaten/kota | 🟢 Gratis |
| `Data #16c` | **Google Solar API** | Ekstraksi luas atap, bayangan, & output kWh untuk 3,000 titik Jabodetabek | 💰 Berbayar (Tersedia Free Credit $300) |
| `Data #16b` | **Overture Maps / Bing** | Unduh *GeoParquet* masif untuk *Local Spatial Join* offline se-Jabodetabek | 🟢 Gratis |
| `Data #19` | **Planet Labs / GEE** | Citra satelit resolusi super tinggi untuk validasi area atap dan Park & Ride | 💰 Berbayar |

**Data Format & Handover Strategy (Dual-Native)**:
1. **WebGIS Native (Dashboard)**: Menggunakan format `GeoJSON` dan `CSV` agar dapat langsung dirender secara ringan oleh Streamlit (menggunakan Folium/PyDeck).
2. **GIS Native (Handover)**: Hasil akhir (kompilasi final) akan diekspor menjadi `GeoPackage (.gpkg)`. Format ini adalah standar industri masa kini (*single-file SQLite database*) untuk diserahkan dan diolah di *software* pemetaan tingkat *enterprise* seperti ArcGIS Pro atau QGIS.

**Opsi Akselerasi Pipeline Ekstraksi Atap (Fase 2):**
Untuk memproses data regional Jabodetabek (~3,000 titik prioritas dari total ratusan ribu objek):
- **Opsi A (Premium/Instan): Google Solar API.** Langsung mengembalikan luas m², parameter bayangan, dan output kWh tahunan per titik. Biaya bersih: **~$19.68 (~Rp 310K)** untuk validasi visual 3,000 titik setelah dipotong Free Credit GCP $300.
- **Opsi B (Gratis/Ngebut): Overture Maps / Bing Building Footprints.** Mengunduh total *dataset* atap Jabodetabek (GeoParquet) dan melakukan *Local Spatial Join* secara *offline*. 100x lebih cepat dari *scraping* API OpenStreetMap.

### ⚡ Phase 3: Page "Kapasitas & Produksi Energi"
**Tujuan**: Mengonversi luasan spasial menjadi angka energi absolut (MWp dan GWh).
**Kebutuhan Fitur**: Input Slider teknis, Integrasi Radiasi Matahari, dan *Benchmark Metrik* konsumsi kota.
**Dataset yang Dibutuhkan**:

| ID | Sumber Data | Kegunaan / Target | Status Biaya |
|:---|:---|:---|:---|
| `Data #21` | **PVGIS (JRC Europe)** | Data *Peak Sun Hours* (PSH) dan solar iradiasi Jabodetabek | 🟢 Gratis |
| `Data #22` | **NASA POWER** | Data cuaca dan radiasi historis (sebagai pembanding PVGIS) | 🟢 Gratis |
| `Data #24` | **Solargis** | Alternatif sumber data *Solar Irradiation* (GHI/DNI) resolusi tinggi | 💰 Berbayar (API) |
| `Data #2` | **PLN Statistics** | Penjualan listrik per sektor (publik/komersial) untuk membandingkan GWh | 🟢 Gratis |
| `Data #25-28` | **Existing Solar PV** | Angka aktual produksi dan kapasitas (*lessons learned* dari Bandara Soetta, dll) | 🟢 Gratis (OSINT) |

### 🌱 Phase 4: Page "Triple-Benefits & Mitigasi UHI"
**Tujuan**: Menjawab hipotesis lingkungan dan sosial berbasis rujukan akademik dan perhitungan kelayakan finansial.
**Kebutuhan Fitur**: 
- Kalkulator reduksi CO2 dan ROI proyeksi.
- **Visualisasi Korelasi Beton & Suhu**: Menganalisis tren 2004-2020 di mana area aspal/beton memicu suhu ekstrem (32-36°C) untuk menjustifikasi urgensi *solar canopy*.
- **Mitigasi Kubah Panas**: Pemodelan efek *shading* pada siang hari saat suhu Jakarta memuncak >37°C (selaras dengan waktu *Peak Sun Hours*).
- **Pemetaan Episentrum SUHI**: Overlay titik infrastruktur (Halte/Parkir) langsung di atas zona merah SUHI Jakarta.
**Dataset yang Dibutuhkan**:

| ID | Sumber Data | Kategori | Kegunaan / Target | Status Biaya |
|:---|:---|:---|:---|:---|
| `Data #40` | **Jurnal Siswanto et al. (2023)** | Lingkungan | Parameter penurunan *Land Surface Temperature* & UHI | 🟢 Gratis |
| `Data #3` | **Kementerian ESDM** | Lingkungan | Angka faktor emisi karbon grid Jawa-Bali | 🟢 Gratis |
| `Data #34` | **PLN Tariff** | Ekonomi | Tarif dasar listrik untuk estimasi penghematan (OPEX) | 🟢 Gratis |
| `Data #33` | **Solar EPC Companies** | Ekonomi | Estimasi CAPEX kanopi surya (Rp/kWp) untuk model investasi | 🟢 Gratis |
| `Data #35` | **Bank Indonesia** | Ekonomi | Tingkat inflasi & *discount rate* (untuk NPV) | 🟢 Gratis |
| `Data #32` | **PERMEN ESDM 26/2021** | Regulasi | Prosedur interkoneksi dan kapasitas maksimal PLTS atap | 🟢 Gratis |

---

## 3. Eksekusi Akuisisi Data Terdekat (Sprint 1)
Berdasarkan *Roadmap* di atas, untuk bisa meluncurkan Phase 1 dan 2, kita harus segera mengeksekusi ekstraksi (*scraping*/API) untuk data spasial KRITIKAL:
1. **Pemetaan Halte TransJakarta (`Data #11`)**: Saat ini OSM baru mengkover 64 halte (23%).
2. **Data Parkir (`Data #16` & `#20`)**: Verifikasi 946 titik parkir dari OSM dan Google Places.
3. **Data PSH PVGIS (`Data #21`)**: Mengotomatisasi penarikan radiasi via API Python.
