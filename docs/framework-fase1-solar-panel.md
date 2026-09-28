# Framework Riset FASE 1
## Teduhi Ruang Kota Kami: Potensi Instalasi Dual-Use Infrastructure PLTS Atap di JABODETABEK

> Ini adalah dokumen untuk FASE 1 dari proyek riset CELIOS.
> Sumber Outline: ref/Paper Teduhi Ruang Kota Kami.pdf & ref/1-s2.0-S2352938523001441-main.pdf
> Fokus Wilayah: JABODETABEK (Provinsi DKI Jakarta, Kab/Kota Bogor, Kota Depok, Kab/Kota Tangerang, Kota Tangerang Selatan, Kab/Kota Bekasi)
> Fokus Infrastruktur: Infrastruktur Urban Transportasi dan Publik (Halte BRT, Stasiun KRL/MRT/LRT, JPO, Park & Ride Komuter, Lapangan Parkir Terbuka, MSCP, Koridor Pedestrian)
> Kebijakan Data: No Mock Data, Pure Data Driven (Pagu Safety Buffer: 4,000 Titik Regional, Status: Estimasi Belum Tervalidasi Riil)

---

## 1. Pertanyaan Utama Riset

> "Sejauh mana infrastruktur urban dan simpul transportasi di kawasan metropolitan Jabodetabek dapat dialihfungsikan menjadi dual-use infrastructure untuk PLTS Atap guna mewujudkan kedaulatan energi kawasan aglomerasi dan memitigasi efek Urban Heat Island?"

### Sub-Pertanyaan Penelitian

| No | Pertanyaan Penelitian |
|----|-----------------------|
| P1 | Apa saja kategori infrastruktur publik di Jabodetabek yang paling potensial untuk instalasi solar canopy? |
| P2 | Berapa estimasi luasan area potensial dari infrastruktur-infrastruktur tersebut? |
| P3 | Berapa estimasi total kapasitas terpasang (MWp) yang dapat dihasilkan? |
| P4 | Berapa estimasi produksi listrik tahunan (GWh) dan seberapa besar kontribusinya terhadap konsumsi energi kawasan metropolitan Jabodetabek? |
| P5 | Bagaimana dampak instalasi ini terhadap reduksi emisi CO2? |
| P6 | Sejauh mana implementasi solar canopy ini dapat memitigasi efek Urban Heat Island (UHI) secara lokal pada koridor komuter dan pusat aktivitas? |
| P7 | Apa hambatan regulasi dan model pembiayaan (bisnis) utama dalam implementasinya antar yurisdiksi daerah (DKI, Jabar, Banten, dan Pusat)? |

---

## 2. Timeline Produksi

| Bulan | Milestone |
|-------|----------|
| Bulan 1 (Minggu 1-2) | Akuisisi data spasial (OSM BBOX Jabodetabek) dan estimasi awal PSH (PVGIS) |
| Bulan 1 (Minggu 3-4) | Pengumpulan data operator transportasi (TransJakarta, KAI Commuter Jabodetabek, MRT, LRT, BPTJ, Dishub Bodetabek) dan literatur UHI |
| Bulan 2 (Minggu 1-2) | Analisis konversi luasan ke kapasitas energi dan perhitungan reduksi emisi |
| Bulan 2 (Minggu 3-4) | Penyusunan laporan, dashboard Streamlit, dan perumusan rekomendasi kebijakan |

---

## 3. Rencana Temuan Studi (Target Output)

| Fokus | Temuan yang Ditargetkan |
|-------|------------------------|
| Inventarisasi Infrastruktur | Peta sebaran infrastruktur potensial se-Jabodetabek (Pagu safety buffer 4,000 titik; Catatan: angka ini estimasi plafon atas belum tervalidasi riil) |
| Kedaulatan Energi | Kawasan metropolitan tidak lagi memindahkan beban produksi energinya ke daerah pedesaan (sacrificial zones) |
| Kapasitas & Produksi | Angka definitif MWp dan GWh dari pemanfaatan infrastruktur urban dan simpul transportasi |
| Lingkungan (Mitigasi UHI) | Potensi penurunan suhu permukaan di area pejalan kaki/parkiran akibat kanopi (merujuk pada profil spasio-temporal SUHI Jabodetabek) |
| Lingkungan (Emisi) | Kuantifikasi reduksi CO2 dari substitusi konsumsi grid PLN Jawa-Madura-Bali |
| Sosial | Peningkatan kenyamanan termal komuter dan pejalan kaki (terlindungi dari panas ekstrem/heatstroke) dan inklusi sosial |
| Ekonomi | Penghematan biaya operasional (OPEX) operator transportasi dan pengelola fasilitas publik |

---

## Modul Pembahasan & Analisis (Sinkronisasi Dashboard)

### Phase 1: Overview & Kedaulatan Energi Kota

#### 1.1 Latar Belakang & Isu Kedaulatan Energi (*Sacrificial Zones*)
Fokus: Mengurai argumen ketidakadilan spasial dalam transisi energi (*top-down approach*) di mana kota sebagai lokus konsumsi memindahkan beban produksi energinya dengan mengekstraksi ruang hidup/ekologis di wilayah pedesaan.
Tujuan: Menjadikan *Dual-Use Infrastructure* di kawasan aglomerasi Jabodetabek sebagai bentuk tanggung jawab kemandirian energi regional.

#### 1.2 Transparansi & Status Akuisisi Data Infrastruktur
Fokus: Menyajikan papan status (*live-status*) atas progres pengumpulan data primer dan sekunder untuk infrastruktur urban regional.

Sumber Data:

| ID Data | Sumber Data | Kegunaan / Target Regional Jabodetabek |
|---|---|---|
| `Data #11` | PT TransJakarta & Dishub Bodetabek | Ekstraksi ~650 titik halte (TJ koridor/non-koridor + feeder Biskita Bogor, Trans Patriot Bekasi, Tayo Tangerang) |
| `Data #12` | PT KAI Commuter (KCI) | Ekstraksi 85 stasiun KRL Commuter Line se-Jabodetabek |
| `Data #13` | PT MRT Jakarta | Ekstraksi 13 stasiun MRT Fase 1 |
| `Data #14` | PT Kereta Api Indonesia (LRT Jabodebek) & PT LRT Jakarta | Ekstraksi 18 stasiun LRT Jabodebek + 6 stasiun LRT Jakarta |
| `Data #15` | Dishub DKI, Jabar, Banten & BPTJ / Kemenhub | Data ~475 JPO, 25 Terminal Bus Tipe A/B, serta 60+ kantung Park & Ride stasiun komuter |

---

### Phase 2: Inventarisasi Spasial Infrastruktur Urban

#### 2.1 Metodologi Pemetaan & Ekstraksi Data
Fokus: Mendokumentasikan teknik pengumpulan poligon spasial (*building footprints*) dan titik POI menggunakan OSMnx, Geocoding, dan *Places API* tanpa harus bergantung pada pembebasan lahan baru.

#### 2.2 Kategorisasi Aset & Luasan Potensial
Fokus: Mengklasifikasikan aset infrastruktur ke dalam 2 klaster besar (13 kategori komprehensif Jabodetabek):
- **Klaster A: Infrastruktur Transit & Mobilitas (7 Kategori Baseline)**: Halte BRT, Stasiun KRL, Stasiun MRT/LRT/Bandara/KCIC, JPO, Lapangan Parkir Terbuka / Park & Ride, Gedung Parkir (*MSCP*), dan Koridor Pedestrian TOD.
- **Klaster B: Tambahan Infrastruktur Fasilitas Publik (6 Kategori Ekspansi)**:
  1. **Sekolah Negeri**: SD, SMP, SMA/SMK Negeri se-Jabodetabek.
  2. **Universitas**: Kampus perguruan tinggi negeri & swasta.
  3. **Fasilitas Kesehatan**: Rumah Sakit (RSUD/Swasta) & Puskesmas Kecamatan/Kelurahan.
  4. **Pasar**: Pasar Tradisional & Pasar Rakyat (PD Pasar Jaya / pasar daerah).
  5. **Bandara**: Terminal penumpang, hanggar, dan fasilitas aviasi (Soekarno-Hatta & Halim).
  6. **Fasilitas Olahraga**: Stadion utama & Gelanggang Olahraga (GOR).
Menghitung luasan bersih (*usable area ratio*) dari atap/kanopi untuk masing-masing kategori.

#### 2.3 Format Data Spasial & Strategi Handover (Dual-Native)
- **Web-Native (Streamlit)**: *Output* pemrosesan disimpan dalam `GeoJSON` dan `CSV` untuk performa rendering yang cepat di WebGIS (tanpa *dependency* GIS yang berat di *server*).
- **GIS-Native (Serah Terima/Archive)**: Kompilasi final (*handover*) kepada analis/mitra proyek akan diserahkan dalam bentuk `GeoPackage (.gpkg)`. Satu *file database* SQLite ini menggantikan puluhan *Shapefile* dan 100% kompatibel dengan *software* seperti ArcGIS Pro dan QGIS.

#### 2.4 Akselerasi Pipeline Geospasial
Sebagai alternatif *OpenStreetMap (OSM)* yang lambat dan rawan limit blokir API, dua platform *enterprise* dapat digunakan untuk analisis massal (28.000+ titik infrastruktur):
1. **Google Solar API**: Solusi *machine-learning* berbayar; otomatis menyediakan luas atap bersih, elevasi, bayangan, dan angka potensi produksi GWh/tahun.
2. **Overture Maps Foundation**: Solusi gratis berkecepatan tinggi; mengunduh *GeoParquet* masif berisi atap bangunan seluruh kota, dilanjutkan operasi *Offline Spatial Join* di memori RAM laptop.

Sumber Data:

| ID Data | Sumber Data | Kegunaan Utama | Status Biaya |
|---|---|---|---|
| `Data #16` | OpenStreetMap (OSM) | Ekstraksi luasan *building footprints* dan POI infrastruktur via OSMnx | 🟢 Gratis |
| `Data #16b` | Overture Maps Foundation | Alternatif *building footprints* offline via *GeoParquet* masif | 🟢 Gratis |
| `Data #16c` | Google Solar API | Alternatif ekstraksi luas atap, *shading*, & GWh terotomasi | 💰 Berbayar |
| `Data #19` | Planet Labs / GEE | Alternatif citra satelit resolusi tinggi untuk validasi spasial | 💰 Berbayar / 🟢 Gratis (Tier) |
| `Data #20` | Google Maps API | Validasi Geocoding & Places (500+ titik parkir komersial/mal) | 💰 Berbayar |
| `Data #6` | Jakarta Open Data | CKAN API untuk dimensi bangunan | 🟢 Gratis |
| `Data #4` | One Map Indonesia | Peta dasar Jakarta & batas administrasi | 🟢 Gratis |

---

### Phase 3: Kapasitas & Produksi Energi

#### 3.1 Konversi Luasan ke Potensi Daya (MWp & GWh)
Fokus: Menerjemahkan meter persegi (m²) kanopi menjadi daya energi menggunakan parameter teknis efisiensi panel, *Performance Ratio* (PR), dan iradiasi lokal.

#### 3.2 Substitusi Beban Konsumsi Kota
Fokus: Mengkomparasikan proyeksi *output* energi tahunan dengan beban konsumsi eksisting Jakarta (Misal: sektor publik menghabiskan 24.8 juta MWh di tahun 2024 berdasarkan data PLN).

#### 3.3 Studi Komparasi Implementasi Global
Fokus: Mengambil preseden keberhasilan (*lessons learned*) pembangunan *solar canopy* di Prancis (mandatori tempat parkir), Jepang, hingga implementasi domestik di Bandara Soetta dan Surabaya.

Sumber Data:

| ID Data | Sumber Data | Kegunaan Utama | Status Biaya |
|---|---|---|---|
| `Data #21` | PVGIS (JRC Europe) | Data iradiasi dan *Peak Sun Hours* (PSH) per m² | 🟢 Gratis |
| `Data #22` | NASA POWER | Data cuaca historis (pembanding PVGIS) | 🟢 Gratis |
| `Data #24` | Solargis | Alternatif data iradiasi surya (GHI) resolusi tinggi & cuaca | 💰 Berbayar |
| `Data #2` | PLN Statistics | Data *baseline* konsumsi dan penjualan listrik per sektor | 🟢 Gratis |
| `Data #25-28` | Existing Solar PV | Angka aktual produksi (*lessons learned* bandara, dll) | 🟢 Gratis (OSINT) |

---

### Phase 4: Analisis Triple-Benefits & Mitigasi UHI

#### 4.1 Mitigasi Urban Heat Island & Kenyamanan Termal
Fokus:
- **Substitusi Area Beton**: Menghalangi radiasi langsung ke aspal yang memicu suhu ekstrem 32°C-36°C (berdasarkan tren tata lahan 2004-2020).
- **Mitigasi Kubah Panas**: Meredam lonjakan *transect* suhu ekstrem (>37°C) di siang bolong.
- **Intervensi Episentrum SUHI**: Instalasi tepat sasaran di episentrum kepadatan dan panas untuk melindungi kenyamanan warga (mencegah *heatstroke* & inklusi sosial).

#### 4.2 Reduksi Emisi Karbon
Fokus: Menghitung penghindaran CO₂ berkat substitusi konsumsi dari sistem *grid* kelistrikan Jawa-Bali yang masih didominasi batu bara.

#### 4.3 Analisis Tantangan: Teknis, Regulasi, Pembiayaan
Fokus: 
- Mengurai limitasi kuota interkoneksi PLN (Permen ESDM 26/2021).
- Memecahkan kendala pembiayaan *CAPEX* mahal lewat skema *BOOT*, *KPBU*, atau penyewaan atap.
- Membahas persoalan *ownership* (kepemilikan aset) antara Pemda, BUMN/BUMD, dan swasta.

#### 4.4 Rekomendasi Kebijakan (3 Fase Eksekusi)
Fokus: 
- Fase 1 (0–2 tahun): Pilot *project* di fasilitas BUMD.
- Fase 2 (2–5 tahun): Ekspansi ke parkiran komersial swasta.
- Fase 3 (5–10 tahun): Mandatori panel surya terintegrasi untuk seluruh IMB bangunan dan parkiran baru.

Sumber Data Utama:

| ID Data | Sumber Data | Kegunaan Utama | Status Biaya |
|---|---|---|---|
| `Data #40` | Siswanto et al. (2023) | Basis parameter profil *Surface Urban Heat Island* (SUHI) Jakarta | 🟢 Gratis |
| `Data #3` | Kementerian ESDM | Angka faktor emisi karbon grid Jawa-Bali | 🟢 Gratis |
| `Data #34` | PLN Tariff | Tarif dasar listrik untuk estimasi OPEX | 🟢 Gratis |
| `Data #33` | Solar EPC Companies | Estimasi CAPEX kanopi surya (Rp/kWp) | 🟢 Gratis |
| `Data #35` | Bank Indonesia | Tingkat inflasi & *discount rate* untuk NPV/ROI | 🟢 Gratis |
| `Data #32` | PERMEN ESDM 26/2021 | Regulasi interkoneksi dan kapasitas PLTS Atap | 🟢 Gratis |

---

## 5. Kebutuhan Data Fase 1 - Master List

### Data Infrastruktur & Spasial
| Data | Sumber | Status |
|------|--------|--------|
| Titik lokasi Halte TransJakarta | OSM / PT TransJakarta | Belum Lengkap |
| Koordinat Parkir Terbuka & MSCP | OSM / Google Places | Belum Lengkap |
| Titik lokasi Stasiun KRL/MRT/LRT | OSM / Operator | Belum Lengkap |
| Pola tata guna lahan (LULCC) Jakarta | Analisis Landsat/MODIS | Selesai (Rujukan Paper) |

### Data Energi & Iklim
| Data | Sumber | Status |
|------|--------|--------|
| Peak Sun Hours (PSH) Jakarta | PVGIS / NASA POWER | Belum Lengkap |
| Penjualan Listrik PLN per Sektor | PLN Statistics | Selesai (Baseline) |
| Profil LST (Suhu Permukaan Darat) JKT | Siswanto et al. (2023) | Selesai |
| Emisi Grid Jawa-Bali | Kementerian ESDM | Belum Lengkap |

---

## 6. Metodologi Analisis

### Pendekatan Utama
1. Analisis Inventarisasi Spasial: Ekstraksi fitur poligon dan titik (OSMnx) untuk memetakan ruang infrastruktur yang dapat digunakan.
2. Pemodelan Estimasi Energi (Energy Yield): Penggunaan formula kapasitas energi berbasis luas wilayah dan iradiasi spesifik (PVGIS).
3. Penilaian Dampak (Impact Assessment): Perhitungan penghematan CO2 secara kuantitatif dan analisis kualitatif literatur mengenai efek naungan pada penurunan SUHI (Surface Urban Heat Island).

### Unit Analisis
- Level Mikro: Sampel halte spesifik, peron stasiun, atau tempat parkir.
- Level Makro: Agregat luasan area parkir dan infrastruktur di seluruh wilayah DKI Jakarta.

---

## 7. Referensi & Sumber Acuan

- Kertas Konsep Riset: Teduhi Ruang Kota Kami (CELIOS)
- Basis Akademik Mitigasi Suhu Kota: Siswanto, S., Nuryanto, D. E., Ferdiansyah, M. R., Prastiwi, A. D., Dewi, O. C., Gamal, A., & Dimyati, M. (2023). Spatio-temporal characteristics of urban heat Island of Jakarta metropolitan. Remote Sensing Applications: Society and Environment, 32, 101062.
- Data Acuan Pertumbuhan Penduduk & Listrik: BPS dan Kementerian ESDM.
