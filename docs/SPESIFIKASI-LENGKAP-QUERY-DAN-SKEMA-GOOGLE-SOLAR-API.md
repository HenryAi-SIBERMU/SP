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
*Dokumen ini merupakan bagian dari Master Data Governance CELIOS Solar Research 2026. Seluruh hak cipta dan merek dagang Google Solar API dimiliki oleh Google LLC.*
