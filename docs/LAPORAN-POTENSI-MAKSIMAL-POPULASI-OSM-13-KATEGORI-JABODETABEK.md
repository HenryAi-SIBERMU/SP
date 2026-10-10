# Laporan Pemetaan Potensi Maksimal Populasi Berbasis Bank Data OSM & Data Resmi
## Sensus 13 Kategori Infrastruktur Publik Dual-Use PLTS Atap se-Jabodetabek
**Dokumen Referensi:** Riset Potensi PLTS Atap Kawasan Aglomerasi Jabodetabek — Celios & Mitra  
**Status Dokumen:** 🟢 Laporan Resmi Pemetaan Kapasitas Spasial & Potensi Makro  
**Versi:** 1.0  
**Tanggal:** 10 Oktober 2026  
**Penulis:** Tim Data & Geospasial Celios  
**Rujukan Regulasi Internal:** `.agents/rules/anti_yesman_spatial_methodology_integrity.md`, `.agents/rules/no_hardcoded_data.md`, & `.agents/rules/strict_data_folder_boundary.md`  

---

## 📌 1. Ringkasan Eksekutif

Dalam perencanaan awal riset implementasi *Google Solar API*, jumlah objek yang dianalisis dibatasi secara ketat pada pagu **2.000 titik infrastruktur** se-Jabodetabek. Pembatasan ini **murni dipicu oleh kendala pagu anggaran operasional Cloud Billing GCP (alokasi Rp 5.000.000)**, bukan karena keterbatasan aset fisik di lapangan.

Laporan ini menyajikan hasil sensus kapasitas penuh (*unconstrained capacity audit*) dari bank database lokal OpenStreetMap (OSM) dan dataset resmi operasional yang tersimpan di direktori `data/raw/`. 

### Temuan Kunci Sensus:
1. **Daya Tampung Riil 13 Kategori:**  
   Jika tidak dibatasi oleh biaya API, bank data spasial Jabodetabek memiliki **12.397 titik beratap dan bernama resmi** (dengan fokus Halte koridor BRT terintegrasi) atau mencapai **19.132 titik** jika menyerap seluruh halte/shelter tiang angkutan umum *feeder* (Biskita Bogor, Tayo Tangerang, Trans Patriot Bekasi, dll.).
2. **Tingkat Penyerapan Kuota Riset Saat Ini:**  
   Pagu 2.000 titik yang sedang berjalan saat ini baru menyerap **~10,4%** dari total potensi fasilitas fisik yang memenuhi kualifikasi atap permanen di Jabodetabek.
3. **Potensi Ekstra Klaster Kantor Pemerintah:**  
   Di luar 13 kategori utama, OpenStreetMap menyimpan **3.179 titik Gedung Pemerintah (`office=government`)** bernama resmi di Jabodetabek. Jika diintegrasikan, total aset publik beratap menembus **> 22.000 titik**.

---

## 🔬 2. Metodologi Audit & Batasan Geospasial

### A. Parameter Geospasial (Bounding Box Jabodetabek)
Seluruh titik diekstraksi dan difilter menggunakan koordinat batas resmi Aglomerasi Jabodetabek:
$$\text{BBOX} = [\text{Lat: } -6.65 \text{ s.d. } -6.05, \text{ Lon: } 106.55 \text{ s.d. } 107.15]$$
Mencakup: Provinsi DKI Jakarta, Kota & Kab. Bogor, Kota Depok, Kota & Kab. Tangerang, Kota Tangerang Selatan, serta Kota & Kab. Bekasi.

### B. Protokol Integritas Metodologi (Zero Dummy Entities)
Sesuai amanat [`.agents/rules/anti_yesman_spatial_methodology_integrity.md`](file:///C:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/.agents/rules/anti_yesman_spatial_methodology_integrity.md):
- **Wajib Memiliki Nama Resmi (`name IS NOT NULL`):** Menolak seluruh entitas tanpa identitas kepemilikan.
- **Pembersihan Entitas Sintetis:** Dilarang menggunakan label buatan berbasis ID poligon angka seperti `#OSM_ID` atau `#139546494`.
- **Deduplikasi Spasial Mutlak:** Menggunakan algoritma pohon spasial `scipy.spatial.cKDTree` dengan radius toleransi 20–50 meter untuk mencegah titik tumpang-tindih (*overlapping points*).

---

## 📊 3. Tabel Sensus Potensi Penuh: Kuota Riset vs Kapasitas Riil Bank Data

Tabel berikut memetakan perbandingan antara alokasi kuota anggaran 2.000 titik saat ini dengan populasi riil yang terverifikasi pada bank data repositori:

| No | Kategori Infrastruktur | Klaster Sektor | Kuota Riset Saat Ini *(Pagu Budget)* | Potensi Maksimal Bank Data *(Entitas Bernama & Beratap)* | Rasio Penyerapan Kuota | File Sumber Primer Lokal (`data/raw/`) | Keterangan & Karakteristik Populasi di Lapangan |
|:---:|:---|:---|:---:|:---:|:---:|:---|:---|
| 1 | **Sekolah Menengah & Dasar** | Edukasi Publik | **450** | **8.295** | 5,4% | `osm/schools_osm_overpass.json` | **Sangat Melimpah**. Mencakup SMA, SMK, SMP, MA, dan SD negeri/swasta bernama. Bentuk atap pelana/dak sangat ideal untuk fotogrametri surya. |
| 2 | **Fasilitas Kesehatan (RS & Puskesmas)** | Layanan Kesehatan | **300** | **2.569** | 11,7% | `osm/hospitals_jakarta.gpkg` & Overpass Query | **Melimpah**. Terdiri dari 620 RS Rujukan/Swasta dan 1.949 Klinik & Puskesmas Kecamatan/Kelurahan. Memiliki profil beban listrik 24 jam (*baseload*). |
| 3 | **Universitas & Kampus** | Edukasi Publik | **180** | **556** | 32,4% | `osm/universities_osm_overpass.json` | **Sangat Memadai**. Gedung rektorat dan fakultas bertingkat dengan komitmen dekarbonisasi kampus hijau. |
| 4 | **Halte Bus (BRT & Shelter Transit)** | Transportasi Bus | **400** | **7.135** *(OSM)* <br> *(7.644 di CSV Resmi)* | 5,6% | `transjakarta/transjakarta_stations.csv` & `osm/bus_stops_jakarta.gpkg` | **Sangat Melimpah**. 400 titik mencakup halte koridor BRT utama; 7.135 titik mencakup seluruh shelter feeder transit Jabodetabek (Biskita Bogor, Tayo, dll). |
| 5 | **Gedung Parkir (MSCP)** | Parkir Beratap | **100** | **101** | 99,0% | `osm/parking_jakarta.gpkg` | **Mentok / Sensus Penuh**. Dari 946 poligon parkir di OSM, hanya 101 yang merupakan gedung beratap dengan nama resmi (sisanya lapangan aspal terbuka). |
| 6 | **Pasar Tradisional & Rakyat** | UMKM / Perdagangan | **100** | **107** | 93,5% | `poi/candidates_2200_titik.csv` | **Mendekati Sensus Penuh**. Mencakup seluruh pasar kelolaan Perumda Pasar Jaya dan pasar induk kota/kabupaten penyangga. |
| 7 | **Stasiun KRL Commuter Line** | Transportasi Rel | **80** | **88** | 90,9% | `krl/krl_stations.csv` & `osm/stations_jakarta.gpkg` | **Mendekati Sensus Penuh**. 88 adalah populasi total seluruh stasiun aktif komuter di seluruh Daerah Operasi (Daop) 1 Jabodetabek. |
| 8 | **Pusat Perbelanjaan / Mall** | Komersial Modern | **80** | **85** | 94,1% | `poi/candidates_2200_titik.csv` | **Mendekati Sensus Penuh**. 85 titik mencakup hampir 100% mall komersial kelas A & B di seluruh kawasan aglomerasi. |
| 9 | **Stadion, GOR & Arena Olahraga** | Fasilitas Publik | **55** | **67** | 82,1% | `poi/candidates_2200_titik.csv` | **Mendekati Sensus Penuh**. Seluruh gelanggang olahraga terdaftar di Jabodetabek (termasuk JIS, GBK, Patriot, Pakansari). |
| 10 | **Terminal Bus & Simpul Antarmoda** | Simpul Transit | **35** | **43** | 81,4% | `poi/candidates_2200_titik.csv` | **Mendekati Sensus Penuh**. Mencakup terminal bus Tipe A dan Tipe B se-Jabodetabek (Pulogebang, Kampung Rambutan, Baranangsiang, dll). |
| 11 | **Stasiun MRT & LRT** | Transportasi Rel | **35** | **37** | 94,6% | `mrt_lrt/mrt_stations.csv` & `lrt_*.geojson` | **100% Populasi Fisik**. MRT Fase 1 (13 stasiun), LRT Jabodebek (18 stasiun), dan LRT Jakarta (6 stasiun). |
| 12 | **Jembatan Penyeberangan (JPO) Beratap** | Pedestrian Terintegrasi | **30** | **35** | 85,7% | `jpo/jpo_jakarta.csv` & data Bina Marga | **100% Populasi Beratap**. Hanya 35 JPO yang memiliki struktur atap kanopi permanen yang kokoh untuk menopang beban modul surya. |
| 13 | **Fasilitas Penunjang Bandara** | Logistik Khusus | **15** | **14** | 100,0% | `poi/candidates_2200_titik.csv` | **100% Populasi Fisik**. Terminal penumpang, kargo, dan fasilitas perawatan pesawat (GMF AeroAsia) Soetta & Halim. |
| 🎯 | **SUBTOTAL 13 KATEGORI (FOKUS BRT)** | | **2.000** | **12.397 Titik** | **16,1%** | | **Skenario Halte difokuskan pada Koridor BRT terintegrasi.** |
| 🌟 | **TOTAL POTENSI MAKSIMAL (FULL FEEDER)** | | **2.000** | **19.132 Titik** | **10,4%** | | **Skenario seluruh Shelter Transit perkotaan Jabodetabek diserap.** |

---

## 🏛️ 4. Potensi Kategori Ekstra: Gedung Kantor Pemerintah

Di luar 13 kategori eksisting, OpenStreetMap wilayah Jabodetabek menyimpan data kantor institusi publik yang sangat masif:

| Kategori Tambahan | Parameter Query OSM | Jumlah Entitas Bernama | Status Legalitas & Relevansi Kebijakan |
|:---|:---|:---:|:---|
| **Gedung & Kantor Pemerintah** | `office=government` + `name!=null` | **3.179 titik** | Sangat Strategis. Mendukung mandat **Inpres No. 7/2022** tentang Percepatan Pemanfaatan PLTS Atap pada Gedung Instansi Pemerintah Pusat dan Daerah (Balai Kota, Kantor Walikota/Bupati, Kantor Camat, Lurah, dan Dinas Teknis). |

> Jika kategori Kantor Pemerintah ini dimasukkan ke dalam portofolio riset, total potensi publik di Jabodetabek mencapai **22.311 titik**.

---

## 🔍 5. Analisis Tipologi & Karakteristik Data Lapangan

Dari pembacaan tabel di atas, 13 kategori infrastruktur terbagi ke dalam 3 kelompok perilaku data:

### A. Kelompok "Sensus Penuh" (*Saturated / Finite Population*)
Kategori seperti **Stasiun Rel (KRL/MRT/LRT), Bandara, Mall, Terminal Bus, dan JPO Beratap** memiliki jumlah fisik yang memang terbatas di dunia nyata. 
* Kuota riset 2.000 titik saat ini **sudah berhasil menyerap 80% hingga 100% dari seluruh aset riil yang ada**.
* Penambahan anggaran untuk kategori ini tidak akan menaikkan jumlah titik secara signifikan karena populasinya sudah hampir habis disensus.

### B. Kelompok "Raksasa Terpangkas Biaya" (*Mega-Scale Inventory*)
Kategori **Sekolah (8.295 titik), Fasilitas Kesehatan (2.569 titik), Universitas (556 titik), dan Halte Bus Feeder (>7.000 titik)** adalah sektor yang paling terdampak oleh batasan anggaran.
* Kuota 2.000 titik saat ini hanya mengambil **5% – 30%** dari total populasi.
* Sektor ini merupakan "ladang emas" jika ada ekspansi riset di masa depan, karena atap bangunannya luas, bertingkat, dan memiliki legalitas aset publik yang jelas.

### C. Kelompok "Anomali Data Spasial" (*Data Bottleneck*)
Kategori **Gedung Parkir (MSCP)** hanya memiliki 101 titik bernama resmi di OpenStreetMap.
* Dari 946 poligon berlabel `amenity=parking`, 845 di antaranya adalah lapangan aspal terbuka (*surface lot*) tanpa atap permanen dan tanpa nama.
* Oleh karena itu, kuota 100 titik pada riset saat ini sudah merupakan angka plafon maksimal yang jujur secara ilmiah agar tidak terjadi halusinasi data fotogrametri pada aspal terbuka.

---

## ⚡ 6. Proyeksi Dampak Kapasitas Energi (MWp)

Berdasarkan benchmark rata-rata kapasitas terpasang per kategori dari data uji coba Google Solar API:

| Skenario Pemetaan | Jumlah Titik | Estimasi Kapasitas Daya (MWp) | Estimasi Produksi Listrik (GWh/tahun) | Keterangan |
|:---|:---:|:---:|:---:|:---|
| **Skenario Pagu Anggaran Saat Ini** | 2.000 titik | **180 – 260 MWp** | 250 – 360 GWh/thn | Dibatasi anggaran Rp 5 Juta (Google Solar API). |
| **Skenario Maksimal 13 Kategori (Fokus BRT)** | 12.397 titik | **750 – 1.100 MWp** | 1.050 – 1.540 GWh/thn | Menyerap seluruh sekolah, RS, kampus, pasar, dan mall bernama. |
| **Skenario Sensus Lengkap (+ Feeder & Pemda)** | 22.311 titik | **1.400 – 2.200 MWp** | 1.960 – 3.080 GWh/thn | Menjadikan Jabodetabek lumbung energi surya terdistribusi mandiri. |

---

## 🚀 7. Rekomendasi Strategis untuk Celios

1. **Tahap 1 (Saat Ini — Pagu 2.000 Titik):**
   * Tuntaskan eksekusi penarikan data Google Solar API untuk 2.000 titik terkurasi bersih (0 entitas dummy) untuk membuktikan kelayakan metodologi secara presisi.
2. **Tahap 2 (Advokasi Pendanaan Hibah / Fase Lanjutan):**
   * Gunakan tabel sensus 12.397 titik ini sebagai bahan proposal ke donor/mitra strategis (seperti Bloomberg Philanthropies, Tara Climate, atau Kementerian ESDM) untuk memperluas jangkauan analisis ke seluruh populasi sekolah dan rumah sakit di kawasan aglomerasi Jabodetabek.
3. **Pemanfaatan Alternatif Non-API untuk Skala Penuh:**
   * Untuk mengolah seluruh 12.000+ titik tanpa membebani biaya API Google ($60+ per 1.000 titik), tim dapat mengombinasikan data 2.000 titik Google Solar API sebagai *ground-truth benchmark*, lalu mengekstrapolasi sisa 10.000+ titik menggunakan poligon *building footprints* dari **Overture Maps Foundation / Bing Footprints** yang tersedia secara gratis.
