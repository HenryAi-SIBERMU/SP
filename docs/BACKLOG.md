# BACKLOG - Celios8 Solar Panel Project
## JABODETABEK PLTS Atap Dual-Use Infrastructure Research

**Project Status**: 🟡 In Progress - Regional Expansion & Data Validation Phase

---

## 📅 BACKLOG PER TANGGAL

### [2026-09-27] - Scope Expansion: Tambahan 6 Kategori Public Infrastructure (Non-Transit)

**Status**: 🟡 **ACTIVE - Category Scope Expanded**  
**Created**: 27 September 2026, 10:45 WIB  

**Summary**:
- **Penambahan Kategori Infrastruktur Publik**: Berdasarkan kebutuhan riset, ditambahkan 6 kategori infrastruktur publik (non-transit) melengkapi 7 kategori mobilitas eksisting:
  1. **Sekolah Negeri**: SD, SMP, SMA/SMK Negeri (Dapodik Kemendikbud & Disdik)
  2. **Universitas**: Kampus perguruan tinggi negeri & swasta (PDDIKTI)
  3. **RS & Puskesmas**: Rumah sakit dan puskesmas (SIRS Kemenkes)
  4. **Pasar**: Pasar tradisional & pasar rakyat (Perumda Pasar Jaya & daerah)
  5. **Bandara**: Terminal penumpang & fasilitas kargo (InJourney / Angkasa Pura)
  6. **Stadion / GOR**: Stadion utama & gelanggang olahraga (Dispora)
- **Evaluasi Kelayakan Google Solar API**: Ke-6 kategori memiliki atap bangunan berukuran besar/kontinu dan 100% eligible untuk analisis Building Insights dan Data Layers (Annual Solar Flux).
- **Sinkronisasi Dokumen & RAB**: Diintegrasikan ke dalam dokumen riset (`GOOGLE-SOLAR-API-PLAN.md`, `framework-fase1-solar-panel.md`, `DATA-ACQUISITION-PLAN.md`) dan RAB HTML (`celios8-solar-rab-annualflux.html`).

---

### [2026-09-24] - Scope Expansion to JABODETABEK (Safety Buffer 4,000 Titik) & RAB Update

**Status**: 🟡 **ACTIVE - Regional Scope Expanded**  
**Created**: 24 September 2026, 14:15 WIB  
**Last Updated**: 24 September 2026, 14:15 WIB

> ⚠️ **DISCLAIMER STATUS VALIDASI DATA**:  
> Seluruh angka infrastruktur di bawah menggunakan **4,000 titik sebagai SAFETY BUFFER (PAGU AMAN ANGGARAN)** agar pendanaan riset tidak tekor/kurang. **ANGKA INI ADALAH ESTIMASI DAN BELUM TERVALIDASI 100% SECARA RIIL DI LAPANGAN**. Kuota query Google Solar API aktual akan disesuaikan bertahap mengikuti titik yang lolos verifikasi spasial.

**Summary**:
- **Scope Expansion**: Wilayah riset resmi diperluas dari DKI Jakarta ke **JABODETABEK** (Provinsi DKI Jakarta, Kab/Kota Bogor, Kota Depok, Kab/Kota Tangerang, Kota Tangerang Selatan, Kab/Kota Bekasi).
- **Target Titik Pagu Aman**: Ditetapkan plafon batas atas **4,000 titik regional Jabodetabek** (safety buffer +33% dari estimasi dasar 3,000 titik).
- **RAB Google Solar API Direkalkulasi (Pagu 4,000 Titik)**:
  - Opsi 1 (Building Insights Only): **$26.64 (~Rp 420.912)** *(Pengajuan: Rp 500.000)*
  - Opsi 2 (BI + Visual Validation RGB/Mask/DSM): **$426.24 (~Rp 6.734.592)** *(**USULAN PENGAJUAN PROPOSAL: Rp 7.000.000** - Jika akun baru dapat Free Credit $300 GCP, out-of-pocket bersih hanya **~Rp 1.99 juta**)*
  - Opsi 3 (ALL-IN Comprehensive 5 Layers): **$692.64 (~Rp 10.943.712)** *(**USULAN PENGAJUAN PROPOSAL: Rp 11.000.000** - Net out-of-pocket **~Rp 6.20 juta** setelah Free Credit)*
- **Blocker**: Data extraction pipeline harus menggunakan BBOX geospasial Jabodetabek penuh (OSM Overpass / Overture Maps).

---

### [2026-09-02] - Data Validation & Critical Gap Analysis

**Status**: ⚪ Logged Historical  
**Created**: 2 September 2026, 14:30 WIB  

**Summary**:
- Identified critical data gap pada lingkup Jakarta: 1,415 target locations vs 1,089 actual (77% coverage)
- Jakarta Open Data extraction blocked (Puppeteer JSON parsing issue)
- RAB Google Solar API needs recalculation based on validated data

---

## 🎯 PRIORITAS TINGGI (Critical Path)

### 1. ⚠️ VALIDASI JUMLAH TITIK INFRASTRUKTUR (SKALA JABODETABEK)

**Status**: 🔴 **CRITICAL - Regional Data Acquisition & Validation Needed**

> ⚠️ **CATATAN VALIDASI**: Angka 4,000 titik adalah **ESTIMASI PAGU ATAS (SAFETY BUFFER) BELUM TERVALIDASI**. Angka ini sengaja dipatok lebih tinggi agar anggaran tidak tekor saat ada penambahan titik baru di lapangan.

#### Estimasi Titik: Target Lama (DKI) vs Safety Buffer (JABODETABEK):

| No | Kategori | Target Lama (DKI) | Safety Buffer (Jabodetabek) | Penambahan | Rincian Aset Regional (Estimasi Belum Tervalidasi) |
|:--:|----------|:-----------------:|:---------------------------:|:----------:|----------------------------------------------------|
| 1 | **Halte BRT & Bus Shelter** | 284 | **850** | **+566** | TransJakarta koridor & rute perbatasan + feeder Biskita Bogor, Trans Patriot Bekasi, Tayo Tangerang, Feeder Depok/Tangsel |
| 2 | **Stasiun KRL Commuter Line** | 80 | **100** | **+20** | Seluruh lintas KRL Jabodetabek (Bogor, Cikarang, Rangkasbitung, Tangerang, Tanjung Priok) |
| 3 | **Stasiun MRT, LRT & Bandara** | 31 | **60** | **+29** | MRT Jakarta, LRT Jakarta, LRT Jabodebek (18 stasiun), KA Bandara Soetta, KCIC Halim |
| 4 | **JPO (Jembatan Penyeberangan)**| 300 | **640** | **+340** | JPO DKI Jakarta + JPO koridor jalan nasional/provinsi Bodetabek |
| 5 | **Parkir Terbuka, Park & Ride & Terminal** | 500 | **1,850** | **+1,350** | Kantung Park & Ride stasiun komuter Bodetabek + Terminal Bus Tipe A/B + Mall/RS/Kampus terbuka |
| 6 | **MSCP Gedung Parkir** | 200 | **440** | **+240** | Gedung parkir komersial, stasiun, dan perkantoran Bodetabek |
| 7 | **Koridor Pedestrian Beratap / TOD** | 20 | **60** | **+40** | Jalur pejalan kaki terintegrasi TOD transit hub di Jabodetabek |
| **TOTAL** | **Semua Kategori** | **1,415** | **4,000** | **+2,585** | **Safety Buffer Pagu Atas Penganggaran** |

**Impact**:
- ✅ **RAB Google Solar API Aman**: Menggunakan pagu Rp 7.000.000 (Opsi 2) s.d. Rp 11.000.000 (Opsi 3) sehingga anggaran tidak akan kurang.
- ⚠️ **Keterangan Status**: Wajib mencantumkan catatan bahwa angka 4,000 adalah batas pagu estimasi belum tervalidasi.
- 🔴 **Validasi Spasial**: Diperlukan tahapan verifikasi spasial bertahap (POC 20 titik) sebelum melakukan query massal.

**Action Items**:
- [ ] **A1.1** - Tentukan BBOX resmi koordinat geospasial Jabodetabek (`[ -6.80, 106.35, -5.95, 107.25 ]`)
- [ ] **A1.2** - Ekstrak seluruh stasiun KRL Jabodetabek & LRT Jabodebek via Overpass API
- [ ] **A1.3** - Ekstrak kantung Park & Ride di sekitar stasiun komuter Bodetabek
- [ ] **A1.4** - Ekstrak halte BRT Bodetabek (Biskita, Trans Patriot, Tayo) & TransJakarta
- [ ] **A1.5** - Ekstrak JPO di sepanjang koridor jalan arteri primer Jabodetabek
- [ ] **A1.6** - Filter poligon parkir terbuka (OSM `amenity=parking` + `parking=surface`) se-Jabodetabek
- [ ] **A1.7** - Verifikasi sampel 20 lokasi untuk POC Google Solar API di Jabodetabek

**Deadline**: 9 September 2026 (1 minggu)  
**Owner**: Data Team  
**Blocker**: Jakarta Open Data extraction (Puppeteer script perlu fix)

---

### 2. 🔧 FIX JAKARTA OPEN DATA EXTRACTION

**Status**: 🟡 **IN PROGRESS - Stuck di JSON Extraction**

**Problem**: Puppeteer script berhasil klik tombol "Lihat JSON" tapi data belum ter-extract properly.

#### Current State:
- ✅ Script navigate ke page: `tools/jakarta_opendata/extract_json_data.js`
- ✅ Button "Lihat JSON" ter-klik
- ❌ JSON data belum ter-extract dari popup/preview window
- ❌ File output masih berupa HTML page content, bukan pure JSON

**Files Affected**:
```
tools/jakarta_opendata/extract_json_data.js          - Script yang perlu fix
data/raw/jakarta_opendata/data-halte-transjakarta.json  - Output saat ini HTML, bukan JSON
```

**Target Output**: 
```json
[
  {
    "nama_halte": "Harmoni",
    "koordinat_x": "-6.162687",
    "koordinat_y": "106.81992",
    "lokasi": "Jalan Hayam Wuruk",
    "wilayah": "Kota Adm. Jakarta Pusat",
    "kecamatan": "Gambir",
    "kelurahan": "Gambir",
    "periode_data": "2024"
  },
  ... (538 records total)
]
```

**Action Items**:
- [ ] **A2.1** - Fix Puppeteer selector: ganti `page.$()` → `page.evaluateHandle()` untuk extract JSON dari preview popup
- [ ] **A2.2** - Parse JSON data dari element text content
- [ ] **A2.3** - Save clean JSON to `data/raw/jakarta_opendata/*.json`
- [ ] **A2.4** - Validate 538 records dengan koordinat valid
- [ ] **A2.5** - Convert JSON → GeoJSON/GeoPackage untuk GIS analysis

**Deadline**: 5 September 2026 (3 hari)  
**Owner**: Web Scraping Team  
**Reference**: Context transfer message #9-10 (Puppeteer error log)

---

## 🟡 PRIORITAS SEDANG (Important but not blocking)

### 3. 📊 DATA ACQUISITION PLAN COMPLETION

**Status**: 🟡 **IN PROGRESS - 60% Complete**

**Reference**: `docs/DATA-ACQUISITION-PLAN.md`

#### Data Status Summary:

**✅ COMPLETED** (Already collected):
- ✅ PVGIS Solar Data: PSH Jakarta 5.0 h/day
- ✅ OSM Buildings: 5,729 buildings
- ✅ OSM Parking: 946 areas
- ✅ OSM Hospitals: 358 locations
- ✅ OSM Stations: 79 (KRL/MRT/LRT)
- ✅ OSM Bus Stops: 7,341 + 64 TransJakarta
- ✅ PLN Tariff 2026: 12 categories

**🟡 PARTIAL** (Collected but needs processing):
- 🟡 Jakarta Open Data TransJakarta: 538 records (needs extraction)
- 🟡 Stations: 79 total (needs split by type)
- 🟡 Parking: 946 total (needs separation MSCP vs open lot)

**🔴 MISSING** (Not started):
- ❌ JPO (Jembatan Penyeberangan): 0 / 300 target
- ❌ Koridor Pedestrian: 0 / 20 target
- ❌ Google Solar API: 0 / 1,415 target (pending validation)

**Action Items**:
- [ ] **A3.1** - Update DATA-ACQUISITION-PLAN.md dengan status actual per 2 Sep 2026
- [ ] **A3.2** - Add section "Data Quality Issues" untuk dokumentasi gap
- [ ] **A3.3** - Prioritize data sources: critical (halte) vs nice-to-have (pedestrian)

**Deadline**: 16 September 2026 (2 minggu)  
**Owner**: Research Lead

---

### 4. 💰 UPDATE RAB GOOGLE SOLAR API (SAFETY BUFFER 4,000 TITIK JABODETABEK)

**Status**: ✅ **UPDATED (SAFETY BUFFER CEILING APPLIED: 4,000 TITIK)**

> ⚠️ **DISCLAIMER PENTING**: Jumlah 4,000 titik adalah **PAGU AMAN ANGGARAN (SAFETY BUFFER) BELUM TERVALIDASI**. Angka ini sengaja dipatok lebih tinggi agar proposal pendanaan tidak tekor jika ada penambahan titik riil di lapangan.

**Summary Hasil RAB Pagu 4,000 Titik (tools/solar_api/GOOGLE-SOLAR-API-PLAN.md)**:
- **Opsi 1 (Building Insights Only)**: $26.64 (~Rp 420.912) — Pagu Proposal: **Rp 500.000**.
- **Opsi 2 (BI + 3 Data Layers: RGB/Mask/DSM)**: $426.24 (~Rp 6.734.592) — **USULAN PENGAJUAN: Rp 7.000.000**. *(Out-of-pocket bersih hanya **~Rp 1.99 juta** jika akun baru GCP mendapat Free Credit $300)*.
- **Opsi 3 (ALL-IN Comprehensive 5 Layers)**: $692.64 (~Rp 10.943.712) — **USULAN PENGAJUAN: Rp 11.000.000**. *(Out-of-pocket bersih **~Rp 6.20 juta** jika ada Free Credit $300)*.

**Action Items**:
- [x] **A4.1** - Rekalkulasi 3 opsi skenario RAB untuk 4,000 titik safety buffer Jabodetabek
- [x] **A4.2** - Cantumkan disclaimer formal bahwa angka 4,000 titik adalah estimasi belum tervalidasi
- [x] **A4.3** - Rumuskan angka pengajuan aman proposal (Rp 7 Juta untuk Opsi 2 / Rp 11 Juta untuk Opsi 3)
- [ ] **A4.4** - Eksekusi POC test 20 lokasi sampel (Free Trial) sebelum batch query massal

---

## 🟢 PRIORITAS RENDAH (Nice to have)

### 5. 🗺️ GIS DATA INTEGRATION

**Status**: 🟢 **PLANNED - Not Started**

**Goal**: Merge semua data infrastruktur ke single GeoPackage untuk analysis

**Target Output**: `data/processed/jakarta_infrastructure_all.gpkg` dengan layers:
- halte_transjakarta (validated ~300)
- stasiun_krl (~50)
- stasiun_mrt (~13)
- stasiun_lrt (~18)
- jpo (~300)
- parking_lot (~500)
- mscp (~200)
- koridor_pedestrian (~20)

**Action Items**:
- [ ] **A5.1** - Create GeoPackage schema
- [ ] **A5.2** - Merge & deduplicate all datasources
- [ ] **A5.3** - Add metadata fields (source, date_collected, validation_status)
- [ ] **A5.4** - Generate QGIS project file (.qgs) untuk visualization

**Deadline**: 23 September 2026 (3 minggu)  
**Owner**: GIS Team

---

### 6. 📈 DASHBOARD STREAMLIT PREPARATION

**Status**: 🟢 **PLANNED - Not Started**

**Goal**: Prepare data pipeline untuk Streamlit dashboard

**Dependencies**: 
- A1.7 (validated location count)
- A5.4 (integrated GeoPackage)

**Action Items**:
- [ ] **A6.1** - Design dashboard mockup (Figma/sketch)
- [ ] **A6.2** - Setup Streamlit project structure
- [ ] **A6.3** - Create data loading functions (GeoPackage → Streamlit)
- [ ] **A6.4** - Implement interactive map (Folium/Plotly)

**Deadline**: 30 September 2026 (4 minggu)  
**Owner**: Frontend Team

---

## 📋 BACKLOG ITEMS (Future Work)

### 7. 🔬 GOOGLE SOLAR API IMPLEMENTATION

**Status**: ⏸️ **ON HOLD - Waiting for Data Validation**

**Blocker**: A1.7 (validated location count)

**Next Steps**:
- [ ] Setup Google Cloud project
- [ ] Enable Solar API & create API key
- [ ] Test 10 sample locations (POC)
- [ ] Batch query all validated locations
- [ ] Process & store results

**Estimated Start**: 16 September 2026 (after validation complete)

---

### 8. 📊 ANALISIS KAPASITAS ENERGI

**Status**: ⏸️ **ON HOLD - Waiting for Roof Area Data**

**Dependencies**: A7 (Google Solar API results)

**Next Steps**:
- [ ] Calculate MWp per kategori
- [ ] Estimate annual kWh production
- [ ] CO2 reduction calculation
- [ ] Economic analysis (NPV, ROI)

**Estimated Start**: 23 September 2026

---

### 9. 📝 PAPER WRITING

**Status**: ⏸️ **ON HOLD - Waiting for Analysis Results**

**Dependencies**: A8 (energy capacity analysis)

**Target Sections**:
- [ ] Introduction & Background
- [ ] Methodology
- [ ] Results & Discussion
- [ ] Conclusion & Recommendations

**Estimated Start**: 30 September 2026  
**Deadline**: 31 Oktober 2026 (2 bulan)

---

## 🚨 RISKS & ISSUES

### Risk Register:

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R1 | Jakarta Open Data extraction gagal | Medium | High | Fallback: manual download + parsing |
| R2 | JPO data tidak tersedia | High | Medium | Reduce scope: focus on 5 kategori instead of 7 |
| R3 | Google Solar API Jakarta coverage rendah | Low | High | Test 10 samples first before bulk query |
| R4 | Budget Solar API exceed Rp 5 juta | Medium | Medium | Use tiered approach: priority subset first |
| R5 | Timeline delay karena data collection | High | High | Parallel track: start analysis dengan data available |

---

## 📅 MILESTONE TIMELINE

```
Sep 2026    Week 1 [====X===] Data Validation & Jakarta Open Data Fix
            Week 2 [========] JPO Data Collection & GIS Integration
            Week 3 [========] Google Solar API POC Testing
            Week 4 [========] Batch Query & Data Processing

Oct 2026    Week 1-2 [========] Energy Analysis & Visualization
            Week 3-4 [========] Dashboard Development
            
Nov 2026    Week 1-4 [========] Paper Writing & Review
```

**Current Position**: Week 1 Sep 2026 - Data Validation Phase ⬅️ **YOU ARE HERE**

---

## 📞 CONTACTS & OWNERSHIP

| Task Area | Owner | Contact | Status |
|-----------|-------|---------|--------|
| Data Collection | Data Team | - | Active |
| Web Scraping | Dev Team | - | Active |
| GIS Processing | GIS Team | - | Standby |
| Solar API Integration | API Team | - | Standby |
| Dashboard Development | Frontend Team | - | Planned |
| Research Writing | Research Lead | - | Planned |

---

## 📝 CHANGELOG

### [2026-09-24] 13:30 WIB - Regional Scope Expansion to JABODETABEK & 3,000 Points Recalculation
**Type**: 🔄 Scope Expansion & Budget Update  
**Author**: AI Assistant / Research Team  
**Branch**: main

**Added & Updated**:
- ✅ Perluasan cakupan geografis: DKI Jakarta ➡️ **JABODETABEK** (DKI Jakarta, Bogor, Depok, Tangerang, Bekasi).
- ✅ Penyesuaian estimasi titik: **3,000 lokasi regional** (Halte BRT 650, Stasiun KRL 85, Stasiun MRT/LRT/Bandara 50, JPO 475, Parkir & Terminal 1,350, MSCP 350, Pedestrian TOD 40).
- ✅ Update kalkulasi RAB Google Solar API di `tools/solar_api/GOOGLE-SOLAR-API-PLAN.md` untuk 3,000 lokasi (Opsi 1: Rp 315K, Opsi 2: Rp 5.05M [Net Rp 310K via Free Credit], Opsi 3: Rp 8.2M).
- ✅ Identifikasi aset potensial baru: Kantung Park & Ride stasiun komuter Bodetabek dan Terminal Bus Tipe A/B.

### [2026-09-02] 14:30 WIB - Initial Backlog Creation
**Type**: 🆕 New  
**Author**: AI Assistant  
**Branch**: main

**Added**:
- ✅ Created initial BACKLOG.md structure
- ✅ Identified critical data validation issue (1,415 target vs 1,089 actual)
- ✅ Documented Jakarta Open Data extraction blocker
- ✅ Added 9 action items (A1.1 - A6.4) across 6 priority areas
- ✅ Created risk register with 5 identified risks
- ✅ Set milestone timeline (Sep-Nov 2026)

**Status Snapshot**:
- Data Collected: 60%
- Data Validated: 40%
- Critical Gaps: 3 categories (Halte -220, JPO -300, Pedestrian -20)
- Blockers: 1 (Jakarta Open Data extraction)

**Next Actions**:
1. Fix Puppeteer JSON extraction (Priority 1)
2. Validate & merge halte datasets (Priority 1)
3. Update RAB with actual data (Priority 2)

**Files Modified**:
- `docs/BACKLOG.md` (created)

---

### [YYYY-MM-DD] HH:MM WIB - Template untuk Entry Berikutnya
**Type**: 🔄 Update / 🆕 New / ✅ Completed / 🔴 Blocked  
**Author**: [Name]  
**Branch**: [branch-name]

**Added**:
- [ ] Item baru yang ditambahkan

**Completed**:
- [x] Item yang selesai

**Blocked**:
- [ ] Item yang terblokir + alasan

**Status Changes**:
- Task X: In Progress → Completed
- Task Y: Planned → Blocked (reason: ...)

**Next Actions**:
1. Action item pertama
2. Action item kedua

**Files Modified**:
- `path/to/file1.md`
- `path/to/file2.py`

---

## 🔗 REFERENCES

- Framework: `docs/framework-fase1-solar-panel.md`
- Data Plan: `docs/DATA-ACQUISITION-PLAN.md`
- Solar API Plan: `tools/solar_api/GOOGLE-SOLAR-API-PLAN.md`
- Jakarta Open Data Script: `tools/jakarta_opendata/extract_json_data.js`
- Data Locations:
  - OSM: `data/raw/osm/*.gpkg`
  - Jakarta Open Data: `data/raw/jakarta_opendata/*.json`
