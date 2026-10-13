# Spesifikasi Lengkap Query Parameter & Skema Data Google Solar API
**Dokumen Standar Teknis & Integrasi Sistem CELIOS Solar Research (2026)**  
*Referensi Resmi: Google Maps Platform — Solar API REST v1*

---

## 1. Ikhtisar Arsitektur Endpoint

Google Maps Platform Solar API menyediakan dua endpoint utama berbasis REST untuk mengekstraksi data fotogrametri surya dan citra geospasial 3D:

| No | Nama Kategori Endpoint | HTTP Method | Path URL Endpoint | Karakteristik Output | Biaya Standar GCP |
| :-: | :--- | :---: | :--- | :--- | :---: |
| **1** | **Building Insights** | `GET` | `https://solar.googleapis.com/v1/buildingInsights:findClosest` | Objek JSON berstruktur (analisis fisik atap, segmen 3D, panel layout, dan fluks) | **$0.010** / call |
| **2** | **Data Layers** | `GET` | `https://solar.googleapis.com/v1/dataLayers:get` | URL sementara Cloud Storage untuk mengunduh berkas GeoTIFF raster georeferensi | **$0.075** / call |

---

## 2. Kategori 1: Building Insights (`buildingInsights:findClosest`)

Endpoint ini mencari bangunan terdekat dari koordinat masukan yang memiliki model fotogrametri satelit, lalu mengembalikan data tabular dimensi bangunan, estimasi kapasitas panel, fluks radiasi, segmentasi bidang atap 3D, serta estimasi energi tahunan.

### 2.1 Parameter Query HTTP Request (Input)

| Parameter Query | Tipe Data | Wajib / Opsional | Nilai Standar / Opsi | Deskripsi Teknis |
| :--- | :---: | :---: | :--- | :--- |
| **`location.latitude`** | `Double` | **Wajib** | Rentang: `-90.0` s.d. `+90.0` (contoh: `-6.239940`) | Titik lintang pusat pencarian gedung pada sistem koordinat WGS 84. |
| **`location.longitude`** | `Double` | **Wajib** | Rentang: `-180.0` s.d. `+180.0` (contoh: `106.798430`) | Titik bujur pusat pencarian gedung pada sistem koordinat WGS 84. |
| **`requiredQuality`** | `String` (Enum) | Opsional | `BASE` *(default)*, `MEDIUM`, `HIGH` | Kualitas minimal citra satelit yang dapat diterima. Jika citra di lokasi berada di bawah kualitas ini, API akan mengembalikan status `404 NOT_FOUND`. |
| **`experiments`** | `String[]` (Enum) | Opsional | `EXPANDED_COVERAGE` | Mengaktifkan cakupan wilayah yang lebih luas bila tersedia dalam tahap preview / eksperimental Google. |
| **`key`** | `String` | **Wajib** | Kunci API Google Cloud (string alfanumerik) | Kunci autentikasi API GCP yang telah mengaktifkan Solar API dan verifikasi billing. |

---

### 2.2 Skema Data Response JSON Tingkat Atas (Root Fields)

| Nama Kolom / Field | Tipe Data | Keterangan & Makna Fungsional | Contoh Nilai |
| :--- | :---: | :--- | :--- |
| **`name`** | `String` | Identifier unik gedung dalam katalog geospasial Google Maps (*Resource Name*). | `"buildings/GhIJn1JxqKH1GMAREbOc1hqzWkA"` |
| **`center`** | `Object` | Koordinat titik centroid fisik geometri atap gedung (`latitude`, `longitude`). | `{"latitude": -6.2399009, "longitude": 106.7986716}` |
| **`boundingBox`** | `Object` | Batas poligon terkecil (*bounding box*) atap gedung, berisi koordinat sudut barat-daya (`sw`) dan timur-laut (`ne`). | `{"sw": {"latitude": -6.2401, "longitude": 106.7984}, "ne": {"latitude": -6.2397, "longitude": 106.7989}}` |
| **`imageryDate`** | `Object` | Tanggal penerbangan satelit/pesawat yang menghasilkan citra fotogrametri (`year`, `month`, `day`). | `{"year": 2025, "month": 8, "day": 16}` |
| **`imageryProcessedDate`** | `Object` | Tanggal pemrosesan fotogrametri citra oleh algoritma Google. | `{"year": 2025, "month": 8, "day": 20}` |
| **`postalCode`** | `String` | Kode pos administratif lokasi bangunan. | `"12160"` |
| **`administrativeArea`**| `String` | Nama provinsi / wilayah administratif tingkat 1. | `"Daerah Khusus Ibukota Jakarta"` |
| **`regionCode`** | `String` | Kode negara dua huruf berbasis standar ISO 3166-1 alpha-2. | `"ID"` |
| **`imageryQuality`** | `String` (Enum) | Mutu citra riil yang berhasil diambil: `HIGH` (< 0.1 m/px), `MEDIUM` (0.1–0.25 m/px), atau `BASE` (0.25 m/px). | `"BASE"` |
| **`solarPotential`** | `Object` | Objek utama yang memuat kalkulasi teknis fotogrametri surya (diuraikan pada Tabel 2.3). | *(Nested Object)* |

---

### 2.3 Skema Objek `solarPotential` (Metrik Utama Potensi Surya)

| Nama Field | Tipe Data | Satuan | Deskripsi & Formulasi Ilmiah |
| :--- | :---: | :---: | :--- |
| **`maxArrayPanelsCount`** | `Integer` | unit modul | Jumlah maksimum modul surya yang muat dipasang pada bidang atap layak (bebas bayangan dan memenuhi batas jarak tepi). |
| **`panelCapacityWatts`** | `Float` | Watt peak (Wp) | Kapasitas daya nominal per modul surya yang digunakan sebagai acuan dasar Google (standar: **`400.0` Wp**). |
| **`panelHeightMeters`** | `Float` | meter | Dimensi tinggi fisik panel surya acuan Google (standar: **`1.879` m**). |
| **`panelWidthMeters`** | `Float` | meter | Dimensi lebar fisik panel surya acuan Google (standar: **`1.045` m**). |
| **`panelLifetimeYears`** | `Integer` | tahun | Estimasi umur operasional garansi modul surya (standar: **`20` tahun**). |
| **`maxArrayAreaMeters2`** | `Float` | $m^2$ | Luas permukaan atap efektif yang layak dipasangi modul surya (*Usable Roof Area*). |
| **`maxSunshineHoursPerYear`**| `Float` | jam/tahun | Jumlah jam penyinaran matahari puncak ekuivalen (*Peak Sun Hours* / PSH) per tahun pada titik tertinggi bidang atap. |
| **`carbonOffsetFactorKgPerMwh`** | `Float` | kg CO₂/MWh | **Faktor emisi intensitas karbon grid regional** resmi yang di-return langsung oleh Google Solar API (untuk Jabodetabek: **`808.999` kg CO₂/MWh**). |
| **`wholeRoofStats`** | `Object` | — | Statistik luasan dan radiasi dari seluruh bidang atap bangunan (mencakup area miring maupun terhalang bayangan). Memuat `areaMeters2`, `groundAreaMeters2`, dan `sunshineQuantiles`. |
| **`buildingStats`** | `Object` | — | Statistik tapak bangunan secara keseluruhan (*Building Footprint*). |
| **`roofSegmentStats[]`** | `Array` | — | Rincian geometris dan orientasi per bidang segmentasi atap 3D (diuraikan pada Tabel 2.4). |
| **`solarPanels[]`** | `Array` | — | Koordinat posisi persis dan azimuth penempatan masing-masing modul surya (diuraikan pada Tabel 2.5). |
| **`solarPanelConfigs[]`** | `Array` | — | Skenario kapasitas bertingkat, mulai dari 4 panel hingga kapasitas penuh (diuraikan pada Tabel 2.6). |
| **`financialAnalyses[]`** | `Array` | — | Simulasi keekonomian belanja listrik, net metering, dan masa impas (tersedia khusus negara dengan integrasi tarif). |

---

### 2.4 Skema Array `roofSegmentStats[]` (Geometri & Karakteristik Bidang Atap 3D)

Setiap elemen dalam array ini merepresentasikan satu bidang miring/datar atap hasil segmentasi fotogrametri algoritma Google:

| Nama Field | Tipe Data | Satuan | Deskripsi & Interpretasi Fungsional |
| :--- | :---: | :---: | :--- |
| **`pitchDegrees`** | `Float` | derajat ($^\circ$) | Sudut kemiringan bidang atap terhadap bidang horizontal ($0^\circ$ = dak datar sempurna, $90^\circ$ = dinding vertikal). |
| **`azimuthDegrees`** | `Float` | derajat ($^\circ$) | Arah hadap kompas bidang atap ($0^\circ$/$360^\circ$ = Utara, $90^\circ$ = Timur, $180^\circ$ = Selatan, $270^\circ$ = Barat). |
| **`planeHeightAtCenterMeters`** | `Float` | meter | Ketinggian bidang atap pada titik centroid segmen di atas permukaan tanah (*Absolute DSM Elevation*). |
| **`center`** | `Object` | koordinat | Koordinat geospasial titik pusat segmen (`latitude`, `longitude`). |
| **`boundingBox`** | `Object` | koordinat | Batas poligon terkecil segmen atap (`sw`, `ne`). |
| **`stats.areaMeters2`** | `Float` | $m^2$ | Luas permukaan riil 3D dari segmen atap ini (memperhitungkan kemiringan bidang). |
| **`stats.groundAreaMeters2`** | `Float` | $m^2$ | Luas proyeksi 2D tapak segmen atap ke atas permukaan tanah datar. |
| **`stats.sunshineQuantiles`** | `Float[11]` | jam/tahun | 11 nilai kuantil sebaran jam radiasi matahari tahunan pada segmen ini (mulai dari kuantil $0\%$ / minimum, $10\%$, $20\%$, $\dots$, hingga $100\%$ / maksimum). |

---

### 2.5 Skema Array `solarPanels[]` (Posisi Presisi Setiap Modul Surya)

Array ini memuat data mikro penempatan setiap keping panel surya yang divisualisasikan pada layer *Panels Overlay*:

| Nama Field | Tipe Data | Opsi Nilai | Deskripsi Fungsional |
| :--- | :---: | :---: | :--- |
| **`center.latitude`** | `Double` | `-90.0` s.d. `+90.0` | Titik koordinat lintang presisi pusat fisik modul surya. |
| **`center.longitude`** | `Double` | `-180.0` s.d. `+180.0` | Titik koordinat bujur presisi pusat fisik modul surya. |
| **`orientation`** | `String` (Enum) | `PORTRAIT`, `LANDSCAPE` | Orientasi pemasangan modul surya di atas atap (berdiri/tegak atau melebar/mendatar). |
| **`segmentIndex`** | `Integer` | `0, 1, 2, ...` | Indeks referensi ke bidang atap dalam array `roofSegmentStats[]` tempat modul ini menempel. |
| **`yearlyEnergyDcKwh`** | `Float` | kWh DC / tahun | Estimasi produksi energi listrik arus searah (DC) tahunan yang dihasilkan secara mandiri oleh satu modul ini. |

---

### 2.6 Skema Array `solarPanelConfigs[]` (Skenario Ukuran Instalasi)

Array ini memuat konfigurasi simulasi bertingkat mulai dari pemasangan minimal (biasanya 4 panel) hingga kapasitas atap maksimal:

| Nama Field | Tipe Data | Satuan | Deskripsi Fungsional |
| :--- | :---: | :---: | :--- |
| **`panelsCount`** | `Integer` | unit | Jumlah total modul surya yang dipasang dalam konfigurasi skenario ini. |
| **`yearlyEnergyDcKwh`** | `Float` | kWh DC / tahun | **Total energi listrik arus searah (DC) tahunan** yang diproduksi oleh seluruh panel dalam konfigurasi ini sebelum konversi inverter. |
| **`roofSegmentSummaries[]`** | `Array` | — | Ringkasan distribusi panel per segmen atap untuk konfigurasi ini: memuat `panelsCount`, `yearlyEnergyDcKwh`, `segmentIndex`, `pitchDegrees`, dan `azimuthDegrees`. |

---

## 3. Kategori 2: Data Layers (`dataLayers:get`)

Endpoint ini mengekstrak data raster geospasial beresolusi tinggi dalam format GeoTIFF untuk wilayah di sekitar lokasi sasaran. Respons API mengembalikan tautan sementara Cloud Storage yang berlaku selama kurun waktu tertentu untuk mengunduh citra asli.

### 3.1 Parameter Query HTTP Request (Input)

| Parameter Query | Tipe Data | Wajib / Opsional | Nilai Standar / Batasan | Deskripsi Teknis |
| :--- | :---: | :---: | :--- | :--- |
| **`location.latitude`** | `Double` | Wajib* | Rentang: `-90.0` s.d. `+90.0` | Titik lintang pusat kotak analisis raster. (*Wajib jika `exactBoundingBox` tidak digunakan). |
| **`location.longitude`** | `Double` | Wajib* | Rentang: `-180.0` s.d. `+180.0` | Titik bujur pusat kotak analisis raster. (*Wajib jika `exactBoundingBox` tidak digunakan). |
| **`radiusMeters`** | `Float` | Wajib* | Rentang: `0.0` s.d. `100.0` meter | Jari-jari lingkaran cakupan raster dari titik pusat. Batas maksimal resmi Google adalah **100 meter**. |
| **`view`** | `String` (Enum) | Opsional | `FULL_LAYERS` *(default)*, `DSM_ONLY`, `IMAGERY_AND_ANNUAL_FLUX` | Menyaring lapisan raster yang ingin dihasilkan untuk menghemat lebar pita jaringan (*bandwidth*). |
| **`requiredQuality`** | `String` (Enum) | Opsional | `BASE`, `MEDIUM`, `HIGH` | Tingkat mutu fotogrametri minimal yang diterima. |
| **`pixelSizeMeters`** | `Float` | Opsional | Contoh: `0.1`, `0.25`, `0.5` | Ukuran dimensi riil per piksel citra raster (resolusi spasial). Nilai default di Jabodetabek adalah **0.25 meter/piksel**. |
| **`exactBoundingBox.*`**| `Object` | Opsional | Poligon `sw` dan `ne` | Digunakan jika pengguna ingin mendefinisikan batas kotak raster secara manual tanpa memakai `location` + `radiusMeters`. |
| **`experiments`** | `String[]` | Opsional | `EXPANDED_COVERAGE` | Opsi fitur eksperimental cakupan satelit. |
| **`key`** | `String` | **Wajib** | API Key Google Cloud Platform | Kunci autentikasi GCP bertagihan aktif. |

---

### 3.2 Skema Data Response JSON (Daftar URL Pengunduhan GeoTIFF)

| Nama Field Response | Tipe Data | Format Berkas Tautan | Deskripsi Lapisan Raster yang Diunduh |
| :--- | :---: | :---: | :--- |
| **`imageryDate`** | `Object` | Tanggal (`Y-M-D`) | Tanggal akuisisi pemotretan udara satelit. |
| **`imageryProcessedDate`**| `Object` | Tanggal (`Y-M-D`) | Tanggal pengolahan fotogrametri raster. |
| **`imageryQuality`** | `String` (Enum) | `BASE` / `MEDIUM` / `HIGH` | Tingkat resolusi spasial riil berkas raster yang disediakan. |
| **`dsmUrl`** | `String` (URL) | GeoTIFF (`.tif`) | Tautan unduh **Digital Surface Model (DSM 3D)**: Model elevasi permukaan bumi dan struktur atap. |
| **`rgbUrl`** | `String` (URL) | GeoTIFF (`.tif`) | Tautan unduh **Citra Foto Udara Warna Sejati (True Color RGB)** asli satelit. |
| **`maskUrl`** | `String` (URL) | GeoTIFF (`.tif`) | Tautan unduh **Roof Binary Mask**: Segmentasi biner atap bangunan (1 = atap, 0 = tanah/jalan/pohon). |
| **`annualFluxUrl`** | `String` (URL) | GeoTIFF (`.tif`) | Tautan unduh **Annual Solar Flux Heatmap**: Peta sebaran radiasi matahari tahunan per piksel. |
| **`monthlyFluxUrl`** | `String` (URL) | GeoTIFF (`.tif`) | Tautan unduh **Monthly Solar Flux**: Citra komposit 12 band radiasi matahari bulanan (Januari–Desember). |
| **`hourlyShadeUrls[]`** | `String[12]` | 12x GeoTIFF (`.tif`) | Array berisi 12 tautan berkas citra bayangan per jam (*hourly shade bitmask*) untuk tanggal 21 setiap bulan. |

---

### 3.3 Spesifikasi Teknis & Format Berkas GeoTIFF Data Layers

| Nama Layer Geospasial | Tipe Data Piksel | Jumlah Band | Rentang Nilai Piksel | Satuan / Interpretasi Nilai Piksel | Penanganan Nilai Kosong (*NoData*) |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **True Color Aerial (RGB)** | `Byte` (Uint8) | 3 atau 4 (RGBA) | `0` s.d. `255` | Spektrum cahaya tampak (Merah, Hijau, Biru). Visualisasi asli atap. | `0` (transparan) |
| **Digital Surface Model (DSM)** | `Float32` | 1 Band | `-50.0` s.d. `8000.0` | **Ketinggian fisik dalam satuan Meter** di atas permukaan laut / geoid EGM96. | `-9999.0` |
| **Roof Building Mask** | `Byte` (Uint8) | 1 Band | `0` atau `1` | `1` = Bidang Atap Bangunan Terverifikasi, `0` = Bukan Atap Bangunan. | `0` |
| **Annual Solar Flux Heatmap** | `Float32` | 1 Band | `0.0` s.d. `2500.0` | **Fluks radiasi tahunan dalam satuan $kWh/kWp/tahun$** pada permukaan atap. | `-9999.0` |
| **Monthly Solar Flux** | `Float32` | 12 Band | `0.0` s.d. `300.0` | **Fluks radiasi bulanan ($kWh/kWp/bulan$)**. Band 1 = Januari, ..., Band 12 = Desember. | `-9999.0` |
| **Hourly Shade Bitmask** | `Uint32` | 12 Berkas (per bulan) | Bitmask 24-bit | Setiap bit merepresentasikan status bayangan pada jam ke-$n$ pada tanggal 21 tiap bulan ($1$ = terkena sinar matahari, $0$ = terhalang bayangan). | `0` |

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
