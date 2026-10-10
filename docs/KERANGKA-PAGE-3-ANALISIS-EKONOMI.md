# Kerangka Desain & Struktur Analisis Riset (Page 3)
## CELIOS8: Analisis Ekonomi Kebijakan Publik & Kelayakan Fiskal PLTS Atap Jabodetabek
**Dokumen Referensi:** `docs/KERANGKA-PAGE-3-ANALISIS-EKONOMI.md`  
**Target Implementasi:** `pages/3_Analisis_Ekonomi.py`  
**Standar Gaya Riset:** 100% Mengadopsi Standar Riset CELIOS 2 (ECC / D3TLH) — Pendekatan Ekonomi Kebijakan Publik (*Public Policy & Macro-Fiscal Framework*)  
**Kepatuhan Regulasi:** Mematuhi 5 Agent Rules (`no_hardcoded_data`, `anti_yesman_spatial_methodology_integrity`, `statistical_auditor_role`, `strict_data_folder_boundary`, `never_use_destructive_commands`)  
**Penomoran Bab:** Hierarkis Standar Bab 3 (3.1, 3.2, 3.3, 3.4, 3.5)  

---

## 1. Ringkasan Visi & Pendekatan Halaman

Halaman **"Analisis Ekonomi Kebijakan Publik & Kelayakan Fiskal"** bertindak sebagai **pilar pembuktian kelayakan praktis (*policy feasibility*)** dalam Triple-Benefits Framework CELIOS (*Ekonomi, Lingkungan, Sosial*). Halaman ini mentransformasi potensi energi fisik hasil kalkulasi satelit pada Page 1 dan Page 2 ($\text{MWp}$ dan $\text{GWh/tahun}$) menjadi **narasi dampak ekonomi makro dan dividen sosial yang mudah dipahami oleh pembuat kebijakan, media massa, dan masyarakat umum**.

### Mengapa Pendekatan Ekonomi Kebijakan Publik Dipilih (Bukan Corporate Project Finance)?
Dalam tradisi riset advokasi CELIOS, presentasi ekonomi di hadapan publik dan pemangku kepentingan daerah (DPRD, Dinas Perhubungan, Bappenas) **tidak boleh terjebak dalam kerumitan rumus perbankan mikro korporat** (*WACC, Discounted Cash Flow 25 tahun, terminal value, dan depresiasi inverter*) yang rawan menjadi polemik teknis berbelit-belit. 

Sebaliknya, halaman ini fokus menjawab **3 pertanyaan kunci pembuat kebijakan dan media**:
1. **Berapa modal investasinya dan berapa penghematan belanja listrik tahunannya?** (Neraca Makro & Titik Impas Sederhana).
2. **Uang hemat tersebut setara dengan membiayai apa saja untuk masyarakat?** (*Fiscal Dividend / Opportunity Cost* — subsidi komuter, operasional puskesmas, beasiswa).
3. **Bagaimana Pemda bisa mengeksekusi jika kas APBD terbatas?** (Solusi pengadaan *Zero-APBD* via skema PPA/sewa atap pihak ketiga).

---

## 2. Struktur Visual & Komponen Antarmuka (UI/UX CELIOS)

Mengadopsi komponen antarmuka yang terbukti tangguh pada CELIOS 2:
1. **Org Badge Institusi:** `CELIOS — Center of Economic and Law Studies`
2. **Main Title Gradien Hijau:** `Analisis Ekonomi Kebijakan Publik`
3. **Sub-Title Analitis:** Menjelaskan cakupan investasi makro, penghematan belanja operasional, dividen fiskal daerah, dan penciptaan lapangan kerja hijau se-Jabodetabek.
4. **Dropdown Metodologi Transparan:** Mengurai alur kausalitas ekonomi publik, variabel $X$ dan $Y$, serta metode perhitungan baku (Pengali Ketenagakerjaan Hijau IRENA/IESR dan Standar Biaya Layanan Publik BPS/Kemendagri).
5. **Hero Statement (Narasi Kritis Utama):** Paragraf pembuka tajam yang membantah mitos "transisi energi adalah beban APBD".
6. **Bento Metric Cards (6 Indikator Kebijakan Publik):** Nilai moneter dan dampak sosial riil dengan warna fungsional dan baris sitasi file fisik sumber di `data/`.
7. **Struktur Sub-Bab 3.1 s.d. 3.5:** Setiap sub-bab mengikuti ritme: *Tesis Advokasi ➔ Visualisasi Komparatif ➔ Kotak Fakta Data & Interpretasi Kritis ➔ Expander Data Mentah CSV*.

---

## 3. Rincian Hierarkis Sub-Bab (Penomoran 3.1, 3.2, 3.3, 3.4, 3.5)

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                        BAGIAN HEADER & METODOLOGI UTAMA (TOP-LEVEL)                              |
|  • Org Badge: CELIOS — Center of Economic and Law Studies                                        |
|  • Main Title: Analisis Ekonomi Kebijakan Publik PLTS Atap                                       |
|  • Sub-Title: Evaluasi Investasi Makro, Efisiensi Belanja Daerah, dan Dividen Sosial Warga       |
|  • Dropdown Metodologi: Alur Kausalitas Kebijakan, Standar Pengali IRENA, Formulasi Baku        |
|  • Hero Statement: Membongkar Mitos "Transisi Energi Mahal" Melalui Pembebasan Ruang Fiskal      |
|  • Bento Metric Cards: 6 Indikator Kunci (Investasi, Hemat Tahunan, Payback, Green Jobs, Dividen)|
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.1: NERACA INVESTASI & PENGHEMATAN BELANJA LISTRIK TAHUNAN                             |
|  3.1.1 Dekomposisi Biaya Modal: Rooftop Dak vs Solar Carport & Kanopi Baja                       |
|  3.1.2 Proyeksi Penghematan Belanja Listrik Tahunan & Periode Balik Modal (Simple Payback)       |
|  • Visualisasi: Grouped Bar & Waterfall Chart: Modal Awal vs Akumulasi Penghematan Listrik       |
|  • Kotak Callout: Fakta Data Titik Impas 6–7 Tahun & 18 Tahun Panen Energi Bebas Biaya           |
|  • Data Lineage: Expander tabel data mentah CAPEX dan penghematan per kategori (CSV)             |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.2: EKUIVALENSI DIVIDEN FISKAL APBD (OPPORTUNITY COST & PUBLIC DIVIDEND)               |
|  3.2.1 Konversi Penghematan Listrik Menjadi Nilai Manfaat Layanan Publik Nyata                   |
|  3.2.2 Pembebasan Ruang Fiskal Daerah (Fiscal Space) Tanpa Menaikkan Pajak Warga                 |
|  • Visualisasi: Infografis Horizontal Bar / Pictogram: Pilihan Alokasi Dividen Belanja Daerah    |
|  • Kotak Callout: Fakta Data Rekomendasi Alokasi Penghematan Listrik untuk Subsidi Komuter       |
|  • Data Lineage: Expander tabel konversi unit biaya layanan publik (CSV)                         |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.3: DAMPAK PENCIPTAAN LAPANGAN KERJA HIJAU (GREEN JOBS MULTIPLIER)                     |
|  3.3.1 Kuantifikasi Serapan Tenaga Kerja Lokal (Fase Konstruksi vs Fase Operasional 25 Tahun)    |
|  3.3.2 Distribusi Penyerapan Tenaga Kerja per Klaster Infrastruktur (Rangka Baja, Teknisi PV)    |
|  • Visualisasi: Stacked Bar Chart Penyerapan Tenaga Kerja Hijau per Kategori Fasilitas           |
|  • Kotak Callout: Fakta Data Multiplier Lapangan Kerja Lokal Transisi Energi Berkeadilan         |
|  • Data Lineage: Expander tabel pengali ketenagakerjaan hijau IRENA / IESR (CSV)                 |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.4: MATRIKS PRIORITAS INVESTASI: KLASTER FASILITAS PALING STRATEGIS                    |
|  3.4.1 Kuadran Prioritas: Quick Wins (Mall/Parkir) vs Pelayanan Publik (RS/Sekolah/Stasiun)      |
|  3.4.2 Peta Jalan Pentahapan Implementasi Pemda (Tahap 1 Quick Wins ➔ Tahap 2 Skalasi Penuh)    |
|  • Visualisasi: Scatter / Bubble Chart Kuadran Prioritas (Payback vs Dampak Publik)              |
|  • Kotak Callout: Panduan Bertindak Kepala Daerah untuk Menghindari Beban Anggaran Sekaligus     |
|  • Data Lineage: Expander tabel matriks prioritas 13 kategori infrastruktur (CSV)                |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.5: SOLUSI PENGADAAN "ZERO-APBD" (MEMBONGKAR ALIBI KETERBATASAN KAS DAERAH)            |
|  3.5.1 Skema PPA / Sewa Atap (Solar as a Service): Swasta Memodali, Pemda Langsung Terima Hemat  |
|  3.5.2 Kemitraan Konsesi Parkir (Carport Solar) & Kerjasama BUMD Transportasi                    |
|  • Visualisasi: Diagram Alur Proses & Perbandingan Beban Fiskal: APBD Murni vs Skema PPA         |
|  • Kotak Callout: Argumen Telak Advokasi CELIOS: Transisi Energi Terkendala Mau, Bukan Uang      |
|  • Data Lineage: Expander tabel perbandingan matriks model pengadaan zero-APBD (CSV)             |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 📌 Ringkasan 5 Sub-Bab Baru (Hierarkis 3.1 s.d. 3.5):

| No Sub-Bab | Topik Pembahasan | Fokus Utama yang Akan Anda Sampaikan |
|:---:|:---|:---|
| **3.1** | **Neraca Investasi & Penghematan Listrik Tahunan** | Menunjukkan perbandingan modal awal vs pemotongan tagihan PLN, dengan titik impas 6–7 tahun dan sisa 18 tahun panen energi gratis. |
| **3.2** | **Ekuivalensi Dividen Fiskal APBD (*Public Dividend*)** | Mengonversi penghematan listrik menjadi manfaat sosial nyata (subsidi tiket transportasi, operasional puskesmas, beasiswa). |
| **3.3** | **Dampak Penciptaan Lapangan Kerja Hijau (*Green Jobs*)** | Menghitung serapan ribuan tenaga kerja lokal pada fase konstruksi dan pemeliharaan jangka panjang. |
| **3.4** | **Matriks Prioritas Investasi Klaster Fasilitas** | Memetakan klaster mana yang cepat balik modal (*Quick Wins* di parkir/mall) vs klaster bernilai pelayanan publik (stasiun, RSUD, sekolah). |
| **3.5** | **Solusi Pengadaan "Zero-APBD"** | Memberikan opsi skema PPA/sewa atap swasta untuk membuktikan bahwa transisi energi tidak terkendala uang, melainkan regulasi dan kemauan politik. |

---

## 4. Uraian Detail Teknis Per Sub-Bab

### Header Halaman & Dropdown Metodologi
* **Alur Kausalitas Metodologis:**
  $$\text{Potensi Energi } (GWh) \ \& \ \text{Tarif PLN} \longrightarrow \text{Investasi \& Penghematan Operasional} \longrightarrow \text{Ekuivalensi Dividen Fiskal APBD} \longrightarrow \text{Penciptaan Green Jobs} \longrightarrow \text{Model Pengadaan Zero-APBD}$$
* **Variabel Masukan Teknis (X):**
  - Total kapasitas terpasang ($kWp$) dan estimasi produksi energi tahunan ($kWh$) hasil validasi satelit Google Solar API.
  - Asumsi standar biaya pengadaan industri EPC Indonesia 2026:
    * *Rooftop Dak Standar:* $\text{Rp 12,5 juta/kWp}$.
    * *Solar Carport & Kanopi Baja:* $\text{Rp 18,5 juta/kWp}$ (memperhitungkan struktur penopang baja galvanis dan fondasi).
  - Tarif Dasar Listrik PLN 2026 (`data/raw/pln/pln_tariff_2026.csv`): Golongan P-1/P-2/P-3 ($\approx \text{Rp 1.444,70 – 1.699,53/kWh}$) dan Golongan B-2/B-3 ($\approx \text{Rp 1.444,70 – 1.467,28/kWh}$).
  - Standar Pengali Ketenagakerjaan Hijau (*Green Jobs Multiplier* IRENA/IESR): $\approx 15\text{ job-years per MWp}$ untuk fase manufaktur/instalasi, dan $\approx 0,8\text{ permanent jobs per MWp}$ untuk operasional dan pemeliharaan (O&M) jangka panjang.
  - Parameter Satuan Biaya Layanan Publik (Data BPS / Pemprov DKI): Biaya operasional Puskesmas Kelurahan, subsidi tarif tiket TransJakarta per penumpang ($\approx \text{Rp 10.000}$ per perjalanan), dan beasiswa siswa per tahun.
* **Variabel Keluaran Kebijakan (Y):**
  - Estimasi Total Kebutuhan Modal Awal ($\text{CAPEX}_{\text{agregat}}$ Triliun Rp).
  - Penghematan Belanja Listrik Tahunan ($\text{OPEX Savings}$ Miliar Rp/tahun).
  - Periode Impas Sederhana (*Simple Payback Period* dalam tahun).
  - Dividen Sosial Fiskal: Jumlah perjalanan penumpang bersubsidi, jumlah unit puskesmas terdanai, jumlah beasiswa siswa.
  - Total Serapan Tenaga Kerja Hijau (*Green Jobs* dalam orang-tahun / pekerja tetap).
* **Standar Perhitungan Baku (Tanpa Scratch Math Liar):**
  - Formulasi Biaya Modal Agregat: $\text{CAPEX} = \sum (\text{Kapasitas\_kWp}_i \times \text{Standar\_Biaya}_i)$
  - Formulasi Penghematan Belanja Listrik: $\text{Hemat} = \text{Produksi\_kWh} \times \text{Tarif\_PLN}$
  - Formulasi Periode Impas: $\text{Payback} = \frac{\text{CAPEX}}{\text{Hemat Tahunan}}$
  - Formulasi Tenaga Kerja Hijau (Standar IRENA): $\text{Jobs} = \text{Kapasitas\_MWp} \times \text{Multiplier\_Jobs}$

---

### Hero Statement (Narasi Kritis Utama)
* **Pola Narasi:**
  Mengintegrasikan angka makro moneter dengan dividen sosial secara dinamis:
  > *"Pemerintah daerah dan operator transportasi perkotaan kerap menunda transisi energi dengan dalih keterbatasan anggaran belanja modal (CAPEX). Namun, temuan empiris pada 2.000 titik infrastruktur Jabodetabek membuktikan bahwa kebutuhan investasi sebesar **`{total_capex_triliun}` Triliun Rupiah** akan memangkas belanja rutin tagihan listrik sebesar **`{total_savings_miliar}` Miliar Rupiah setiap tahun**. Dengan periode impas rata-rata **`{avg_payback_years}` tahun**, proyek ini menghasilkan sisa 18 tahun masa panen energi gratis yang setara dengan mendanai **`{commuter_subsidy_pax:,}` perjalanan komuter bersubsidi** atau biaya operasional **`{puskesmas_funded_count:,}` unit Puskesmas Kelurahan**. Pemasangan PLTS Atap bukan beban fiskal APBD, melainkan pembebasan ruang belanja daerah secara permanen untuk dialihkan ke pelayanan dasar warga."*

---

### Bento Metric Cards (6 Indikator Kebijakan Publik)
1. **Total Kebutuhan Investasi:** `{total_capex_triliun}` Triliun Rp (`#4CAF50` Hijau Investasi). Sumber: `pow_solar_ekonomi_kebijakan.csv`.
2. **Penghematan Belanja Listrik:** `{total_savings_miliar}` Miliar Rp/thn (`#66BB6A` Hijau Terang). Sumber: `pow_solar_ekonomi_kebijakan.csv`.
3. **Periode Balik Modal Rata-Rata:** `{avg_payback_years}` Tahun (`#FFA726` Emas Impas). Simple Payback Industri.
4. **Penciptaan Lapangan Kerja Hijau:** `{total_green_jobs:,}` Pekerja Hijau (`#42A5F5` Biru Lapangan Kerja). Standar Multiplier IRENA/IESR.
5. **Dividen Subsidi Tiket Komuter:** `{commuter_subsidy_pax:,}` Perjalanan/thn (`#26A69A` Hijau Toska). Ekuivalensi Beban APBD.
6. **Beban Likuiditas APBD:** `Rp 0,- (Zero-APBD)` (`#AB47BC` Ungu Kebijakan). Opsi Skema PPA / Sewa Atap Swasta.

---

### 3.1 Neraca Investasi & Penghematan Belanja Listrik Tahunan
* **3.1.1 Dekomposisi Biaya Modal: Rooftop Dak vs Solar Carport & Kanopi Baja:**
  - Menjelaskan perbedaan biaya teknis pengadaan secara transparan:
    * **Rooftop Dak Beton (RSUD, Sekolah, Kampus, Mall, Pasar):** Biaya rata-rata $\approx \text{Rp 12,5 juta/kWp}$. Murah karena struktur atap dak sudah kokoh dan hanya membutuhkan penopang rel aluminium standar.
    * **Solar Carport & Kanopi Baja (Lapangan Parkir Terbuka, Halte Busway, Terminal):** Biaya rata-rata $\approx \text{Rp 18,5 juta/kWp}$. Lebih tinggi karena mencakup konstruksi rangka baja bentang lebar, fondasi anti-angin, dan peninggian struktur agar kendaraan bebas bermanuver.
* **3.1.2 Proyeksi Penghematan Belanja Listrik Tahunan & Periode Balik Modal:**
  - Mengalikan output energi tahunan ($kWh$) dengan Tarif Dasar Listrik PLN 2026.
  - Menghitung periode impas rata-rata portofolio selama **6,5 – 7,5 tahun**.
  - Menggarisbawahi fakta bahwa panel surya memiliki masa garansi kinerja 25 tahun, yang berarti fasilitas publik menikmati **17–18 tahun listrik tanpa biaya energi (bebas tagihan)** setelah titik impas terlewati.
* **Visualisasi:** Grouped Bar Chart Dekomposisi CAPEX per Kategori & Waterfall Chart: Modal Awal vs Garis Akumulasi Penghematan Belanja Listrik (Tahun 1 s.d. 25).
* **Kotak Interpretasi:**
  - `Fakta Data:` Pemasangan kanopi surya pada halte dan parkiran komuter mencapai titik impas pada tahun ke-7.
  - `Interpretasi Kebijakan:` Membeli listrik dari PLN adalah biaya hangus (*sunk cost*) seumur hidup tanpa aset, sedangkan PLTS atap mengubah tagihan rutin bulanan menjadi aset produktif daerah yang menghasilkan keuntungan bersih selama 18 tahun.
* **Data Lineage:** Expander tabel rincian CAPEX dan penghematan per kategori dari `pow_solar_ekonomi_kebijakan.csv`.

---

### 3.2 Ekuivalensi Dividen Fiskal APBD (*Opportunity Cost & Public Dividend*)
* **3.2.1 Konversi Angka Hemat Menjadi Nilai Manfaat Layanan Publik Nyata:**
  - Menerjemahkan angka miliaran rupiah penghematan tagihan listrik PLN menjadi dampak sosial konkret yang menyentuh masyarakat bawah:
    * **Opsi Alokasi 1 (Subsidi Tiket Komuter):** Penghematan listrik stasiun dan halte dialihkan untuk menutup subsidi tarif integrasi TransJakarta/KRL bagi ratusan ribu komuter berpenghasilan rendah.
    * **Opsi Alokasi 2 (Kesehatan Masyarakat):** Penghematan listrik fasilitas RSUD dialihkan untuk membiayai operasional puluhan Puskesmas Pembantu di kawasan padat kumuh.
    * **Opsi Alokasi 3 (Pendidikan & Beasiswa):** Penghematan listrik atap sekolah negeri dialihkan untuk beasiswa perlengkapan sekolah anak-anak keluarga pra-sejahtera.
* **3.2.2 Pembebasan Ruang Fiskal Daerah (*Fiscal Space Expansion*):**
  - Menunjukkan bahwa penghematan belanja rutin operasional gedung daerah secara efektif memperluas ruang fiskal Pemprov DKI dan Pemda Bodetabek tanpa perlu menaikkan tarif pajak daerah atau retribusi warga.
* **Visualisasi:** Pictogram Chart / Horizontal Bar Chart Interaktif: Pilihan Skenario Konversi Dividen Fiskal (Jumlah Tiket Bersubsidi vs Unit Puskesmas vs Beasiswa Siswa).
* **Kotak Interpretasi:**
  - `Fakta Data:` Penghematan belanja listrik agregat dari 2.000 titik mampu membiayai subsidi transportasi publik untuk jutaan perjalanan komuter setiap tahunnya.
  - `Interpretasi Advokasi CELIOS:` Transisi energi bukan sekadar isu teknis dekarbonisasi, melainkan instrumen redistribusi keadilan sosial yang mengembalikan uang rakyat dalam bentuk peningkatan layanan dasar publik.
* **Data Lineage:** Expander tabel asumsi biaya satuan layanan publik dari `data/processed/references/standar_biaya_layanan_publik.csv`.

---

### 3.3 Dampak Penciptaan Lapangan Kerja Hijau (*Green Jobs Creation*)
* **3.3.1 Kuantifikasi Serapan Tenaga Kerja Lokal Transisi Energi:**
  - Menerapkan metodologi resmi International Renewable Energy Agency (IRENA) dan Institute for Essential Services Reform (IESR):
    * **Fase Konstruksi & Fabrikasi (Tahun 1–2):** Menyerap tenaga kerja lokal dalam jumlah besar untuk perakitan struktur baja kanopi, pemasangan bracket, instalasi elektrikal, dan sertifikasi laik operasi.
    * **Fase Pemeliharaan & Operasi (Tahun 1–25):** Menciptakan lapangan kerja permanen untuk tim teknisi O&M, operator monitoring sistem cerdas, dan petugas pembersihan berkala panel surya.
* **3.3.2 Distribusi Penyerapan Kerja per Klaster Infrastruktur:**
  - Klaster lapangan parkir terbuka dan halte transit menyerap proporsi tenaga kerja fabrikasi baja dan konstruksi sipil terbesar di kawasan aglomerasi.
* **Visualisasi:** Stacked Bar Chart: Distribusi Lapangan Kerja Konstruksi (Short-term) vs Pemeliharaan Permanen (Long-term) per Kategori Infrastruktur.
* **Kotak Interpretasi:**
  - `Fakta Data:` Potensi PLTS pada 2.000 titik menciptakan ribuan lapangan kerja hijau langsung di wilayah Bodetabek dan DKI Jakarta.
  - `Interpretasi Ketenagakerjaan:` Proyek ini membuktikan tesis *Just Energy Transition*: peralihan ke energi bersih di perkotaan membuka lapangan kerja teknis bagi lulusan SMK/Politeknik lokal, mengurangi angka pengangguran muda perkotaan.
* **Data Lineage:** Expander tabel perhitungan multiplier tenaga kerja dari `pow_solar_green_jobs_multiplier.csv`.

---

### 3.4 Matriks Prioritas Investasi: Klaster Fasilitas Paling Strategis
* **3.4.1 Kuadran Prioritas Implementasi (Matriks 3 Kuadran):**
  - **Kuadran 1: Cepat Balik Modal (*Quick Wins*):**
    * *Fasilitas:* Gedung Parkir Bertingkat (MSCP) dan Pusat Perbelanjaan/Mall.
    * *Karakteristik:* Dak beton sudah datar, konsumsi listrik AC siang hari sangat tinggi $\rightarrow$ periode impas tercepat ($< 5,5\text{ tahun}$).
  - **Kuadran 2: Dividen Pelayanan Publik & Edukasi Warga:**
    * *Fasilitas:* RSUD, Gedung Kampus, dan Sekolah Menengah Negeri.
    * *Karakteristik:* Balik modal moderat ($6,0 – 7,5\text{ tahun}$), memangkas langsung pos APBD pendidikan dan kesehatan, serta menjadi sarana edukasi generasi muda.
  - **Kuadran 3: Visibilitas Tinggi & Perlindungan Komuter:**
    * *Fasilitas:* Halte TransJakarta, Stasiun KRL/LRT, dan Terminal Bus.
    * *Karakteristik:* Butuh struktur kanopi baja (balik modal $7,5 – 8,5\text{ tahun}$), namun memberikan manfaat ganda (*co-benefits*) peneduh cuaca ekstrem bagi jutaan komuter harian.
* **3.4.2 Peta Jalan Pentahapan Implementasi Pemda:**
  - Tahap 1 (Tahun 1): Eksekusi klaster *Quick Wins* dan fasilitas percontohan BUMD.
  - Tahap 2 (Tahun 2–3): Ekspansi massal ke seluruh simpul transportasi dan sekolah/RSUD.
* **Visualisasi:** Scatter Plot / Bubble Chart Kuadran Prioritas (Sumbu X: Waktu Balik Modal Tahun, Sumbu Y: Dampak Kemanfaatan Publik, Ukuran Bubble: Kapasitas MWp).
* **Kotak Interpretasi:**
  - `Fakta Data:` Gedung parkir komersial dan mall adalah mesin penghematan tercepat, sedangkan halte transit adalah etalase edukasi publik terbaik.
  - `Interpretasi Strategis Pemda:` Kepala daerah disarankan memulai dari klaster *Quick Wins* agar bukti penghematan langsung terlihat dalam laporan pertanggungjawaban APBD tahun pertama.
* **Data Lineage:** Expander tabel matriks kuadran 13 kategori infrastruktur.

---

### 3.5 Solusi Pengadaan "Zero-APBD" (Membongkar Alibi Keterbatasan Kas Daerah)
* **3.5.1 Skema PPA / Sewa Atap (*Solar as a Service*): Solusi Tanpa Utang & Tanpa APBD:**
  - Menjawab keberatan klasik pejabat birokrasi daerah: *"APBD kami sedang defisit, dari mana uangnya?"*
  - **Mekanisme Skema PPA (Power Purchase Agreement):**
    1. Perusahaan pengembang surya swasta (*Solar Developer/EPC*) menanggung **100% modal awal pengadaan, konstruksi, dan asuransi**.
    2. Pemda atau operator transportasi (TransJakarta/KAI) hanya menyediakan ruang atap halte/stasiun yang selama ini menganggur.
    3. Fasilitas publik langsung membeli listrik surya dari pengembang dengan **tarif diskon 15–20% lebih murah dari tarif PLN** sejak hari pertama operasi.
    4. Setelah masa kontrak sewa atap selesai (misal 15–20 tahun), seluruh kepemilikan aset panel surya diserahkan gratis (*transfer of ownership*) menjadi aset milik Pemda.
* **3.5.2 Kemitraan Konsesi Parkir (Solar Carport) & Kerjasama BUMD:**
  - Pengelola swasta membiayai kanopi peneduh parkir dan SPKLU pengisian daya mobil/motor listrik, ditukar dengan hak bagi hasil retribusi parkir ramah lingkungan.
* **Visualisasi:** Diagram Alur Proses Interaktif (Infografis Skema Aliran Uang & Tanggung Jawab: APBD Murni vs Skema PPA Swasta) & Bar Komparasi Beban Kas Daerah.
* **Kotak Interpretasi:**
  - `Fakta Data:` Skema PPA memangkas pengeluaran kas modal daerah menjadi **Rp 0,-** sekaligus langsung mengamankan efisiensi tagihan listrik sejak bulan pertama.
  - `Interpretasi Advokasi Pamungkas CELIOS:` Fakta ini membuktikan bahwa mandeknya transisi energi di Jabodetabek **bukan karena ketiadaan anggaran daerah, melainkan karena ketiadaan regulasi dan kemauan politik (*political will*)**. Solusi pasar dan inovasi pembiayaan telah tersedia untuk dieksekusi tanpa risiko fiskal.
* **Data Lineage:** Expander tabel komparasi model pengadaan zero-APBD.

---

## 5. Pemetaan Sumber Data Sub-Bab 3.1 s.d. 3.5 (Audit Ketergantungan Data)

| Sub-Bab | Topik Pembahasan | Status Google Solar API | Sumber Pendukung Non-Solar API | Status Ketersediaan Lokal di Repositori |
|:---|:---|:---:|:---|:---|
| **3.1** | **Neraca Modal & Penghematan Tahunan** | 🟡 **Hibrida**<br>(Kapasitas kWp & Yield kWh) | **Standar Biaya EPC Indonesia & Tarif PLN 2026** | 🟢 **Sudah Lengkap di Repositori**<br>Baseline kWp/kWh di `pow_solar_kumulatif_summary.csv`; tarif dasar listrik di `data/raw/pln/pln_tariff_2026.csv`. |
| **3.2** | **Ekuivalensi Dividen Fiskal APBD** | 🔴 **Bukan Solar API**<br>(Output penghematan Rp dikonversi) | **Data Terbuka Pemprov DKI & BPS (Biaya Layanan Publik)** | 🟡 **Perlu File Rujukan Terstruktur**<br>Standar tarif subsidi TransJakarta (~Rp 10.000/tiket) dan biaya operasional Puskesmas dibukukan ke CSV `standar_biaya_layanan_publik.csv`. |
| **3.3** | **Dampak Lapangan Kerja Hijau** | 🔴 **Bukan Solar API**<br>(Kapasitas MWp dikalikan multiplier) | **Studi Multiplier Ketenagakerjaan IRENA & IESR** | 🟢 **Sudah Lengkap di Literatur**<br>Faktor pengali resmi 15 job-years/MWp (konstruksi) dan 0,8 jobs/MWp (O&M) dibukukan ke CSV `pow_solar_green_jobs_multiplier.csv`. |
| **3.4** | **Matriks Prioritas Investasi** | 🟡 **Hibrida**<br>(Atribut Kategori & Hasil 3.1) | **Hasil Analisis Pengelompokan Klaster Kebijakan** | 🟢 **Dapat Dihitung Otomatis**<br>Diturunkan langsung dari tabel gabungan 13 kategori infrastruktur. |
| **3.5** | **Solusi Pengadaan Zero-APBD (PPA)** | 🔴 **Bukan Solar API**<br>(Analisis Kebijakan & Regulasi) | **Peraturan Menteri ESDM No. 2/2024 & Praktik Terbaik PPA Komersial** | 🟢 **Sudah Lengkap di Literatur**<br>Matriks model PPA versus APBD dibukukan ke `matriks_skema_pengadaan_zero_apbd.csv`. |

---

## 6. Pemetaan Tabel Data yang Perlu Dihimpun (Data Acquisition Mapping)

Mematuhi aturan `no_hardcoded_data.md` dan `strict_data_folder_boundary.md`, seluruh asumsi biaya dan multiplier wajib tersimpan di file fisik:

### A. Tabel Data yang Dihasilkan / Disediakan ke `data/processed/`

| No | Nama Dataset Target | Kategori Data | Dokumen Sumber Resmi | Rencana File Ekstraksi CSV | Struktur Kolom Utama | Kegunaan Spesifik di Page 3 |
|:---:|:---|:---:|:---|:---|:---|:---|
| **1** | **Ringkasan Ekonomi Kebijakan PLTS** | Olahan Finansial Makro | Pipa gabungan Solar API + Tarif PLN 2026 | `data/processed/calculations/pow_solar_ekonomi_kebijakan.csv` | • `category`<br>• `total_kwp`<br>• `total_annual_mwh`<br>• `capex_total_miliar`<br>• `savings_annual_miliar`<br>• `simple_payback_years`<br>• `green_jobs_count` | Menopang Hero Metrics dan Sub-Bab **3.1**, **3.3**, dan **3.4**. |
| **2** | **Standar Biaya Layanan Publik Jabodetabek** | Data Pemda / BPS | Laporan Akuntabilitas Kinerja Pemprov DKI / BPTJ | `data/processed/references/standar_biaya_layanan_publik.csv` | • `jenis_layanan`<br>• `biaya_satuan_rp`<br>• `satuan_layanan`<br>• `sumber_dokumen`<br>• `tahun_anggaran` | Menopang visualisasi infografis dividen sosial pada **Sub-Bab 3.2**. |
| **3** | **Matriks Skema Pengadaan Zero-APBD** | Regulasi & Bisnis | Permen ESDM 2/2024 & Pedoman PPA Asosiasi Solar | `data/processed/references/matriks_skema_pengadaan_zero_apbd.csv` | • `skema_pengadaan`<br>• `beban_kas_daerah`<br>• `tarif_diskon_pct`<br>• `risiko_teknis`<br>• `kecepatan_implementasi` | Menopang diagram alur dan komparasi pada **Sub-Bab 3.5**. |

---

## 7. Checklist Eksekusi Pengembangan

- [x] Kerangka kerja desain Page 3 direfaktor ke pendekatan **Ekonomi Kebijakan Publik & Kelayakan Fiskal** di `docs/KERANGKA-PAGE-3-ANALISIS-EKONOMI.md`.
- [x] Struktur sub-bab dipastikan hierarkis menggunakan penomoran baku **3.1, 3.2, 3.3, 3.4, 3.5**.
- [x] Bahasa penyajian dirancang ramah diseminasi publik, bebas dari jebakan rumus DCF/WACC mikro perbankan.
- [x] Narasi dividen fiskal APBD, penciptaan green jobs, kuadran prioritas, dan skema Zero-APBD diintegrasikan penuh.
- [x] Pemetaan ketergantungan data dan tabel CSV pendukung didokumentasikan transparan (Section 5 & 6).
- [ ] Buat skrip pembentuk tabel data turunan ekonomi di `tools/financial/generate_economic_public_policy.py` untuk menghasilkan `pow_solar_ekonomi_kebijakan.csv` dari `pow_solar_kumulatif_summary.csv` dan `pln_tariff_2026.csv`.
- [ ] Implementasi kode frontend Streamlit di `pages/3_Analisis_Ekonomi.py`.
- [ ] Pengujian visualisasi interaktif dan kompilasi modul.
- [ ] Auto-commit seluruh artefak ke Git repository sesuai aturan keselamatan kode.
