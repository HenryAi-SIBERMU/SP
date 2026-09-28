---
description: Larangan Mutlak Mengagregasi, Memvisualisasi, atau Menarik Kesimpulan di Luar Folder Data yang Dihimpun (Strict Local Dataset Boundary)
---

# Aturan Mutlak Batasan Dataset (Strict Local Dataset Boundary)

Aturan ini mengikat seluruh agen AI dalam repositori ini tanpa pengecualian:

---

### 1. LARANGAN KERAS MENGAGREGASI DI LUAR FOLDER DATASET INTERNAL
- **DILARANG KERAS** melakukan agregasi, kompilasi, membuat metrik baru, atau memvisualisasikan angka yang sumber primernya tidak ada di dalam folder `data/` (khususnya `data/processed/` dan `data/raw/`).
- Seluruh grafik, tabel, metric card, dan narasi temuan harus memiliki **data lineage (garis keturunan data)** yang dapat dibuktikan secara langsung ke nama file CSV/GeoJSON, nama kolom, dan nomor baris data yang dihimpun.

---

### 2. DILARANG MENCIPTAKAN "NAMA DATASET SEMU / FIKTIF"
- **DILARANG KERAS** mencantumkan sitasi atau label sumber data yang seolah-olah merupakan file lokal (seperti "HPL Kemenperin", "Registri Kawasan Industri") jika file fisik tersebut tidak benar-benar ada di dalam direktori `data/`.
- Jika sebuah data merupakan data sekunder eksternal, dilarang menyamarkannya sebagai dataset internal.

---

### 3. LARANGAN HARDCODING / INJEKSI MANUAL PADA SKRIP KALKULASI
- Dilarang menyisipkan angka manual (`col: "manual", value: ...`) di dalam skrip Python untuk menambal data yang tidak ada di dataset internal tanpa mencatat file fisik sumbernya di folder `data/`.
- Jika sebuah entitas penting (seperti kawasan industri smelter) belum tercakup di dataset minerba ESDM, agen **WAJIB menghimpun dan membuat file dataset terstruktur baru di folder `data/processed/` terlebih dahulu** sebelum melakukan analisis/agregasi.

---

### 4. KEWAJIBAN BUKTI FORENSIK DORKING / OSINT / WEB SEARCH (MANDATORY RAW PROOF)
Jika agen melakukan penelusuran eksternal via dorking, OSINT, scraping web, atau ekstraksi publikasi resmi (PDF, AMDAL, SK, LHKPN, Laporan Riset):
- **WAJIB Simpan Berkas Fisik Bukti ke `data/raw/`**: Seluruh dokumen asli hasil temuan (berkas `.pdf`, unduhan halaman web `.html`/`.mhtml`, arsip laporan resmi) **WAJIB diunduh dan disimpan secara fisik ke dalam folder `data/raw/evidence_dorking/` atau `data/raw/sources/`**.
- **Larangan Mengutip Tanpa File Bukti Fisik**: **DILARANG KERAS** menggunakan atau memasukkan angka hasil dorking/web ke dalam analisis jika berkas unduhannya tidak tersimpan di folder `data/raw/`. Angka yang masuk tanpa berkas bukti fisik di repositori dikategorikan sebagai **improvisasi liar tanpa dasar (*unsubstantiated fabrication*)** dan otomatis ditolak oleh sistem.
- **Relasi Lineage**: Setiap baris data di `data/processed/` yang dihasilkan dari proses dorking wajib mencantumkan kolom path file bukti fisik di `data/raw/` dan nomor halaman referensinya.

---

### 5. PRINSIP AUDIT KELENGKAPAN DATA (DATASET GAP DISCLOSURE)
- Jika ditemukan gap antara ruang lingkup riset (misal: hilirisasi smelter) dengan cakupan dataset yang dihimpun (misal: hanya mencakup tambang hulu ESDM), agen wajib melaporkan kondisi riil tersebut secara jujur kepada tim/pengguna terlebih dahulu, bukan menutupinya dengan asumsi tersembunyi.