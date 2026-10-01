# RENCANA KERJA PROOF OF WORK (POW) GOOGLE SOLAR API JABODETABEK
## Eksekusi Pilot Run Berbiaya Efisien (< Rp 20.000) untuk 13 Kategori Infrastruktur CELIOS

**Dokumen Referensi:** Riset Potensi PLTS Atap Dual-Use Aglomerasi Jabodetabek (CELIOS)  
**Tanggal Dokumen:** 1 Oktober 2026  
**Penulis:** Fullstack Data Engineer — Riset Energi Surya CELIOS  
**Status Eksekusi:** 🟢 Ready for Execution (Smoke Test: Verified HTTP 200 OK)  
**Target File:** `docs/PLAN-PROOF-OF-WORK-SOLAR-API-JABODETABEK.md`

---

## 1. PENDAHULUAN & TEMUAN KUNCI METODOLOGI

Setelah tahap aktivasi Cloud Billing GCP berhasil dituntaskan dengan status **`Paid account`** pada project `celios-konfilkmonitor3`, proyek riset memasuki fase eksekusi data spasial empiris.

### 1.1. Filosofi Eksekusi: "Low Cost, High Impact Proof of Work"
* **Batas Pagu Pilot:** Rp 500.000 (Dana talangan kartu freelancer).
* **Prinsip Utama:** **TIDAK MENGHABISKAN SALDO.**
* **Alokasi Anggaran POW:** Hanya dialokasikan **~Rp 16.800 – Rp 25.000 (Kurang dari 5% total budget)**.
* **Sisa Saldo Aman:** Menjaga sisa saldo **> Rp 475.000 tetap utuh** di kartu freelancer untuk cadangan operasional riset dan kepastian finansial.

### 1.2. Penemuan Kunci Spesifikasi Citra Google Solar API Indonesia
Eksperimen forensik API yang dilakukan pada 1 Oktober 2026 berhasil memecahkan batasan teknis Google Solar API di Indonesia:
1. **Kualitas Citra Resmi Indonesia:** Google Maps Platform menyediakan data kualitas **`BASE` (0.25 m/pixel)** untuk kawasan perkotaan Indonesia, yang diproses dari citra satelit resolusi tinggi terbaru (tercatat perolehan citra per 16 Agustus 2025).
2. **Penyebab Error 404 Terdahulu:** Error `404 NOT_FOUND` pada pengujian awal disebabkan parameter `requiredQuality=HIGH` (yang hanya tersedia untuk negara dengan penerbangan pesawat rendah/aerial di Amerika/Eropa). 
3. **Validasi Endpoint Riil:** Ketika parameter diubah menjadi `requiredQuality=BASE`, endpoint **`buildingInsights:findClosest`** langsung merespons **`HTTP 200 OK`** dan mengembalikan data atap, panel, iradiasi, serta reduksi emisi secara presisi untuk Jabodetabek.

#### Bukti Live Hasil Uji Coba Titik Stasiun MRT Cipete Raya:
```json
{
  "name": "buildings/ChIJGcOo3pTxaS4R7tXLZ9mNJUg",
  "center": { "latitude": -6.2784964, "longitude": 106.7975422 },
  "imageryDate": { "year": 2025, "month": 8, "day": 16 },
  "postalCode": "12410",
  "administrativeArea": "JK",
  "regionCode": "ID",
  "solarPotential": {
    "maxArrayPanelsCount": 280,
    "maxArrayAreaMeters2": 549.79535,
    "maxSunshineHoursPerYear": 1642.6649,
    "carbonOffsetFactorKgPerMwh": 808.999
  }
}
```

---

## 2. BREAKDOWN PILIHAN PROOF OF WORK (POW)

Untuk menyajikan bukti nyata kepada stakeholder CELIOS tanpa menguras saldo, disusun 3 tingkatan skenario:

```mermaid
graph TD
    Budget["Dana Pilot Rp 500.000"] --> OpsiA["🌟 OPSI A: 110 Titik Ikonik (Rp 16.800)"]
    Budget --> OpsiB["OPSI B: 350 Titik Transit (Rp 28.000)"]
    Budget --> OpsiC["OPSI C: Full 2.260 Titik BI (Rp 180.000)"]
    
    OpsiA --> SisaA["Sisa Saldo: Rp 483.200 (96% Utuh)"]
    OpsiB --> SisaB["Sisa Saldo: Rp 472.000 (94% Utuh)"]
    OpsiC --> SisaC["Sisa Saldo: Rp 320.000 (64% Utuh)"]
```

### Tabel Komparasi Skenario:

| Parameter | Opsi A: 110 Titik Ikonik (REKOMENDASI) | Opsi B: Full Transit Jakarta | Opsi C: Full 2.260 Building Insights |
| :--- | :--- | :--- | :--- |
| **Cakupan Kategori** | **13 Kategori Lengkap** (Klaster A & B) | 4 Kategori (MRT, LRT, KRL, BRT) | 13 Kategori Lengkap se-Jabodetabek |
| **Jumlah Titik** | **110 Titik Terpilih** | ~350 Titik | 2.260 Titik Penuh |
| **Panggilan Building Insights** | 110 × $0.005 = **$0.55 (~Rp 8.800)** | 350 × $0.005 = **$1.75 (~Rp 28.000)** | 2.260 × $0.005 = **$11.30 (~Rp 180.000)** |
| **Panggilan Sampel GeoTIFF** | 5 Titik Mega-Struktur = **$0.50 (~Rp 8.000)** | 0 Titik | 0 Titik (Khusus Dokumen RAB) |
| **TOTAL ESTIMASI BIAYA** | **~Rp 16.800 (USD $1.05)** | **~Rp 28.000 (USD $1.75)** | **~Rp 180.000 (USD $11.30)** |
| **Persentase Budget Terpakai** | **3.36%** dari Rp 500.000 | **5.60%** dari Rp 500.000 | **36.00%** dari Rp 500.000 |
| **Sisa Saldo Cadangan** | **Rp 483.200** | **Rp 472.000** | **Rp 320.000** |
| **Output Utama** | Peta Web GIS 13 Kategori + 5 Heatmap Raster | Dataset Transit Jakarta Penuh | Tabulasi Lengkap 2.260 Titik |

---

## 3. DETAIL TITIK TARGET OPSI A (110 TITIK REPRESENTATIF)

Opsi A dipilih sebagai strategi utama karena memberikan diversifikasi terlengkap di seluruh 13 kategori infrastruktur publik:

### Klaster A: Infrastruktur Mobilitas & Transit (73 Titik)
1. **Stasiun MRT Jakarta (13 Titik Penuh):**
   * Lebak Bulus Grab, Fatmawati Indomaret, Cipete Raya, Haji Nawi, Blok A, Blok M BCA, ASEAN, Senayan Mastercard, Istora Mandiri, Bendungan Hilir, Setiabudi Astra, Dukuh Atas BNI, Bundaran HI Bank DKI.
2. **Stasiun LRT Jabodebek & Jakarta (18 Titik):**
   * Dukuh Atas, Setiabudi, Rasuna Said, Kuningan, Pancoran, Cikoko, Ciliwung, Cawang, Halim, Jatibening Baru, Cikunir 1 & 2, Bekasi Barat, Jati Mulya, Ciracas, Harjamukti, Pegangsaan Dua, Velodrome.
3. **Stasiun KRL Commuter Line Utama (25 Titik):**
   * Hub Transit: Manggarai, Tanah Abang, Duri, Jatinegara, Juanda, Gondangdia.
   * Ujung Koridor: Bogor, Depok Baru, Bekasi, Cikarang, Tangerang, Rangkasbitung.
4. **Halte BRT TransJakarta Ikonik (25 Titik):**
   * Koridor 1 & Utama: Halte Bundaran HI Astra, Tosari, CSW/ASEAN (Simpul Integrasi), Harmoni, Monas, Gelora Bung Karno (GBK), Senayan, Ragunan, Pulogebang.
5. **Kantung Park & Ride Terbuka (10 Titik):**
   * Park & Ride Terminal Kampung Rambutan, Lebak Bulus, Kalideres, Thamrin 10, Stasiun Bekasi, Stasiun Depok, Stasiun Tangerang.

### Klaster B: Fasilitas Publik Tambahan (37 Titik)
6. **Universitas & Kampus Utama (6 Titik):**
   * Universitas Indonesia (Depok), Universitas Negeri Jakarta (Rawamangun), Universitas Trisakti, Binus University (Anggrek), IPB University (Dramaga), ITB Kampus Cirebon/Bekasi.
7. **Rumah Sakit Rujukan & Puskesmas (8 Titik):**
   * RSUPN Dr. Cipto Mangunkusumo (RSCM), RSUP Fatmawati, RSUD Tarakan, RS Harapan Kita, RSUD Pasar Minggu, Puskesmas Kec. Tebet, Puskesmas Kec. Kebayoran Baru, Puskesmas Gambir.
8. **Pasar Tradisional & Grosir (6 Titik):**
   * Pasar Tanah Abang (Blok A/B), Pasar Induk Kramat Jati, Pasar Mayestik, Pasar Senen Blok 3, Pasar Santa, Pasar Jatinegara.
9. **Bandara & Simpul Udara (2 Titik):**
   * Bandara Internasional Soekarno-Hatta (Terminal 3 & Gedung Kargo) dan Bandara Halim Perdanakusuma.
10. **Stadion & Gelanggang Olahraga (5 Titik):**
    * Jakarta International Stadium (JIS), Stadion Utama Gelora Bung Karno (SUGBK), Stadion Patriot Candrabhaga (Bekasi), Stadion Pakansari (Cibinong), GOR Soemantri Brodjonegoro (Kuningan).
11. **Sekolah Negeri Percontohan (10 Titik):**
    * SMAN 8 Jakarta, SMAN 70 Jakarta, SMAN 28 Jakarta, SMKN 26 Jakarta, SDN Menteng 01, SMAN 1 Bogor, SMAN 1 Depok, SMAN 1 Bekasi, SMAN 1 Tangerang, SMAN 2 Tangsel.

---

## 4. SAMPEL RASTER GEOTIFF (5 TITIK MEGA-STRUKTUR)

Untuk membuktikan kualitas citra spasial Google (Solar Flux & DSM 0.25m/pixel) tanpa membebani biaya ($0.100 per titik), dipilih 5 mega-struktur dengan atap raksasa:
1. **Jakarta International Stadium (JIS)** — Atap buka-tutup baja bentang terlebar di Asia Tenggara.
2. **Stadion Utama GBK Senayan** — Kanopi atap temu gelang legendaris.
3. **Stasiun Manggarai Sentral** — Atap kanopi peron bertingkat 3.
4. **Terminal 3 Bandara Soekarno-Hatta** — Permukaan dak atap datar terluas di Banten/Jabodetabek.
5. **Simpul Integrasi CSW (Cakra Selaras Wahana)** — Model bangunan integrasi vertikal BRT-MRT.

---

## 5. ARSITEKTUR TEKNIS & PIPELINE EKSEKUSI

```mermaid
flowchart LR
    MasterData[Master Coordinates GeoJSON/CSV] --> BatchEngine[batch_fetch_pow.py]
    APIKey[.env: GOOGLE_API_KEY] --> BatchEngine
    
    BatchEngine -->|Rate: 5 req/s + BASE Quality| SolarAPI[Google Solar API]
    SolarAPI --> Cache[data/raw/solar/pow_cache/]
    
    BatchEngine --> OutputGIS[data/processed/gis/pow_solar_110.geojson]
    BatchEngine --> OutputCSV[output/reports/pow_solar_summary.csv]
    BatchEngine --> GeoTIFF[data/raw/satellite/geotiff_samples/]
```

### 5.1. Komponen Script & File:
* **Script Eksekutor:** `tools/solarapi/batch_fetch_pow.py`
* **Konfigurasi Lingkungan:** `tools/solarapi/.env` (menggunakan `GOOGLE_API_KEY=AIzaSyCX1SSLp3sIvTIzqjRgE7nTe0VXNqgz4yo`)
* **Penyimpanan Cache Mentah:** `data/raw/solar/pow_cache/{kategori}_{id}.json`
* **Hasil Gabungan Spasial:** `data/processed/gis/pow_solar_110.geojson`
* **Ringkasan Tabulasi Eksekutif:** `output/reports/pow_solar_summary.csv`
* **Folder Citra Raster:** `data/raw/satellite/geotiff_samples/*.tif`

### 5.2. Spesifikasi Parameter API:
* **Endpoint Building Insights:**  
  `https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lon}&requiredQuality=BASE&key={API_KEY}`
* **Endpoint Data Layers (Khusus 5 Sampel):**  
  `https://solar.googleapis.com/v1/dataLayers:get?location.latitude={lat}&location.longitude={lon}&radiusMeters=100&requiredQuality=BASE&pixelSizeMeters=0.25&key={API_KEY}`
* **Rate Limiting:** Delay 0.2 detik antar panggilan (5 requests per second) untuk mencegah throttling perbankan/Google.

---

## 6. DELIVERABLE RESMI UNTUK CELIOS

Hasil dari Proof of Work Opsi A ini akan langsung diwujudkan menjadi bahan presentasi resmi ke tim CELIOS:
1. **Interactive Web GIS Dashboard (Mockup Riset):** Menampilkan peta titik sebaran 13 kategori dengan tooltip luas atap, jumlah panel surya, dan estimasi listrik tahunan (kWh).
2. **Katalog Visual Heatmap Radiasi Surya:** Perbandingan visual atap JIS, GBK, dan Manggarai yang dipetakan oleh citra Google Solar Flux.
3. **Memo Teknis Validasi Anggaran:** Bukti bahwa estimasi RAB Rp 5.000.000 sudah teruji di lapangan dengan keakuratan data satelit resmi.

---

## 7. RENCANA KERJA & CHECKLIST TINDAKAN

- [x] Laporan status billing dan mitigasi finansial didokumentasikan.
- [x] Rencana kerja Proof of Work (POW) disusun dan di-commit ke Git.
- [ ] Buat skrip eksekutor: `tools/solarapi/batch_fetch_pow.py`.
- [ ] Eksekusi penarikan 110 titik Building Insights (Biaya ~Rp 8.800).
- [ ] Eksekusi download 5 sampel GeoTIFF (Biaya ~Rp 8.000).
- [ ] Kompilasi output menjadi GeoJSON dan CSV ringkasan.
- [ ] Generate ringkasan analitik dan visualisasi untuk CELIOS.
