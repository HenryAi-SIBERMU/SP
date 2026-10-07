# Strategi Eksekusi 5 Pilar: Skalasi 2.000 Titik Potensi PLTS Atap Jabodetabek
## Riset Potensi Energi Surya - Celios & Mitra
**Versi Dokumen:** 1.0  
**Tanggal:** 6 Oktober 2026  
**Status:** Draf Strategis (Disetujui untuk Implementasi Bertahap)  
**Referensi Pagu Anggaran:** Rp 5.000.000 (RAB Ref: `2026-09-27-celios8-solar-rab-annualflux.html`)

---

## 📌 Ringkasan Eksekutif

Setelah keberhasilan eksekusi **100 Titik Pilot Representatif** (Proof of Work) yang mencakup 13 kategori infrastruktur se-Jabodetabek dengan total kapasitas **70,93 MWp** (177.329 panel surya), proyek kini melangkah ke fase utama: **Skalasi Penuh Menuju 2.000 Titik Infrastruktur Aglomerasi Jabodetabek**.

Dokumen ini menetapkan **5 Pilar Strategis** yang dirancang berdasarkan temuan empiris fase pilot untuk memastikan penarikan data berjalan **cepat, presisi tinggi secara spasial, hemat biaya (di bawah pagu Rp 5 juta), dan aman terhadap batasan penyimpanan/repositori**.

```
+----------------------------------------------------------------------------------------------------+
|                                    KERANGKA STRATEGI 5 PILAR                                       |
+----------------------------------------------------------------------------------------------------+
|  [Pilar 1] Kurasi Data & Komposisi Kategori (13 Kategori, 2.000 Titik Terverifikasi)               |
|  [Pilar 2] Filter Spasial Anti-404 & Micro-Targeting (Pre-Validation Bounding Mesh)                |
|  [Pilar 3] Arsitektur Eksekusi Bertahap (8 Batch @ 250 Titik, Rate Limiter, Smart Checkpoint)      |
|  [Pilar 4] Manajemen Penyimpanan & Repositori Git (Pemisahan Tabular Master vs Raster Masif)       |
|  [Pilar 5] Pengendalian Anggaran Riil GCP & Protokol Proteksi Saldo (Maks. ~Rp 1,2 Juta)          |
+----------------------------------------------------------------------------------------------------+
```

---

## PILAR 1: Kurasi Sumber Data & Komposisi Kategori

Target 2.000 titik dibagi secara proporsional ke dalam 13 kategori infrastruktur publik dan komersial, dengan memanfaatkan aset data mentah yang telah tersedia di repositori lokal (`data/raw/`):

### A. Alokasi Titik Per Kategori

| No | Kategori Infrastruktur | Klaster | Target Titik | Porsi (%) | Sumber Data Mentah Lokal |
|:---|:---|:---:|:---:|:---:|:---|
| 1 | **Halte TransJakarta & Bus Shelter** | Transit | 400 | 20,0% | `data/raw/transjakarta/transjakarta_stations.csv` |
| 2 | **Stasiun KRL Commuter Line** | Transit | 80 | 4,0% | `data/raw/krl/krl_stations.csv` (seluruh stasiun aktif) |
| 3 | **Stasiun MRT & LRT** | Transit | 40 | 2,0% | `data/raw/mrt_lrt/*.geojson` (seluruh stasiun aktif) |
| 4 | **Terminal Bus & Simpul Antarmoda** | Transit | 30 | 1,5% | `data/raw/osm/terminals_jakarta.geojson` & GPKG |
| 5 | **Gedung Parkir & Area Parkir (MSCP)** | Parkir | 900 | 45,0% | `data/raw/osm/parking_jakarta.gpkg` |
| 6 | **Sekolah Menengah (SMA/SMK/SMP)** | Publik | 150 | 7,5% | `data/raw/osm/education_jakarta.geojson` |
| 7 | **Universitas & Kampus** | Publik | 50 | 2,5% | `data/raw/osm/education_jakarta.geojson` |
| 8 | **Rumah Sakit & Fasilitas Medis** | Publik | 100 | 5,0% | `data/raw/osm/hospitals_jakarta.gpkg` |
| 9 | **Pasar Tradisional (PD Pasar Jaya)** | Publik | 80 | 4,0% | `data/raw/osm/markets_jakarta.geojson` |
| 10 | **Pusat Perbelanjaan / Mall** | Komersial | 70 | 3,5% | `data/raw/osm/commercial_jakarta.geojson` |
| 11 | **Stadion, GOR & Arena Olahraga** | Publik | 50 | 2,5% | `data/raw/osm/sports_jakarta.geojson` |
| 12 | **Fasilitas Penunjang Bandara** | Logistik | 20 | 1,0% | `data/raw/osm/airports_jakarta.geojson` |
| 13 | **Jembatan Penyeberangan Orang (JPO)** | Transit | 30 | 1,5% | `data/raw/jpo/` (Kanopi percontohan terpilih) |
| **TOTAL** | **13 Kategori Gabungan** | - | **2.000** | **100,0%** | **100% Berbasis Dataset Lokal Terkurasi** |

### B. Prinsip Bebas Hardcoding (Zero Hardcoded Data)
* Seluruh titik wajib dihasilkan dari proses filter dan kurasi berbasis script (`tools/poi_curation/`).
* Tidak boleh ada penulisan koordinat manual di dalam script penarikan API.
* File master input disimpan dalam format standar: `data/raw/poi/target_2000_titik.csv` dan `target_2000_titik.geojson`.

---

## PILAR 2: Filter Spasial Anti-404 & Micro-Targeting

### A. Tantangan Cakupan Google Solar API di Wilayah Aglomerasi
Temuan empiris dari fase pilot menunjukkan bahwa:
1. **DKI Jakarta, Tangerang Kota, Tangerang Selatan, Depok, dan Bogor (Kota/Kab Barat):** Memiliki cakupan *stereoscopic 3D flight mesh* yang sangat rapat dan lengkap.
2. **Bekasi Timur & Pelosok Pinggiran Bodetabek:** Sebagian area berada di luar koridor penerbangan fotogrametri Google, sehingga API mengembalikan respon `HTTP 404 NOT_FOUND`.

### B. Mekanisme Fast-Probe (Pre-Validation Bounding Mesh)
Untuk mencegah kegagalan penarikan di tengah jalan:
1. **Modul Fast-Probe:** Sebelum script mengunduh file berat, modul probe ringan memverifikasi status koordinat kandidat ke endpoint Building Insights.
2. **Pool Kandidat Cadangan (Fallback Buffer):** Sistem menyiapkan daftar cadangan (*pool buffer*) sebesar 10% (~200 titik cadangan). Jika kandidat utama berstatus 404, sistem secara otomatis menukar dengan kandidat terdekat dari kategori yang sama yang berada di dalam wilayah cakupan valid.
3. **Hasil:** Target 2.000 titik yang masuk ke pipeline penarikan final dijamin 100% valid tanpa eror 404.

### C. Standardisasi Micro-Snapping Kanopi
* Khusus infrastruktur transit ramping (Halte Busway dan Stasiun Kereta), titik koordinat yang bersumber dari aspal jalan raya akan digeser presisi 5–15 meter ke atas sumbu kanopi fisik atap agar Google Solar API tidak salah mengunci gedung ruko tetangga.

---

## PILAR 3: Arsitektur Eksekusi Bertahap (Batching, Pacing & Checkpoint)

Penarikan 2.000 titik dilarang dijalankan secara monolitik dalam satu proses panjang tanpa pengaman.

```
ALUR KERJA PER BATCH (250 TITIK):
[Kurasi Pool] ──> [Fast Probe] ──> [Fetch API] ──> [ETL Transform] ──> [Audit Quality] ──> [Git Commit]
```

### A. Pembagian 8 Batch Eksekusi (@ 250 Titik)

* **Batch 1:** Klaster Rel & Simpul Transit (KRL 80, MRT/LRT 40, Terminal 30, JPO 30, Fasilitas Bandara 20, Halte Koridor 1–3: 50 titik) — **250 Titik**
* **Batch 2:** Klaster Halte Busway Koridor Utama TransJakarta — **250 Titik**
* **Batch 3:** Klaster Halte Pengumpan & Shelter Non-BRT Bodetabek — **250 Titik**
* **Batch 4:** Gedung Parkir Vertikal & Park & Ride (MSCP Tahap 1) — **250 Titik**
* **Batch 5:** Lapangan Parkir Komersial & Terbuka (MSCP Tahap 2) — **250 Titik**
* **Batch 6:** Fasilitas Pendidikan (SMA/SMK Negeri 150 titik + Kampus 50 titik + Sekolah Bodetabek 50 titik) — **250 Titik**
* **Batch 7:** Fasilitas Kesehatan (RSUP/RSUD/Puskesmas 100 titik) + Pasar Tradisional (80 titik) + Fasilitas Publik 70 titik — **250 Titik**
* **Batch 8:** Pusat Perbelanjaan / Mall (70 titik) + Stadion/GOR (50 titik) + Parkir Mall/Komersial 130 titik — **250 Titik**

### B. Kecepatan Panggilan (Rate Limiter / Pacing)
* **Batas Maksimal Google:** 600 QPM (10 request/detik).
* **Ritme Operasional Aman:** **3 request/detik** (180 QPM).
* **Estimasi Waktu per Batch (250 Titik):**
  * Building Insights: ~1,5 menit.
  * Unduh Data Layers (4 GeoTIFF): ~6–10 menit.
  * Total durasi per batch: **~8–12 menit**.

### C. Smart Checkpoint & Idempotent Caching
* Setiap file mentah yang berhasil diunduh langsung disimpan di direktori `data/raw/solar/`.
* Script dilengkapi mekanisme verifikasi keberadaan file (`if out_file.exists(): continue`).
* Jika terjadi gangguan koneksi internet atau kendala daya di titik ke-1.120, script dapat langsung dilanjutkan kembali dari titik ke-1.121 tanpa mengulang titik-titik sebelumnya dan tanpa risiko biaya ganda (*zero double-billing*).

---

## PILAR 4: Manajemen Penyimpanan (Storage) & Repositori Git

### A. Estimasi Volume Data 2.000 Titik

| Komponen Data | Jumlah File | Rata-rata Ukuran per File | Total Estimasi Ukuran | Penanganan Git |
|:---|:---:|:---:|:---:|:---|
| **JSON Building Insights** | 2.000 file | ~40 KB | **~80 MB** | **Wajib di-commit** ke Git |
| **Data Tabular Hasil ETL**<br>*(CSV, Parquet, GeoJSON)* | ~6 file master | ~5 MB | **~20 MB** | **Wajib di-commit** ke Git |
| **GeoTIFF Raster Mentah**<br>*(DSM, RGB, Mask, Flux)* | 8.000 file | ~1 MB | **~6 – 8 GB** | **Diabaikan (.gitignore)**<br>Tersimpan lokal |
| **Gambar SKU Preview (PNG)**<br>*(Jika digenerate semua)* | 12.000 file | ~700 KB | **~8 – 10 GB** | **Dibatasi / Selective** |

### B. Strategi Pengamanan GitHub (Mencegah Error Push & Timeout)
1. **Raster GeoTIFF (.tif):** Sudah masuk aturan `.gitignore` (`data/raw/**/*.tif`), sehingga tidak membebani repositori remote GitHub.
2. **Data Tabular & Spasial (Output Inti):** Disimpan dalam format kompresi tinggi (`.parquet` dan `.geojson`), di-commit dan di-push bertahap per batch.
3. **Kartu Visualisasi SKU (Preview PNG):**
   * *Rekomendasi:* Visualisasi kartu teknis digenerate secara penuh untuk **250 titik percontohan unggulan (Showcase Pilot)** (~1.500 file PNG, ~1,2 GB).
   * Untuk sisa 1.750 titik lainnya, kartu visualisasi dapat di-render secara *on-demand* di Streamlit Dashboard menggunakan citra GeoTIFF lokal tanpa perlu menimbun belasan ribu file PNG statis di git.

---

## PILAR 5: Pengendalian Anggaran Riil GCP & Proteksi Saldo

### A. Struktur Penagihan Resmi Google Maps Platform (Environment APIs)
Berdasarkan ketentuan resmi Google Maps Platform:
* **Solar API - Building Insights:** Mendapatkan jatah gratis **10.000 requests / bulan**.
* **Solar API - Data Layers:** Mendapatkan jatah gratis **1.000 requests / bulan**. Di atas kuota gratis, tarif resmi adalah **\$75,00 per 1.000 requests** (\$0,075 / call).
* **Fakta Kunci Billing Data Layers:** 1 kali panggilan ke endpoint `dataLayers:get` sudah mencakup **seluruh 4 layer GeoTIFF (DSM, RGB, Mask, Annual Flux)**. Google tidak menagih per file citra yang diunduh.

### B. Simulasi Anggaran Riil untuk 2.000 Titik

```
Perhitungan Biaya Aktual:
1. Building Insights (2.000 calls) : Masuk kuota gratis 10.000 calls/bulan  --> Rp 0,-
2. Data Layers (1.000 calls pertama): Masuk kuota gratis 1.000 calls/bulan  --> Rp 0,-
3. Data Layers (1.000 calls kedua)  : 1.000 calls x $0,075 = $75,00         --> Rp 1.185.000,-
-------------------------------------------------------------------------------------------------
TOTAL ESTIMASI BIAYA AKTUAL         : $75,00 (Kurs Rp 15.800)               --> ~Rp 1.185.000,-
PAGU DOKUMEN RAB RESMI CELIOS       : Rp 5.000.000,-
-------------------------------------------------------------------------------------------------
SISA SURPLUS ANGGARAN (HEMAT)       : ~Rp 3.815.000,- (Surplus ~76%)
```

### C. Protokol Keamanan Finansial (SOP Billing GCP)
1. **Budget Alert Threshold:** Di Google Cloud Console, batas notifikasi anggaran disetel ketat pada nilai **Rp 2.000.000**.
2. **Daily Quota Cap:** Menyetel batas aman harian maksimal 1.000 request per hari di menu *APIs & Services > Quotas* untuk mencegah konsumsi berlebih yang tidak disengaja.
3. **Audit Log Rutin:** Melakukan pengecekan billing dashboard GCP setelah setiap batch 250 titik selesai dieksekusi.

---

## 📅 Roadmap Tahapan Eksekusi

```
[Tahap 1: Persiapan & Kurasi] 
 └── Generate kandidat target 2.000 titik dari dataset lokal
 └── Jalankan Fast-Probe 404 filter & siapkan buffer fallback

[Tahap 2: Eksekusi Batch 1–4 (Titik 1 – 1.000)]
 └── Penarikan klaster transportasi, stasiun, halte, dan parkir
 └── Memanfaatkan kuota gratis 1.000 calls pertama Data Layers

[Tahap 3: Verifikasi Billing & Checkpoint Tengah]
 └── Audit saldo billing GCP setelah 1.000 titik selesai
 └── Konfirmasi kesiapan penarikan berbayar (maks ~$75) untuk titik 1.001 – 2.000

[Tahap 4: Eksekusi Batch 5–8 (Titik 1.001 – 2.000)]
 └── Penarikan fasilitas publik, sekolah, kampus, RS, pasar, mall, dan stadion
 └── ETL agregasi 2.000 titik penuh ke Parquet, CSV, dan GeoJSON

[Tahap 5: Laporan Akhir & Integrasi Dashboard]
 └── Penyusunan Laporan Analisis Potensi Energi Surya Aglomerasi Jabodetabek
 └── Sinkronisasi peta interaktif dan analitik ke Streamlit Dashboard
```
