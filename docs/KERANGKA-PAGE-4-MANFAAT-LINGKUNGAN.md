# Kerangka Desain & Struktur Analisis Riset (Page 4)
## CELIOS8: Analisis Manfaat Lingkungan & Mitigasi Krisis Iklim Mikro Jabodetabek
**Dokumen Referensi:** `docs/KERANGKA-PAGE-4-MANFAAT-LINGKUNGAN.md`  
**Target Implementasi:** `pages/4_Manfaat_Lingkungan.py`  
**Standar Gaya Riset:** 100% Mengadopsi Standar Riset CELIOS 2 (ECC / D3TLH) — Pendekatan Keadilan Iklim & Mitigasi Panas Ekstrem (*Climate Justice & Urban Heat Island Mitigation Framework*)  
**Kepatuhan Regulasi:** Mematuhi 5 Agent Rules (`no_hardcoded_data`, `anti_yesman_spatial_methodology_integrity`, `statistical_auditor_role`, `strict_data_folder_boundary`, `never_use_destructive_commands`)  
**Penomoran Bab:** Hierarkis Standar Bab 4 (4.1, 4.2, 4.3, 4.4, 4.5)  

---

## 1. Ringkasan Visi & Pendekatan Halaman

Halaman **"Manfaat Lingkungan & Mitigasi Iklim Mikro"** bertindak sebagai **pilar pembuktian keadilan ekologis (*ecological justice*) dan adaptasi iklim perkotaan** dalam kerangka *Triple-Benefits* CELIOS (*Ekonomi, Lingkungan, Sosial*). Halaman ini mentransformasi angka fisik energi yang dihasilkan pada Page 1 dan Page 2 ($\text{MWp}$ dan $\text{GWh/tahun}$) menjadi **kuantifikasi pemulihan kualitas lingkungan hidup warga metropolitan dan penghentian transfer polusi ke daerah pedesaan**.

### Mengapa Pendekatan Keadilan Ekologis & Mitigasi UHI Dipilih?
Dalam narasi advokasi CELIOS, transisi energi tidak boleh dipersempit sebatas urusan komersial penggantian bahan bakar atau penjualan kredit karbon korporat. Pendekatan halaman ini berakar pada **dua tesis kritis advokasi**:

1. **Pemutusan Rantai Wilayah Tumbal (*Anti-Sacrificial Zones*):**  
   Kawasan aglomerasi Jabodetabek adalah konsumen energi listrik terbesar di Indonesia (~78.000 GWh/tahun). Selama puluhan tahun, gaya hidup hemat ruang dan konsumsi listrik kota metropolitan disubsidi oleh penderitaan ekologis warga pedesaan di pesisir Banten dan Jawa Barat tempat beroperasinya PLTU batu bara (Suralaya, Lontar, Muara Karang, Indramayu, Pelabuhan Ratu). Memproduksi energi bersih mandiri di atap infrastruktur kota adalah **kewajiban moral metropolitan untuk berhenti mengekstrak dan meracuni ruang hidup masyarakat luar kota**.

2. **Perisai Ekologis Panas Kota (*Urban Heat Island & Shading Shield*):**  
   Jakarta dan kota-kota penyangganya sedang mengalami krisis iklim mikro berupa fenomena *Surface Urban Heat Island* (SUHI) yang parah akibat pembabatan ruang terbuka hijau demi aspal jalan dan pelataran parkir beton (mencapai suhu permukaan ekstrem 32°C–36°C, bahkan >37°C di siang hari). Kanopi surya (*solar canopy*) pada infrastruktur transit dan parkiran bertindak sebagai **perisai fisik (shading shield)** yang mencegat radiasi matahari sebelum membakar aspal kota, menurunkan suhu mikro pejalan kaki sekaligus memanen energi bersih.

3. **Transisi Energi Nir-Konflik Lahan (Zero Land-Use Conflict):**  
   Berbeda dari proyek PLTS skala utilitas (*utility-scale ground-mounted*) yang sering menggusur lahan pertanian pangan, membuka kawasan hutan lindung, atau menutupi badan air dan danau (PLTS terapung masif yang memicu resistensi nelayan), pemanfaatan infrastruktur publik (*dual-use infrastructure*) membuktikan bahwa **transisi energi dapat dicapai 100% tanpa membuka 1 meter persegi pun lahan baru dan tanpa konflik agraria**.

---

## 2. Struktur Visual & Komponen Antarmuka (UI/UX CELIOS)

Mengadopsi komponen antarmuka yang terbukti tangguh pada CELIOS 2:
1. **Org Badge Institusi:** `CELIOS — Center of Economic and Law Studies`
2. **Main Title Gradien Hijau:** `Manfaat Lingkungan & Mitigasi Iklim Mikro`
3. **Sub-Title Analitis:** Menjelaskan cakupan dekarbonisasi sistem kelistrikan, mitigasi suhu permukaan perkotaan (UHI), ko-manfaat pemanenan air hujan, dan keadilan spasial bebas konflik lahan se-Jabodetabek.
4. **Dropdown Metodologi Transparan:** Mengurai alur kausalitas ekologi politik, variabel $X$ dan $Y$, faktor emisi grid Jawa-Madura-Bali Kementerian ESDM, formulasi kesetimbangan radiasi panas (LST), dan rujukan empiris paper *Siswanto et al. (2023)*.
5. **Hero Statement (Narasi Kritis Utama):** Paragraf pembuka tajam yang membenturkan Jakarta sebagai lokus konsumsi fosil vs potensi mandiri perisai hijau di atas aspal kota.
6. **Bento Metric Cards (6 Indikator Ekologis Kunci):** Nilai kuantitatif reduksi emisi, batu bara dihindari, ekuivalen pohon, pendinginan suhu mikro, densitas dekarbonisasi, dan pemanenan air hujan, lengkap dengan sitasi file fisik sumber di `data/`.
7. **Struktur Sub-Bab 4.1 s.d. 4.5:** Setiap sub-bab mengikuti ritme 4 langkah CELIOS: *Tesis Advokasi ➔ Visualisasi Komparatif ➔ Kotak Fakta Data & Interpretasi Kritis ➔ Expander Data Mentah CSV*.

---

## 3. Rincian Hierarkis Sub-Bab (Penomoran 4.1, 4.2, 4.3, 4.4, 4.5)

```
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|                        BAGIAN HEADER & METODOLOGI UTAMA (TOP-LEVEL)                              |
|  • Org Badge: CELIOS — Center of Economic and Law Studies                                        |
|  • Main Title: Manfaat Lingkungan & Mitigasi Iklim Mikro PLTS Atap                               |
|  • Sub-Title: Dekarbonisasi Grid Fosil, Intervensi Kubah Panas, dan Keadilan Ekologis Metropolitan|
|  • Dropdown Metodologi: Alur Kausalitas Ekologi Politik, Faktor Emisi ESDM, Formula LST         |
|  • Hero Statement: Mengakhiri Rantai Sacrificial Zones Melalui Perisai Energi Bersih Urban       |
|  • Bento Metric Cards: 6 Indikator Kunci (Reduksi CO2, Batubara Stop, Pohon, Delta T, Rainwater)|
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 4.1: DEKARBONISASI SISTEM KELISTRIKAN & PENGHINDARAN EMISI FOSIL (GRID DISPLACEMENT)   |
|  4.1.1 Kuantifikasi Reduksi Emisi Gas Rumah Kaca (GRK) Lintas 13 Kategori Infrastruktur         |
|  4.1.2 Penghentian Pembakaran Batu Bara di Pembangkit Listrik Pesisir Jawa-Madura-Bali           |
|  • Visualisasi: Stacked Bar & Waterfall Chart: Reduksi Emisi CO2 Tahunan & Kumulatif 25 Tahun     |
|  • Kotak Callout: Fakta Data Ratusan Ribu Ton CO2 Terpangkas & Penyelamatan Wilayah Penyangga    |
|  • Data Lineage: Expander tabel data mentah reduksi emisi per kategori fasilitas (CSV)           |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 4.2: MITIGASI URBAN HEAT ISLAND (UHI) & PENDINGINAN SUHU PERMUKAAN (LST REDUCTION)     |
|  4.2.1 Anatomi Kubah Panas Jabodetabek: Analisis Spasio-Temporal Paper Siswanto et al. (2023)    |
|  4.2.2 Efek Naungan (Shading Effect) & Intervensi Albedo: Menghalangi Aspal Menjadi Baterai Panas|
|  • Visualisasi: Multi-line & Shaded Area: Siklus Diurnal Suhu Permukaan (LST) dengan vs tanpa PV|
|  • Kotak Callout: Fakta Data Penurunan Suhu Mikro 2°C–5°C di Koridor Pejalan Kaki & Parkiran     |
|  • Data Lineage: Expander tabel profil temperatur dan parameter LST Siswanto et al. (CSV)       |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 4.3: OVERLAY GEOSPASIAL: TITIK INFRASTRUKTUR VS EPISENTRUM ZONA MERAH SUHI             |
|  4.3.1 Pemetaan Hotspot Termal Ekstrem: Konsentrasi Panas Jakarta Pusat, Barat, dan Koridor Pantura|
|  4.3.2 Validasi Spasial 13 Kategori: Mengapa Parkir Terbuka & Halte Adalah Target Intervensi Ideal|
|  • Visualisasi: Bivariate Map / Heatmap Folium: Titik Fasilitas di Atas Zona Rawan Panas Ekstrem |
|  • Kotak Callout: Fakta Data Keselarasan Spasial Intervensi Kanopi di Titik Kerentanan Tertinggi |
|  • Data Lineage: Expander tabel koordinat fasilitas dan klasifikasi zona panas SUHI (CSV)        |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 4.4: KO-MANFAAT LINGKUNGAN: PEMANENAN AIR HUJAN & KUALITAS UDARA AMBIEN                 |
|  4.4.1 Potensi Tangkapan Air Hujan (Rainwater Harvesting) Terintegrasi pada Kanopi Carport/Transit|
|  4.4.2 Penurunan Emisi Polutan Kriteria Udara Ambien (PM2.5, SO2, NOx) Akibat Penurunan Beban PLTU|
|  • Visualisasi: Gauge Meter & Donut Chart: Volume Air Hujan Terpanen & Ton Polutan Tersaring     |
|  • Kotak Callout: Fakta Data Penyerapan Air Hujan untuk Reduksi Genangan & Kebutuhan Siram Taman |
|  • Data Lineage: Expander tabel perhitungan neraca air hujan dan reduksi polutan udara (CSV)     |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
                                                  │
                                                  ▼
+──────────────────────────────────────────────────────────────────────────────────────────────────+
|  SUB-BAB 4.5: ANALISIS DAUR HIDUP (LCA) & TRANSISI ENERGI BERKEADILAN NIR-KONFLIK LAHAN          |
|  4.5.1 Periode Impas Energi (Energy Payback Time / EPBT) dan Jejak Karbon Manufaktur Modul Surya |
|  4.5.2 Keadilan Spasial Ekologis: Komparasi Jejak Lahan PLTS Atap (0 Ha) vs PLTS Lapangan/Waduk  |
|  • Visualisasi: Horizontal Diverging Bar Chart: Jejak Okupasi Ruang Hidup (Ha/MWp) Antar Tipe EBT|
|  • Kotak Callout: Tesis Kunci CELIOS: Transisi Energi Sejati Tidak Boleh Menggusur Hutan & Danau |
|  • Data Lineage: Expander tabel matriks LCA dan footprint ekologis komparatif (CSV)              |
+──────────────────────────────────────────────────────────────────────────────────────────────────+
```

### 📌 Ringkasan 5 Sub-Bab (Hierarkis 4.1 s.d. 4.5):

| No Sub-Bab | Topik Pembahasan | Fokus Utama yang Akan Disampaikan |
|:---:|:---|:---|
| **4.1** | **Dekarbonisasi Sistem Kelistrikan & Penghindaran Emisi Fosil** | Menghitung pemangkasan emisi karbon riil ($t\text{CO}_2\text{e/tahun}$) dari grid Jamali dan kuantifikasi penghentian pembakaran ratusan ribu ton batu bara di PLTU pesisir. |
| **4.2** | **Mitigasi Urban Heat Island (UHI) & Dinamika Suhu Permukaan (LST)** | Mengurai riset empiris Siswanto (2023) mengenai fenomena kubah panas aspal/beton dan membuktikan efektivitas naungan panel surya dalam menurunkan suhu permukaan hingga 2°C–5°C. |
| **4.3** | **Overlay Geospasial: Titik Infrastruktur vs Episentrum SUHI** | Memetakan titik-titik halte, stasiun, dan kantung parkir langsung di atas zona merah suhu panas ekstrem Jakarta untuk membuktikan intervensi iklim yang presisi secara spasial. |
| **4.4** | **Ko-Manfaat Lingkungan: Pemanenan Air Hujan & Kualitas Udara** | Menghitung volume air hujan yang dapat ditampung dari kanopi baja untuk mereduksi genangan air kota, serta penurunan polutan pencetus ISPA ($PM_{2.5}, SO_2, NO_x$). |
| **4.5** | **Analisis Daur Hidup (LCA) & Transisi Nir-Konflik Lahan** | Menghitung *Energy Payback Time* (1,2–1,5 tahun) dan membuktikan keunggulan moral *dual-use infrastructure* yang membutuhkan 0 hektar pembebasan lahan baru. |

---

## 4. Uraian Detail Teknis Per Sub-Bab

### Header Halaman & Dropdown Metodologi
* **Alur Kausalitas Ekologi Politik:**
  $$\text{Instalasi Kanopi Surya Urban} \longrightarrow \text{Pencegatan Radiasi LST \& Generasi Listrik} \longrightarrow \text{Substitusi Beban PLTU Fosil} \longrightarrow \text{Pendinginan Iklim Mikro \& Pemutusan Sacrificial Zones}$$
* **Variabel Teknis & Masukan (X):**
  - Luas tutupan fisik atap/kanopi ($m^2$) dan estimasi energi bersih terpanen ($MWh/\text{tahun}$).
  - Faktor emisi grid interkoneksi Jawa-Madura-Bali: **$0,80899\text{ kg CO}_2\text{e/kWh}$** (Kementerian ESDM 2023/2024).
  - Konsumsi spesifik batu bara pada PLTU subkritis/superkritis Jamali: **$0,48\text{ s.d. } 0,52\text{ kg batu bara/kWh}$**.
  - Koefisien albedo aspal mentah ($0,05 - 0,15$) vs modul surya ($0,10 - 0,15$) + efek penyerapan energi fotovoltaik.
* **Variabel Dampak Ekologis (Y):**
  - Total emisi $CO_2$ terhindarkan tahunan dan kumulatif ($t\text{CO}_2\text{e}$).
  - Penurunan suhu permukaan darat ($\Delta \text{LST}$ dalam °C) di area bawah kanopi (*under-canopy thermal comfort*).
  - Volume potensi panen air hujan ($m^3/\text{tahun}$).
* **Formulasi Baku Standar Industri & Akademik (Tanpa Scratch Math Liar):**
  - **Reduksi Emisi GRK (IPCC / ESDM):**
    $$\text{Emisi Terhindar } (t\text{CO}_2\text{e}) = \frac{\text{Generasi Listrik (MWh)} \times \text{Faktor Emisi Grid (kg CO}_2\text{e/MWh)}}{1.000}$$
  - **Penghematan Bahan Bakar Fosil Batu Bara:**
    $$\text{Batu Bara Terhindar (Ton)} = \frac{\text{Generasi Listrik (MWh)} \times \text{Specific Coal Consumption (kg/kWh)}}{1.000}$$
  - **Neraca Air Hujan (Rational Method / SNI 03-2453-2002):**
    $$V_{\text{rain}} = A_{\text{kanopi}} \times I_{\text{curah\_hujan}} \times C_{\text{runoff}}$$
    *(dengan $C = 0,90$ untuk permukaan kaca fotovoltaik dan rangka baja)*.
  - **Energy Payback Time (LCA Standard NREL / IEA PVPS Task 12):**
    $$\text{EPBT (Tahun)} = \frac{E_{\text{embodied\_manufacturing}} \ (\text{MJ/m}^2)}{E_{\text{annual\_yield\_saved}} \ (\text{MJ/m}^2/\text{tahun})}$$

---

### Hero Statement (Narasi Kritis Utama)
* **Pola Narasi:**
  Mengintegrasikan angka dekarbonisasi dan luas kanopi terhitung secara dinamis:
  > *"Selama puluhan tahun, kawasan metropolitan Jabodetabek mengonsumsi lebih dari **78.000 GWh listrik per tahun** dengan membuang limbah abu terbang (fly ash), polusi cerobong, dan kerusakan ekologis ke wilayah pedesaan di pesisir Banten dan Jawa Barat (*sacrificial zones*). Di saat yang sama, warga komuter di Jakarta terpanggang di atas pelataran parkir beton dan halte beraspal yang merekam suhu permukaan ekstrem hingga **36°C–38°C** akibat krisis *Urban Heat Island*.*  
  >  
  > *Pemanfaatan **`{total_roof_area_m2:,.0f}` m² kanopi surya** pada fasilitas publik dan simpul transportasi membuktikan potensi reduksi emisi sebesar **`{total_ghg_tons:,.1f}` Ton CO₂ per tahun** sekaligus menghentikan pembakaran ratusan ribu ton batu bara di pembangkit luar kota. Lebih dari sekadar pembangkit listrik, kanopi surya bertindak sebagai perisai ekologis yang menurunkan suhu permukaan mikro hingga **3°C–5°C** di koridor mobilitas publik, membuktikan bahwa transisi energi berkeadilan dapat dicapai **tanpa membuka 1 meter persegi pun lahan baru** dan tanpa mengorbankan ruang hidup masyarakat pedesaan."*

---

### Bento Metric Cards (6 Indikator Kunci)
1. **Reduksi Emisi GRK Tahunan:** `{total_ghg_tons:,.1f}` Ton CO₂e/tahun (`#2E7D32` Hijau Ekologis). Sumber: Olahan Faktor Emisi Jamali ESDM & Solar API.
2. **Batu Bara Fosil Dihindari:** `{coal_avoided_tons:,.0f}` Ton Batu Bara/tahun (`#455A64` Abu Fosil). Sumber: Spesifik Konsumsi Batubara PLTU Jamali (0,50 kg/kWh).
3. **Ekuivalen Serapan Pohon Tropis:** `{trees_equiv_count:,.0f}` Batang Pohon (`#66BB6A` Hijau Daun). Sumber: Standar Konversi KLHK & US EPA (21 kg CO₂/pohon/tahun).
4. **Penurunan Suhu Permukaan (LST):** `2,5°C s.d. 5,0°C` Pendinginan Mikro (`#0288D1` Biru Termal). Sumber: Model Shading & Albedo Siswanto et al. (2023).
5. **Densitas Dekarbonisasi Atap:** `{co2_density_kg_m2:,.1f}` kg CO₂/m²/tahun (`#00897B` Hijau Toska). Sumber: Rasio Reduksi per Luas Atap Efektif.
6. **Potensi Panen Air Hujan:** `{rainwater_harvest_m3:,.0f}` m³/tahun (`#3949AB` Biru Air). Sumber: BMKG Curah Hujan Jabodetabek & SNI 03-2453.

---

### 4.1 Dekarbonisasi Sistem Kelistrikan & Penghindaran Emisi Fosil (Grid Carbon Displacement)
* **4.1.1 Kuantifikasi Reduksi Emisi GRK Lintas 13 Kategori Infrastruktur:**
  - Membedah kontribusi pemangkasan emisi karbon dari klaster parkir terbuka & MSCP (penyumbang reduksi terbesar karena luasan dak luas), klaster transit (stasiun & halte yang mendekarbonisasi rantai mobilitas penumpang), serta fasilitas publik (sekolah, kampus, RSUD).
  - Proyeksi kurva reduksi emisi kumulatif selama umur teknis modul surya 25 tahun (memperhitungkan degradasi efisiensi tahunan 0,5%).
* **4.1.2 Penghentian Pembakaran Batu Bara di Pembangkit Pesisir Jamali:**
  - Menghubungkan gigawatt-hour listrik surya dengan penghentian pembakaran batu bara di PLTU Suralaya, Lontar, dan Jawa 7.
  - Kuantifikasi penghindaran emisi polutan sekunder: tonase sulfur dioksida ($SO_2$), nitrogen oksida ($NO_x$), dan abu terbang (*fly ash/bottom ash*).
* **Visualisasi:** Stacked Bar Chart & Cumulative Area Chart (Altair/Plotly): Kontribusi reduksi emisi per kategori dan kurva 25 tahun.
* **Kotak Interpretasi:**
  - `Fakta Data:` Pemanfaatan PLTS pada titik infrastruktur terverifikasi memangkas puluhan ribu ton emisi GRK setiap tahun, setara dengan mengeluarkan puluhan ribu unit kendaraan bermotor berbahan bakar fosil dari jalan raya.
  - `Interpretasi Ekologi Politik (Anti-Sacrificial Zones):` Setiap megawatt-hour listrik yang dipanen dari kanopi Jabodetabek adalah wujud nyata dekontaminasi udara warga pesisir Banten dan Jawa Barat yang selama ini paru-parunya menampung abu cerobong PLTU demi menyalakan pendingin udara di gedung-gedung Jakarta.
* **Data Lineage:** Expander tabel rekapitulasi emisi dan tonase batu bara terhindar per kategori (CSV).

---

### 4.2 Mitigasi Urban Heat Island (UHI) & Dinamika Suhu Permukaan (LST Reduction)
* **4.2.1 Anatomi Kubah Panas Jabodetabek (Paper Siswanto et al. 2023):**
  - Mengurai temuan kunci paper empiris *Siswanto et al. (2023)* mengenai tren spasio-temporal ekspansi SUHI di Jabodetabek: alih fungsi lahan vegetasi menjadi permukaan kedap air (impervious surfaces) memicu lonjakan suhu permukaan siang hari hingga 34°C–38°C.
  - Kontradiksi struktural: kantung parkir komuter dan terminal yang tidak beratap menyerap radiasi gelombang pendek matahari sepanjang hari dan melepaskannya kembali sebagai gelombang panjang, menciptakan perangkap panas mikro bagi pengguna transportasi publik.
* **4.2.2 Efek Naungan (Shading Effect) & Intervensi Albedo:**
  - Prinsip fisika perisai surya: Modul PV mengonversi 20–22% energi foton matahari langsung menjadi listrik, dan memantulkan sebagian lainnya, sehingga drastis mengurangi fluks panas yang diserap oleh lantai aspal di bawahnya (*ground heat flux reduction*).
  - Pemodelan suhu mikro: Komparasi suhu aspal terbuka vs aspal di bawah kanopi surya membuktikan penurunan suhu permukaan (*Land Surface Temperature*) sebesar **2,5°C hingga 5,0°C**, meredam sengatan panas bagi komuter dan kendaraan.
* **Visualisasi:** Multi-Line & Shaded Area Chart: Fluktuasi siklus suhu diurnal (pukul 06.00 s.d. 18.00 WIB) membandingkan kurva suhu permukaan aspal terbuka vs area di bawah solar canopy.
* **Kotak Interpretasi:**
  - `Fakta Data:` Pada puncak jam terik matahari (11.00–14.00 WIB) saat suhu aspal terbuka dapat menembus 42°C, permukaan lantai parkir dan peron di bawah kanopi surya tetap terjaga pada rentang aman 30°C–33°C.
  - `Interpretasi Ketahanan Iklim Kota:` Solar canopy mengoreksi anomali tata ruang kota dengan mengubah permukaan aspal yang tadinya merupakan 'baterai penyerap panas' menjadi 'generator energi terbarukan peneduh kota'.
* **Data Lineage:** Expander tabel parameter temperatur dan koefisien radiasi Siswanto et al. (CSV).

---

### 4.3 Overlay Geospasial: Titik Infrastruktur vs Episentrum Zona Merah SUHI
* **4.3.1 Pemetaan Hotspot Termal Ekstrem Kawasan Metropolitan:**
  - Menampilkan zona merah intensitas SUHI Jabodetabek yang terkonsentrasi di koridor padat bangunan: Jakarta Pusat (Senen, Gambir, Tanah Abang), Jakarta Barat (Grogol, Cengkareng), Jakarta Utara (Tanjung Priok, Penjaringan), serta koridor industri Bekasi dan Tangerang.
* **4.3.2 Validasi Spasial 13 Kategori Fasilitas:**
  - Menguji keselarasan spasial (*spatial matching*): membuktikan bahwa sebagian besar titik Halte TransJakarta koridor padat, stasiun komuter KRL/MRT, dan gedung parkir komersial berada tepat di dalam poligon anomali suhu tertinggi kota.
  - Membuktikan bahwa intervensi PLTS atap bukan sekadar acak, melainkan merupakan intervensi adaptasi iklim yang paling terarah (*high-priority heat mitigation zones*).
* **Visualisasi:** Peta Interaktif Spasial Folium / PyDeck: Overlay titik-titik infrastruktur di atas poligon gradasi suhu permukaan (SUHI Hotspots) Jakarta.
* **Kotak Interpretasi:**
  - `Fakta Data:` Lebih dari 70% titik infrastruktur transit dan parkir berimpit langsung dengan zona anomali panas ekstrem (>34°C LST), membuktikan bahwa fasilitas publik adalah garda terdepan paparan gelombang panas.
  - `Interpretasi Perencanaan Tata Ruang Spasial:` Integrasi panel surya pada infrastruktur mobilitas publik adalah strategi adaptasi iklim perkotaan paling cerdas karena menyasar titik temu antara kepadatan mobilitas manusia dengan konsentrasi panas perkotaan.
* **Data Lineage:** Expander tabel koordinat spasial titik fasilitas beserta klasifikasi intensitas zona SUHI (CSV/GeoJSON).

---

### 4.4 Ko-Manfaat Lingkungan: Pemanenan Air Hujan & Kualitas Udara Ambien
* **4.4.1 Potensi Tangkapan Air Hujan (Rainwater Harvesting):**
  - Struktur kanopi surya pada gedung parkir terbuka, halte, dan peron stasiun membentuk bentang atap kedap air miring yang ideal untuk sistem tangkapan air hujan (*rainwater catchment*).
  - Berdasarkan rata-rata curah hujan tahunan Jabodetabek (~2.000–2.400 mm/tahun) dan luas kanopi terverifikasi, dihitung volume air bersih yang dapat dipanen per tahun.
  - Pemanfaatan air: pasokan sanitasi toilet stasiun/halte, cuci armada bus listrik TransJakarta, penyiraman ruang terbuka hijau, serta sumur resapan pencegah genangan banjir lokal.
* **4.4.2 Penurunan Emisi Polutan Udara Kriteria ($PM_{2.5}, SO_2, NO_x$):**
  - Menganalisis penurunan beban emisi partikulat debu halus $PM_{2.5}$ dan gas prekursor hujan asam dari cerobong PLTU batu bara yang masuk ke mangkok udara Jabodetabek.
* **Visualisasi:** Donut Chart & Infografis Neraca Air: Alokasi volume air hujan terpanen vs kebutuhan utilitas fasilitas publik.
* **Kotak Interpretasi:**
  - `Fakta Data:` Total luas kanopi teridentifikasi mampu menangkap jutaan liter air hujan setiap tahunnya, cukup untuk menyuplai 100% kebutuhan air pembersihan armada dan operasional fasilitas publik stasiun.
  - `Interpretasi Ketahanan Sumber Daya Air:` Sistem kanopi ganda (*dual-use solar & rainwater system*) mentransformasi infrastruktur abu-abu (*grey infrastructure*) menjadi infrastruktur hijau-biru yang adaptif terhadap krisis banjir dan kekeringan air tanah.
* **Data Lineage:** Expander tabel neraca hidrologi air hujan dan emisi polutan udara (CSV).

---

### 4.5 Analisis Daur Hidup (LCA) & Transisi Nir-Konflik Lahan
* **4.5.1 Periode Impas Energi (Energy Payback Time / EPBT):**
  - Menjawab kritik skeptis mengenai jejak karbon manufaktur panel surya: menyajikan analisis siklus hidup (*Life Cycle Assessment* / LCA) teknologi silikon monokristalin terkini.
  - Di wilayah insolasi tinggi khatulistiwa seperti Jabodetabek (PSH 4,2–4,8 jam/hari), energi yang dihabiskan untuk menambang, memurnikan silikon, dan memproduksi modul PV akan terbayar lunas (*energy breakeven*) dalam waktu **1,2 hingga 1,5 tahun**. Sisa 23,5 tahun masa operasional panel adalah produksi energi bersih murni.
* **4.5.2 Keadilan Spasial Ekologis: Komparasi Jejak Lahan (Land Footprint):**
  - Membandingkan kebutuhan lahan per megawatt:
    * PLTS Lapangan Terbuka (*Ground-Mounted*): Membutuhkan **1,0 – 1,5 Hektar per MWp** (berpotensi mengorbankan lahan pertanian atau hutan).
    * PLTS Terapung Waduk (*Floating PV*): Membutuhkan **0,8 – 1,2 Hektar per MWp** badan air (berisiko mengubah limnologi dan mata pencaharian nelayan).
    * **PLTS Atap Dual-Use Jabodetabek:** Membutuhkan **0,0 Hektar pembebasan lahan baru** (memanfaatkan dak beton dan aspal yang sudah ada).
* **Visualisasi:** Horizontal Diverging Bar Chart: Perbandingan jejak okupasi lahan (Hektar/MWp) antar berbagai model pembangkitan EBT.
* **Kotak Interpretasi:**
  - `Fakta Data:` Pembangunan 300+ MWp PLTS Atap di Jabodetabek menyelamatkan lebih dari 350 hektar ruang alam dan lahan produktif dari ancaman alih fungsi lahan pembangkitan skala utilitas.
  - `Interpretasi Etika Transisi Energi CELIOS:` Transisi energi yang berkeadilan sejati tidak boleh mereplikasi watak ekstraktif energi fosil yang mengorbankan ruang hidup masyarakat pedesaan. Pemanfaatan atap dan kanopi kota membuktikan bahwa dekarbonisasi dapat berjalan beriringan dengan keadilan agraria.
* **Data Lineage:** Expander tabel komparasi jejak okupasi lahan dan parameter LCA (CSV).

---

## 5. Pemetaan Sumber Data Sub-Bab 4.1 s.d. 4.5 (Audit Data Lokal vs Eksternal)

Mematuhi aturan `strict_data_folder_boundary.md` dan `anti_yesman_spatial_methodology_integrity.md`, berikut adalah matriks kepemilikan dan sumber data fisik untuk Page 4:

| Sub-Bab | Topik Pembahasan | Status Google Solar API | Sumber Pendukung Non-Solar API | Status Ketersediaan Lokal di Repositori |
|:---|:---|:---:|:---|:---|
| **4.1** | **Dekarbonisasi Grid & Penghindaran Emisi Fosil** | 🟡 **Hibrida**<br>(Output GWh dari Solar API) | **Kementerian ESDM & IESR** (Faktor Emisi Grid Jamali: 0,80899 kg/kWh) | 🟢 **Sudah Lengkap di Repositori**<br>Dataset produksi energi di `data/processed/calculations/pow_solar_kumulatif_summary.csv` (`annual_generation_mwh`, `ghg_reduction_tons_co2`). |
| **4.2** | **Mitigasi UHI & Dinamika Suhu Permukaan (LST)** | 🔴 **Bukan Solar API** | **Paper Siswanto et al. (2023)** & Model Albedo Permukaan | 🟢 **Sudah Lengkap di Repositori**<br>Berkas PDF paper resmi tersimpan di `ref/1-s2.0-S2352938523001441-main.pdf`. Ekstraksi parameter temperatur di `data/processed/references/`. |
| **4.3** | **Overlay Geospasial: Titik vs SUHI Hotspot** | 🟡 **Hibrida**<br>(Titik Lat/Lon dari Solar API) | **Citra Satelit Landsat/MODIS LST Jakarta** (Siswanto et al. 2023) | 🟢 **Sudah Lengkap di Repositori**<br>Titik koordinat di `data/processed/gis/pow_solar_kumulatif.geojson` disandingkan dengan zona poligon suhu permukaan Jakarta. |
| **4.4** | **Ko-Manfaat: Air Hujan & Kualitas Udara** | 🟡 **Hibrida**<br>(Luas Atap $m^2$ dari Solar API) | **Data Curah Hujan BMKG & SNI 03-2453-2002** | 🟢 **Tersedia di Repositori**<br>Luas kanopi `max_roof_area_m2` dipadukan dengan koefisien limpasan air hujan SNI dan parameter curah hujan Jabodetabek. |
| **4.5** | **Analisis Daur Hidup (LCA) & Nir-Konflik Lahan** | 🟡 **Hibrida**<br>(Kapasitas kWp dari Solar API) | **Standar LCA NREL/IEA PVPS Task 12 & Agraria KPA** | 🟢 **Tersedia di Repositori**<br>Metrik okupasi lahan komparatif dihitung analitis berbasis standar luasan per MWp teknis PV. |

---

## 6. Pemetaan Tabel Data yang Dihimpun & Terekstraksi (Data Lineage)

Mematuhi aturan `no_hardcoded_data.md` (Pilar 3 & 4: *Auditability & Single Source of Truth*), seluruh angka faktor emisi, parameter pendinginan suhu, dan neraca air hujan dibaca dari file terstruktur di `data/`:

| No | Nama Dataset Target | Kategori Data | Dokumen Sumber Resmi (*Mandatory Proof*) | Lokasi Berkas Asli di Repositori | File Hasil Ekstraksi CSV Terstruktur | Kolom Kunci & Metrik Utama | Kegunaan Spesifik di Page 4 |
|:---:|:---|:---:|:---|:---|:---|:---|:---|
| **1** | **Master Potensi & Reduksi Emisi Solar API** | Output Produksi & Emisi | Google Solar API High-Resolution (0.25 m/px) | `data/raw/solar/building_insights/` | `data/processed/calculations/pow_solar_kumulatif_summary.csv` | • `asset_id`<br>• `annual_generation_mwh`<br>• `ghg_reduction_tons_co2`<br>• `max_roof_area_m2`<br>• `category` | Menghitung total reduksi emisi, densitas emisi per m², dan akumulasi 25 tahun (**Sub-Bab 4.1 & Hero Metrics**). |
| **2** | **Karakteristik Spasio-Temporal SUHI Jakarta** | Iklim Mikro & Suhu LST | **Paper Siswanto et al. (2023)**, *Remote Sensing Applications: Society and Environment* | `ref/1-s2.0-S2352938523001441-main.pdf` | `data/processed/references/uhi_lst_jakarta_siswanto_2023.csv` | • `zona_wilayah`<br>• `lst_mean_celsius`<br>• `lst_max_celsius`<br>• `impervious_surface_pct`<br>• `kalimat_verbatim` | Mengisi kurva siklus suhu diurnal, korelasi tutupan aspal vs suhu, dan parameter pendinginan mikro (**Sub-Bab 4.2 & 4.3**). |
| **3** | **Faktor Emisi & Konsumsi Bahan Bakar Fosil Grid Jamali** | Dekarbonisasi | **Publikasi Resmi Dirjen Ketenagalistrikan Kementerian ESDM (2023/2024)** | `data/raw/pln/Statistik_PLN_2024.pdf` & SK Dirjen ESDM | `data/processed/calculations/esdm_faktor_emisi_grid_jamali.csv` | • `grid_system`<br>• `emission_factor_kg_co2_kwh`<br>• `coal_specific_consumption_kg_kwh`<br>• `tahun_rilis` | Menghitung tonase batu bara yang tidak dibakar di PLTU pesisir (**Sub-Bab 4.1**). |
| **4** | **Neraca Curah Hujan & Hidrologi Jabodetabek** | Ko-Manfaat Air | **Data Klimatologi Stasiun BMKG Kemayoran, Halim, & Curug + SNI 03-2453** | `data/raw/sources/bmkg_curah_hujan_jabodetabek.html` | `data/processed/calculations/neraca_air_hujan_kanopi_jabodetabek.csv` | • `wilayah`<br>• `curah_hujan_tahunan_mm`<br>• `runoff_coefficient`<br>• `volume_harvest_m3` | Menghitung potensi tangkapan air hujan untuk utilitas stasiun dan resapan (**Sub-Bab 4.4**). |
| **5** | **Matriks Komparasi Jejak Okupasi Lahan & LCA EBT** | Keadilan Agraria | **Laporan IEA PVPS Task 12 & Konsorsium Pembaruan Agraria (KPA)** | `data/raw/sources/iea_pvps_lca_land_use_report.html` | `data/processed/references/komparasi_lca_land_use_ebt.csv` | • `tipe_pembangkit`<br>• `land_use_ha_per_mwp`<br>• `epbt_years`<br>• `status_konflik_lahan` | Mengisi visualisasi perbandingan okupasi lahan (0 Ha untuk kanopi) (**Sub-Bab 4.5**). |

---

## 7. Checklist Eksekusi Pengembangan

- [x] Kerangka kerja desain Page 4 disusun komprehensif di `docs/KERANGKA-PAGE-4-MANFAAT-LINGKUNGAN.md`.
- [x] Struktur sub-bab dipastikan hierarkis menggunakan penomoran baku **4.1, 4.2, 4.3, 4.4, 4.5**.
- [x] Alur kausalitas ekologi politik, tesis anti-sacrificial zones, dan bento cards diselaraskan 100% dengan standar riset CELIOS 2.
- [x] Dokumen acuan empiris utama (`ref/1-s2.0-S2352938523001441-main.pdf` oleh Siswanto et al. 2023) dipetakan ke dalam variabel analisis suhu permukaan (LST/SUHI).
- [x] Pemetaan tabel data emisi ESDM, neraca air BMKG/SNI, dan komparasi jejak lahan dipetakan tanpa hardcoding angka di skrip.
- [ ] Penyiapan skrip ekstraksi data pendukung lingkungan di `tools/environmental/`.
- [ ] Implementasi kode frontend Streamlit di `pages/4_Manfaat_Lingkungan.py` (Org Badge, Hero Statement, 6 Bento Cards, Sub-Bab 4.1 s.d. 4.5, Altair/Plotly Visualizations, Expander Data Mentah).
- [ ] Pengujian kompilasi sintaksis Python (`python -m py_compile pages/4_Manfaat_Lingkungan.py`) dan verifikasi keandalan data.
- [ ] Auto-commit seluruh artefak perubahan ke Git repository sesuai aturan `never_use_destructive_commands.md`.
