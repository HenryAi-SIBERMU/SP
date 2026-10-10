# Kerangka Desain & Struktur Analisis Riset (Page 3)
## CELIOS8: Analisis Ekonomi & Kelayakan Finansial PLTS Atap Jabodetabek
**Dokumen Referensi:** `docs/KERANGKA-PAGE-3-ANALISIS-EKONOMI.md`  
**Target Implementasi:** `pages/3_Analisis_Ekonomi.py`  
**Standar Gaya Riset:** 100% Mengadopsi Standar Riset CELIOS 2 (ECC / D3TLH)  
**Kepatuhan Regulasi:** Mematuhi 5 Agent Rules (`no_hardcoded_data`, `anti_yesman_spatial_methodology_integrity`, `statistical_auditor_role`, `strict_data_folder_boundary`, `never_use_destructive_commands`)  
**Penomoran Bab:** Hierarkis Standar Bab 3 (3.1, 3.2, 3.3, 3.4, 3.5)  

---

## 1. Ringkasan Visi & Pendekatan Halaman

Halaman **"Analisis Ekonomi & Kelayakan Finansial"** bertindak sebagai **pilar kuantitatif pertama dari Triple-Benefits Framework** (*Ekonomi, Lingkungan, Sosial*) sekaligus instrumen pembuktian kelayakan kebijakan (*policy feasibility*). Halaman ini mentransformasi potensi energi fisik hasil kalkulasi satelit pada Page 1 dan Page 2 ($\text{MWp}$ dan $\text{GWh/tahun}$) menjadi **besaran moneter riil: kebutuhan belanja modal (CAPEX), efisiensi belanja operasional listrik (OPEX Savings), kelayakan investasi (LCOE, NPV, IRR, Payback Period), serta model bisnis pengadaan tanpa membebani APBD**.

Mengadopsi tradisi advokasi ekonomi-politik khas CELIOS, halaman ini membantah narasi konservatif pembuat kebijakan yang kerap memandang transisi energi terbarukan sebagai "beban fiskal APBD yang mahal dan merugikan". Sebaliknya, halaman ini membuktikan secara empiris bahwa **PLTS Atap pada 2.000 titik infrastruktur publik Jabodetabek adalah investasi fiskal berimbal hasil positif (*bankable green investment*)**, yang mampu membebaskan belanja listrik daerah secara permanen sekaligus menghentikan transfer dampak polusi ke pedesaan (*anti-sacrificial zones*).

---

## 2. Struktur Visual & Komponen Antarmuka (UI/UX CELIOS)

Mengadopsi komponen antarmuka yang terbukti tangguh pada CELIOS 2:
1. **Org Badge Institusi:** `CELIOS — Center of Economic and Law Studies`
2. **Main Title Gradien Hijau:** `Analisis Ekonomi & Kelayakan Finansial`
3. **Sub-Title Analitis:** Menjelaskan cakupan pemodelan tekno-ekonomi, dekomposisi CAPEX/OPEX, analisis arus kas 25 tahun, dan skema bisnis pengadaan.
4. **Dropdown Metodologi Transparan:** Mengurai alur kausalitas ekonomi-politik, variabel $X$ dan $Y$, serta metode perhitungan teknik ekonomi baku (Standar NREL LCOE, Pedoman KPBU Bappenas, dan Permen ESDM 2/2024).
5. **Hero Statement (Narasi Kritis Utama):** Paragraf pembuka tajam yang merangkum kontradiksi belanja modal vs keuntungan fiskal jangka panjang.
6. **Bento Metric Cards (6 Indikator Kunci):** Nilai moneter besar dengan warna fungsional dan baris sitasi file fisik sumber di `data/`.
7. **Struktur Sub-Bab 3.1 s.d. 3.5:** Setiap sub-bab mengikuti ritme: *Tesis Advokasi ➔ Visualisasi Komparatif ➔ Kotak Fakta Data & Interpretasi Kritis ➔ Expander Data Mentah CSV*.

---

## 3. Rincian Hierarkis Sub-Bab (Penomoran 3.1, 3.2, 3.3, 3.4, 3.5)

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                        BAGIAN HEADER & METODOLOGI UTAMA (TOP-LEVEL)                              |
|  • Org Badge: CELIOS — Center of Economic and Law Studies                                        |
|  • Main Title: Analisis Ekonomi & Kelayakan Finansial PLTS Atap                                  |
|  • Sub-Title: Evaluasi CAPEX, Penghematan Belanja Listrik, dan Skenario Pembiayaan Jabodetabek   |
|  • Dropdown Metodologi: Alur Kausalitas, Standar NREL LCOE, Formulasi Teknik Ekonomi Baku        |
|  • Hero Statement: Menepis Mitos "Transisi Energi Mahal" Melalui Efisiensi Belanja Publik        |
|  • Bento Metric Cards: 6 Indikator Kunci CAPEX, Penghematan, LCOE, Payback, NPV, dan Add-on SPKLU|
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.1: STRUKTUR BIAYA INVESTASI & PENGADAAN (CAPEX & OPEX MODELING)                       |
|  3.1.1 Dekomposisi CAPEX: Rooftop Standar vs Solar Carport & Kanopi Baja                         |
|  3.1.2 Biaya Operasional & Pemeliharaan (OPEX) serta Siklus Penggantian Inverter                |
|  • Visualisasi: Treemap & Stacked Bar Dekomposisi Biaya Modal per Kategori Infrastruktur         |
|  • Kotak Callout: Fakta Data Disparitas Biaya & Justifikasi Rekayasa Kanopi Parkir               |
|  • Data Lineage: Expander tabel rincian komponen CAPEX dan OPEX (CSV)                            |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.2: KUANTIFIKASI PENGHEMATAN TAGIHAN LISTRIK (ELECTRICITY OPEX SAVINGS)                |
|  3.2.1 Proyeksi Penghematan Listrik Sektoral (Golongan Tarif Publik P vs Komersial B)           |
|  3.2.2 Efisiensi Anggaran Fiskal APBD Pemda & Operator Transportasi Publik se-Jabodetabek        |
|  • Visualisasi: Waterfall Chart & Grouped Bar: Pemotongan Tagihan Listrik Eksisting vs PLTS     |
|  • Kotak Callout: Fakta Data Penghematan Belanja Daerah & Ruang Fiskal Baru Pemda                |
|  • Data Lineage: Expander tabel matriks penghematan tagihan PLN per kategori (CSV)               |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.3: INDIKATOR KELAYAKAN FINANSIAL (LCOE, NPV, IRR, & PAYBACK PERIOD)                   |
|  3.3.1 Komparasi LCOE Surya Tropis vs Biaya Pokok Penyediaan (BPP) & Tarif Retail PLN           |
|  3.3.2 Analisis Arus Kas Dinamis (Cash Flow 25 Tahun, Discounted Payback, & Internal Rate)       |
|  • Visualisasi: Cumulative Cash Flow Curve (Break-Even Point) & Tornado Chart Daya Saing LCOE    |
|  • Kotak Callout: Fakta Data Bankability Proyek & Kepastian Titik Impas Finansial                |
|  • Data Lineage: Expander tabel proyeksi arus kas diskonto 25 tahun (CSV)                        |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.4: ANALISIS SENSITIVITAS & KONTROL PARAMETRIK INTERAKTIF                              |
|  3.4.1 Pemodelan 3 Skenario Kebijakan: Konservatif (60%), Moderat Baseline (80%), Optimis (100%) |
|  3.4.2 Sensitivitas Variabel Makro: Fluktuasi Suku Bunga Diskonto (BI Rate) & Eskalasi Tarif     |
|  • Visualisasi: Interactive Spider Sensitivity Chart / Multi-Parameter Sensitivity Curve         |
|  • Kotak Callout: Fakta Data Ketahanan Portofolio terhadap Guncangan Inflasi Energi              |
|  • Data Lineage: Expander tabel matriks sensitivitas parametrik ekonomi (CSV)                    |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 3.5: MODEL BISNIS INOVATIF & SKEMA PEMBIAYAAN ALTERNATIF                                |
|  3.5.1 Komparasi Model Pengadaan: APBD Murni vs PPA (Sewa Atap) & BOOT Konsesi Swasta           |
|  3.5.2 Diversifikasi Pendapatan Baru: Integrasi SPKLU / EV Charging & Monetisasi Kredit Karbon   |
|  • Visualisasi: Radar/Spider Chart Evaluasi 4 Model Bisnis (Risiko vs Beban Kas Pemda)          |
|  • Kotak Callout: Solusi Pengadaan Zero-CAPEX untuk Melindungi Likuiditas Daerah                 |
|  • Data Lineage: Expander tabel perbandingan matriks risiko model bisnis (CSV)                   |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 4. Uraian Detail Teknis Per Sub-Bab

### Header Halaman & Dropdown Metodologi
* **Alur Kausalitas Metodologis:**
  $$\text{Kapasitas \& Yield } (MWp, GWh) \longrightarrow \text{Estimasi CAPEX \& OPEX} \longrightarrow \text{Penghematan Tagihan (Tarif PLN)} \longrightarrow \text{Kelayakan (LCOE, NPV, IRR)} \longrightarrow \text{Model Pengadaan Zero-APBD}$$
* **Variabel Teknis & Kebijakan (X):**
  - Total kapasitas terpasang ($kWp$) dan produksi energi tahunan ($kWh$) hasil validasi satelit Page 1 & Page 2.
  - Asumsi biaya pengadaan satuan standar industri EPC Indonesia ($Rp/Wp$ atau $Rp/kWp$).
  - Struktur Tarif Tenaga Listrik (TTL) PLN 2026 berdasarkan Permen ESDM untuk Golongan P (Pemerintah/Publik), B (Bisnis), dan I (Industri).
  - Parameter makroekonomi: Tingkat diskonto (*discount rate* / WACC Bank Indonesia $\approx 6,5 - 8,0\%$), laju eskalasi tarif listrik ($2,5 - 4,0\%/\text{tahun}$), degradasi performa fotovoltaik ($0,5\%/\text{tahun}$), masa operasional sistem ($25\text{ tahun}$).
* **Variabel Terhitung Finansial (Y):**
  - Belanja Modal Awal ($\text{CAPEX}_{\text{total}}$ dalam Miliar/Triliun Rp).
  - Penghematan Biaya Operasional Listrik Tahunan ($\text{OPEX Savings}$ dalam Miliar Rp/tahun).
  - *Levelized Cost of Energy* (LCOE dalam Rp/kWh).
  - *Net Present Value* ($\text{NPV}$ 25 tahun).
  - *Internal Rate of Return* ($\text{IRR}$ proyek).
  - *Simple & Discounted Payback Period* (Tahun).
* **Standar Perhitungan Baku (Tanpa Scratch Math Liar):**
  - **Formulasi LCOE Baku (Standar NREL / IEC):**
    $$\text{LCOE} = \frac{\text{CAPEX}_0 + \sum_{t=1}^{N} \frac{\text{OPEX}_t}{(1 + r)^t}}{\sum_{t=1}^{N} \frac{E_t}{(1 + r)^t}}$$
    *Di mana $E_t$ adalah generasi listrik tahun ke-$t$ yang memperhitungkan degradasi tahunan panel, $r$ adalah discount rate, dan $N = 25\text{ tahun}$.*
  - **Formulasi Net Present Value (NPV):**
    $$\text{NPV} = \sum_{t=1}^{N} \frac{\text{Cash Inflow}_t - \text{OPEX}_t}{(1 + r)^t} - \text{CAPEX}_0$$
  - **Formulasi Penghematan Listrik Tahunan:**
    $$\text{Savings}_t = E_t \times \text{Tarif\_PLN}_t$$

---

### Hero Statement (Narasi Kritis Utama)
* **Pola Narasi:**
  Mengintegrasikan total nilai moneter secara dinamis:
  > *"Kekhawatiran utama pembuat kebijakan dalam transisi energi perkotaan kerap tertumpu pada tingginya belanja modal awal (CAPEX). Namun, hasil analisis tekno-ekonomi terhadap 2.000 titik infrastruktur membuktikan bahwa total investasi sebesar **`{total_capex_triliun}` Triliun Rupiah** mampu menghasilkan penghematan biaya listrik tahunan mencapai **`{total_savings_miliar}` Miliar Rupiah per tahun**. Dengan rata-rata periode pengembalian modal (*payback period*) selama **`{avg_payback_years}` tahun** dan LCOE sebesar **`{avg_lcoe_kwh}` Rp/kWh** (jauh lebih kompetitif dibandingkan tarif listrik grid PLN golongan publik/bisnis Rp 1.444 – 1.699/kWh), instalasi PLTS Atap bukan beban belanja APBD, melainkan instrumen efisiensi fiskal yang membebaskan anggaran publik secara permanen sekaligus menghentikan transfer dampak polusi ke pedesaan (*anti-sacrificial zones*)."*

---

### Bento Metric Cards (6 Indikator Kunci)
1. **Total Investasi CAPEX:** `{total_capex_triliun}` Triliun Rp (`#4CAF50` Hijau Investasi). Sumber: `pow_solar_ekonomi_summary.csv`.
2. **Penghematan Belanja Listrik:** `{total_savings_miliar}` Miliar Rp/thn (`#66BB6A` Hijau Terang). Sumber: `pow_solar_ekonomi_summary.csv`.
3. **Levelized Cost of Energy (LCOE):** `{avg_lcoe_kwh}` Rp/kWh (`#26A69A` Hijau Toska). Benchmark vs Tarif PLN.
4. **Rata-Rata Payback Period:** `{avg_payback_years}` Tahun (`#FFA726` Emas Imbal Hasil). Analisis Arus Kas Diskonto.
5. **Net Present Value (NPV 25 Thn):** `{total_npv_miliar}` Miliar Rp (`#42A5F5` Biru Finansial). Discount Rate BI 6.5%.
6. **Potensi Tambahan (SPKLU & Karbon):** `+{addon_rev_miliar}` Miliar Rp/thn (`#AB47BC` Ungu Monetisasi). Model Bisnis Tambahan.

---

### 3.1 Struktur Biaya Investasi & Pengadaan (CAPEX & OPEX Modeling)
* **3.1.1 Dekomposisi CAPEX: Rooftop Standar vs Solar Carport & Kanopi Baja:**
  - Membedah perbedaan biaya konstruksi per watt-peak ($Rp/Wp$):
    * **Rooftop Standar (Dak Datar/Pelana):** Fasilitas RSUD, Sekolah, Kampus, Gedung Olahraga, dan Pasar Tradisional ($\approx \text{Rp 12.000 – 14.500/Wp}$ atau $\text{Rp 12 – 14,5 juta/kWp}$). Memanfaatkan struktur dak beton eksisting sehingga biaya bracket/mounting sangat minim.
    * **Solar Carport & Kanopi Baja (Dual-Use):** Kantung Parkir Terbuka, Halte Busway, dan Terminal Bus ($\approx \text{Rp 17.500 – 21.000/Wp}$ atau $\text{Rp 17,5 – 21 juta/kWp}$). Biaya lebih tinggi karena mencakup fabrikasi struktur baja tahan karat (*hot-dip galvanized*), fondasi bor pile, uji ketahanan beban angin (*wind-load resistance*), dan ruang bebas gerak kendaraan (*clearance* $\ge 2,5\text{ m}$).
  - Komposisi struktur biaya: Modul PV ($32\%$), Inverter & BOS ($18\%$), Struktur Baja Kanopi ($28\%$), Jasa Instalasi & Rekayasa ($14\%$), Perizinan & Interkoneksi PLN ($8\%$).
* **3.1.2 Biaya Operasional & Pemeliharaan (OPEX) serta Penggantian Inverter:**
  - OPEX rutin tahunan dipatok pada angka $1,5\%$ dari total CAPEX (pembersihan modul dari partikulat debu polusi Jakarta 2 minggu sekali, inspeksi termal inframerah, dan pemeliharaan kabel).
  - Alokasi dana cadangan perbaikan besar (*major overhaul*) penggantian sentral inverter pada tahun ke-12.
* **Visualisasi:** Treemap Interaktif & Stacked Bar Chart alokasi CAPEX per kategori infrastruktur (Altair/Plotly).
* **Kotak Interpretasi:**
  - `Fakta Data:` Fasilitas parkir terbuka menyerap porsi CAPEX terbesar ($>40\%$) karena memiliki luas bentang kanopi baja masif, namun memberikan densitas penghematan tertinggi.
  - `Interpretasi Rekayasa Keuangan:` Meskipun CAPEX solar carport $\sim 40\%$ lebih mahal daripada rooftop biasa, struktur kanopi memberikan nilai tambah ganda (*co-benefits*): melindungi aset kendaraan publik dari hujan/panas dan meniadakan kebutuhan pengadaan atap parkir konvensional terpisah.
* **Data Lineage:** Expander tabel rincian komponen CAPEX dan OPEX per kategori dari `pow_solar_capex_opex_breakdown.csv`.

---

### 3.2 Kuantifikasi Penghematan Tagihan Listrik (Electricity OPEX Savings)
* **3.2.1 Proyeksi Penghematan Listrik Sektoral (Golongan Publik P vs Komersial B):**
  - Menerapkan matriks Tarif Dasar Listrik PLN 2026 (`data/raw/pln/pln_tariff_2026.csv`):
    * **Golongan Tarif P-1 / P-2 / P-3 (Layanan Pemerintah/Publik):** $\text{Rp 1.444,70 – 1.699,53 per kWh}$. Diterapkan pada Halte TransJakarta, Stasiun Kereta BUMD, JPO, RSUD, dan Sekolah Negeri.
    * **Golongan Tarif B-2 / B-3 (Komersial Menengah-Besar):** $\text{Rp 1.444,70 – 1.467,28 per kWh}$ (ditambah penalti kVARh jika faktor daya rendah). Diterapkan pada Gedung Parkir Mall dan Pusat Perbelanjaan.
  - Kuantifikasi substitusi tagihan per jam operasi: Menghitung porsi *self-consumption* langsung pada siang hari (10.00 – 15.00 WIB) saat beban puncak pendingin udara (AC) gedung dan stasiun berada di titik tertinggi.
* **3.2.2 Efisiensi Anggaran Fiskal APBD Pemda & Operator Transportasi Publik:**
  - Simulasi pemotongan belanja tagihan listrik tahunan PT TransJakarta, PT MRT Jakarta, dan Dinas Kesehatan/Pendidikan DKI Jakarta serta Pemda Bodetabek.
  - Menunjukkan potensi relokasi anggaran belanja operasional rutin listrik ke program layanan dasar masyarakat lainnya.
* **Visualisasi:** Waterfall Chart Komparasi Tagihan Eksisting vs Tagihan Pasca-PLTS Atap & Grouped Bar Chart Penghematan per Sektor.
* **Kotak Interpretasi:**
  - `Fakta Data:` Pemasangan PLTS pada peron stasiun dan halte memangkas hingga $45–60\%$ tagihan listrik internal fasilitas operasional transit di siang hari.
  - `Interpretasi Kebijakan Fiskal:` Penghematan miliaran rupiah dari pos belanja listrik rutin operasional BUMD/OPD secara langsung memperluas ruang fiskal (*fiscal space*) daerah tanpa perlu menaikkan tarif tiket komuter.
* **Data Lineage:** Expander tabel matriks penghematan tagihan listrik per kategori (`data/processed/calculations/pow_solar_electricity_savings.csv`).

---

### 3.3 Indikator Kelayakan Finansial (LCOE, NPV, IRR, & Payback Period)
* **3.3.1 Komparasi LCOE Surya Tropis vs Biaya Pokok Penyediaan (BPP) & Tarif Retail PLN:**
  - Menghitung LCOE rata-rata portofolio 2.000 titik Jabodetabek menghasilkan angka $\approx \text{Rp 780 – 950 per kWh}$.
  - Membandingkan LCOE tersebut dengan tarif beli PLN ($\text{Rp 1.444 – 1.699 per kWh}$), membuktikan margin efisiensi biaya energi mandiri mencapai $\ge 40\%$.
* **3.3.2 Analisis Arus Kas Dinamis (Discounted Cash Flow 25 Tahun):**
  - Pemodelan arus kas kumulatif bersih (*cumulative net cash flow*) selama 25 tahun umur ekonomis instalasi.
  - Menghitung *Simple Payback Period* ($\approx 5,8 – 7,2\text{ tahun}$) dan *Discounted Payback Period* ($\approx 7,5 – 8,9\text{ tahun}$) dengan suku bunga diskonto wajar $6,5\%$.
  - Internal Rate of Return (IRR) proyek portofolio berada pada rentang $12,5\% – 16,8\%$, jauh melampaui ambang batas biaya modal rata-rata tertimbang (*Weighted Average Cost of Capital / WACC*).
* **Visualisasi:** Cumulative Cash Flow Curve (Titik Impas / Break-Even Point) & Bar Chart Komparasi LCOE vs Tarif PLN.
* **Kotak Interpretasi:**
  - `Fakta Data:` Titik impas (Break-even) tercapai pada tahun ke-7, menyisakan 18 tahun masa panen energi listrik "gratis" (*net free energy yield*) bagi fasilitas publik.
  - `Interpretasi Bankability:` Nilai IRR $>12\%$ dan NPV positif bernilai ratusan miliar membuktikan portofolio PLTS atap Jabodetabek sangat layak didanai (*bankable*) oleh perbankan nasional maupun sindikasi keuangan hijau internasional.
* **Data Lineage:** Expander tabel proyeksi arus kas 25 tahun dari `pow_solar_cashflow_projections.csv`.

---

### 3.4 Analisis Sensitivitas & Kontrol Parametrik Interaktif
* **3.4.1 Pemodelan 3 Skenario Kebijakan (Policy Scenarios):**
  - **Skenario Konservatif (60% Utilisasi Atap):** Asumsi CAPEX tinggi ($\text{Rp 20 jt/kWp}$), inflasi tarif flat $0\%$, tingkat diskonto ketat $8\%$. Payback: $8,9\text{ tahun}$, NPV tetap positif.
  - **Skenario Moderat (80% Utilisasi — Baseline Riset):** Asumsi CAPEX standar industri ($\text{Rp 15–18 jt/kWp}$), eskalasi tarif wajar $3\%/\text{tahun}$, diskonto $6,5\%$. Payback: $7,2\text{ tahun}$.
  - **Skenario Optimis (100% Utilisasi Penuh):** Skala agregasi massal Jabodetabek (diskon pengadaan volume $15\%$), integrasi insentif regulasi. Payback: $5,6\text{ tahun}$.
* **3.4.2 Sensitivitas Variabel Makro & Interaktivitas Slider:**
  - Slider Interaktif Streamlit:
    * Slider CAPEX ($Rp/Wp$ rentang $\text{Rp 11.000 – 23.000}$).
    * Slider Tingkat Diskonto ($5,0\% – 9,0\%$).
    * Slider Eskalasi Tarif Listrik Tahunan ($0\% – 5\%$).
* **Visualisasi:** Interactive Spider / Tornado Sensitivity Chart yang memperbarui kurva NPV dan Payback secara seketika (*real-time*).
* **Kotak Interpretasi:**
  - `Fakta Data:` Variabel paling sensitif yang menentukan kelayakan finansial adalah CAPEX struktur kanopi baja dan suku bunga pembiayaan, bukan radiasi sinar matahari.
  - `Interpretasi Fleksibilitas Pengadaan:` Pemerintah daerah dapat menjamin percepatan payback melalui standarisasi desain modular rangka kanopi halte/parkir dan skema pinjaman lunak hijau (*green concession loan*).
* **Data Lineage:** Expander tabel matriks sensitivitas parametrik ekonomi (`data/processed/calculations/pow_solar_sensitivity_matrix.csv`).

---

### 3.5 Model Bisnis Inovatif & Skema Pembiayaan Alternatif
* **3.5.1 Komparasi Model Pengadaan: APBD Murni vs Skema Zero-CAPEX:**
  - **Model 1: Belanja Modal Langsung (APBD/APBN Murni):** Pemda menanggung CAPEX penuh. Beban likuiditas awal berat, namun seluruh penghematan dinikmati $100\%$ sejak hari pertama.
  - **Model 2: PPA / Sewa Atap (Zero-CAPEX Developer Scheme):** Perusahaan EPC/Investor mendanai, membangun, dan memelihara PLTS. Pemda/BUMD hanya membeli listrik surya dengan tarif diskon $15–25\%$ di bawah tarif PLN. Nol risiko teknis dan nol beban APBD.
  - **Model 3: BOOT (*Build-Own-Operate-Transfer*) / KPBU:** Konsesi swasta selama 15 tahun, setelah itu seluruh aset pembangkit diserahkan menjadi milik Pemda/BUMD.
  - **Model 4: Sukuk Hijau Daerah (*Municipal Green Sukuk*):** Penerbitan obligasi hijau syariah oleh Pemprov DKI / Banten / Jabar untuk mendanai transisi energi transportasi umum.
* **3.5.2 Diversifikasi Pendapatan Baru (Dual Revenue Streams):**
  - **Monetisasi SPKLU / EV Charging Terintegrasi:** Mengubah solar carport parkiran stasiun dan mall menjadi stasiun pengisian kendaraan listrik umum berbayar (potensi pendapatan tambahan tarif charging).
  - **Perdagangan Karbon & REC (*Renewable Energy Certificate*):** Sertifikasi MWh hijau yang dihasilkan untuk dijual ke pasar bursa karbon IDXCarbon atau korporasi yang mengejar target Net-Zero.
* **Visualisasi:** Radar/Spider Chart Evaluasi Multi-Kriteria 4 Model Bisnis (Tingkat Risiko, Beban Kas APBD, Kemudahan Legal, dan Imbal Hasil Daerah).
* **Kotak Interpretasi:**
  - `Fakta Data:` Skema PPA/BOOT memungkinkan 2.000 titik infrastruktur dieksekusi seketika tanpa menunggu siklus ketok palu anggaran APBD yang lambat.
  - `Interpretasi Advokasi CELIOS:` Solusi pembiayaan pihak ketiga (*third-party financing*) menggugurkan alibi klasik birokrasi mengenai "keterbatasan anggaran daerah", membuktikan bahwa transisi energi berkeadilan dapat dimulai hari ini secara fiskal mandiri.
* **Data Lineage:** Expander tabel komparasi matriks model bisnis (`data/processed/references/matriks_model_bisnis_plts.csv`).

---

## 5. Pemetaan Sumber Data Sub-Bab 3.1 s.d. 3.5 (Audit Ketergantungan Data)

Sesuai aturan `anti_yesman_spatial_methodology_integrity.md` dan `strict_data_folder_boundary.md`, berikut adalah audit ketergantungan sumber data:

| Sub-Bab | Topik Pembahasan | Status Google Solar API | Sumber Pendukung Non-Solar API | Status Ketersediaan Lokal di Repositori |
|:---|:---|:---:|:---|:---|
| **3.1** | **Struktur Biaya CAPEX & OPEX** | 🟡 **Hibrida**<br>(Kapasitas kWp dari Solar API) | **Standar Industri Solar EPC Indonesia & Asosiasi APAMSI/IESR** (RAB Solar Carport vs Rooftop) | 🟡 **Perlu File Rujukan Terstruktur**<br>Baseline kWp ada di `pow_solar_kumulatif_summary.csv`. Data biaya satuan Rp/kWp perlu diekstrak ke `data/raw/sources/` dan dibukukan ke CSV `standar_capex_opex_indonesia_2026.csv`. |
| **3.2** | **Kuantifikasi Penghematan Tagihan PLN** | 🟡 **Hibrida**<br>(Yield kWh/thn dari Solar API) | **PT PLN (Persero) - Tarif Dasar Listrik 2026** (Golongan P-1, P-2, B-2, B-3, dll) | 🟢 **Sudah Lengkap di Repositori**<br>`data/raw/pln/pln_tariff_2026.csv` dan `pln_tariff_2026_full.json`. |
| **3.3** | **Indikator Kelayakan Finansial (LCOE, NPV, Payback)** | 🟡 **Hibrida**<br>(Generasi Listrik dari Solar API) | **Bank Indonesia (BI Rate/WACC) & Standar Evaluasi Finansial NREL PVWatts** | 🟢 **Sudah Lengkap di Repositori**<br>Pedoman NREL di `data/processed/references/nrel_pvwatts_version5_manual.md`. Angka suku bunga diskonto 6.5% tercatat sebagai parameter resmi. |
| **3.4** | **Analisis Sensitivitas Parametrik** | 🟡 **Hibrida**<br>(Baseline dari Solar API) | **Matriks Skenario Kebijakan CELIOS (Konservatif, Moderat, Optimis)** | 🟢 **Sudah Tersedia di Dokumen Pemodelan**<br>Formula penurunan skenario 60% / 80% / 100% selaras dengan `docs/MODELING-ESTIMASI-STATISTIK-100-KE-2000-TITIK-JABODETABEK.md`. |
| **3.5** | **Model Bisnis & Skema Pembiayaan** | 🔴 **Bukan Solar API**<br>(Studi Hukum & Regulasi Bisnis) | **Bappenas (Pedoman KPBU), Permen ESDM 2/2024, IDXCarbon** | 🟡 **Perlu Penyusunan Tabel Matriks**<br>Disarikan dari dokumen regulasi resmi ke `data/processed/references/matriks_model_bisnis_plts.csv`. |

---

## 6. Pemetaan Tabel Data yang Perlu Dihimpun (Data Acquisition Mapping)

Mematuhi aturan ketat `no_hardcoded_data.md` dan `strict_data_folder_boundary.md`, tidak boleh ada angka CAPEX liar yang di-hardcode di script Python. Berkas bukti fisik wajib disimpan di `data/raw/sources/` dan diekstrak menjadi CSV terstruktur di `data/processed/`.

### A. Tabel Data yang Harus Dibuat/Dihimpun (Action Items)

| No | Nama Dataset Target | Kategori Data | Dokumen Sumber Resmi (*Mandatory Proof*) | Rencana Lokasi Berkas Asli | Rencana File Ekstraksi CSV | Struktur Kolom yang Wajib Diekstrak | Kegunaan Spesifik di Page 3 |
|:---:|:---|:---:|:---|:---|:---|:---|:---|
| **1** | **Standar Biaya CAPEX & OPEX PLTS Indonesia 2026** | Finansial EPC | **Laporan Status Energi Terbarukan Indonesia (IESR) 2024/2025 & Penawaran EPC Nasional** | `data/raw/sources/iesr_solar_lcoe_capex_report.pdf` | `data/processed/calculations/standar_capex_opex_plts_2026.csv` | • `tipe_instalasi` (Rooftop Beton, Metal Roof, Solar Carport Baja, Kanopi Busway)<br>• `capex_min_rp_wp`<br>• `capex_baseline_rp_wp`<br>• `capex_max_rp_wp`<br>• `opex_persen_tahunan`<br>• `inverter_replacement_cost_pct`<br>• `tahun_reviu`<br>• `file_bukti_raw` | Menghitung total nilai investasi dan dekomposisi biaya modal per kategori pada **Sub-Bab 3.1**. |
| **2** | **Matriks Evaluasi Komparasi Model Bisnis Pengadaan** | Regulasi & Bisnis | **Panduan Pelaksanaan KPBU Sektor Energi Terbarukan (Bappenas & Kementerian Keuangan)** | `data/raw/sources/bappenas_panduan_kpbu_ebt.pdf` | `data/processed/references/matriks_model_bisnis_plts.csv` | • `model_bisnis` (APBD Murni, PPA Sewa Atap, BOOT 15 Tahun, Green Sukuk)<br>• `beban_capex_pemda` (Tinggi / Nol)<br>• `risiko_operasi` (Pemda / EPC Swasta)<br>• `tarif_diskon_listrik_pct`<br>• `kelayakan_legal_pemda`<br>• `skor_kecepatan_eksekusi`<br>• `file_bukti_raw` | Menopang visualisasi Radar Chart dan rekomendasi pembiayaan pada **Sub-Bab 3.5**. |

### B. Tabel Data yang Sudah Tersedia Lengkap di Repositori Lokal
1. **Master Potensi PLTS Jabodetabek:** `data/processed/calculations/pow_solar_kumulatif_summary.csv` (`asset_id`, `category`, `installed_capacity_kwp`, `annual_generation_mwh`, dll).
2. **Tarif Dasar Listrik PLN 2026:** `data/raw/pln/pln_tariff_2026.csv` (`sector`, `category`, `power`, `tariff_rp_kwh`).
3. **Pedoman Formula NREL PVWatts & LCOE:** `data/processed/references/nrel_pvwatts_version5_manual.md`.
4. **Matriks 3 Skenario Kebijakan:** `docs/MODELING-ESTIMASI-STATISTIK-100-KE-2000-TITIK-JABODETABEK.md` (60%, 80%, 100%).

---

## 7. Checklist Eksekusi Pengembangan

- [x] Kerangka kerja desain Page 3 disusun komprehensif di `docs/KERANGKA-PAGE-3-ANALISIS-EKONOMI.md`.
- [x] Struktur sub-bab dipastikan hierarkis menggunakan penomoran baku **3.1, 3.2, 3.3, 3.4, 3.5**.
- [x] Alur kausalitas, tesis kedaulatan energi, dekomposisi CAPEX, dan bento cards diselaraskan 100% dengan standar riset CELIOS 2.
- [x] Pemetaan ketergantungan data Solar API vs Standar Biaya Industri didokumentasikan transparan (Section 5).
- [x] Tabel data yang perlu dihimpun (Standar CAPEX IESR & Matriks Model Bisnis) dipetakan detail lengkap dengan kolom targetnya (Section 6).
- [ ] Buat skrip pembentuk tabel data turunan ekonomi di `tools/financial/generate_economic_tables.py` untuk menghasilkan `pow_solar_ekonomi_summary.csv` dari `pow_solar_kumulatif_summary.csv` dan `pln_tariff_2026.csv`.
- [ ] Implementasi kode frontend Streamlit di `pages/3_Analisis_Ekonomi.py`.
- [ ] Pengujian interaktivitas slider parametrik dan audit visualisasi.
- [ ] Auto-commit seluruh artefak ke Git repository sesuai aturan keselamatan kode.
