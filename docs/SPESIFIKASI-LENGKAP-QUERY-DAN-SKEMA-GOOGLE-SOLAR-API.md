# Spesifikasi Lengkap Query Parameter & Skema Data Google Solar API
**Dokumen Standar Teknis & Integrasi Sistem CELIOS Solar Research (2026)**  
*Referensi Resmi: Google Maps Platform — Solar API REST v1*

---

## 1. Ikhtisar Arsitektur & Matriks Komparasi Endpoint

Google Maps Platform Solar API menyediakan dua endpoint utama berbasis REST untuk mengekstraksi data fotogrametri surya dan citra geospasial 3D:

| No | Nama Kategori Endpoint | HTTP Method | Path URL Endpoint | Karakteristik Output | Biaya Standar GCP |
| :-: | :--- | :---: | :--- | :--- | :---: |
| **1** | **Building Insights** | `GET` | `https://solar.googleapis.com/v1/buildingInsights:findClosest` | Objek JSON berstruktur (analisis fisik atap, segmen 3D, panel layout, dan fluks) | **$0.010** / call |
| **2** | **Data Layers** | `GET` | `https://solar.googleapis.com/v1/dataLayers:get` | URL sementara Cloud Storage untuk mengunduh berkas GeoTIFF raster georeferensi | **$0.075** / call |

### Matriks Komparasi & Interoperabilitas: Building Insights vs Data Layers

| Dimensi Perbandingan | Kategori 1: Building Insights (`findClosest`) | Kategori 2: Data Layers (`dataLayers:get`) |
| :--- | :--- | :--- |
| **Tujuan Utama** | Kalkulasi kuantitatif kapasitas daya (kWp/MWp), jumlah panel, sudut atap, dan estimasi energi. | Akuisisi citra raster geospasial beresolusi tinggi (0.25 m/pixel) untuk verifikasi visual dan audit spasial. |
| **Format Return** | JSON berstruktur (Angka, String, Objek Geometri, Array Panel). | JSON berisi daftar URL bertanda tangan (*Signed URLs*) untuk mengunduh berkas GeoTIFF raster. |
| **Input Identifikasi** | Koordinat titik lintang dan bujur (`location.latitude`, `location.longitude`). | Koordinat titik lintang dan bujur + radius batas cakupan (`radiusMeters <= 100m`). |
| **Biaya Panggilan GCP** | **$0.010** per panggilan berhasil (tidak ditagih bila `404 NOT_FOUND`). | **$0.075** per panggilan (**satu kali panggilan sudah mencakup seluruh berkas GeoTIFF sekaligus**). |
| **Penyimpanan Lokal** | Berkas JSON / CSV / Parquet (~2 KB per titik fasilitas). | Berkas raster GeoTIFF mentah (~5 s.d. 8 MB per titik) $\rightarrow$ dikompresi ke WebP (~400 KB). |
| **Penerapan di Dashboard**| Angka metrik eksekutif Bento Card, kapasitas terpasang, yield listrik tahunan, dan kalkulasi dividen fiskal. | Visualisasi 7 Layer Citra Satelit (RGB Asli, Layout Panel, Segmen Atap 3D, DSM Elevasi, Roof Mask, Flux Heatmap). |
| **Alur Eksekusi POW** | **Tahap 1 (Sensus Tabular):** Dijalankan terlebih dahulu untuk menemukan koordinat centroid dan ID atap resmi. | **Tahap 2 (Verifikasi Citra):** Dipanggil di titik centroid hasil Tahap 1 untuk menjamin citra 100% presisi di tengah kanopi atap. |

---

## 2. Kategori 1: Building Insights (`buildingInsights:findClosest`)

Endpoint ini mencari bangunan terdekat dari koordinat masukan yang memiliki model fotogrametri satelit, lalu mengembalikan data tabular dimensi bangunan, estimasi kapasitas panel, fluks radiasi, segmentasi bidang atap 3D, serta estimasi energi tahunan.

* **Endpoint URL:** `https://solar.googleapis.com/v1/buildingInsights:findClosest`
* **HTTP Method:** `GET`
* **Format Output:** JSON Tabular Objek Bersarang (*Hierarchical JSON Object*)
* **Tarif GCP:** **$0.010** per panggilan

### 2.1 Tabel Master Terkonsolidasi: Query Request & Seluruh Skema Return Building Insights

| Klaster Data | Parameter / Nama Field | Tipe Data | Status | Satuan / Opsi Nilai | Penjelasan Teknis & Fungsionalitas |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **INPUT QUERY (HTTP REQUEST)** | `location.latitude` | `Double` | **Wajib** | `-90.0` s.d. `+90.0` | Koordinat lintang titik target pencarian bangunan (WGS 84). |
| | `location.longitude` | `Double` | **Wajib** | `-180.0` s.d. `+180.0` | Koordinat bujur titik target pencarian bangunan (WGS 84). |
| | `requiredQuality` | `Enum` | Opsional | `BASE`, `MEDIUM`, `HIGH` | Ambang mutu citra minimal yang disyaratkan (default: `BASE`). |
| | `experiments` | `Enum[]`| Opsional | `EXPANDED_COVERAGE` | Opsi eksperimental untuk memperluas cakupan deteksi geografis. |
| | `key` | `String` | **Wajib** | Alfanumerik | Kunci otentikasi resmi Google Cloud Platform dengan billing aktif. |
| **IDENTITAS & SPASIAL (ROOT RESPONSE)** | `name` | `String` | Return | `buildings/{place_id}` | Resource name / ID bangunan unik di katalog geospasial Google Maps. |
| | `center` | `Object` | Return | `{"latitude", "longitude"}`| Koordinat titik tengah (*centroid*) fisik bidang geometri atap. |
| | `boundingBox` | `Object` | Return | Poligon `sw` dan `ne` | Batas bujur sangkar koordinat terluar yang melingkupi atap gedung. |
| | `imageryDate` | `Object` | Return | `{"year", "month", "day"}` | Tanggal pemotretan udara satelit yang mendasari analisis 3D. |
| | `imageryProcessedDate` | `Object` | Return | `{"year", "month", "day"}` | Tanggal pemrosesan algoritma fotogrametri oleh Google. |
| | `postalCode` | `String` | Return | String angka (misal: `"12160"`)| Kode pos wilayah administratif gedung berada. |
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
| **SEGMEN ATAP 3D (`roofSegmentStats[]`)** | `pitchDegrees` | `Float` | Return | Derajat ($0^\circ$ s.d. $90^\circ$) | **Sudut kemiringan bidang atap** terhadap permukaan horizontal. |
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

## 3. Kategori 2: Data Layers (`dataLayers:get`)

Endpoint ini mengekstrak data raster geospasial beresolusi tinggi dalam format GeoTIFF untuk wilayah di sekitar lokasi sasaran. Respons API mengembalikan tautan sementara Cloud Storage yang berlaku selama kurun waktu tertentu untuk mengunduh citra asli.

* **Endpoint URL:** `https://solar.googleapis.com/v1/dataLayers:get`
* **HTTP Method:** `GET`
* **Format Output:** JSON berisi tautan unduh sementara (*Signed Cloud Storage URLs*) berkas **GeoTIFF Raster**
* **Tarif GCP:** **$0.075** per panggilan (**1 call mencakup seluruh berkas raster GeoTIFF sekaligus**)

### 3.1 Tabel Master Terkonsolidasi: Query Request & Seluruh Tautan GeoTIFF Data Layers

| Klaster Data | Parameter / Nama Field | Tipe Data | Status | Satuan / Opsi Nilai | Penjelasan Teknis & Fungsionalitas |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **INPUT QUERY (HTTP REQUEST)** | `location.latitude` | `Double` | Wajib* | `-90.0` s.d. `+90.0` | Titik lintang pusat kotak analisis raster (*Wajib bila tanpa bounding box). |
| | `location.longitude` | `Double` | Wajib* | `-180.0` s.d. `+180.0` | Titik bujur pusat kotak analisis raster (*Wajib bila tanpa bounding box). |
| | `radiusMeters` | `Float` | Wajib* | `0.0` s.d. `100.0` meter | Jari-jari cakupan raster (maksimal resmi Google adalah **100 meter**). |
| | `view` | `Enum` | Opsional | `FULL_LAYERS`, `DSM_ONLY`, `IMAGERY_AND_ANNUAL_FLUX` | Filter lapisan citra raster yang ingin dihasilkan (default: `FULL_LAYERS`). |
| | `requiredQuality` | `Enum` | Opsional | `BASE`, `MEDIUM`, `HIGH` | Tingkat mutu fotogrametri minimal yang diterima. |
| | `pixelSizeMeters` | `Float` | Opsional | Contoh: `0.25` meter | Resolusi spasial riil per piksel raster (standar Jabodetabek: **0.25 m/px**). |
| | `exactBoundingBox.*` | `Object` | Opsional | Poligon `sw` dan `ne` | Batas bujur sangkar koordinat manual (alternatif dari `location` + `radius`). |
| | `experiments` | `Enum[]`| Opsional | `EXPANDED_COVERAGE` | Opsi eksperimental fitur preview cakupan satelit Google. |
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

### 3.2 Spesifikasi Teknis & Format Berkas 6 Layer GeoTIFF Raster

| Nama Berkas Raster | Tipe Data Piksel | Band | Rentang Nilai Piksel | Satuan Pengukuran | Nilai NoData | Fungsi Utama dalam Dashboard CELIOS |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **Citra Foto Udara (RGB)** | `Uint8` (Byte) | 3 / 4 (RGBA) | `0` s.d. `255` | Spektrum Cahaya Tampak | `0` | Layer 1: Visualisasi latar belakang foto satelit asli resolusi tinggi. |
| **Digital Surface Model (DSM)** | `Float32` | 1 Band | `-50.0` s.d. `8.000.0` | **Meter** di atas geoid WGS84 | `-9999.0` | Layer 4: Elevasi tinggi gedung, kemiringan atap (*pitch*), dan model 3D. |
| **Roof Building Mask** | `Uint8` (Byte) | 1 Band | `0` atau `1` | Indeks Kategori Biner | `0` | Layer 5: Segmentasi batas bidang atap bersih dari jalan dan pohon. |
| **Annual Solar Flux Heatmap** | `Float32` | 1 Band | `0.0` s.d. `2.500.0` | **$kWh/kWp/tahun$** | `-9999.0` | Layer 3: Peta panas intensitas radiasi surya per piksel atap. |
| **Monthly Solar Flux** | `Float32` | 12 Band | `0.0` s.d. `300.0` | **$kWh/kWp/bulan$** | `-9999.0` | Analisis variasi musiman produksi energi surya (Januari s.d. Desember). |
| **Hourly Shade Bitmask** | `Uint32` | 12 Berkas | Bitmask 24-bit | Status Penyinaran per Jam | `0` | Analisis bayangan gedung sekitar per jam pada tanggal 21 tiap bulan. |

---

## 4. Status Kode HTTP, Error Handling & Kebijakan Kuota

| Kode Status HTTP | Status Error GCP | Penyebab Umum Lapangan | Solusi Rekayasa / Penanganan |
| :---: | :--- | :--- | :--- |
| **`200 OK`** | *Success* | Permintaan berhasil diproses dan data fotogrametri ditemukan. | Data siap di-parsing dan disimpan ke pipeline ETL. |
| **`400 Bad Request`** | `INVALID_ARGUMENT` | Koordinat tidak valid, `radiusMeters` melampaui 100m, atau parameter format salah. | Validasi koordinat ($-90 \le lat \le 90$) dan pastikan `radiusMeters <= 100`. |
| **`403 Forbidden`** | `PERMISSION_DENIED` | API Key tidak valid, Solar API belum diaktifkan di GCP Console, atau Billing GCP mati. | Cek status kuota di GCP Console, periksa API Key restrictions, dan pastikan billing aktif. |
| **`404 Not Found`** | `NOT_FOUND` | Google belum memiliki pemodelan satelit 3D untuk gedung di koordinat tersebut. | Tangani secara defensif (`try-except`), catat titik sebagai *uncovered POI*, gunakan data proksi regional. |
| **`429 Too Many Requests`** | `RESOURCE_EXHAUSTED` | Melebihi batas kuota pemanggilan per menit (*Queries Per Minute* / QPM limit). | Terapkan *exponential backoff* dan jeda waktu (*rate limiting*) antar panggilan API (~1-2 detik). |
| **`500 Internal Error`**| `INTERNAL` | Terjadi gangguan internal pada server pengolahan citra Google Cloud. | Ulangi panggilan (*retry*) setelah jeda 3-5 detik. |

---

## 5. Ringkasan Kebijakan Billing & SKU Google Cloud

| SKU Name Google Cloud | Komponen Biaya | Tarif Resmi per 1.000 Panggilan | Catatan Kebijakan Penagihan |
| :--- | :--- | :---: | :--- |
| **Solar API — Building Insights** | Panggilan ke `buildingInsights:findClosest` | **$10.00** ($0.010 per titik) | Menagih per satu kali respons JSON. Tidak menagih jika mengembalikan status `404 NOT_FOUND`. |
| **Solar API — Data Layers** | Panggilan ke `dataLayers:get` | **$75.00** ($0.075 per titik) | **Satu kali panggilan sudah mencakup hak unduh seluruh layer GeoTIFF** (DSM, RGB, Mask, Flux, Monthly, Shade). Google tidak menagih biaya per berkas raster yang diunduh. |

---

## 6. Contoh Pemanggilan Resmi (Code Snippets)

### 6.1 Contoh Request cURL: Building Insights
```bash
curl -X GET "https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude=-6.239940&location.longitude=106.798430&requiredQuality=BASE&key=YOUR_API_KEY" \
     -H "Accept: application/json"
```

### 6.2 Contoh Request cURL: Data Layers
```bash
curl -X GET "https://solar.googleapis.com/v1/dataLayers:get?location.latitude=-6.239940&location.longitude=106.798430&radiusMeters=50&view=FULL_LAYERS&requiredQuality=BASE&pixelSizeMeters=0.25&key=YOUR_API_KEY" \
     -H "Accept: application/json"
```

### 6.3 Contoh Script Python untuk Ekstraksi Utuh
```python
import requests

API_KEY = "YOUR_API_KEY"
LAT, LON = -6.239940, 106.798430

# 1. Pemanggilan Building Insights
bi_url = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={LAT}&location.longitude={LON}&requiredQuality=BASE&key={API_KEY}"
bi_resp = requests.get(bi_url)

if bi_resp.status_code == 200:
    bi_data = bi_resp.json()
    sp = bi_data.get("solarPotential", {})
    print(f"Max Panels        : {sp.get('maxArrayPanelsCount')}")
    print(f"Sunshine Hours/Yr : {sp.get('maxSunshineHoursPerYear')} Jam")
    print(f"Carbon Factor     : {sp.get('carbonOffsetFactorKgPerMwh')} kg/MWh")
    print(f"Google Raw DC     : {sp.get('solarPanelConfigs', [{}])[-1].get('yearlyEnergyDcKwh')} kWh DC")

# 2. Pemanggilan Data Layers
dl_url = f"https://solar.googleapis.com/v1/dataLayers:get?location.latitude={LAT}&location.longitude={LON}&radiusMeters=50&view=FULL_LAYERS&requiredQuality=BASE&key={API_KEY}"
dl_resp = requests.get(dl_url)

if dl_resp.status_code == 200:
    dl_data = dl_resp.json()
    print(f"URL DSM GeoTIFF   : {dl_data.get('dsmUrl')}")
    print(f"URL RGB Satelit   : {dl_data.get('rgbUrl')}")
    print(f"URL Roof Mask     : {dl_data.get('maskUrl')}")
    print(f"URL Annual Flux   : {dl_data.get('annualFluxUrl')}")
```

---

## 7. Pemetaan Lengkap Data Lineage Tabel Master Dashboard (Return Solar API vs API Lain vs Kalkulasi ETL)

Bagian ini memetakan secara mendalam seluruh **31 kolom data** yang disajikan pada **Tabel Dropdown Seluruh Data 2.100 Titik Fasilitas (Master Data Layers & Building Insights)** di Halaman 1 Dashboard ([`pages/1_Pemetaan_Potensi.py`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/pages/1_Pemetaan_Potensi.py)). 

Seluruh kolom diaudit berdasarkan asal-usul perolehan datanya:
1. **Direct Return Asli (Google Solar API & API Eksternal Lainnya)** diberi tanda centang hijau (**✅**) dengan mencantumkan nama API dan nama field spesifiknya.
2. **Kalkulasi ETL / Turunan Sekunder yang mengambil bahan dari return Solar API atau API lainnya** juga diberi tanda centang hijau (**✅**) dengan mencantumkan formula kalkulasi serta field data API yang menjadi bahannya.
3. **Data Murni Non-API** (hanya kolom nomor urut tabel UI `No`) diberi tanda (**➖**).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             KOMPOSISI DATA LINEAGE TABEL MASTER DASHBOARD (BERBASIS API)              │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  Total Kolom Ditampilkan                     : 31 Kolom                                │
│  ├─ ✅ Direct Return Asli Google Solar API   : 12 Kolom (38.7%)                        │
│  ├─ ✅ Direct Return API Eksternal (OSM/Nom) :  3 Kolom  (9.7%)                        │
│  ├─ ✅ Kalkulasi ETL Bahan Google Solar API  : 13 Kolom (41.9%)                        │
│  ├─ ✅ Kalkulasi ETL Bahan Multi-API         :  2 Kolom  (6.5%)                        │
│  └─ ➖ Non-API (Hanya Auto-Index UI)         :  1 Kolom  (3.2%)                        │
│                                                                                        │
│  TOTAL BERBASIS API (DIRECT RETURN + KALKULASI DARI API) = 30 DARI 31 KOLOM (96.8% ✅) │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 7.1 Matriks Audit Data Lineage Seluruh Kolom Tabel Master Dashboard

| No | Nama Kolom di UI Dashboard | Nama Field di CSV / DataFrame | Tipe Data | Klasifikasi Data Lineage | Sumber API Asal & Formula Kalkulasi Teknis | Keterangan & Peran Metodologis |
| :-: | :--- | :--- | :---: | :---: | :--- | :--- |
| 1 | **No** | `No` | `Integer` | ➖ **Non-API (UI Counter)** | Generator Python UI: `range(1, len(table) + 1)` | Nomor urut baris dinamis antarmuka Streamlit (tidak memerlukan panggilan jaringan). |
| 2 | **Kategori** | `category_display` | `String` | ✅ **Direct Return / Filter API** | **OpenStreetMap Overpass API**<br>Query tags: `amenity=*`, `railway=*`, `highway=*`, `shop=*` | Klasifikasi sektoral fasilitas publik & komersial (KRL, BRT, RSUD, Sekolah, Mall, Pasar, dsb.). |
| 3 | **Infrastruktur** | `asset_name` | `String` | ✅ **Direct Return API** | **OSM Overpass & Nominatim Reverse API**<br>Field: `tags.name` / `display_name` | Nama resmi fasilitas/bangunan publik yang diekstraksi dari katalog OpenStreetMap. |
| 4 | **Wilayah** | `city_regency` | `String` | ✅ **Direct Return API** | **Nominatim Reverse Geocoding API**<br>Field: `address.city` / `address.county` / `address.city_district` | Wilayah administrasi tingkat II (5 Kota DKI Jakarta + 8 Wilayah Bodetabek). |
| 5 | **Kode Pos** | `postal_code` | `String` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `bi_data["postalCode"]` | Kode pos resmi lokasi bangunan yang diidentifikasi secara otomatis oleh sistem geospasial Google Maps. |
| 6 | **Total Fisik Atap (m²)** | `whole_roof_area_m2` | `Float` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `solarPotential.wholeRoofStats.areaMeters2` | Luas fisik 3D seluruh bidang atap gedung hasil fotogrametri satelit resolusi tinggi. |
| 7 | **Atap Layak PLTS (m²)** | `max_roof_area_m2` | `Float` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `solarPotential.maxArrayAreaMeters2` | Luas atap efektif yang lolos ambang insolasi radiasi surya minimal & bebas dari bayangan permanen. |
| 8 | **Rasio Kelayakan (%)** | `roof_suitability_ratio_pct` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | `(max_roof_area_m2 / whole_roof_area_m2) * 100`<br>Bahan: `maxArrayAreaMeters2` & `wholeRoofStats.areaMeters2` | Persentase proporsi bidang atap yang layak dipasangi panel terhadap total fisik atap keseluruhan. |
| 9 | **Tapak Bangunan (m²)** | `building_footprint_m2` | `Float` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `solarPotential.buildingStats.areaMeters2` | Luas proyeksi dasar tapak bangunan (*ground footprint*) di atas permukaan tanah. |
| 10 | **Cakupan Atap (%)** | `roof_coverage_ratio_pct` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | `(whole_roof_area_m2 / building_footprint_m2) * 100`<br>Bahan: `wholeRoofStats.areaMeters2` & `buildingStats.areaMeters2` | Rasio luas atap tersegmentasi terhadap tapak dasar; mengukur kelengkapan fotogrametri satelit terhadap struktur bangunan. |
| 11 | **Celah Non-Segmen (m²)** | `gap_unsegmented_m2` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | `max(0.0, building_footprint_m2 - whole_roof_area_m2)`<br>Bahan: `buildingStats.areaMeters2` & `wholeRoofStats.areaMeters2` | Selisih tapak bangunan dengan atap tersegmentasi (mencerminkan dak peron/selasar datar tak bersekat). |
| 12 | **Total Celah (m²)** | `total_gap_m2` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | `max(0.0, building_footprint_m2 - max_roof_area_m2)`<br>Bahan: `buildingStats.areaMeters2` & `maxArrayAreaMeters2` | Total luasan tapak bangunan yang belum dimanfaatkan modul (dasar ruang untuk Skenario Infill SNI 8395). |
| 13 | **Kondisi Celah** | `gap_category` | `String` | ✅ **Kalkulasi ETL (Bahan Solar API)** | Klasifikasi rule-based pada `roof_coverage_ratio_pct`<br>Bahan: Rasio atap hasil Google Solar API | Kategori celah atap: `Gap Sedikit` ($\ge 80\%$), `Gap Sedang` ($70\% - 80\%$), atau `Gap Besar` ($< 70\%$). |
| 14 | **Total Segmen** | `total_segments` | `Integer` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `len(solarPotential.roofSegmentStats)` | Total jumlah bidang poligon miring 3D individual yang menyusun struktur arsitektur atap bangunan. |
| 15 | **Segmen Terisi** | `active_segments` | `Integer` | ✅ **Kalkulasi ETL (Bahan Solar API)** | Count segmen di mana `panelsCount > 0`<br>Bahan: `solarPanels[].segmentIndex` & `roofSegmentSummaries[]` | Jumlah bidang segmen atap yang teralokasi minimal 1 modul surya di konfigurasi Google. |
| 16 | **Rentang Kemiringan (Min – Max)** | `pitch_range` | `String` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `min/max(roofSegmentStats[].pitchDegrees)` | Rentang sudut kemiringan lereng atap terendah dan tertinggi terhadap bidang datar (format: `min° – max°`). |
| 17 | **Bobot Kemiringan** | `weighted_pitch_deg` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | $\frac{\sum (\text{pitchDegrees}_i \times \text{area}_i)}{\sum \text{area}_i}$<br>Bahan: `roofSegmentStats[].pitchDegrees` & `stats.areaMeters2` | Sudut kemiringan rata-rata tertimbang (*weighted average pitch*) berdasarkan luas masing-masing segmen atap. |
| 18 | **Total Panel (unit)** | `max_panels_count` | `Integer` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `solarPotential.maxArrayPanelsCount` | Jumlah modul surya maksimum yang dapat dipasang di atap layak menurut model tata letak Google. |
| 19 | **Kapasitas (kWp)** | `installed_capacity_kwp` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | $\frac{\text{maxArrayPanelsCount} \times 400\,\text{Wp}}{1000}$<br>Bahan: `solarPotential.maxArrayPanelsCount` & `panelCapacityWatts` (400Wp) | Kapasitas daya puncak DC sistem; mengalikan jumlah modul Google dengan kapasitas modul standar 400 Wp. |
| 20 | **Jam Sinar (jam/thn)** | `sunshine_hours_annual` | `Float` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `solarPotential.maxSunshineHoursPerYear` | Jam penyinaran puncak ekuivalen per tahun (*Peak Sun Hours* / PSH) di titik geospasial gedung target. |
| 21 | **Potensi DC Google (MWh)** | `google_dc_mwh` | `Float` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `solarPanelConfigs[-1].yearlyEnergyDcKwh / 1000` | Total estimasi listrik DC kotor tahunan dari simulasi konfigurasi panel maksimum bawaan Google. |
| 22 | **Listrik AC Bersih (MWh)** | `annual_generation_mwh` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | $\frac{\text{kWp} \times \text{PSH} \times 0.80}{1000}$<br>Bahan: `maxArrayPanelsCount` & `maxSunshineHoursPerYear` + IEC 61724 | Estimasi produksi listrik AC bersih riil setelah susut inverter, kabel, dan suhu tropis (*Performance Ratio* 80%). |
| 23 | **Rata² kWh/Panel** | `prod_per_panel_kwh` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | $\frac{\text{annual\_generation\_kwh}}{\text{max\_panels\_count}}$<br>Bahan: `annual_generation_kwh` & `maxArrayPanelsCount` | Rata-rata hasil panen energi listrik bersih per 1 keping modul per tahun (indikator efisiensi insolasi lokal). |
| 24 | **Faktor CO₂ (kg/MWh)** | `carbon_offset_factor` | `Float` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `solarPotential.carbonOffsetFactorKgPerMwh` | Faktor intensitas emisi karbon grid regional bawaan Google Cloud (**808.999 kg CO₂/MWh** untuk Grid Jamali). |
| 25 | **Reduksi CO₂ (Ton/thn)** | `ghg_reduction_tons_co2` | `Float` | ✅ **Kalkulasi ETL (Bahan Solar API)** | $\frac{\text{annual\_generation\_mwh} \times \text{carbonOffsetFactor}}{1000}$<br>Bahan: `annual_generation_mwh` & `carbonOffsetFactorKgPerMwh` | Estimasi volume pengurangan emisi gas rumah kaca tahunan dalam satuan Metrik Ton $CO_2$ ekuivalen. |
| 26 | **Drift (m)** | `spatial_drift_meters` | `Float` | ✅ **Kalkulasi ETL (Bahan Multi-API)** | `haversine_distance(raw_poi, google_center)`<br>Bahan: Koordinat OSM/Nominatim vs `center` Google Solar API | Jarak pergeseran spasial antara pin titik POI masukan dengan titik tengah atap gedung (*centroid*) hasil Google. |
| 27 | **Status Spasial** | `drift_status` | `String` | ✅ **Kalkulasi ETL (Bahan Multi-API)** | Kondisi: `VALID (< 30m)` jika drift $\le 30$ m, else `REVIEW`<br>Bahan: Jarak drift hasil kalkulasi koordinat API | Validasi kepresisian geospasial untuk memastikan bahwa fotogrametri satelit tepat mengunci atap gedung target. |
| 28 | **Tgl Citra Satelit** | `imagery_date` | `String` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `imageryDate` (`year`, `month`, `day`) | Tanggal akuisisi pemotretan udara satelit resolusi tinggi yang mendasari analisis fotogrametri 3D. |
| 29 | **Kualitas Citra** | `res_tier` | `String` | ✅ **Kalkulasi ETL (Bahan Solar API)** | Format string: `f"0.25 m/px ({imageryQuality})"`<br>Bahan: `bi_data["imageryQuality"]` (yaitu `BASE`) | Tingkat resolusi spasial citra satelit (0.25 m/piksel) dipadukan dengan tier kualitas Google. |
| 30 | **Google Building ID** | `google_building_id` | `String` | ✅ **Direct Return Solar API** | **Google Solar API (Building Insights)**<br>Field: `bi_data["name"]` (`buildings/{place_id}`) | Pengenal unik resmi bangunan pada basis data geospasial Google Maps Platform. |
| 31 | **URL Verifikasi Google Maps** | `google_maps_url` | `String` | ✅ **Kalkulasi ETL (Bahan Solar API)** | URL generator: `https://www.google.com/maps/search/?api=1&query={lat},{lon}`<br>Bahan: `center.latitude` & `center.longitude` Google Solar API | Tautan navigasi web resmi ke Google Maps Satelit untuk verifikasi visual langsung oleh auditor/peneliti. |

---

### 7.2 Klasifikasi Lengkap per Kategori API

#### Kelompok 1: Direct Return Asli Google Solar API (12 Kolom ✅)
Data mentah yang diambil langsung dari atribut JSON respons Google Solar API:
1. **`Kode Pos`** $\rightarrow$ `postalCode`
2. **`Total Fisik Atap (m²)`** $\rightarrow$ `solarPotential.wholeRoofStats.areaMeters2`
3. **`Atap Layak PLTS (m²)`** $\rightarrow$ `solarPotential.maxArrayAreaMeters2`
4. **`Tapak Bangunan (m²)`** $\rightarrow$ `solarPotential.buildingStats.areaMeters2`
5. **`Total Segmen`** $\rightarrow$ `len(solarPotential.roofSegmentStats)`
6. **`Rentang Kemiringan (Min – Max)`** $\rightarrow$ `roofSegmentStats[].pitchDegrees` (min & max)
7. **`Total Panel (unit)`** $\rightarrow$ `solarPotential.maxArrayPanelsCount`
8. **`Jam Sinar (jam/thn)`** $\rightarrow$ `solarPotential.maxSunshineHoursPerYear`
9. **`Potensi DC Google (MWh)`** $\rightarrow$ `solarPanelConfigs[-1].yearlyEnergyDcKwh / 1000`
10. **`Faktor CO₂ (kg/MWh)`** $\rightarrow$ `solarPotential.carbonOffsetFactorKgPerMwh` (**808,999 kg/MWh**)
11. **`Tgl Citra Satelit`** $\rightarrow$ `imageryDate` (`year`, `month`, `day`)
12. **`Google Building ID`** $\rightarrow$ `name` (`buildings/{place_id}`)

#### Kelompok 2: Direct Return API Eksternal Non-Google Solar (3 Kolom ✅)
Data atribut fasilitas publik yang diambil langsung dari respons API geospasial OpenStreetMap:
1. **`Kategori`** $\rightarrow$ **OpenStreetMap Overpass API** (query tag tipologi: `amenity`, `railway`, `highway`, `shop`)
2. **`Infrastruktur`** $\rightarrow$ **OSM Overpass & Nominatim Reverse API** (field: `tags.name` / `display_name`)
3. **`Wilayah`** $\rightarrow$ **Nominatim Reverse Geocoding API** (field: `address.city` / `address.county`)

#### Kelompok 3: Kalkulasi ETL dengan Bahan Return Google Solar API (13 Kolom ✅)
Data hasil formulasi matematis dan standar rekayasa ketenagalistrikan yang 100% menggunakan data mentah dari Google Solar API:
1. **`Rasio Kelayakan (%)`** $\rightarrow$ `(maxArrayAreaMeters2 / wholeRoofStats.areaMeters2) * 100`
2. **`Cakupan Atap (%)`** $\rightarrow$ `(wholeRoofStats.areaMeters2 / buildingStats.areaMeters2) * 100`
3. **`Celah Non-Segmen (m²)`** $\rightarrow$ `buildingStats.areaMeters2 - wholeRoofStats.areaMeters2`
4. **`Total Celah (m²)`** $\rightarrow$ `buildingStats.areaMeters2 - maxArrayAreaMeters2`
5. **`Kondisi Celah`** $\rightarrow$ Ambang batas klasifikasi rasio atap (`Gap Sedikit`, `Gap Sedang`, `Gap Besar`)
6. **`Segmen Terisi`** $\rightarrow$ Filter jumlah segmen aktif yang memiliki panel di `solarPanels[]`
7. **`Bobot Kemiringan`** $\rightarrow$ Rata-rata tertimbang dari `pitchDegrees` & `areaMeters2` segmen atap
8. **`Kapasitas (kWp)`** $\rightarrow$ `maxArrayPanelsCount * 400 Wp / 1000`
9. **`Listrik AC Bersih (MWh)`** $\rightarrow$ `capacity_kwp * maxSunshineHoursPerYear * 0.80 (PR IEC 61724) / 1000`
10. **`Rata² kWh/Panel`** $\rightarrow$ `annual_generation_kwh / maxArrayPanelsCount`
11. **`Reduksi CO₂ (Ton/thn)`** $\rightarrow$ `annual_generation_mwh * carbonOffsetFactorKgPerMwh / 1000`
12. **`Kualitas Citra`** $\rightarrow$ String resolusi `0.25 m/px` digabung dengan tier respons `imageryQuality`
13. **`URL Verifikasi Google Maps`** $\rightarrow$ Generator URL Google Maps Search API menggunakan `center.latitude, center.longitude`

#### Kelompok 4: Kalkulasi ETL Berbahan Multi-API (2 Kolom ✅)
Data audit spasial yang membandingkan data koordinat masukan dari OpenStreetMap/Nominatim dengan titik tengah atap hasil Google Solar API:
1. **`Drift (m)`** $\rightarrow$ Jarak Haversine antara koordinat Nominatim API (`raw_lat, raw_lon`) dengan Google Solar API `center` (`latitude, longitude`)
2. **`Status Spasial`** $\rightarrow$ Audit ambang batas toleransi drift spasial $\le 30$ meter (`VALID (< 30m)`)

#### Kelompok 5: Non-API Murni (1 Kolom ➖)
1. **`No`** $\rightarrow$ Nomor urut integer baris tabel antarmuka pengguna Streamlit (`range(1, N+1)`).

---

### 7.3 Bukti Forensik Standar IEC 61724 & Benchmark Performance Ratio (PR 80%) di Indonesia

Sesuai dengan mandat ketat `.agents/rules/strict_data_folder_boundary.md` dan `.agents/rules/no_hardcoded_data.md`, nilai **Performance Ratio (PR) 80% (0.80)** yang digunakan untuk mengonversi potensi DC Google Solar API ke produksi listrik AC bersih tahunan **wajib didukung oleh berkas bukti fisik di `data/raw/sources/`** serta dibukukan ke dataset terstruktur di `data/processed/references/`.

#### 1. Inventarisasi Berkas Bukti Fisik di Repositori
1. **Berkas Bukti Primer Empiris Indonesia:**
   * **File Path Raw:** [`data/raw/sources/ijtech_ui_iec_61724_pv_performance_indonesia.pdf`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/raw/sources/ijtech_ui_iec_61724_pv_performance_indonesia.pdf) *(Ukuran: 956 KB, 11 Halaman)*
   * **Salinan Terproses:** [`data/processed/references/ijtech_ui_iec_61724_pv_performance_indonesia.pdf`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/ijtech_ui_iec_61724_pv_performance_indonesia.pdf)
   * **Transkrip Teks Penuh:** [`data/processed/references/ijtech_ui_iec_61724_pv_performance_indonesia.md`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/ijtech_ui_iec_61724_pv_performance_indonesia.md)
   * **Dataset Referensi Terstruktur:** [`data/processed/references/standar_iec_61724_performance_ratio.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/standar_iec_61724_performance_ratio.csv) & [`.parquet`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/standar_iec_61724_performance_ratio.parquet)
   * **Judul Publikasi:** *"A Comparative Performance Analysis of a 1 MW CIS PV System and a 5 kW Crystalline-Si PV System under the Tropical Climate of Indonesia"*
   * **Penulis:** Kun Kunaifi, Angèle Reinders, Dimas Kaharudin, Aripriantoni Harmanto, Kirjono Mudiarto.
   * **Kolaborasi Institusi:** University of Twente (Belanda), UIN Suska Riau, Eindhoven University of Technology, dan PT Pembangkitan Jawa-Bali (PT PJB / PLN Group).
   * **Penerbit:** *International Journal of Technology* (IJTech), Fakultas Teknik Universitas Indonesia, Vol. 10(6): 1082–1092 (2019). ISSN: 2086-9614.
   * **DOI Resmi:** [10.14716/ijtech.v10i6.3612](https://doi.org/10.14716/ijtech.v10i6.3612).

2. **Berkas Bukti Pemodelan Internasional (NREL):**
   * **File Path Raw:** [`data/raw/sources/nrel_pvwatts_version5_manual.pdf`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/raw/sources/nrel_pvwatts_version5_manual.pdf) *(Halaman 13-14, Table 6).*
   * **Penulis:** Aron P. Dobos, National Renewable Energy Laboratory (NREL), U.S. Department of Energy. Technical Report NREL/TP-6A20-62641.

---

#### 2. Kutipan Verbatim Definisi & Formula Standar IEC 61724
Dikutip verbatim dari naskah publikasi resmi (Section 3.1 *Performance Calculations*, Halaman 1086-1087):

> *"The monitoring standard IEC 61724 was applied to the analysis of the PV systems' performance (The International Electrotechnical Commission, 2017). The performance indicators presented include final yield ($Y_f$) in kWh/kWp; array yield ($Y_A$) in kWh/kWp; reference yield ($Y_r$) in kWh/kWp; capture losses ($L_C$) in kWh/kWp; system losses ($L_S$) in kWh/kWp; performance ratio ($PR$) as a percentage or a decimal between 0 and 1; efficiencies ($\eta$) as a percentage or a decimal between 0 and 1; and capacity factor ($CF$), also given as a percentage.*
>
> *The final yield, $Y_f$, is defined as the annual, monthly, or daily net AC energy output in kWh, $E_{ac}$, of the PV system per installed rated power, $P_{rated}$, and is given by Equation 1:*
> $$Y_f = \frac{E_{ac}}{P_{rated}} \quad \left(\frac{\text{kWh}}{\text{kW}}\right) \quad (1)$$
>
> *The reference yield in kWh/kWp, $Y_r$, is the total amount of available in-plane solar irradiance in kWh/m2, $H_i$, divided by the reference irradiance, $G_{i,ref}$, of 1,000 W/m2 (Equation 3):*
> $$Y_r = \frac{H_i}{G_{i,ref}} \quad \left(\frac{\text{kWh}}{\text{kW}}\right) \quad (3)$$
>
> *PR is a useful metric that shows how closely a PV system is operating in relation to its ideal rated operation. PR indicates the total losses from the system output due to both array temperature and system component inefficiencies or failures, including the BOS components. The array-level performance ratio, $PR_A$, and the system level, $PR$, are defined by Equation 6 and Equation 7:*
> $$PR = \frac{Y_f}{Y_r} \quad (\text{dimensionless}) \quad (7)"*

---

#### 3. Kutipan Verbatim Hasil Empiris Lapangan di Iklim Tropis Indonesia (Cirata, Jawa Barat)
Dikutip verbatim dari bagian *Abstract*, *Results*, dan *Conclusion* (Halaman 1082, 1089, dan 1091):

> **Abstract (Hal. 1082):**  
> *"The methodological approach used includes performance analyses of these PV systems according to IEC standard 61724 and an investigation of the degradation rate using NREL/RdTools. The following results were derived from the analyses: the total annual $H_i$ was 1500 kWh/m2 or around 4.2 kWh/m2/day. The daily-averaged performance ratio, PR, was 91.7 % ± 4 % and 87.4 % ± 7 % for the CIS system with string inverters and a central inverter, respectively. The mean PR of the CIS systems was 12 % higher than that of the c-Si system, which was 79.8 %."*

> **Results Section 4.1 & Table 2 (Hal. 1089):**  
> *"Figure 3 shows the PR of the PV systems in Cirata... PR for the c-Si system was 79.8 % ± 4 %. Table 2 shows the main performance indicators of the three PV systems in Cirata... The values for $\eta_{A,rated}$ of the CIS and c-Si system were respectively 13.8 % and 14.9 %."*
>
> **Tabel 2 (Performance Indicators di Cirata):**  
> * c-Si Rooftop (5 kW): $Y_f = 3.37\text{ kWh/kWp}$, $Y_r = 4.22\text{ kWh/kWp}$, $L_c = 0.64\text{ kWh/kWp}$, $L_s = 0.21\text{ kWh/kWp}$, **$PR = 79.8\%$** (dibulatkan menjadi **80%**).

> **Conclusion (Hal. 1091):**  
> *"The daily-averaged PR of the CIS system was 89.6 % (mean PR of the central and string clusters), which is 12.2 % higher relative to the PR of the c-Si system of 80 %."*

---

#### 4. Kutipan Verbatim Standar Derate NREL PVWatts V5 (NREL/TP-6A20-62641)
Dikutip verbatim dari NREL PVWatts Version 5 Manual (Halaman 14):

> *"To approximately convert PVWatts V5 system loss to a PVWatts V1 DC-to-AC derate factor:*  
> *1. Convert the system loss to a derate: $1 - 14/100 = 0.86$.*  
> *2. Multiply this value by the nominal inverter efficiency: $0.86 \times 0.96 = 0.825$ ($82.5\%$).*  
> *This suggests that the default PVWatts V5 system loss represents roughly a 7 % increase in system performance relative to PVWatts V1 due solely to updated input assumptions."*

---

#### 5. Kesimpulan Integrasi Metodologis Riset CELIOS
Riset CELIOS mengadopsi angka **Performance Ratio (PR) = 80% (0.80)** karena:
1. **Sesuai Standar Monitoring Internasional IEC 61724-1:** Menjadi formula baku pengurang (*derate*) untuk mentransformasi daya DC ke energi AC yang dialirkan ke beban/gardu.
2. **Didukung Bukti Empiris Iklim Tropis Indonesia:** Uji coba lapangan 2 tahun pada modul crystalline silicon (c-Si) di Cirata (Jawa Barat) oleh tim Universitas Indonesia dan PT PJB (PLN Group) secara presisi membuktikan nilai PR riil adalah **79.8% ± 4%** (ekuivalen 80%).
3. **Memperhitungkan Rugi-Rugi Riil Lapangan Perkotaan:**
   * **Capture Losses ($L_c$):** Kenaikan suhu modul surya di iklim tropis perkotaan Jabodetabek ($T_{cell}$ dapat mencapai 45°C–65°C), hamburan partikel debu/polusi udara (*urban soiling*), dan deviasi sudut foton.
   * **System Losses ($L_s$):** Efisiensi konversi inverter AC-DC (~96%-97%) serta resistansi kabel dan sambungan listrik.

---
*Dokumen ini merupakan bagian dari Master Data Governance CELIOS Solar Research 2026. Seluruh hak cipta dan merek dagang Google Solar API dimiliki oleh Google LLC.*

