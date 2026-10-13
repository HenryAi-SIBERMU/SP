# Tabel Master Khusus: Google Solar API (Building Insights & Data Layers)
**Kompilasi Pengelompokan Lengkap Parameter Query & Skema Data Return**  
*Pusat Referensi Teknis CELIOS Solar Dashboard (2026)*

---

## 1. Tabel Khusus Kategori 1: Building Insights

* **Endpoint URL:** `https://solar.googleapis.com/v1/buildingInsights:findClosest`
* **HTTP Method:** `GET`
* **Format Output:** JSON Tabular Objek Bersarang (*Hierarchical JSON Object*)
* **Tarif GCP:** **$0.010** per panggilan (tidak ditagih bila mengembalikan `404 NOT_FOUND`)
* **Fungsi Utama:** Analisis dimensi atap, potensi modul surya, karakter bidang atap 3D, dan energi listrik DC.

### Tabel Pengelompokan Komprehensif Building Insights

| Kategori / Klaster | Nama Field / Parameter | Tipe Data | Wajib / Opsional | Satuan / Opsi Nilai | Penjelasan Teknis & Fungsionalitas |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **INPUT QUERY (HTTP REQUEST)** | `location.latitude` | `Double` | **Wajib** | `-90.0` s.d. `+90.0` | Koordinat lintang titik target pencarian bangunan (WGS 84). |
| | `location.longitude` | `Double` | **Wajib** | `-180.0` s.d. `+180.0` | Koordinat bujur titik target pencarian bangunan (WGS 84). |
| | `requiredQuality` | `Enum` | Opsional | `BASE`, `MEDIUM`, `HIGH` | Ambang mutu citra minimal yang disyaratkan (default: `BASE`). |
| | `experiments` | `Enum[]`| Opsional | `EXPANDED_COVERAGE` | Opsi eksperimental untuk memperluas cakupan deteksi geografis. |
| | `key` | `String` | **Wajib** | Alfanumerik | Kunci otentikasi resmi Google Cloud Platform dengan billing aktif. |
| **IDENTITAS & SPASIAL GEDUNG (ROOT RESPONSE)** | `name` | `String` | Return | `buildings/{place_id}` | Resource name / ID bangunan unik di katalog geospasial Google Maps. |
| | `center` | `Object` | Return | `{"latitude", "longitude"}`| Koordinat titik tengah (*centroid*) fisik bidang geometri atap. |
| | `boundingBox` | `Object` | Return | Poligon `sw` dan `ne` | Batas bujur sangkar koordinat terluar yang melingkupi atap gedung. |
| | `imageryDate` | `Object` | Return | `{"year", "month", "day"}` | Tanggal pemotretan udara satelit yang mendasari analisis 3D. |
| | `imageryProcessedDate` | `Object` | Return | `{"year", "month", "day"}` | Tanggal pemrosesan algoritma fotogrametri oleh Google. |
| | `postalCode` | `String` | Return | String angka (misal: `"12160"`)| Kode pos wilayah gedung berada. |
| | `administrativeArea` | `String` | Return | String teks wilayah | Nama provinsi / daerah tingkat I (misal: `"DKI Jakarta"`). |
| | `regionCode` | `String` | Return | 2 Karakter ISO 3166 | Kode negara (misal: `"ID"` untuk Indonesia). |
| | `imageryQuality` | `Enum` | Return | `BASE` / `MEDIUM` / `HIGH` | Mutu resolusi citra riil yang berhasil diekstraksi Google. |
| **METRIK INTI POTENSI SURYA (`solarPotential`)** | `maxArrayPanelsCount` | `Integer` | Return | Unit Modul | **Jumlah modul surya maksimum** yang dapat dipasang di atap layak. |
| | `panelCapacityWatts` | `Float` | Return | Watt peak (Wp) | Daya nominal modul acuan bawaan Google (**400.0 Wp**). |
| | `panelHeightMeters` | `Float` | Return | Meter | Tinggi fisik modul surya acuan Google (**1.879 meter**). |
| | `panelWidthMeters` | `Float` | Return | Meter | Lebar fisik modul surya acuan Google (**1.045 meter**). |
| | `panelLifetimeYears` | `Integer` | Return | Tahun | Masa operasional garansi modul surya (**20 tahun**). |
| | `maxArrayAreaMeters2` | `Float` | Return | $m^2$ | **Luas atap efektif** yang layak panel surya bebas bayangan. |
| | `maxSunshineHoursPerYear`| `Float`| Return | Jam / Tahun | Jam penyinaran puncak ekuivalen (*Peak Sun Hours* / PSH per tahun). |
| | `carbonOffsetFactorKgPerMwh`| `Float`| Return | kg CO₂ / MWh | **Faktor intensitas emisi karbon grid regional** (**808.999 kg/MWh**). |
| | `wholeRoofStats` | `Object` | Return | `areaMeters2`, quantiles | Statistik luasan dan sebaran radiasi dari seluruh penampang atap. |
| | `buildingStats` | `Object` | Return | `areaMeters2`, quantiles | Statistik luas tapak dasar bangunan (*building footprint*). |
| **SEGMENTASI BIDANG ATAP 3D (`roofSegmentStats[]`)** | `pitchDegrees` | `Float` | Return | Derajat ($0^\circ$ s.d. $90^\circ$) | **Sudut kemiringan bidang atap** terhadap permukaan horizontal. |
| | `azimuthDegrees` | `Float` | Return | Derajat ($0^\circ$ s.d. $360^\circ$)| **Arah hadap kompas bidang atap** ($0^\circ$ Utara, $180^\circ$ Selatan). |
| | `planeHeightAtCenterMeters`| `Float`| Return | Meter | Elevasi ketinggian pusat segmen di atas permukaan tanah. |
| | `center` | `Object` | Return | `{"latitude", "longitude"}`| Koordinat centroid geospasial segmen atap spesifik. |
| | `boundingBox` | `Object` | Return | Poligon `sw` dan `ne` | Batas bujur sangkar koordinat segmen atap terkait. |
| | `stats.areaMeters2` | `Float` | Return | $m^2$ | Luas permukaan fisik 3D bidang segmen atap miring. |
| | `stats.groundAreaMeters2` | `Float` | Return | $m^2$ | Luas proyeksi 2D bidang segmen atap ke atas tanah datar. |
| | `stats.sunshineQuantiles` | `Float[11]`| Return | Jam / Tahun | 11 titik persentil radiasi fluks surya (0%, 10%, ..., 100%). |
| **LAYOUT MODUL PRESISI (`solarPanels[]`)** | `center.latitude` | `Double` | Return | Koordinat lintang | Titik lintang pusat fisik per keping modul surya di atap. |
| | `center.longitude` | `Double` | Return | Koordinat bujur | Titik bujur pusat fisik per keping modul surya di atap. |
| | `orientation` | `Enum` | Return | `PORTRAIT` / `LANDSCAPE` | Orientasi pemasangan modul di atap (vertikal / horizontal). |
| | `segmentIndex` | `Integer` | Return | `0, 1, 2, ...` | Indeks bidang atap tempat modul menempel di `roofSegmentStats`. |
| | `yearlyEnergyDcKwh` | `Float` | Return | kWh DC / tahun | **Energi listrik DC tahunan** yang diproduksi mandiri oleh modul ini. |
| **SKENARIO KAPASITAS BERTAHAP (`solarPanelConfigs[]`)**| `panelsCount` | `Integer` | Return | Unit Modul | Total modul yang dipasang pada skenario kapasitas tertentu. |
| | `yearlyEnergyDcKwh` | `Float` | Return | kWh DC / tahun | **Total energi listrik DC tahunan kotor** seluruh panel dalam skenario. |
| | `roofSegmentSummaries[]` | `Array` | Return | Rincian per segmen | Alokasi jumlah panel dan daya DC per masing-masing segmen atap. |

---

## 2. Tabel Khusus Kategori 2: Data Layers

* **Endpoint URL:** `https://solar.googleapis.com/v1/dataLayers:get`
* **HTTP Method:** `GET`
* **Format Output:** JSON berisi tautan unduh sementara (*Signed Cloud Storage URLs*) untuk mengunduh berkas raster **GeoTIFF**
* **Tarif GCP:** **$0.075** per panggilan (**1 call mencakup seluruh berkas raster GeoTIFF sekaligus**)
* **Fungsi Utama:** Validasi spasial citra satelit resolusi tinggi (0.25 m/pixel), elevasi 3D DSM, segmentasi mask atap, dan heatmap radiasi.

### Tabel Pengelompokan Komprehensif Data Layers

| Kategori / Klaster | Nama Field / Parameter | Tipe Data | Wajib / Opsional | Satuan / Opsi Nilai | Penjelasan Teknis & Fungsionalitas |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **INPUT QUERY (HTTP REQUEST)** | `location.latitude` | `Double` | Wajib* | `-90.0` s.d. `+90.0` | Koordinat lintang pusat kotak analisis raster (*Wajib bila tanpa bounding box). |
| | `location.longitude` | `Double` | Wajib* | `-180.0` s.d. `+180.0` | Koordinat bujur pusat kotak analisis raster (*Wajib bila tanpa bounding box). |
| | `radiusMeters` | `Float` | Wajib* | `0.0` s.d. `100.0` meter | Jari-jari cakupan raster (maksimal resmi Google adalah **100 meter**). |
| | `view` | `Enum` | Opsional | `FULL_LAYERS`, `DSM_ONLY`, `IMAGERY_AND_ANNUAL_FLUX` | Filter lapisan citra raster yang ingin dihasilkan (default: `FULL_LAYERS`). |
| | `requiredQuality` | `Enum` | Opsional | `BASE`, `MEDIUM`, `HIGH` | Tingkat mutu fotogrametri minimal yang diterima. |
| | `pixelSizeMeters` | `Float` | Opsional | Contoh: `0.25` meter | Resolusi spasial riil per piksel raster (standar: **0.25 m/piksel**). |
| | `exactBoundingBox.*` | `Object` | Opsional | Poligon `sw` dan `ne` | Batas bujur sangkar koordinat manual (alternatif dari `location` + `radius`). |
| | `experiments` | `Enum[]`| Opsional | `EXPANDED_COVERAGE` | Opsi eksperimental fitur preview Google. |
| | `key` | `String` | **Wajib** | Alfanumerik | Kunci otentikasi resmi GCP dengan tagihan billing aktif. |
| **METADATA RESPONSE JSON** | `imageryDate` | `Object` | Return | `{"year", "month", "day"}` | Tanggal akuisisi pemotretan udara satelit. |
| | `imageryProcessedDate` | `Object` | Return | `{"year", "month", "day"}` | Tanggal pemrosesan fotogrametri citra raster oleh Google. |
| | `imageryQuality` | `Enum` | Return | `BASE` / `MEDIUM` / `HIGH` | Tingkat resolusi spasial riil berkas raster yang disediakan. |
| **TAUTAN UNDUH GEOTIFF RASTER** | `rgbUrl` | `String` (URL) | Return | Berkas `.tif` Cloud Storage | Tautan unduh berkas GeoTIFF **Foto Udara Satelit Warna Sejati (RGB)**. |
| | `dsmUrl` | `String` (URL) | Return | Berkas `.tif` Cloud Storage | Tautan unduh berkas GeoTIFF **Digital Surface Model (DSM 3D)**. |
| | `maskUrl` | `String` (URL) | Return | Berkas `.tif` Cloud Storage | Tautan unduh berkas GeoTIFF **Roof Binary Mask**. |
| | `annualFluxUrl` | `String` (URL) | Return | Berkas `.tif` Cloud Storage | Tautan unduh berkas GeoTIFF **Annual Solar Flux Heatmap**. |
| | `monthlyFluxUrl` | `String` (URL) | Return | Berkas `.tif` Cloud Storage | Tautan unduh berkas GeoTIFF **Monthly Solar Flux Composite** (12 Band). |
| | `hourlyShadeUrls[]` | `String[12]` | Return | 12x Berkas `.tif` | Array 12 tautan unduh GeoTIFF **Hourly Shade Bitmask** (tgl 21 tiap bulan). |

---

### Tabel Spesifikasi Teknis 6 Berkas GeoTIFF Raster Data Layers

| Nama Berkas Raster | Tipe Data Piksel | Band | Rentang Nilai | Satuan Pengukuran | Nilai NoData | Fungsi Utama dalam Dashboard CELIOS |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Citra Foto Udara (RGB)** | `Uint8` (Byte) | 3 / 4 (RGBA) | `0` s.d. `255` | Spektrum Cahaya Tampak | `0` | Visualisasi latar belakang satelit asli fotogrametri resolusi tinggi. |
| **Digital Surface Model (DSM)** | `Float32` | 1 Band | `-50` s.d. `8.000` | **Meter** di atas geoid WGS84 | `-9999.0` | Menghitung ketinggian gedung, kemiringan atap (*pitch*), dan model 3D. |
| **Roof Binary Mask** | `Uint8` (Byte) | 1 Band | `0` atau `1` | Indeks Kategori Biner | `0` | Memotong tapak atap bangunan dari lingkungan sekitar (jalan/pohon). |
| **Annual Solar Flux Heatmap** | `Float32` | 1 Band | `0` s.d. `2.500` | **$kWh/kWp/tahun$** | `-9999.0` | Memetakan titik atap terik vs bayangan untuk menentukan penempatan panel. |
| **Monthly Solar Flux** | `Float32` | 12 Band | `0` s.d. `300` | **$kWh/kWp/bulan$** | `-9999.0` | Menganalisis variasi musiman produksi energi surya (kemarau vs hujan). |
| **Hourly Shade Bitmask** | `Uint32` | 12 Berkas | Bitmask 24-bit | Status Penyinaran per Jam | `0` | Menghitung bayangan gedung tetangga pada tanggal 21 setiap bulan. |

---

## 3. Tabel Perbandingan & Matriks Interoperabilitas: Building Insights vs Data Layers

Tabel berikut memetakan bagaimana kedua endpoint saling melengkapi dalam pipeline riset geospasial:

| Parameter Perbandingan | Kategori 1: Building Insights (`findClosest`) | Kategori 2: Data Layers (`dataLayers:get`) |
| :--- | :--- | :--- |
| **Tujuan Utama** | Kalkulasi kuantitatif kapasitas atap, jumlah panel, dan potensi energi. | Akuisisi citra raster geospasial resolusi tinggi (0.25 m/pixel) untuk verifikasi visual. |
| **Format Return** | JSON berstruktur (Angka, String, Array Geometri). | JSON memuat daftar URL unduh berkas GeoTIFF raster (*Cloud Storage*). |
| **Input Identifikasi** | Koordinat titik lintang/bujur (`location.latitude`, `location.longitude`). | Koordinat titik lintang/bujur + radius batas cakupan (`radiusMeters <= 100m`). |
| **Biaya Panggilan GCP** | **$0.010** per panggilan berhasil. | **$0.075** per panggilan (mencakup seluruh layer GeoTIFF sekaligus). |
| **Penyimpanan Lokal** | Berkas JSON / CSV / Parquet (~2 KB per titik). | Berkas raster GeoTIFF & PNG preview (~5 s.d. 8 MB per titik). |
| **Peran di Dashboard POW** | Menghasilkan angka metrik Bento Card, kapasitas MWp, MWh AC, dan reduksi CO₂. | Menampilkan 7 layer citra: RGB, Panels Overlay, Segments 3D, DSM, Roof Mask, Flux Heatmap. |
| **Ketergantungan Alur** | **Tahap 1 (Sensus Tabular):** Dijalankan terlebih dahulu untuk menemukan ID gedung resmi. | **Tahap 2 (Verifikasi Citra):** Dipanggil di titik centroid gedung hasil tahap 1 agar presisi 100%. |

---
*Dokumen Master Governance CELIOS Solar Research 2026. Seluruh hak cipta arsitektur Google Solar API dimiliki oleh Google LLC.*
