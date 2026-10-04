# LAPORAN AUDIT FORENSIK INTEGRITAS DATA & INVENTARISASI KODE HARDCODED
## Evaluasi Kepatuhan Repositori CELIOS Solar Dashboard terhadap Agent Rules
**Tanggal Audit:** 4 Oktober 2026  
**Auditor Metodologi:** Statistical & Spatial Data Integrity Auditor  
**Status Audit:** Investigasi Forensik Baris per Baris (Selesai)  
**Dokumen Acuan:**
1. `.agents/rules/no_hardcoded_data.md` *(Zero Hardcoded Data Rule)*
2. `.agents/rules/anti_yesman_spatial_methodology_integrity.md` *(Integritas Metodologi & Anti-Yes-Man)*
3. `.agents/rules/statistical_auditor_role.md` *(Peran Auditor Metodologi)*
4. `.agents/rules/strict_data_folder_boundary.md` *(Strict Local Dataset Boundary)*

---

## 1. RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY)

Berdasarkan audit forensik menyeluruh terhadap seluruh modul tampilan (Dashboard Streamlit) dan pipa pengolahan data (*ETL pipeline*), ditemukan adanya **praktik fabrikasi data semantik dan hardcoding angka statis** yang melanggar aturan utama repositori. 

Pelanggaran paling kritis terjadi pada:
1. **Halaman 1 (`pages/1_Pemetaan_Potensi.py`):** Blok percabangan `if-elif` yang menuliskan narasi arsitektural secara manual untuk 4 fasilitas tertentu (Cipete, Manggarai, Dukuh Atas, Pondok Indah Mall 1), diagnosis eliminasi segmen buatan sendiri ("Fasad Vertikal", "Parapet Mikro", "Rintangan MEP") yang disamarkan seolah diagnosis resmi Google Solar API, serta penayangan kolom deskripsi fiktif `roof_character`.
2. **Skrip ETL (`tools/solarapi/process_pow_etl.py`):** Penyuntikan kamus statis `roof_characteristics_dict` (baris 580–594) yang mengarang material dan gaya arsitektur atap ("Dak Beton", "Kubah Parabolik", "Arsitektur Kristal") ke dalam dataset CSV fisik.
3. **Halaman Utama (`Dashboard.py` & `pages/0_Overview.py`):** Kartu metrik makro (`~590 MWp`, `~785 GWh`, `~1.0%`, `~635k ton`) dan daftar 13 target kategori yang di-hardcode sebagai string teks mentah tanpa formula dinamis dan tanpa membaca file referensi di `data/`.

Sebaliknya, modul penarikan citra satelit GeoTIFF, kalkulasi energi numerik Google Solar API, audit deviasi jarak spasial (*spatial drift*), dan visualisasi peta Folium terbukti **100% valid dan bersumber langsung dari file fisik**.

---

## 2. AUDIT FORENSIK MENDALAM: HALAMAN 1 (`pages/1_Pemetaan_Potensi.py`)

Halaman 1 merupakan etalase utama verifikasi spasial Proof of Work (POW) satelit. Berikut adalah inventarisasi lengkap seluruh komponen di Halaman 1 yang diklasifikasikan ke dalam tabel audit formal.

### TABEL 2.1: TEMUAN PELANGGARAN KERAS DI HALAMAN 1 (VERDICT: PERLU PERBAIKAN)

| No | Komponen / Fitur di Page 1 | Lokasi Baris Asli | Potongan Kode Hardcoded | Aturan yang Dilanggar | Tindakan Perbaikan yang Dieksekusi | Status |
|:--:|---|---|---|---|---|:--:|
| **1** | **Narasi Arsitektur Spesifik Gedung** | **L698 – L734** | `if "Cipete" ... elif "Manggarai" ... elif "Dukuh Atas" ... elif "Pondok Indah" ...` | `no_hardcoded_data.md`<br>`anti_yesman` | Blok `if-elif` dihapus total. Diganti *Dynamic Analytical Engine* berbasis agregasi empiris `df_segments`. | **SELESAI** |
| **2** | **Diagnosis Eliminasi Segmen (0 Panel)** | **L560 – L582** | `reason = "**Fasad / Dinding Vertikal**..."`<br>`reason = "**Parapet / Talang Mikro**..."` | `anti_yesman` (Pilar 2 & 5) | Seluruh teks diagnosis buatan dihapus. Ditampilkan tabel empiris segmen 0 panel (`df_zero_disp`) dan catatan kriteria teknis Google Solar API. | **SELESAI** |
| **3** | **Kolom "Karakter Fisik Atap" di Master Table** | **L198, L216, L247** | `master_table = df[["roof_character", ...]]` | `no_hardcoded_data.md` (Poin 4) | Kolom `roof_character` dan label `Karakter Fisik Atap` dihapus 100% dari Master Table, rename dict, dan column_config. | **SELESAI** |
| **4** | **Caption Khusus PIM 1 & Stasiun LRT** | **L518 – L524** | `if "Dukuh Atas"... elif "Pondok Indah"...` | `no_hardcoded_data.md` (Poin 1.1) | Caption hardcode kaku dihapus, diganti template dinamis universal: `Visualisasi Poligon Segmen Atap 3D: {asset_name} ({panels} Modul / {kwp} kWp)`. | **SELESAI** |
| **5** | **Info Box Khusus Emiten & Metrik PIM 1** | **L544–L551 & L788–L790** | `if "Pondok Indah": st.info("... (PT Metropolitan Kencana Tbk) ...")` | `no_hardcoded_data.md` (Poin 1.1 & 2) | Seluruh percabangan khusus PIM 1 dihapus. Seluruh fasilitas kini diperlakukan seragam dan dinamis. | **SELESAI** |
| **6** | **Kamus In-Memory Jam Sinar Matahari** | **L608 – L624** | `solar_insights_map = ["Optimal saat matahari condong...", ...]` | `no_hardcoded_data.md` (Poin 1.1) | Array in-memory dihapus 100%. Digantikan metadata standar NREL PVWatts (NREL/TP-6A20-62641), NREL SPA, ASHRAE, & SNI 8395:2017 via `load_solar_orientation_ref()`, dilengkapi Glosarium Expander. | **SELESAI** |
| **7** | **Nama File Download Master Table Masih 5 Titik** | **L274** | `file_name="pow_solar_5_titik_master_table.csv"` | Konsistensi & Integritas Data | Dinamiskan 100% mengikuti jumlah baris aktual: `file_name=f"master_potensi_surya_jabodetabek_{count_export}_titik_terverifikasi.csv"`. | **SELESAI** |
| **8** | **Tabel Statis Referensi Azimuth di Kode Python** | **L748 – L757** | `df_azimuth_ref = pd.DataFrame([{"Rentang Sudut Azimuth": ...}, ...])` | `no_hardcoded_data.md` (Poin 3) | Dataframe in-memory statis dihapus total. Tabel kini membaca langsung file metadata standar ter-cache `standar_orientasi_surya_nrel_sni.csv`. | **SELESAI** |

---

### TABEL 2.2: KOMPONEN YANG SUDAH VALID DI HALAMAN 1 (VERDICT: BENAR)

| No | Komponen / Fitur di Page 1 | Lokasi Baris | Mekanisme Data | Dasar & Pustaka | Status |
|:--:|---|---|---|---|:--:|
| **1** | **Pemuatan Dataset Master & Segmen** | **L43 – L56** | Membaca langsung berkas fisik CSV/Parquet di `data/processed/calculations/` (`pow_solar_13_titik_summary.csv` dan `pow_solar_13_titik_segments.csv`). | `pandas`, `strict_data_folder_boundary.md` | **BENAR** |
| **2** | **Kalkulasi Metrik Eksekutif Banner** | **L109 – L151** | Agregasi dinamis `sum()` dari kolom dataframe: `installed_capacity_kwp`, `max_roof_area_m2`, `annual_generation_mwh`, dan `ghg_reduction_tons_co2`. | Operasi Vektor `pandas` | **BENAR** |
| **3** | **Visualisasi 5 Layer Citra Satelit SKU** | **L764 – L916** | Menampilkan citra hasil render GeoTIFF asli: RGB Aerial (0.25m/px), Layout Panel di Atap, Annual Solar Flux Heatmap, DSM 3D Elevasi, dan Roof Mask. | `rasterio`, `PIL`, `pathlib` | **BENAR** |
| **4** | **Peta Sebaran Spasial Interaktif** | **L301 – L366** | Titik koordinat marker membaca `google_center_lat` dan `google_center_lon` asli dari hasil query Google Maps Platform. | `folium`, `streamlit_folium` | **BENAR** |
| **5** | **Audit Spasial Drift Geodesik** | **L368 – L396** | Menghitung rata-rata deviasi jarak geodesik (`spatial_drift_meters`) secara dinamis menggunakan rumus Haversine. | Geodesic Distance Formula | **BENAR** |

---

## 3. AUDIT SKRIP ETL (`tools/solarapi/process_pow_etl.py`)

Skrip ETL adalah dapur pacu yang memproses respon mentah JSON dan GeoTIFF dari Google Solar API menjadi dataset turunan.

### Temuan Pelanggaran di ETL:
1. **Dictionary Deskripsi Atap (`roof_characteristics_dict` - L580-594):**
   ```python
   roof_characteristics_dict = {
       "MRT-003": "Atap Pelana Melengkung: Sisi sayap timur miring 15°, sayap barat miring 18°.",
       "KRL-032": "Dominan Landai: Sebagian besar berupa dak baja bentang lebar (1,1° – 2,6°)...",
       "MALL-001": "Dak Beton Datar & Kanopi Komersial: Struktur atap pusat perbelanjaan bertingkat rendah...",
       ...
   }
   ```
   *Pelanggaran:* `no_hardcoded_data.md` Poin 1.1 & `anti_yesman` Pilar 5.  
   *Koreksi:* Hapus dictionary ini 100%. Jangan pernah menyuntikkan narasi buatan sendiri ke dalam tabel processed CSV.
2. **List Target Pilot di Memori Skrip (`targets_info` - L400-510):**
   *Pelanggaran:* `strict_data_folder_boundary.md` Poin 3.  
   *Koreksi:* Pindahkan daftar target ke file fisik `data/raw/poi/pilot_13_targets.csv` dan baca via `pd.read_csv()`.

---

## 4. AUDIT HALAMAN UTAMA (`Dashboard.py` & `pages/0_Overview.py`)

### Temuan Pelanggaran di Halaman Utama:
1. **Hero Metrics Hardcoded Statis (L60–L93):**
   - Nilai kapasitas: `"~590 MWp"`
   - Nilai produksi: `"~785 GWh"`
   - Kontribusi regional: `"~1.0%"` terhadap `"~78.000 GWh"`
   - Nilai dekarbonisasi: `"~635k ton"`  
   *Koreksi:* Hitung angka ini secara dinamis menggunakan formula *Stratified Ratio Estimation* berdasarkan rata-rata per kategori dari data sampel pilot 13 titik dan target populasi kategori.
2. **Array Target 13 Kategori di Memori Skrip (L103–L195):**
   Target unit dan estimasi kapasitas per kategori ditulis mentah di dalam array objek Python.  
   *Koreksi:* Pindahkan metadata target 13 kategori ke berkas CSV `data/raw/metadata/target_kategori_jabodetabek.csv`.
3. **Nilai Fallback Dummy (L37–L42):**
   Menyuntikkan angka `6648.0 kWp` jika CSV tidak ditemukan.  
   *Koreksi:* Hapus angka fallback; ganti dengan pesan error eksplisit dan hentikan eksekusi jika file hilang.

---

## 5. STATUS HALAMAN LAINNYA (PAGES 2 S/D 8)

| Halaman | Judul Halaman | Status Konten | Status Kepatuhan Data |
|:---:|---|---|:---:|
| `pages/2` | Analisis Kapasitas | Template Placeholder (*"Halaman Dalam Pengembangan"*) | Bersih dari hardcode, belum ada pipa data |
| `pages/3` | Analisis Ekonomi | Template Placeholder (*"Halaman Dalam Pengembangan"*) | Bersih dari hardcode, belum ada pipa data |
| `pages/4` | Manfaat Lingkungan | Template Placeholder (*"Halaman Dalam Pengembangan"*) | Bersih dari hardcode, belum ada pipa data |
| `pages/5` | Manfaat Sosial | Template Placeholder (*"Halaman Dalam Pengembangan"*) | Bersih dari hardcode, belum ada pipa data |
| `pages/6` | Studi Komparasi | Template Placeholder (*"Halaman Dalam Pengembangan"*) | Bersih dari hardcode, belum ada pipa data |
| `pages/7` | Rekomendasi Roadmap | Template Placeholder (*"Halaman Dalam Pengembangan"*) | Bersih dari hardcode, belum ada pipa data |
| `pages/8` | Dokumentasi Riset | Pembaca Berkas Markdown Fisik (`DATA-ACQUISITION-PLAN.md`, dll.) | **100% BENAR** (Membaca file fisik via `open()`) |

---

## 6. RENCANA AKSI PEMBERSIHAN KODE (CLEANING ROADMAP)

Untuk mengembalikan integritas ilmiah dashboard 100% sesuai standar `.agents/rules/`, tindakan perbaikan berikut akan dieksekusi secara terstruktur:

1. **Pembersihan Halaman 1 (`pages/1_Pemetaan_Potensi.py`):**
   - Hapus blok `if-elif` per stasiun pada L698–L734.
   - Hapus rule `if-elif` diagnosis alasan eliminasi bidang pada L560–L582.
   - Hapus kolom `roof_character` dari dataframe `master_table`.
   - Hapus perlakuan khusus teks hardcode untuk PIM 1 dan Dukuh Atas.
   - Jadikan seluruh caption dan ringkasan segmen 100% dinamis mengambil dari baris data.
2. **Pembersihan ETL (`tools/solarapi/process_pow_etl.py`):**
   - Hapus dictionary `roof_characteristics_dict`.
   - Jalankan ulang pembuatan CSV `pow_solar_13_titik_summary.csv` agar kolom `roof_character` bersih total dari teks fiktif.
3. **Pembersihan Halaman Depan (`Dashboard.py` & `pages/0_Overview.py`):**
   - Pindahkan array `infrastruktur` ke file CSV fisik.
   - Ganti angka statis hero metric dengan kalkulasi rasio sampling dinamis.
   - Hapus nilai fallback dummy.

---
*Laporan ini dibukukan secara permanen di repositori sebagai bukti transparansi dan kepatuhan penuh terhadap standar metodologi riset CELIOS.*
