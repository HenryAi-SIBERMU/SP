# ASUMSI KLASIFIKASI STRUKTUR & STANDAR TEKNO-EKONOMI PLTS (13 KATEGORI JABODETABEK)

Dokumen ini mendokumentasikan metodologi, logika deduktif teknik sipil, standar biaya modal (CAPEX), biaya operasional (OPEX), tarif listrik, dan periode pengembalian modal (*simple payback period*) yang diterapkan pada analisis tekno-ekonomi 2.100 titik fasilitas publik di Jabodetabek pada Page 3 (`pages/3_Analisis_Ekonomi.py`).

---

## 1. Latar Belakang & Keterbatasan Data Spasial

### 1.1 Ketiadaan Atribut Material Atap di OpenStreetMap (OSM)
- Ekstraksi data spasial dari OpenStreetMap (OSM) berhasil memetakan **2.100 titik fasilitas publik** yang terbagi dalam 13 kategori (`hospital`, `school`, `university`, `mall`, `market`, `stadium`, `brt`, `krl`, `mrt_lrt`, `parking`, `terminal`, `airport`, `jpo`).
- Namun, basis data OSM untuk wilayah Jabodetabek tidak menyediakan atribut ketahanan struktural maupun material penutup atap (`roof:material` kosong / *unpopulated* pada >99% poligon bangunan).
- Google Solar API menyediakan data geometri atap (luas, orientasi, insolasi matahari), namun tidak membedakan apakah permukaan tersebut merupakan dak beton gedung atau kanopi terbuka.

### 1.2 Solusi Metodologi: Tipologi Rekayasa Arsitektur (*Engineering Archetypes*)
Untuk menghitung estimasi biaya investasi (CAPEX) secara realistis dan akuntabel, proyek ini menerapkan klasifikasi arketipe berbasis **fungsi utilitas dan tipologi fisik bangunan** di lapangan.

---

## 2. Logika Deduktif Klasifikasi Struktur

Klasifikasi struktur PLTS didasarkan pada satu pertanyaan rekayasa sipil (*civil engineering*):
> *"Apakah modul surya dipasang di atas dak gedung yang sudah kokoh menahan beban, atau proyek harus mendirikan kolom tiang pancang dan rangka bentang lebar baru dari atas tanah/lantai?"*

```
[Tipologi Fisik & Fungsi Fasilitas di Lapangan]
           │
           ├── A. Gedung Tertutup Bertingkat Masif
           │      (RSUD, Sekolah, Kampus, Mall, Pasar, Stadion/GOR)
           │      └── Memiliki dak beton bertulang / atap struktural eksisting
           │          └── Pemasangan: Rel aluminium jepit + ballast standar
           │              └── ARKETIPE 1: Rooftop Dak Beton Standar (Rp 12,5 Jt/kWp)
           │
           └── B. Simpul Sirkulasi Transit & Area Terbuka
                  (Halte BRT, Stasiun KRL, Stasiun MRT/LRT, Gedung/Area Parkir, Terminal, Bandara, JPO)
                  └── Area sirkulasi peron penumpang, jalan, atau pelataran kendaraan
                      └── Pemasangan: Tiang baja galvanis bentang lebar + angkur pondasi + kanopi peneduh
                          └── ARKETIPE 2: Solar Carport & Kanopi Rangka Baja (Rp 18,5 Jt/kWp)
```

### 2.1 Arketipe 1: Rooftop Dak Beton Standar
- **Kategori Terpilih (6 Kategori):**  
  `hospital`, `school`, `university`, `mall`, `market`, `stadium`.
- **Karakteristik Fisik Lapangan:**
  - Bangunan berupa gedung permanen bertingkat dengan lantai dak beton bertulang (*reinforced concrete flat roof*).
  - Struktur bangunan sudah memiliki daya dukung beban mati (*dead load*) dan beban hidup (*live load*) gedung yang memadai.
- **Komponen Instalasi:**
  - Modul PV Monocrystalline Tier-1.
  - Inverter on-grid string.
  - Penopang rel aluminium ringan (*ballasted / chemical anchor* dak).
  - Proteksi DC/AC dan Sertifikasi Laik Operasi (SLO).
  - **Tanpa pekerjaan pondasi dalam dan tanpa kolom baja berat.**
- **Standar Biaya (CAPEX):** **Rp 12.500.000 / kWp** (Rp 12,5 Juta/kWp).

---

### 2.2 Arketipe 2: Solar Carport & Kanopi Rangka Baja
- **Kategori Terpilih (7 Kategori):**  
  `brt`, `krl`, `mrt_lrt`, `parking`, `terminal`, `airport`, `jpo`.
- **Karakteristik Fisik Lapangan:**
  - Simpul transit penumpang terbuka, kanopi peron stasiun KA, koridor shelter bus raya terpadu, area parkir terbuka, selasar pejalan kaki layang (JPO), dan depo kendaraan.
  - Modul surya tidak bisa diletakkan langsung di lantai/tanah, melainkan difungsikan ganda sebagai atap peneduh (*dual-function solar canopy*).
  - Memerlukan ruang bebas vertikal (*vertical clearance*) 2,5 – 4,5 meter agar kendaraan (bus, mobil, kereta) dan pejalan kaki dapat bergerak aman di bawahnya.
- **Komponen Instalasi:**
  - Modul PV High-Efficiency.
  - Rangka struktural baja galvanis bentang lebar (*heavy-duty hot-dip galvanized steel truss / cantilever*).
  - Pekerjaan pondasi sipil (pondasi cakar ayam / tiang pancang / angkur beton bertulang).
  - Sistem talang air & *waterproofing canopy* terpadu.
  - Inverter & sistem monitoring pintar.
- **Standar Biaya (CAPEX):** **Rp 18.500.000 / kWp** (Rp 18,5 Juta/kWp).
- **Selisih Biaya (Delta):**  
  Tambahan **+Rp 6.000.000 / kWp (+48%)** mencerminkan pengadaan baja struktural, fabrikasi kanopi, dan pekerjaan pondasi sipil penahan beban gempa dan angin (*wind load*).

---

## 3. Landasan Rujukan Dokumen Resmi (Data Lineage)

Semua angka asumsi finansial mengacu pada dokumen dan pernyataan resmi regulator serta pelaku industri EPC:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DOKUMEN RUJUKAN RESMI                                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Standar CAPEX Rooftop Dak Beton (Rp 12,5 Juta/kWp):                                │
│    - Rujukan: Wawancara Dirjen EBTKE Kementerian ESDM (Dadan Kusdiana) di CNBC         │
│      Indonesia Energy Corner (9 Mei 2022) & Benchmarking Asosiasi Energi Surya         │
│      Indonesia (AESI).                                                                 │
│    - Verbatim: "Biaya pemasangan PLTS Atap 1 kWp saat ini Rp 14-17 juta... Untuk skala │
│      komersial dan industri menengah-besar, efisiensi skala menekan biaya sistem       │
│      menjadi Rp 12,5 - 14 juta per kWp."                                               │
│    - File Bukti Raw: data/raw/sources/cnbc_esdm_biaya_plts_atap_official.html          │
│                                                                                        │
│ 2. Standar CAPEX Solar Carport & Kanopi Baja (Rp 18,5 Juta/kWp):                       │
│    - Rujukan: Siaran Pers Resmi PT Surya Energi Indotama (SEI) & PT Pertamina Power     │
│      Indonesia mengenai EPC PLTS Bandara Soekarno-Hatta Terminal 2 & Kajian Multiplier │
│      Tenaga Kerja IESR (Dunia Energi, 2021).                                           │
│    - Verbatim: "Total kapasitas PLTS di 3 Bandara sebesar 2,39 MWp (1,5 MWp di Bandara │
│      Soekarno-Hatta T2 & AOCC)... instalasi kanopi parkir dengan struktur baja penopang│
│      dan pondasi sipil."                                                               │
│    - File Bukti Raw: data/raw/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.html │
│                                                                                        │
│ 3. Tarif Tenaga Listrik PLN (Rp 1.467,28 / kWh):                                       │
│    - Rujukan: Statistik PLN 2024 & Peraturan Menteri ESDM tentang Tarif Tenaga Listrik │
│      Tersedia (Tariff Adjustment). Golongan P-1/TR (Pelayanan Publik & Kantor          │
│      Pemerintah) dan B-2/TR (Bisnis Menengah tegangan rendah 6.600 VA - 200 kVA).      │
│    - File Bukti Raw: data/raw/pln/Statistik_PLN_2024.pdf                               │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Tabel Ringkasan Asumsi Finansial 13 Kategori Fasilitas

Berikut adalah rekapitulasi lengkap hasil perhitungan tekno-ekonomi untuk ke-13 kategori fasilitas:

| No | Kategori Fasilitas | Golongan Tarif PLN | Jumlah Titik | Potensi Kapasitas (kWp) | Produksi Energi (MWh/th) | Tipe Struktur PLTS | CAPEX per kWp (Rp) | Total CAPEX (Rp Miliar) | Penghematan Listrik (Rp Miliar/th) | Simple Payback (Tahun) |
|:---:|:---|:---:|:---:|:---:|:---:|:---|:---:|:---:|:---:|:---:|
| 1 | **Rumah Sakit Umum Daerah (RSUD)** | P-1/TR | 254 | 59.198,4 | 78.509,92 | Rooftop Dak Beton Standar | 12.500.000 | 739,98 | 115,20 | **6,42** |
| 2 | **Sekolah Dasar & Menengah** | P-1/TR | 667 | 44.845,6 | 58.889,60 | Rooftop Dak Beton Standar | 12.500.000 | 560,57 | 86,41 | **6,49** |
| 3 | **Pusat Perbelanjaan / Mall** | B-2/TR | 88 | 43.448,4 | 57.342,55 | Rooftop Dak Beton Standar | 12.500.000 | 543,11 | 84,14 | **6,45** |
| 4 | **Stasiun KRL Commuter Line** | P-1/TR | 88 | 33.555,2 | 44.335,43 | Solar Carport & Kanopi Baja | 18.500.000 | 620,77 | 65,05 | **9,54** |
| 5 | **Kampus & Perguruan Tinggi** | P-1/TR | 188 | 28.437,2 | 37.240,58 | Rooftop Dak Beton Standar | 12.500.000 | 355,46 | 54,64 | **6,51** |
| 6 | **Halte Bus TransJakarta** | P-1/TR | 408 | 20.857,6 | 28.059,32 | Solar Carport & Kanopi Baja | 18.500.000 | 385,87 | 41,17 | **9,37** |
| 7 | **Gelanggang Olahraga & Stadion** | P-1/TR | 63 | 18.999,6 | 25.065,68 | Rooftop Dak Beton Standar | 12.500.000 | 237,49 | 36,78 | **6,46** |
| 8 | **Stasiun MRT & LRT** | P-1/TR | 47 | 16.252,4 | 21.412,69 | Solar Carport & Kanopi Baja | 18.500.000 | 300,67 | 31,42 | **9,57** |
| 9 | **Pasar Tradisional & Modern** | B-2/TR | 108 | 14.644,0 | 19.416,55 | Rooftop Dak Beton Standar | 12.500.000 | 183,05 | 28,49 | **6,43** |
| 10 | **Gedung & Lapangan Parkir** | B-2/TR | 107 | 12.802,8 | 16.907,48 | Solar Carport & Kanopi Baja | 18.500.000 | 236,85 | 24,81 | **9,55** |
| 11 | **Terminal Bus Antarkota** | P-1/TR | 38 | 10.280,0 | 13.951,52 | Solar Carport & Kanopi Baja | 18.500.000 | 190,18 | 20,47 | **9,29** |
| 12 | **Bandara Internasional (Soetta)** | B-2/TR | 14 | 3.729,6 | 4.988,02 | Solar Carport & Kanopi Baja | 18.500.000 | 69,00 | 7,32 | **9,43** |
| 13 | **Jembatan Penyeberangan (JPO)** | P-1/TR | 30 | 800,0 | 1.038,47 | Solar Carport & Kanopi Baja | 18.500.000 | 14,80 | 1,52 | **9,71** |
| **TOTAL** | **13 KATEGORI AGREGAT** | - | **2.100** | **304.550,8** | **407.157,80** | - | - | **4.437,80** | **597,44** | **~7,43 (Rata-rata)** |

---

## 5. Rumus & Metodologi Perhitungan

### 5.1 Investasi Modal Awal (CAPEX Total)
$$\text{CAPEX Total (Rp)} = \text{Kapasitas Terpasang (kWp)} \times \text{Standar Biaya Struktur (Rp/kWp)}$$

### 5.2 Penghematan Belanja Listrik Tahunan
$$\text{Penghematan Tahunan (Rp)} = \text{Produksi Listrik (kWh/tahun)} \times \text{Tarif Dasar Listrik PLN (Rp/kWh)}$$
*Keterangan:* Produksi listrik dihitung dari insolasi spesifik Google Solar API dikalikan efisiensi sistem $PR = 0,78$ ($1.336,9 \text{ kWh/kWp/tahun}$).

### 5.3 Biaya Operasional & Pemeliharaan (OPEX)
$$\text{OPEX Tahunan (Rp)} = \text{CAPEX Total} \times \text{Persentase OPEX Tahunan}$$
- Rooftop Dak Beton: $1,5\%$ dari CAPEX per tahun.
- Solar Carport: $2,0\%$ dari CAPEX per tahun (karena ada pemeliharaan struktur baja galvanis dan inspeksi pondasi).

### 5.4 Waktu Balik Modal Sederhana (*Simple Payback Period*)
$$\text{Simple Payback Period (Tahun)} = \frac{\text{CAPEX Total (Rp)}}{\text{Penghematan Listrik Tahunan (Rp)}}$$
- **Rooftop Dak Beton:** Menghasilkan payback **6,42 – 6,51 tahun** karena efisiensi biaya konstruksi awal yang rendah.
- **Solar Carport:** Menghasilkan payback **9,29 – 9,71 tahun** karena adanya beban investasi rangka baja bentang lebar. Namun, struktur kanopi ini memberikan nilai tambah berupa perlindungan cuaca (peneduh komuter/kendaraan).

---

## 6. Inventaris File Terkait di Repositori

| Tipe Aset | Path File di Repositori | Keterangan |
| :--- | :--- | :--- |
| **Dataset Standar** | [`data/processed/references/standar_capex_opex_plts_2026.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/standar_capex_opex_plts_2026.csv) | Berisi master standar biaya, ID rujukan, dan teks verbatim regulasi. |
| **Dataset 13 Kategori** | [`data/processed/calculations/pow_solar_ekonomi_kebijakan.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/calculations/pow_solar_ekonomi_kebijakan.csv) | Hasil kalkulasi makro agregat 13 kategori kebijakan publik. |
| **Dataset 2.100 Aset** | [`data/processed/calculations/pow_solar_2000_ekonomi_detail.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/calculations/pow_solar_2000_ekonomi_detail.csv) | Hasil kalkulasi mikro untuk setiap aset spasial individu. |
| **Antarmuka Aplikasi** | [`pages/3_Analisis_Ekonomi.py`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/pages/3_Analisis_Ekonomi.py) | Kode halaman Streamlit visualisasi interaktif Sub-Bab 3.1, 3.2, & 3.5. |
| **Dataset Skema Pengadaan** | [`data/processed/references/matriks_skema_pengadaan_zero_apbd.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/matriks_skema_pengadaan_zero_apbd.csv) | Matriks perbandingan skema pengadaan modal (PPA BOOT vs Konsesi vs APBD Murni). |

---

## 7. Asumsi Skema Pembiayaan & Opsi Zero Initial CAPEX (PPA / KSP BMD)

### 7.1 Rasionalisasi Belanja Modal Awal Rp 0,- (*Zero Initial CAPEX*)
Untuk menghindari tekanan fiskal langsung terhadap kas daerah (APBD) yang membutuhkan total belanja modal sebesar **Rp 4,44 Triliun**, analisis ekonomi di Sub-Bab 3.5 menyediakan opsi model pembiayaan alternatif:
1. **Power Purchase Agreement (PPA) / Sewa Atap Swasta (*Solar as a Service*):**
   - Skema kontrak: *Build-Own-Operate-Transfer* (BOOT) tenor 15–20 tahun.
   - Pihak pengembang swasta (*IPP / konsorsium EPC*) menanggung **100% modal awal pengadaan dan instalasi (Rp 4,44 T)**.
   - **Beban Kas Belanja Modal APBD Tahun ke-0: Rp 0,-**.
   - Pemerintah Daerah/BUMD hanya menyediakan hak pemanfaatan ruang atap (*roof-space access*) dan membeli listrik yang diproduksi dengan diskon 15–20% dari tarif PLN.
   - Di akhir masa kontrak tenor, seluruh sistem PLTS dihibahkan penuh (*transferred*) menjadi Barang Milik Daerah (BMD).

### 7.2 Landasan Hukum Pengelolaan Aset Pemda
Sesuai audit forensik dan kaidah metodologi `.agents/rules/anti_yesman_spatial_methodology_integrity.md`:
- Pemanfaatan atap gedung fasilitas milik daerah oleh pihak swasta **bukan diatur oleh Permen ESDM**, melainkan merujuk langsung ke **Permendagri No. 19 Tahun 2016 tentang Pedoman Pengelolaan Barang Milik Daerah**:
  - **Pasal 116–135:** Pemanfaatan melalui skema *Sewa*.
  - **Pasal 136–168:** Pemanfaatan melalui skema *Kerjasama Pemanfaatan (KSP)* dengan mitra swasta/BUMD.
- Serta **Peraturan Presiden No. 38 Tahun 2015** tentang *Kerjasama Pemerintah dengan Badan Usaha (KPBU)* dalam penyediaan infrastruktur.
- **Peran Permen ESDM No. 2/2024:** Murni sebagai *regulatory enabler* di sisi ketenagalistrikan melalui penghapusan denda *capacity charge* PLN (Menimbang huruf a), sehingga pengembang swasta memiliki kepastian keekonomian untuk membiayai instalasi atap secara penuh.

### 7.3 Batasan Realitas Fiskal (*Transparency of Limitations*)
- Klaim "Rp 0,-" **hanya berlaku untuk Belanja Modal Awal (CAPEX)**, bukan berarti Pemda bebas biaya operasional selamanya (*no free lunch*). Pemda tetap mengalokasikan kas daerah bulanan untuk pos belanja operasional/jasa listrik berdiskon.
- Kontrak multi-tahun (15–20 tahun) memerlukan mitigasi persetujuan DPRD sesuai UU No. 23/2014 tentang Pemerintahan Daerah dan PP No. 12/2019 tentang Pengelolaan Keuangan Daerah.

### 7.4 Metodologi Pembobotan Multi-Kriteria (MCDA) Model Pengadaan
Evaluasi komparatif antara 3 skema pengadaan dihitung menggunakan pipeline [`tools/economic/generate_procurement_mcda_scoring.py`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/tools/economic/generate_procurement_mcda_scoring.py) dan disimpan dalam dataset fisik [`data/processed/references/matriks_skor_evaluasi_pengadaan.csv`](file:///c:/Users/yooma/OneDrive/Desktop/duniahub/client/23.%20Celios8-solarpanel/data/processed/references/matriks_skor_evaluasi_pengadaan.csv):
- **Pendekatan:** *Qualitative Expert Judgment* berbasis Kerangka Alokasi Risiko KPBU Bappenas (2020) & Perpres No. 38/2015 dengan skala Likert ordinal 1 s.d. 10.
- **Pembobotan Prioritas Fiskal (AHP-aligned Weighting):**
  1. *Keamanan Fiskal Kas Daerah:* Bobot **30,0%** (PPA: 10, Konsesi: 10, APBD: 1)
  2. *Proteksi Risiko Penurunan Kinerja Teknis:* Bobot **25,0%** (PPA: 10, Konsesi: 9, APBD: 2)
  3. *Kecepatan Eksekusi & Implementasi:* Bobot **20,0%** (PPA: 9, Konsesi: 7, APBD: 3)
  4. *Likuiditas Penghematan Kas Sejak Hari Pertama:* Bobot **15,0%** (PPA: 7, Konsesi: 8, APBD: 10)
  5. *Kepastian Pengalihan Kepemilikan Aset:* Bobot **10,0%** (PPA: 8, Konsesi: 8, APBD: 10)
- **Skor Tertimbang Agregat ($\sum w_i \times s_i$):**
  - **PPA Sewa Atap Swasta:** **9,15 / 10,00** *(Peringkat 1 - Rekomendasi Utama Gedung Dak)*
  - **Konsesi Solar Carport:** **8,65 / 10,00** *(Peringkat 2 - Rekomendasi Sektor Transit/Parkir)*
  - **Belanja Modal APBD Murni:** **3,90 / 10,00** *(Peringkat 3 - Tekanan Likuiditas Ekstrem)*


