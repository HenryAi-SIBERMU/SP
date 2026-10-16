# Strategi Desain Tool ML Ekstrapolasi 20.000 Titik PLTS Atap Jabodetabek
## Berbasis Systematic Literature Review (SLR) 10 Paper Ilmiah & Hybrid Physics-Informed ML
**Dokumen Referensi:** `docs/STRATEGI-TOOL-ML-EKSTRAPOLASI-20000-TITIK-SLR.md`  
**Target Modul Tool:** `tools/ml_extrapolator/`  
**Status Dokumen:** 🟢 Master Blueprint Disetujui (Siap Eksekusi)  
**Versi:** 1.0  
**Tanggal:** 16 Oktober 2026  
**Penulis:** Tim Data & Geospasial Celios  
**Kepatuhan Aturan:** Mematuhi 5 Agent Rules (`anti_yesman_spatial_methodology_integrity`, `no_hardcoded_data`, `statistical_auditor_role`, `strict_data_folder_boundary`, `never_use_destructive_commands`)  

---

## 📌 1. Ringkasan Eksekutif & Latar Belakang Masalah

Riset potensi energi surya CELIOS di kawasan aglomerasi Jabodetabek telah berhasil memetakan **2.100 titik fasilitas publik dan simpul infrastruktur** menggunakan fotogrametri satelit beresolusi sangat tinggi (0,25 m/piksel) melalui Google Solar API BASE Tier (tersimpan di [`data/processed/calculations/pow_solar_kumulatif_summary.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/calculations/pow_solar_kumulatif_summary.csv)).

Namun, berdasarkan audit bank data spasial OpenStreetMap ([`docs/LAPORAN-POTENSI-MAKSIMAL-POPULASI-OSM-13-KATEGORI-JABODETABEK.md`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/docs/LAPORAN-POTENSI-MAKSIMAL-POPULASI-OSM-13-KATEGORI-JABODETABEK.md)), populasi riil infrastruktur beratap permanen se-Jabodetabek mencapai **12.397 titik** (fokus 13 kategori utama) hingga **19.132 – 22.311 titik** (jika menyerap seluruh shelter feeder bus dan kantor instansi pemerintah). 

Menarik sisa 18.000+ titik menggunakan Google Solar API secara langsung akan menelan biaya penagihan API (*billing cost*) sebesar **> \$850 (~Rp 13,5 Juta)**, yang melampaui pagu anggaran operasional Cloud Billing GCP.

**Solusi Strategis:**  
Membangun tool mandiri di folder `tools/ml_extrapolator/` yang mengadopsi **Hybrid Physics-Informed Machine Learning**. Model dilatih menggunakan 2.100 data *ground-truth* Google Solar API, kemudian mengekstrapolasikan **4 Bento Metrics utama** (Kapasitas kWp, Luas Atap Efektif m², Produksi Listrik AC MWh, dan Reduksi Emisi GRK Ton CO₂) ke seluruh populasi 20.000 titik target secara deterministik, akurat, dan memiliki landasan ilmiah yang kuat (*evidence-based*).

---

## 🔬 2. Systematic Literature Review (SLR) 10 Paper Ilmiah

Sebagai landasan ilmiah yang dapat diverifikasi (*forensically verifiable*), tim riset telah mengunduh **10 paper ilmiah primer** ke dalam folder dataset [`data/raw/sources/papers/`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/raw/sources/papers/) dan mem-parsing naskah lengkapnya ke format Markdown di [`data/processed/references/papers/`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/) menggunakan tool `opendataloader-pdf`.

### A. Matriks Analisis 10 Paper Ilmiah

| No | File PDF & Markdown di Repositori | Judul Paper & Penulis | Arsitektur Model AI/ML | Fitur Prediktor ($X$) | Target Prediksi ($Y$) | Kesimpulan Adopsi untuk Proyek Celios |
|:--:|:---|:---|:---|:---|:---|:---|
| **1** | [`paper_01_2106_15268v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_01_2106_15268v1.md) | **Predicting the Solar Potential of Rooftops using Image Segmentation and Structured Data**<br>*(De Barros Soares et al., Paris)* | **Hybrid Pipeline:**<br>Mask R-CNN + **Gradient Boosted Decision Trees (GBDT)** | Luas tapak bangunan ($m^2$), kategori fungsi gedung, pitch, azimuth, tinggi gedung, GHI lokal. | • Luas efektif layak PLTS ($m^2$)<br>• Yield tahunan ($kWh$) | ✅ **DIADOPSI SEBAGAI KERANGKA UTAMA.** Membuktikan bahwa memprediksi luas atap dari atribut tabular tapak bangunan menghasilkan akurasi tertinggi ($R^2 > 0.85$). |
| **2** | [`paper_02_2501_02840v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_02_2501_02840v1.md) | **Enhanced Rooftop Solar Panel Detection by Efficiently Aggregating Local Features**<br>*(Kurte & Kulkarni, 2025)* | **Enhanced CNN:**<br>ResNet/EfficientNet + Feature Pyramid Network (FPN) | Patch citra satelit resolusi tinggi (RGB), tekstur pantulan modul surya. | Deteksi poligon panel surya eksisting di atap. | ❌ **TIDAK DIADOPSI.** Membutuhkan citra satelit resolusi tinggi baru untuk setiap gedung target, yang tidak tersedia untuk 18.000 titik. |
| **3** | [`paper_03_2607_22342v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_03_2607_22342v1.md) | **Beyond Binary Rooftop Mapping: Deep Learning Framework from Open Geospatial Data**<br>*(Bern, Swiss, 2026)* | **Semantic Segmentation:**<br>HRNet & DeepLabV3+ | Ortofoto RGB + LiDAR nDSM (tinggi atap) + batas poligon OSM. | 4-kelas atap (datar, miring, terhalang, tidak layak). | ➖ **DIADOPSI PRINSIPNYA.** Mengadopsi prinsip pemisahan kelas atap datar vs miring pada kategori Halte BRT vs Gedung Publik. |
| **4** | [`paper_04_2511_18882v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_04_2511_18882v1.md) | **Facade and Rooftop Segmentation for Solar Photovoltaic Suitability**<br>*(ETH Zurich, 2025)* | **Vision Transformer:**<br>Swin-Transformer / Mask2Former | Vektor normal 3D amplop gedung, sudut datang matahari, batas fasad. | Luas bidang bebas bayangan ($m^2$) dan potensi kWp. | ❌ **TIDAK DIADOPSI.** Terlalu berorientasi pada fasad vertikal 3D kompleks yang tidak relevan dengan kanopi atap terbuka Jabodetabek. |
| **5** | [`paper_05_2410_08098v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_05_2410_08098v1.md) | **A Generative AI Technique for Synthesizing a Digital Twin for Solar Adoption**<br>*(2024)* | **Generative AI + Ensemble:**<br>Conditional Tabular GAN + **XGBoost / LightGBM** | Luas tapak gedung, tipe kategori bangunan, zona iklim, PSH rata-rata. | Kapasitas terpasang ($kWp$) dan profil generasi 8.760 jam. | ✅ **DIADOPSI TEKNIK TABULARNYA.** Memvalidasi penggunaan XGBoost/LightGBM untuk mengekstrapolasi sampel kecil ke populasi masif perkotaan. |
| **6** | [`paper_06_2111_11397v6`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_06_2111_11397v6.md) | **Lebanon Solar Rooftop Potential Assessment using Buildings Segmentation**<br>*(Charbel et al., 2021)* | **Segmentation + Physics:**<br>Building Footprint Extractor + Transposition Engine | Luas tapak segmented ($m^2$), faktor shading lokal (~25%), radiasi GHI. | Luas atap efektif ($m^2$), MWp regional, dan GWh/thn. | ✅ **DIADOPSI ATURAN FISIKANYA.** Menegaskan bahwa nilai MWp dan GWh wajib dihitung via formula transposisi fisik, bukan tebakan bebas AI. |
| **7** | [`paper_07_2012_14349v4`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_07_2012_14349v4.md) | **Roofpedia: Automatic Mapping of Green and Solar Roofs for Urban Sustainability**<br>*(NUS Singapore, 2021)* | **Multi-Stage DL:**<br>YOLOv3 + ResNet-34 + Spatial Clustering | Poligon OpenStreetMap (OSM), citra satelit udara, rasio aspek atap. | Identifikasi solar panel dan indeks penetrasi atap perkotaan. | ➖ **DIADOPSI STRUKTUR DATANYA.** Menggunakan OpenStreetMap building footprints sebagai jangkar spasial utama populasi target. |
| **8** | [`paper_08_2207_08287v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_08_2207_08287v1.md) | **Spatial Distribution of Solar PV Deployment: Application of Region-Based CNN**<br>*(Kuriyama et al., 2022)* | **Spatial Econometrics:**<br>Faster R-CNN + Spatial Autoregressive Models (SAR) | Luas gedung, kepadatan penduduk, variabel lag spasial (tetangga). | Densitas kWp per wilayah administrasi. | ✅ **DIADOPSI KONTROL SPASIALNYA.** Mengharuskan penerapan **Spatial Cross-Validation** guna mencegah bias autokorelasi spasial antar-wilayah. |
| **9** | [`paper_09_2310_20057v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_09_2310_20057v1.md) | **SolarFormer: Multi-scale Transformer for Solar PV Profiling**<br>*(2023)* | **Temporal Transformer:**<br>Multi-scale Self-Attention | Fluks iradiasi PSH, suhu permukaan modul ($T_m$), efisiensi termal. | Yield spesifik bersih ($kWh/kWp$) dan derating inverter. | ✅ **DIADOPSI PRINSIP DERATINGNYA.** Mengonfirmasi susut panas suhu tropis perkotaan (selaras dengan Performance Ratio 80% IEC 61724). |
| **10** | [`paper_10_2011_09950v1`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/paper_10_2011_09950v1.md) | **Improving Solar and PV Power Prediction with Ensemble Methods**<br>*(2020)* | **Heterogeneous Stacking:**<br>**Random Forest + LightGBM + XGBoost** | Kapasitas terpasang, sudut zenit, suhu ambien, GHI/DNI, tilt array. | Prediksi daya listrik keluaran ($kWh$) & Confidence Intervals. | ✅ **DIADOPSI ENSEMBLE STACKING-NYA.** Menggunakan kombinasi Random Forest, LightGBM, dan XGBoost untuk menghasilkan selang batas keyakinan (P10, P50, P90). |

---

### B. Kesimpulan Sintesis SLR: Rasionalisasi Pilihan Model

Dari telaah 10 paper di atas, terdapat dua mazhab pemodelan energi surya:
1. **Mazhab Computer Vision Murni (Paper 02, 03, 04, 07):**  
   *Kelemahan jika diterapkan di Celios:* Model ini mewajibkan adanya file raster citra satelit resolusi tinggi untuk seluruh 20.000 titik. Karena kita tidak memiliki citra satelit untuk 18.000 titik sisa (akibat pembatasan biaya API), mazhab ini **ditolak** demi efisiensi dan kepatuhan anggaran.
2. **Mazhab Hybrid Physics-Informed ML (Sintesis Paper 01 + Paper 10 + Paper 06):**  
   *Keunggulan Mutlak:* 
   - **Machine Learning (Paper 01 & 10)** hanya bertugas memprediksi **luas atap efektif layak PLTS (`max_roof_area_m2`)** berdasarkan data tabular tapak gedung (OSM Footprint) dan kategori tipologi.
   - **Physics Engine (Paper 06 & 09)** kemudian mengonversi luas atap tersebut menjadi **Kapasitas kWp, Listrik AC Bersih MWh, dan Reduksi Emisi CO₂** menggunakan formula deterministik baku (SNI/IEC 61724-1 PR 80% dan faktor emisi Jamali).
   - Pendekatan ini menjamin **100% konsistensi matematis**, bebas dari halusinasi *black-box AI*, dan dapat diaudit secara transparan (*zero hardcoded data*).

---

## 🏗️ 3. Arsitektur Teknis Tool Ekstrapolasi (`tools/ml_extrapolator/`)

Tool yang akan dibangun di `tools/ml_extrapolator/` dirancang dengan arsitektur **3 Lapisan Terpadu**:

```
┌────────────────────────────────────────────────────────────────────────┐
│ LAPISAN 1: FEATURE STORE & DATA ENRICHMENT ENGINE                     │
│ Sumber Data Latih (Train N = 2.100): pow_solar_kumulatif_summary.csv   │
│ Sumber Target (Target N ≈ 20.000) : OpenStreetMap / Overture Parquet   │
│                                                                        │
│ Vektor Fitur Prediktor (X):                                            │
│ • building_footprint_m2   : Luas tapak proyeksi 2D bangunan            │
│ • perimeter_m             : Keliling poligon tapak bangunan            │
│ • compactness_ratio       : 4 * π * Area / (Perimeter^2) [Indeks Bentuk]│
│ • category_code           : One-Hot Encoding 13 Tipologi Infrastruktur │
│ • city_regency_code       : Koordinasi spasial 5 DKI & 8 Bodetabek    │
│ • psh_annual_hours        : Fluks jam matahari puncak ekuivalen lokal  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAPISAN 2: ENSEMBLE QUANTILE REGRESSION (PAPER 01 & PAPER 10)          │
│                                                                        │
│ Algoritma Base Learners (Library Resmi Scikit-Learn & LightGBM):       │
│ 1. LightGBM Regressor (LGBM)     ──┐                                   │
│ 2. Extreme Gradient Boost (XGB)  ──┼──> Stacking Meta-Learner (Ridge)  │
│ 3. Random Forest Regressor (RF)  ──┘                                   │
│                                                                        │
│ Skema Validasi:                                                        │
│ • Spatial Block Cross-Validation (K-Fold berdasarkan klaster kota)     │
│   guna mencegah kebocoran autokorelasi spasial (Paper 08).             │
│                                                                        │
│ Output Prediksi Probabilistik Luas Atap Layak (max_roof_area_m2):      │
│ • P10 : Estimasi Konservatif (Batas Bawah Keyakinan 90%)              │
│ • P50 : Estimasi Paling Mungkin (Median / Baseline Terbaik)            │
│ • P90 : Estimasi Optimistis (Batas Atas Potensi Fisik)                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ LAPISAN 3: DETERMINISTIC PHYSICS ENGINE (4 BENTO METRICS GENERATOR)    │
│ Diterapkan seragam untuk ketiga skenario probabilitas (P10, P50, P90): │
│                                                                        │
│ 1. Total Luas Atap Efektif (m²):                                       │
│    Hasil langsung prediksi Model ML (P10, P50, P90)                    │
│                                                                        │
│ 2. Total Kapasitas Terpasang (kWp):                                    │
│    Jumlah Panel = floor(Luas_Atap / 1,785 m²)                          │
│    Kapasitas_kWp = (Jumlah_Panel * 400 Wp) / 1000                      │
│                                                                        │
│ 3. Estimasi Produksi Listrik AC Bersih (MWh/tahun):                   │
│    Listrik_AC = (Kapasitas_kWp * PSH_Lokal * 0.80) / 1000              │
│    (Mengacu Standar IEC 61724 PR 80% & Bukti Empiris Cirata UI 2019)   │
│                                                                        │
│ 4. Reduksi Emisi Gas Rumah Kaca (Ton CO₂/tahun):                       │
│    Reduksi_CO2 = (Listrik_AC * 808,99 kg/MWh Jamali) / 1000            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 4. Rencana Struktur File di Repositori

Tool ekstrapolasi akan ditempatkan di direktori baru `tools/ml_extrapolator/` dengan struktur modular:

```
tools/ml_extrapolator/
├── __init__.py
├── config.py                 # Parameter konfigurasi, path data, dan ambang batas
├── feature_extractor.py      # Ekstraksi fitur tapak OSM & enrich atribut spasial
├── train_ensemble.py         # Pelatihan model Stacking Ensemble (LGBM + RF + XGB)
├── spatial_cv.py             # Evaluasi model berbasis Spatial Block Cross-Validation
├── predict_population.py     # Inferensi skala penuh ke 20.000 titik target (P10, P50, P90)
└── physics_engine.py         # Generator 4 Bento Metrics deterministik IEC 61724

Output Dataset Ekstrapolasi:
data/processed/calculations/
├── pow_solar_extrapolasi_20000_summary.parquet  # Dataset kolumnar biner cepat
└── pow_solar_extrapolasi_20000_summary.csv      # Format CSV untuk audit transparan
```

---

## 📊 5. Spesifikasi 4 Bento Metrics Hasil Ekstrapolasi

Output dari ekstrapolasi 20.000 titik akan menyajikan 3 skenario angka pada dashboard:

| Bento Metric Card | Formula Fisika Baku | Skenario P10 (Konservatif) | Skenario P50 (Paling Mungkin / Median) | Skenario P90 (Optimistis) | Sumber Rujukan Metodologis |
|:---|:---|:---:|:---:|:---:|:---|
| **1. Total Kapasitas Terpasang (kWp)** | $\frac{\lfloor \text{Luas} / 1,785 \rfloor \times 400}{1.000}$ | Batas Bawah Kuota | **Kapasitas Riil Diproyeksikan** | Batas Atas Potensi | Standar Modul Surya Tier-1 400Wp ($1,785\text{ m}^2/\text{modul}$) |
| **2. Total Luas Atap Efektif (m²)** | Prediksi Ensemble ML | $\text{Prediksi}_{q=0.10}$ | $\mathbf{\text{Prediksi}_{q=0.50}}$ | $\text{Prediksi}_{q=0.90}$ | Model GBDT Paper 01 & Stacking Paper 10 |
| **3. Estimasi Produksi Listrik (MWh/th)** | $\frac{\text{kWp} \times \text{PSH} \times 0,80}{1.000}$ | $\text{Listrik}_{\text{P10}}$ | $\mathbf{\text{Listrik}_{\text{P50}}}$ | $\text{Listrik}_{\text{P90}}$ | Standar IEC 61724-1 (PR 80% Tropis Cirata IJTech UI) |
| **4. Reduksi Emisi GRK (Ton/th)** | $\frac{\text{MWh} \times 808,99}{1.000}$ | $\text{Emisi}_{\text{P10}}$ | $\mathbf{\text{Emisi}_{\text{P50}}}$ | $\text{Emisi}_{\text{P90}}$ | Faktor Emisi Grid Jamali Ditjen Ketenagalistrikan ESDM |

---

## 🔒 6. Audit Data Lineage & Silsilah Berkas Fisik

Sesuai aturan `strict_data_folder_boundary` dan `no_hardcoded_data`, seluruh model terhubung langsung ke berkas fisik repositori:

1. **Dataset Latih Primer (2.100 Titik):** [`data/processed/calculations/pow_solar_kumulatif_summary.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/calculations/pow_solar_kumulatif_summary.csv)
2. **Kompilasi Kandidat Target (20.000 Titik):** [`data/raw/poi/target_2000_titik.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/raw/poi/target_2000_titik.csv) & pool OpenStreetMap Jabodetabek.
3. **Dokumen Bukti Forensik 10 Paper Ilmiah:** [`data/raw/sources/papers/`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/raw/sources/papers/)
4. **Hasil Parsing Teks Penuh (Markdown):** [`data/processed/references/papers/`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/papers/)
5. **Bukti Standar IEC 61724 (PR 80%):** [`data/raw/sources/ijtech_ui_iec_61724_pv_performance_indonesia.pdf`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/raw/sources/ijtech_ui_iec_61724_pv_performance_indonesia.pdf)

---
*Dokumen ini merupakan bagian dari Master Plan Desain Rekayasa Data CELIOS Solar 2026. Seluruh hak cipta dilindungi dan terikat pada aturan integritas metodologi proyek.*
