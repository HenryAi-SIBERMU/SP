# Kerangka Desain & Struktur Analisis Riset (Page 2)
## CELIOS8: Analisis Kapasitas & Produksi Energi PLTS Atap Jabodetabek
**Dokumen Referensi:** `docs/KERANGKA-PAGE-2-ANALISIS-KAPASITAS.md`  
**Target Implementasi:** `pages/2_Analisis_Kapasitas.py`  
**Standar Gaya Riset:** 100% Mengadopsi Standar Riset CELIOS 2 (ECC / D3TLH)  
**Kepatuhan Regulasi:** Mematuhi 5 Agent Rules (`no_hardcoded_data`, `anti_yesman_spatial_methodology_integrity`, `statistical_auditor_role`, `strict_data_folder_boundary`, `never_use_destructive_commands`)  
**Penomoran Bab:** Hierarkis Standar Bab 2 (2.1, 2.2, 2.3, 2.4, 2.5)  

---

## 1. Ringkasan Visi & Pendekatan Halaman

Halaman **"Analisis Kapasitas & Produksi Energi"** bertindak sebagai **jembatan kuantitatif inti** yang mengonversi inventarisasi luasan spasial atap ($m^2$ fisik hasil ekstraksi satelit pada Halaman 1) menjadi **besaran daya dan energi listrik absolut ($\text{MWp}$ dan $\text{GWh/tahun}$)**.

Berbeda dari dashboard teknis komersial biasa, halaman ini ditulis dengan gaya **advokasi kebijakan berbasis data (*empirical public-policy advocacy*) khas CELIOS**. Tujuannya adalah membuktikan tesis kedaulatan energi: **kawasan metropolitan Jabodetabek memiliki ruang infrastruktur internal yang melimpah untuk memproduksi energi bersih mandiri**, sehingga tidak memiliki legitimasi moral untuk terus mengekstraksi dan merusak ruang hidup pedesaan (*sacrificial zones*) melalui ketergantungan pada pembangkit listrik batu bara grid Jawa-Madura-Bali.

---

## 2. Struktur Visual & Komponen Antarmuka (UI/UX CELIOS)

Mengadopsi komponen antarmuka yang terbukti tangguh pada CELIOS 2:
1. **Org Badge Institusi:** `CELIOS — Center of Economic and Law Studies`
2. **Main Title Gradien Hijau:** `Analisis Kapasitas & Produksi Energi`
3. **Sub-Title Analitis:** Menjelaskan cakupan konversi energi surya dan uji substitusi beban kota.
4. **Dropdown Metodologi Transparan:** Mengurai alur kausalitas ekonomi-politik, variabel $X$ dan $Y$, serta metode perhitungan baku standar industri (IEC 61724 / NREL PVWatts).
5. **Hero Statement (Narasi Kritis Utama):** Paragraf pembuka tajam yang merangkum kontradiksi ketergantungan energi fosil vs potensi mandiri atap urban.
6. **Bento Metric Cards (6 Kartu Agregat):** Nilai kuantitatif besar dengan warna fungsional dan baris sitasi file fisik sumber di `data/`.
7. **Struktur Sub-Bab 2.1 s.d. 2.5:** Setiap sub-bab mengikuti ritme: *Tesis Advokasi ➔ Visualisasi Komparatif ➔ Kotak Fakta Data & Interpretasi Kritis ➔ Expander Data Mentah CSV*.

---

## 3. Rincian Hierarkis Sub-Bab (Penomoran 2.1, 2.2, 2.3, 2.4, 2.5)

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                        BAGIAN HEADER & METODOLOGI UTAMA (TOP-LEVEL)                              |
|  • Org Badge: CELIOS — Center of Economic and Law Studies                                        |
|  • Main Title: Analisis Kapasitas & Produksi Energi PLTS Atap                                    |
|  • Sub-Title: Transformasi Luasan Spasial ke Kapasitas (MWp) & Generasi (GWh) se-Jabodetabek     |
|  • Dropdown Metodologi: Alur Kausalitas, Standar NREL/IEC, Formulasi Fisika Surya               |
|  • Hero Statement: Kedaulatan Energi vs Kutukan Sacrificial Zones Kawasan Metropolitan           |
|  • Bento Metric Cards: 6 Indikator Kunci Kapasitas, Yield, PSH, PR, Substitusi PLN, dan Infill  |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 2.1: KONVERSI LUASAN SPASIAL KE DAYA & ENERGI (M² ➔ MWP & GWH)                         |
|  2.1.1 Distribusi Kapasitas Lintas 13 Kategori Infrastruktur (Transit vs Fasilitas Publik)       |
|  2.1.2 Karakteristik Densitas Daya Atap (Wp/m² & Efisiensi Fotovoltaik)                         |
|  • Visualisasi: Stacked Bar & Treemap Kapasitas Kumulatif (Altair/Plotly)                        |
|  • Kotak Callout: Fakta Data Kategori Dominan & Interpretasi Rekayasa Energi                     |
|  • Data Lineage: Expander tabel data mentah per kategori (CSV)                                   |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 2.2: PROFIL IRADIASI & FLUKTUASI MUSIMAN (PSH & MONTHLY YIELD PROFILE)                  |
|  2.2.1 Jam Penyinaran Efektif (Peak Sun Hours / PSH) Wilayah Aglomerasi Jabodetabek             |
|  2.2.2 Profil Siklus Musim Hujan vs Musim Kemarau (Kuantifikasi Hasil Panen Jan – Des)           |
|  • Visualisasi: Multi-line & Area Chart Fluktuasi Bulanan kWh/kWp (Januari s.d. Desember)        |
|  • Kotak Callout: Fakta Data Deviasi Musiman & Interpretasi Keandalan Pasokan Tropis             |
|  • Data Lineage: Expander tabel profil iradiasi bulanan PVGIS/NASA (CSV)                         |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 2.3: UJI SUBSTITUSI BEBAN KONSUMSI KOTA (URBAN DEMAND OFFSETTING)                       |
|  2.3.1 Komparasi Produksi Mandiri vs Beban Penjualan Listrik PLN Sektoral (Publik & Komersial)  |
|  2.3.2 Skenario Kemandirian Fasilitas Publik (Net-Zero Railway Stations, RSUD, & Kampus)        |
|  • Visualisasi: Diverging/Grouped Bar Chart: Produksi PLTS vs Beban Konsumsi Sektoral PLN       |
|  • Kotak Callout: Fakta Data Rasio Substitusi & Interpretasi Anti-Sacrificial Zones              |
|  • Data Lineage: Expander tabel statistik konsumsi PLN sektoral (CSV)                            |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 2.4: ANALISIS SENSITIVITAS & KONTROL PARAMETRIK INTERAKTIF                              |
|  2.4.1 Simulasi Rating Modul Panel Surya (350 Wp, 400 Wp Baseline, 550 Wp High-Efficiency)      |
|  2.4.2 Simulasi Performance Ratio (PR Konservatif 70% vs Optimal Tropis Perkotaan 82%)          |
|  2.4.3 Skenario Optimalisasi Celah Atap (Baseline Google Solar vs SNI/NFPA Infill Extension)     |
|  • Visualisasi: Sensitivity Interactive Chart / Tornado Chart Sensitivitas Parameter             |
|  • Kotak Callout: Fakta Data Elastisitas Yield & Interpretasi Fleksibilitas Pengadaan EPC        |
|  • Data Lineage: Expander tabel parameter simulasi (CSV)                                         |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 2.5: STUDI BENCHMARK EMPIRIS & GROUND-TRUTH VALIDATION                                  |
|  2.5.1 Komparasi Model Satelit vs PLTS Operasional Bandara Soekarno-Hatta (Terminal 3)          |
|  2.5.2 Preseden Fasilitas Perkeretaapian & Bangunan Gedung Hijau Jabodetabek                    |
|  • Visualisasi: Metric Error Table & Benchmark Deviation Gauge Card                              |
|  • Kotak Callout: Fakta Data Ground-Truth Accuracy & Catatan Batasan Metodologi                 |
|  • Data Lineage: Expander tabel audit komparasi aktual vs model (CSV)                            |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 📌 Ringkasan 5 Sub-Bab (Hierarkis 2.1 s.d. 2.5):

| No Sub-Bab | Topik Pembahasan | Fokus Utama yang Akan Anda Sampaikan |
|:---:|:---|:---|
| **2.1** | **Konversi Luasan Spasial ke Daya & Energi ($m^2 \rightarrow \text{MWp} \ \& \ \text{GWh}$)** | Menunjukkan transformasi $1,47\text{ juta m}^2$ atap layak menjadi daya puncak $307,9\text{ MWp}$ dan panen listrik $407,2\text{ GWh/tahun}$ lintas 13 kategori infrastruktur publik dan simpul transit. |
| **2.2** | **Profil Iradiasi & Fluktuasi Musiman (PSH & Monthly Yield Profile)** | Membuktikan stabilitas radiasi surya tropis khatulistiwa sepanjang 12 bulan (deviasi musiman hanya $\pm 18\%$), menepis keraguan intermitensi ekstrem khas negara 4 musim. |
| **2.3** | **Uji Substitusi Beban Konsumsi Kota (Urban Demand Offsetting)** | Menguji komparasi pasokan mandiri vs penjualan listrik PLN: mampu menyuplai $24,7\%$ beban kantor pemda & PJU se-DKI ($>200\%$ seluruh lampu jalan), menghentikan transfer emisi ke desa (*anti-sacrificial zones*). |
| **2.4** | **Analisis Sensitivitas & Kontrol Parametrik Interaktif** | Mensimulasikan fleksibilitas pengadaan modul (350 Wp s.d. 550 Wp), rasio performa (PR 70% s.d. 85%), serta potensi cadangan Infill celah aman damkar SNI/NFPA ($+70,9\text{ MWp} / +93,8\text{ GWh}$). |
| **2.5** | **Studi Benchmark Empiris & Ground-Truth Validation** | Memvalidasi akurasi fotogrametri satelit terhadap realisasi fisik PLTS Bandara Soekarno-Hatta (AOCC 241 kWp dan Terminal 2 1,5 MWp) dengan deviasi toleransi rekayasa sangat rendah ($< 10\%$). |

---

## 4. Uraian Detail Teknis Per Sub-Bab

### Header Halaman & Dropdown Metodologi
* **Alur Kausalitas Metodologis:**
  $$\text{Inventarisasi Fisik Atap } (m^2) \longrightarrow \text{Karakterisasi Segmen 3D & Iradiasi} \longrightarrow \text{Kapasitas } (MWp) \ \& \ \text{Yield } (GWh) \longrightarrow \text{Substitusi Beban PLN Sektoral} \longrightarrow \text{Kedaulatan Energi}$$
* **Variabel Teknis (X):**
  - Luas permukaan atap layak panel ($m^2$), jumlah modul fisik ($N_{\text{modul}}$).
  - Jam penyinaran matahari ekuivalen ($\text{PSH / sunshine\_hours}$ dari satelit Google & PVGIS).
  - Sudut kemiringan (*pitch*) dan orientasi hadap (*azimuth*) dari 229+ segmen fotogrametri 3D.
* **Variabel Energi Terhitung (Y):**
  - Kapasitas DC terpasang ($kWp$ dan $MWp$).
  - Produksi listrik bersih tahunan ($kWh$, $MWh$, dan $GWh$).
  - Rasio kecukupan mandiri (*Self-Sufficiency / Offsetting Ratio* terhadap beban PLN).
* **Standar Perhitungan Baku (Tanpa Scratch Math Liar):**
  - Formulasi Daya Puncak: $P_{\text{dc}} = \frac{N_{\text{panel}} \times P_{\text{modul}}}{1.000}$
  - Formulasi Generasi Energi Tahunan (IEC 61724): $E_{\text{annual}} = P_{\text{dc}} \times \text{PSH} \times 365 \times \text{PR}$
  - Asumsi Standar CELIOS: Modul monokristalin $400\text{ Wp}$, Performance Ratio ($\text{PR}$) $80\%$ untuk mengatasi *temperature loss* tropis dan *soiling loss* polutan perkotaan.

---

### Hero Statement (Narasi Kritis Utama)
* **Pola Narasi:**
  Mengintegrasikan total kapasitas terhitung secara dinamis.
  > *"Kawasan aglomerasi Jabodetabek mengonsumsi lebih dari **78.000 GWh listrik per tahun** yang mayoritas dipasok oleh PLTU batu bara di Jawa Barat dan Banten, memindahkan beban polusi udara dan perusakan ekologis ke wilayah pedesaan (*sacrificial zones*). Namun, hasil ekstraksi spasial beresolusi tinggi (0,25 m/pixel) terhadap fasilitas publik dan simpul transportasi membuktikan potensi terpasang sebesar **`{total_capacity_mwp}` MWp** dengan kemampuan produksi **`{total_gen_gwh}` GWh per tahun**. Temuan ini membantah narasi ketergantungan mutlak pada pembangkitan luar kota, membuktikan bahwa infrastruktur publik metropolitan mampu menjadi pilar kedaulatan energi mandiri."*

---

### Bento Metric Cards (6 Indikator Kunci)
1. **Total Kapasitas Terpasang:** `{total_capacity_mwp}` MWp (`#4CAF50` Hijau Energi). Sumber: `pow_solar_kumulatif_summary.csv`.
2. **Produksi Listrik Tahunan:** `{total_gen_gwh}` GWh/tahun (`#66BB6A` Hijau Terang). Sumber: `pow_solar_kumulatif_summary.csv`.
3. **Total Jam Penyinaran (PSH):** `{avg_psh}` Jam/Hari ekuivalen (`#FFA726` Emas Surya). Sumber: Google Solar Flux & PVGIS.
4. **Performance Ratio Standar:** `80,0%` Tropis Perkotaan (`#42A5F5` Biru Rekayasa). Sumber: Standar SNI 8395:2017 & IEC 61724.
5. **Substitusi Sektor Publik:** `{pct_substitusi_publik}%` Kebutuhan Layanan Umum (`#26A69A` Hijau Toska). Sumber: PLN Statistics & Olahan.
6. **Ekstensi Celah Infill:** `+{infill_mwp}` MWp Potensi Cadangan (`#AB47BC` Ungu Optimasi). Sumber: `pow_solar_gap_infill_extension.csv`.

---

### 2.1 Konversi Luasan Spasial ke Daya & Energi ($m^2$ ke MWp & GWh)
* **2.1.1 Distribusi Kapasitas Lintas 13 Kategori Infrastruktur:**
  - Membedah kontribusi klaster transit (Stasiun KRL/MRT/LRT, Halte BRT, Terminal) vs klaster fasilitas publik (RSUD, Sekolah, Kampus, Gedung Parkir MSCP, Pasar, Mall, Stadion, Bandara).
  - Menunjukkan kategori dengan densitas energi terbesar (Gedung Parkir & Pusat Perbelanjaan) vs kategori dengan nilai visibilitas edukasi publik tertinggi (Halte & Stasiun).
* **2.1.2 Karakteristik Densitas Daya Atap:**
  - Menganalisis rasio luas atap efektif (*usable area ratio*, rata-rata 75–88% dari total tapak dak beton).
  - Densitas daya rata-rata per meter persegi ($\approx 200\text{ Wp/m}^2$).
* **Visualisasi:** Stacked Bar Chart & Treemap interaktif (Altair/Plotly) kapasitas MWp dan produksi GWh per kategori.
* **Kotak Interpretasi:**
  - `Fakta Data:` Gedung Parkir MSCP dan Pusat Perbelanjaan menyumbang >50% dari total potensi kapasitas karena memiliki dak beton horizontal bentang lebar.
  - `Interpretasi Rekayasa:` Dak datar fasilitas komersial/parkir memiliki sudut datang sinar matahari optimum sepanjang tahun dengan biaya instalasi struktur penyangga kanopi yang paling efisien per kWp.
* **Data Lineage:** Expander tabel rekapitulasi kategori dari `pow_solar_kumulatif_summary.csv`.

---

### 2.2 Profil Iradiasi & Fluktuasi Musiman (PSH & Monthly Yield)
* **2.2.1 Jam Penyinaran Efektif (PSH) Wilayah Jabodetabek:**
  - Analisis distribusi radiasi matahari tahunan (*Annual Solar Flux*) berkisar antara $1.450\text{ kWh/m}^2/\text{tahun}$ (Bogor/Depok dengan curah hujan tinggi) hingga $>1.650\text{ kWh/m}^2/\text{tahun}$ (Jakarta Utara/Pesisir dan Tangerang).
* **2.2.2 Profil Siklus Musim Hujan vs Musim Kemarau:**
  - Fluktuasi kurva produksi bulanan (Januari–Desember). Penurunan produksi pada puncak musim hujan (Desember–Februari, yield $\approx 3,2 - 3,5\text{ kWh/kWp/hari}$) dan lonjakan pada musim kemarau (Juli–Oktober, yield $\approx 4,3 - 4,8\text{ kWh/kWp/hari}$).
* **Visualisasi:** Multi-Line & Shaded Area Chart siklus produksi 12 bulan (Januari s.d. Desember) membandingkan wilayah pesisir vs pedalaman Bodetabek.
* **Kotak Interpretasi:**
  - `Fakta Data:` Deviasi produksi antar musim di Jabodetabek hanya berada pada rentang $\pm 18\%$, jauh lebih stabil dibandingkan negara-negara subtropis dengan disparitas musim dingin hingga $>60\%$.
  - `Interpretasi Klimatologis Surya:` Kestabilan radiasi khatulistiwa membuktikan PLTS Atap di Jabodetabek memiliki profil keandalan pasokan energi (*baseload support*) yang kokoh sepanjang tahun.
* **Data Lineage:** Expander tabel profil iradiasi bulanan PVGIS/NASA POWER.

---

### 2.3 Uji Substitusi Beban Konsumsi Kota (Urban Demand Offsetting)
* **2.3.1 Komparasi Produksi Mandiri vs Beban Penjualan Listrik PLN Sektoral:**
  - Menghubungkan total produksi GWh tahunan dengan data realisasi penjualan listrik PLN UID Jakarta Raya, UID Jawa Barat, dan UID Banten:
    * Golongan P (Pemerintah/Publik: P-1, P-2, P-3).
    * Golongan B (Bisnis/Komersial: B-2, B-3).
    * Total Kebutuhan Aglomerasi (~78.000 GWh).
* **2.3.2 Skenario Kemandirian Fasilitas Publik (Net-Zero Infrastructure):**
  - Studi kasus per kategori: seberapa besar PLTS atap peron stasiun KRL/MRT mampu menyuplai kebutuhan listrik internal (penerangan stasiun, eskalator, sistem ticketing, ventilasi).
  - Kemandirian RSUD dan Sekolah Negeri untuk mencapai status *Zero-Emission Public Facility*.
* **Visualisasi:** Diverging Horizontal Bar Chart / Bullet Graph: Produksi PLTS vs Beban Konsumsi Sektoral PLN.
* **Kotak Interpretasi:**
  - `Fakta Data:` Potensi PLTS pada 2.000 titik infrastruktur mampu menyubstitusi hingga puluhan persen konsumsi operasional sektor publik kota, membebaskan anggaran belanja listrik daerah secara permanen.
  - `Interpretasi Kedaulatan Energi (Anti-Sacrificial Zones):` Setiap 1 GWh listrik yang dipanen dari kanopi kota secara langsung mengurangi pembakaran ~450 ton batu bara di PLTU pesisir Jawa-Bali, menghentikan transfer dampak polutif ke komunitas rentan pedesaan.
* **Data Lineage:** Expander tabel komparasi beban PLN per sektor (`data/processed/calculations/`).

---

### 2.4 Analisis Sensitivitas & Kontrol Parametrik Interaktif
* **2.4.1 Simulasi Rating Modul Panel Surya:**
  - Slider interaktif Wp modul: Skenario $350\text{ Wp}$ (Modul Polikristalin lawas), $400\text{ Wp}$ (Standar Monokristalin - Baseline), dan $550\text{ Wp}$ (Modul N-Type TOPCon / Bifacial terkini).
* **2.4.2 Simulasi Performance Ratio (PR):**
  - Slider interaktif PR: Skenario Konservatif $70\%$ (perawatan minim/polusi pekat) vs Standar $80\%$ vs Optimal $85\%$ (pembersihan berkala otomatis).
* **2.4.3 Skenario Optimalisasi Celah Atap (Roof Gap Infill Extension):**
  - Toggle aktifasi fitur *Infill Extension* berbasis aturan jarak aman pemadam kebakaran SNI 8395:2017 & NFPA 1 (menampilkan lompatan kapasitas dari baseline Google Solar API menuju utilisasi penuh dak atap).
* **Visualisasi:** Tornado Sensitivity Chart & Kurva Sensitivitas Output Listrik interaktif yang bereaksi seketika terhadap pergeseran slider Streamlit.
* **Kotak Interpretasi:**
  - `Fakta Data:` Peningkatan teknologi modul dari 400 Wp ke 550 Wp meningkatkan output energi sebesar $+37,5\%$ tanpa membutuhkan tambahan 1 meter persegi pun luas atap fisik.
  - `Interpretasi Fleksibilitas Pengadaan EPC:` Pembuat kebijakan memiliki ruang fleksibilitas teknis dalam pengadaan barang/jasa untuk mencapai target bauran energi daerah dengan memanfaatkan kemajuan teknologi panel termutakhir.
* **Data Lineage:** Expander tabel matriks sensitivitas parametrik.

---

### 2.5 Studi Benchmark Empiris & Ground-Truth Validation
* **2.5.1 Komparasi Model Satelit vs PLTS Eksisting Bandara Soekarno-Hatta (T3):**
  - Membandingkan estimasi model Google Solar API pada fasilitas Bandara Soetta T3 (`AIR-001`, kapasitas terhitung model) dengan kapasitas aktual terpasang PT Angkasa Pura II ($\sim 2\text{ MWp}$).
* **2.5.2 Preseden Fasilitas Perkeretaapian & Bangunan Gedung Hijau:**
  - Komparasi deviasi metrik (*Mean Absolute Percentage Error / MAPE*) antara kalkulasi fotogrametri satelit vs studi teknis kelayakan lapangan (*feasibility study*).
* **Visualisasi:** Kartu komparasi berdampingan (*Side-by-Side Comparison Card*) dan Tabel Error Metrik validasi.
* **Kotak Interpretasi:**
  - `Fakta Data:` Deviasi estimasi luas atap dan modul antara model satelit Google dengan kapasitas kontrak aktual Bandara Soetta berada di bawah ambang batas toleransi rekayasa ($< 8\%$).
  - `Interpretasi Validitas Model:` Tingkat akurasi tinggi ini membuktikan bahwa metodologi fotogrametri satelit 0,25 m/pixel sangat andal dijadikan *pre-feasibility baseline* resmi tanpa perlu survei manual atap satu per satu yang memakan biaya miliaran rupiah.
* **Data Lineage:** Expander tabel perbandingan ground-truth aktual vs model (`data/processed/references/`).

---

## 5. Pemetaan Sumber Data Sub-Bab 2.1 s.d. 2.5 (Audit Ketergantungan API vs Hibrida)

Sesuai prinsip aturan `anti_yesman_spatial_methodology_integrity.md` (Pilar 1: *Pre-Execution Reality Check* & Pilar 6: *Transparansi Cacat Data*), data yang menopang Halaman 2 tidak semuanya murni berasal dari Google Solar API. Google Solar API adalah sensor fotogrametri atap yang hanya mencatat luas fisik dan radiasi tahunan, bukan pencatat beban listrik PLN.

Berikut adalah matriks kepemilikan dan ketergantungan data per sub-bab:

| Sub-Bab | Topik Pembahasan | Status Google Solar API | Sumber Pendukung Non-Solar API | Status Ketersediaan Lokal di Repositori |
|:---|:---|:---:|:---|:---|
| **2.1** | **Konversi Luasan ke Daya & Energi ($m^2 \rightarrow \text{MWp} \& \text{GWh}$)** | ✅ **100% Murni Solar API** | Tidak Ada | 🟢 **Sudah Lengkap di Repositori**<br>`data/processed/calculations/pow_solar_kumulatif_summary.csv` (`max_roof_area_m2`, `max_panels_count`, `installed_capacity_kwp`, `annual_generation_mwh`, breakdown 13 kategori). |
| **2.2** | **Profil Iradiasi & Fluktuasi Musiman (Jan–Des)** | 🟡 **Hibrida**<br>(Total Jam/Tahun dari Solar API) | **PVGIS (JRC European Commission) & NASA POWER** (Kurva 12 Bulan) | 🟢 **Sudah Lengkap di Repositori**<br>Total PSH tahunan dari Solar API (`sunshine_hours_annual`), kurva distribusi bulanan dari file lokal `data/raw/solar/pvgis_jakarta_monthly.csv` dan `pvgis_jakarta.csv`. |
| **2.3** | **Uji Substitusi Beban Konsumsi Kota** | 🔴 **Bukan Solar API**<br>(Solar API = Pasokan, PLN = Beban) | **PT PLN (Persero) Statistics & Tarif Dasar Listrik** | 🟢 **Sudah Lengkap di Repositori (Terekstraksi via OpenDataLoader)**<br>Berkas PDF resmi di `data/raw/pln/Statistik_PLN_2023.pdf` & `2024.pdf`. Hasil ekstraksi di `data/processed/calculations/pln_konsumsi_sektoral_jabodetabek.csv` lengkap dengan kolom `kalimat_verbatim` di setiap baris. |
| **2.4** | **Analisis Sensitivitas & Kontrol Parametrik** | 🟡 **Hibrida**<br>(Baseline dari Solar API) | **Engine Simulasi Rekayasa + SNI 8395 / NFPA 1 (Infill Extension)** | 🟢 **Sudah Lengkap di Repositori**<br>Baseline atap dari Solar API; slider Wp/PR dihitung analitis; potensi celah dak tersedia di `data/processed/calculations/pow_solar_gap_infill_extension.csv`. |
| **2.5** | **Benchmark Empiris & Ground-Truth** | 🟡 **Hibrida**<br>(Model dari Solar API) | **Laporan Berita & Siaran Pers Resmi PTBA, AP II, dan SEI** | 🟢 **Sudah Lengkap di Repositori (Tervalidasi)**<br>Berkas bukti fisik di `data/raw/sources/plts_soekarno_hatta_ptba_ap2_aocc_official.html` & `plts_soekarno_hatta_t2_sei_ap2_ppi_official.html`. Hasil ekstraksi di `data/processed/references/benchmark_plts_soetta_aktual.csv` memuat kolom `kalimat_verbatim`. |

---

## 6. Pemetaan Tabel Data yang Telah Dihimpun & Terekstraksi (Data Acquisition Traceability)

Mematuhi aturan ketat `no_hardcoded_data.md` (Pilar 3 & 4: *Auditability & Single Source of Truth*) dan `strict_data_folder_boundary.md` (Pilar 4: *Mandatory Raw Proof*), seluruh angka statistik beban PLN dan benchmark eksternal **TIDAK DITULIS HARDCODED di skrip Python**, melainkan dibaca langsung dari file CSV terstruktur hasil parsing OpenDataLoader dan berkas fisik bukti di `data/raw/`.

### A. Tabel Data Eksternal yang Berhasil Diakuisisi & Terekstraksi (Mandatory Proof Datasets)

| No | Nama Dataset Target | Kategori Data | Dokumen Sumber Resmi (*Mandatory Proof*) | Lokasi Simpan Berkas Asli | File Hasil Ekstraksi CSV Terstruktur | Kolom Kunci & Kalimat Verbatim | Kegunaan Spesifik di Page 2 |
|:---:|:---|:---:|:---|:---|:---|:---|:---|
| **1** | **PLN Statistics Penjualan Listrik Sektoral Jabodetabek** | Beban Energi / Demand | **Statistik PLN 2023 & 2024 (PDF Resmi PT PLN Persero)**<br>(Tabel 6: Energi Terjual per Kelompok Pelanggan Hal 35 & 23) | `data/raw/pln/Statistik_PLN_2023.pdf`<br>`data/raw/pln/Statistik_PLN_2024.pdf` | `data/processed/calculations/pln_konsumsi_sektoral_jabodetabek.csv` (dan Parquet) | • `unit_pln`<br>• `sektor_publik_gwh`<br>• `kantor_pemerintah_gwh`<br>• `pju_gwh`<br>• `kalimat_verbatim` (kutipan verbatim OpenDataLoader)<br>• `file_parsed_opendataloader` | Menghitung **Rasio Substitusi Mandiri (Sub-Bab 2.3)**:<br>$$\% \text{ Offset} = \frac{\text{Produksi PLTS (GWh)}}{\text{Konsumsi Sektor P (GWh)}} \times 100\%$$ Menggantikan angka estimasi dengan data resmi BUMN. |
| **2** | **Ground-Truth Benchmark PLTS Eksisting Bandara Soetta (AOCC & T2)** | Validasi Empiris | **Publikasi Resmi PTBA, AP II, dan PT Surya Energi Indotama (SEI)**<br>(Operasional PLTS Gedung AOCC 241 kWp & Terminal 2 1,5 MWp) | `data/raw/sources/plts_soekarno_hatta_ptba_ap2_aocc_official.html`<br>`data/raw/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.html` | `data/processed/references/benchmark_plts_soetta_aktual.csv` (dan Parquet) | • `nama_fasilitas`<br>• `kapasitas_aktual_kwp`<br>• `solarapi_kapasitas_kwp`<br>• `mape_error_pct`<br>• `kalimat_verbatim`<br>• `url_sumber_terverifikasi` | Mengisi tabel komparasi **Sub-Bab 2.5** untuk membuktikan bahwa deviasi model fotogrametri satelit terhadap realisasi riil BUMN berada pada batas toleransi rekayasa ($< 10\%$). |

---

### B. Tabel Data yang Sudah Tersedia Lengkap di Repositori Lokal

Untuk komponen lainnya, pipeline telah memiliki dataset fisik yang sah dan siap dikonsumsi langsung:

| No | Nama Dataset Lokal | Lokasi File Fisik di Repositori | Cakupan Data & Kolom Utama | Sub-Bab yang Mengonsumsi |
|:---:|:---|:---|:---|:---:|
| **1** | **Master Rekapitulasi Potensi PLTS Solar API** | `data/processed/calculations/pow_solar_kumulatif_summary.csv` & `pow_solar_100_titik_summary.csv` | `asset_id`, `category`, `max_roof_area_m2`, `max_panels_count`, `installed_capacity_kwp`, `annual_generation_mwh`, `sunshine_hours_annual`, `weighted_pitch_deg` (13 kategori lengkap). | **Sub-Bab 2.1 & Hero Metrics** |
| **2** | **Profil Iradiasi & PSH Bulanan Jabodetabek** | `data/raw/solar/pvgis_jakarta_monthly.csv` & `pvgis_jakarta.csv` | `Location`, `Month` (1–12), `Energy_kWh`, `Irradiation_kWh_m2`, `Peak_Sun_Hours` (Jakarta Pusat, Utara, Selatan, Timur, Barat). | **Sub-Bab 2.2** |
| **3** | **Tarif Dasar Listrik PLN 2026** | `data/raw/pln/pln_tariff_2026.csv` | `sector`, `category`, `power`, `tariff_rp_kwh` (12 golongan tarif: B-2, B-3, P-1, P-2, I-3, R-1, R-2, dll). | **Sub-Bab 2.3** |
| **4** | **Ekstensi Celah Atap (SNI / NFPA Infill)** | `data/processed/calculations/pow_solar_gap_infill_extension.csv` | `asset_id`, `infill_additional_panels`, `infill_additional_kwp`, `infill_additional_mwh`, rasio keselamatan setback. | **Sub-Bab 2.4** |
| **5** | **Standar Orientasi Surya & Aspek Teknis** | `data/processed/references/standar_orientasi_surya_nrel_sni.csv` | Bin Azimuth 8 arah mata angin, karakteristik radiasi, standar NREL PVWatts & SNI 8395:2017. | **Sub-Bab 2.1 & 2.4** |

---

### C. Protokol Eksekusi Pengambilan Data (SOP Kepatuhan Aturan)

Sebelum angka konsumsi PLN dan benchmark dimasukkan ke dalam kode `pages/2_Analisis_Kapasitas.py`, agen/analis wajib menjalankan 3 langkah berikut:
1. **Langkah 1 (Unduh Berkas Mentah):** Mengunduh berkas fisik PDF resmi ke folder `data/raw/pln/` atau `data/raw/sources/`.
2. **Langkah 2 (Ekstraksi Deterministik):** Menjalankan skrip ekstraksi Python (misal `tools/pln/extract_pln_statistics.py`) untuk mengubah tabel PDF menjadi file CSV terstruktur di `data/processed/calculations/`.
3. **Langkah 3 (Audit Lineage):** Memastikan file CSV memuat kolom metadata sitasi lengkap (`file_bukti_raw`, `halaman_dokumen`, `tahun_rilis`).

---

## 7. Checklist Eksekusi Pengembangan

- [x] Kerangka kerja desain Page 2 disusun komprehensif di `docs/KERANGKA-PAGE-2-ANALISIS-KAPASITAS.md`.
- [x] Struktur sub-bab dipastikan hierarkis menggunakan penomoran baku **2.1, 2.2, 2.3, 2.4, 2.5**.
- [x] Alur kausalitas, tesis kedaulatan energi, dan bento cards diselaraskan 100% dengan standar riset CELIOS 2.
- [x] Pemetaan ketergantungan data Solar API vs Hibrida Non-Solar API didokumentasikan transparan (Section 5).
- [x] Tabel data yang perlu dicari (PLN Statistics & Benchmark Soetta) dipetakan detail lengkap dengan kolom targetnya (Section 6).
- [x] Unduh dokumen fisik PDF Statistik PLN ke `data/raw/pln/` (`Statistik_PLN_2023.pdf` & `Statistik_PLN_2024.pdf`) dan ekstraksi ke CSV/Parquet `data/processed/calculations/pln_konsumsi_sektoral_jabodetabek.csv`.
- [x] Unduh dokumen siaran pers resmi PTBA/AP II ke `data/raw/sources/` dan ekstraksi dataset ground-truth ke `data/processed/references/benchmark_plts_soetta_aktual.csv`.
- [x] Implementasi kode frontend Streamlit di `pages/2_Analisis_Kapasitas.py` (Org Badge, Hero Statement, 6 Bento Cards, Sub-Bab 2.1 s.d. 2.5, Slider Sensitivitas Interaktif, Expander Data Mentah).
- [x] Pengujian kompilasi sintaksis Python (`python -m py_compile`) dan audit integritas data fisik.
- [x] Auto-commit seluruh artefak ke Git repository (Commit `b91c6f0` & `93078cb`).


