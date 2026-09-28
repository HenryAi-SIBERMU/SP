---
description: Aturan Mutlak Larangan Data Hardcoded dalam Skrip, Dashboard, dan Tool Analisis (Zero Hardcoded Data Rule)
---

# Aturan Mutlak Larangan Data Hardcoded (Zero Hardcoded Data Rule)

Aturan ini mengikat seluruh agen AI dan pengembang di seluruh repositori ini tanpa pengecualian.

---

### 1. DEFINISI & PERBEDAAN DATA HARDCODED VS DATA PUBLIKASI SAH

Untuk menjaga integritas ilmiah dan reproduktifitas riset, agen wajib membedakan dua kategori data:

1. **Hardcoding Faktual Liar / Arbitrary (DIHARAMKAN):**
   - Menaruh angka statis di dalam baris kode Python/Streamlit tanpa file dataset fisik dan tanpa berkas bukti dokumen (misal: `col: "manual", value: 2253.0` atau `luas = 4000.0 if entitas == 'BTIIG' else ...`).
   - Membuat kamus statis penampung angka di memori script (`{"Vale": 118017, "Kalla": 200}`).
   - Memotong atau memanipulasi angka CSV langsung di baris kode tanpa dasar (misal memotong paksa konsesi PT GKP dari 1.808,9 Ha menjadi 1.000 Ha).

2. **Data Sekunder Berbasis Publikasi Riset & Dokumen Resmi (SAH & VALID):**
   - Data angka yang disarikan dari dokumen publikasi resmi (seperti **Laporan 50 Taipan Terkaya CELIOS**, laporan tahunan emiten BEI, dokumen AMDAL terpadu, penetapan PSN / IUKI Kemenperin, masterplan kawasan, atau LHKPN KPK) adalah **data sekunder yang sah (*legitimate curated secondary data*)**.
   - Data ini **BUKAN** data fiktif dan memiliki legitimasi bukti dokumen, **DENGAN SYARAT berkas fisik buktinya tersimpan di repositori**.

---

### 2. PROTOKOL DORKING & PENGELOLAAN DATA PUBLIKASI: WAJIB BUKTI FORENSIK DI `data/raw/`

Jika agen melakukan pencarian dokumen eksternal via dorking, OSINT, web crawling, atau mengutip laporan resmi/PDF:

1. **Wajib Simpan Berkas Bukti Fisik (*Forensic Proof*) di `data/raw/`**:
   - Seluruh berkas sumber asli (file `.pdf` dokumen AMDAL/laporan riset/SK, unduhan snapshot web `.html`/`.mhtml`, atau arsip resmi) **WAJIB diunduh dan disimpan secara fisik ke folder `data/raw/evidence_dorking/` atau `data/raw/sources/`**.
   - **DILARANG KERAS** mengklaim angka dari hasil dorking atau kutipan publikasi jika berkas fisiknya tidak ada di folder `data/`. Angka tanpa berkas bukti fisik di repositori dianggap sebagai **improvisasi liar tanpa dasar (*unsubstantiated fabrication*)** dan ditolak.
2. **Ekstraksi ke File Terstruktur di `data/processed/`**:
   - Data dari berkas bukti tersebut dibukukan ke dalam file CSV fisik di `data/processed/` (contoh: `data/processed/sulawesi_kawasan_industri_smelter.csv`).
   - Wajib memuat kolom metadata sitasi lengkap:
     * `nama_entitas`
     * `nilai` & `satuan`
     * `file_bukti_raw`: Path file fisik dokumen bukti di `data/raw/` (misal: `data/raw/evidence_dorking/amdal_vdni_morosi.pdf`).
     * `halaman_sk`: Halaman dokumen atau nomor SK penetapan.
     * `tahun_rilis`: Tahun publikasi dokumen.
3. **Skrip Hanya Mengonsumsi File CSV**:
   - Skrip Python (`.py`), notebook, maupun dashboard Streamlit **hanya boleh membaca data via fungsi pembacaan file** (`pandas.read_csv(...)`, `geopandas.read_file(...)`).
   - **Hasil Mutlak:**
     * Landasan data 100% berbasis dokumen bukti fisik yang dapat diverifikasi (*forensically verifiable*).
     * Skrip Python bersih 100% dari *hardcoded magic numbers*.
     * Batasan repositori `data/` terjaga penuh.

---

### 3. PRINSIP SINGLE SOURCE OF TRUTH (FOLDER `data/`)
- Kode program bertindak **murni sebagai pipa pemrosesan (*data processing pipeline*)**: membaca, membersihkan, menggabungkan (*join/merge*), memodelkan, dan memvisualisasikan.
- Kode program **BUKAN tempat penyimpanan data (*data store*)**.
- Seluruh data faktual, atribut perusahaan, konsesi, kapasitas listrik, status perizinan, dan angka statistik **WAJIB tersimpan dalam format file terstruktur di folder `data/`**.

---

### 4. AUDITABILITY & DATA LINEAGE TRANSPARENCY
Setiap angka yang muncul pada tabel, grafik, kartu metrik, maupun laporan Word/PDF wajib dapat diaudit (*traceable*) hingga ke:
- **Nama file fisik** di `data/` (lengkap dengan path relatifnya).
- **Nama kolom / atribut** yang diambil.
- **Identitas baris / query filter** (misalnya `id_izin`, nomor SK, atau `row_index`).

Jika suatu angka tidak dapat dibuktikan asal-usulnya dari file fisik di folder `data/`, angka tersebut dikategorikan sebagai **data tidak sah (*invalid / unverified data*)** dan dilarang ditampilkan ke pengguna atau dimasukkan ke laporan resmi.