"""
tools/economic/generate_procurement_mcda_scoring.py
Pipeline Penentuan Bobot & Evaluasi Multi-Kriteria Model Pengadaan PLTS Atap Publik

Metodologi:
- Expert Judgment & Qualitative Multi-Criteria Decision Analysis (MCDA)
- Mengadopsi Kerangka Analisis Nilai Manfaat Uang (Value for Money / VfM)
  dan Alokasi Risiko Panduan Kerjasama Pemerintah & Badan Usaha (KPBU Bappenas 2020)
  serta Peraturan Presiden No. 38 Tahun 2015.
- Skala Likert/Ordinal: 1 (Sangat Buruk/Berisiko Tinggi) s.d. 10 (Sangat Unggul/Bebas Risiko)
- Dilengkapi pembobotan prioritas (AHP-aligned Weighting) untuk menghasilkan skor tertimbang.
"""

import os
import pandas as pd


def generate_procurement_mcda_matrix():
    # 1. Definisi 5 Kriteria Penilaian, Rasionalisasi, dan Pembobotan Prioritas Fiskal
    data = [
        {
            "id_kriteria": "CRT-001",
            "urutan_tampil": 1,
            "nama_kriteria": "Keamanan Fiskal Kas Daerah (Bebas Belanja Modal)",
            "bobot_prioritas_pct": 30.0,
            "definisi_kriteria": "Tingkat perlindungan kas daerah dari kebutuhan belanja modal awal (CAPEX). Skema bernilai tinggi tidak menyedot APBD di Tahun ke-0.",
            "skor_ppa_sewa_atap": 10,
            "skor_konsesi_carport": 10,
            "skor_apbd_murni": 1,
            "justifikasi_ppa": "100% CAPEX (Rp 4,44 T) ditanggung investor swasta (BOOT). Kas APBD Tahun ke-0 bernilai Rp 0,-.",
            "justifikasi_konsesi": "Mitra operator mendanai penuh konstruksi kanopi baja carport dan infrastruktur SPKLU.",
            "justifikasi_apbd": "Menguras belanja modal APBD secara masif (Rp 4,44 Triliun) sekaligus di tahun anggaran pertama.",
            "dokumen_rujukan": "Panduan Alokasi Risiko KPBU Bappenas (2020) & Permendagri No. 19/2016",
            "file_bukti_raw": "data/raw/sources/permen_esdm_no_2_tahun_2024_plts_atap.pdf"
        },
        {
            "id_kriteria": "CRT-002",
            "urutan_tampil": 2,
            "nama_kriteria": "Kecepatan Eksekusi & Implementasi Lapangan",
            "bobot_prioritas_pct": 20.0,
            "definisi_kriteria": "Kecepatan fase persiapan lelang hingga fase instalasi komersial siap operasi di lapangan.",
            "skor_ppa_sewa_atap": 9,
            "skor_konsesi_carport": 7,
            "skor_apbd_murni": 3,
            "justifikasi_ppa": "Implementasi cepat (3–6 bulan) melalui perjanjian penyediaan jasa energi tanpa hambatan tender fisik APBD.",
            "justifikasi_konsesi": "Waktu moderat (6–9 bulan) melalui uji tuntas seleksi mitra KSP BUMD pengelola fasilitas.",
            "justifikasi_apbd": "Lambat (12–18 bulan) terhambat siklus pengusulan KUA-PPAS ke DPRD dan birokrasi tender LPSE.",
            "dokumen_rujukan": "Perpres No. 16/2018 jo Perpres 12/2021 tentang Pengadaan Barang dan Jasa Pemerintah",
            "file_bukti_raw": "data/raw/sources/antaranews_esdm_biaya_plts_atap_official.html"
        },
        {
            "id_kriteria": "CRT-003",
            "urutan_tampil": 3,
            "nama_kriteria": "Proteksi Risiko Penurunan Kinerja & Kerusakan Teknis",
            "bobot_prioritas_pct": 25.0,
            "definisi_kriteria": "Pengalihan risiko degradasi panel surya, kerusakan inverter, dan biaya pemeliharaan rutin selama masa manfaat 25 tahun.",
            "skor_ppa_sewa_atap": 10,
            "skor_konsesi_carport": 9,
            "skor_apbd_murni": 2,
            "justifikasi_ppa": "100% risiko teknis ditanggung swasta. Pembayaran berbasis ketersediaan daya kWh (Performance-based).",
            "justifikasi_konsesi": "Pemeliharaan struktural kanopi dan operasional SPKLU menjadi kewajiban penuh operator mitra.",
            "justifikasi_apbd": "Setelah masa garansi vendor 1–2 tahun habis, seluruh risiko kerusakan membebani kas rutin APBD.",
            "dokumen_rujukan": "Best Practice Kontrak PPA BOOT Asosiasi Energi Surya Indonesia (AESI)",
            "file_bukti_raw": "data/raw/sources/cnbc_esdm_biaya_plts_atap_official.html"
        },
        {
            "id_kriteria": "CRT-004",
            "urutan_tampil": 4,
            "nama_kriteria": "Kepastian Pengalihan Kepemilikan Aset Jangka Panjang",
            "bobot_prioritas_pct": 10.0,
            "definisi_kriteria": "Jaminan legalitas bahwa sistem PLTS menjadi Barang Milik Daerah (BMD) yang sah bagi pemerintah daerah.",
            "skor_ppa_sewa_atap": 8,
            "skor_konsesi_carport": 8,
            "skor_apbd_murni": 10,
            "justifikasi_ppa": "Aset ditransfer menjadi milik Pemda secara hibah resmi setelah masa tenor kontrak BOOT (15–20 tahun) selesai.",
            "justifikasi_konsesi": "Struktur kanopi baja dan instalasi PLTS diserahkan ke Pemda di akhir masa konsesi.",
            "justifikasi_apbd": "Aset PLTS langsung berstatus milik sah Pemda sejak hari pertama serah terima pekerjaan (PHO).",
            "dokumen_rujukan": "Permendagri No. 19/2016 tentang Pedoman Pengelolaan Barang Milik Daerah (Pasal 116–168)",
            "file_bukti_raw": "data/raw/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.html"
        },
        {
            "id_kriteria": "CRT-005",
            "urutan_tampil": 5,
            "nama_kriteria": "Likuiditas Penghematan Kas Sejak Hari Pertama",
            "bobot_prioritas_pct": 15.0,
            "definisi_kriteria": "Porsi penghematan belanja listrik bulanan yang langsung dapat dinikmati kas daerah tanpa bagi hasil investor.",
            "skor_ppa_sewa_atap": 7,
            "skor_konsesi_carport": 8,
            "skor_apbd_murni": 10,
            "justifikasi_ppa": "Pemda menikmati penghematan berupa diskon tarif 15–20% dari tarif PLN (sisa nilai kWh untuk amortisasi investor).",
            "justifikasi_konsesi": "Pemda memperoleh bagi hasil pendapatan retribusi parkir dan pengisian EV sebesar 10–25%.",
            "justifikasi_apbd": "100% penghematan belanja listrik (Rp 597 Miliar/tahun) dinikmati kas daerah tanpa dipotong pihak manapun.",
            "dokumen_rujukan": "Tarif Tenaga Listrik PT PLN (Persero) 2024 & Permen ESDM No. 2/2024",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf"
        }
    ]

    df = pd.DataFrame(data)

    # 2. Hitung Skor Tertimbang Agregat (Skor Akhir 0-10)
    total_bobot = df["bobot_prioritas_pct"].sum()
    weighted_ppa = (df["skor_ppa_sewa_atap"] * df["bobot_prioritas_pct"]).sum() / total_bobot
    weighted_konsesi = (df["skor_konsesi_carport"] * df["bobot_prioritas_pct"]).sum() / total_bobot
    weighted_apbd = (df["skor_apbd_murni"] * df["bobot_prioritas_pct"]).sum() / total_bobot

    print("=" * 70)
    print("HASIL PEMBOBOTAN MULTI-KRITERIA MODEL PENGADAAN PLTS ATAP JABODETABEK")
    print("=" * 70)
    print(f"Total Bobot Kriteria        : {total_bobot:.1f}%")
    print(f"Skor Tertimbang PPA Swasta  : {weighted_ppa:.2f} / 10.00 (Peringkat 1 - Rekomendasi Utama)")
    print(f"Skor Tertimbang Konsesi     : {weighted_konsesi:.2f} / 10.00 (Peringkat 2 - Sektor Transit/Parkir)")
    print(f"Skor Tertimbang APBD Murni  : {weighted_apbd:.2f} / 10.00 (Peringkat 3 - Beban Fiskal Tinggi)")
    print("=" * 70)

    # 3. Simpan ke data/processed/references/
    out_dir = os.path.join("data", "processed", "references")
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, "matriks_skor_evaluasi_pengadaan.csv")
    parquet_path = os.path.join(out_dir, "matriks_skor_evaluasi_pengadaan.parquet")

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    print(f"Berhasil membuat: {csv_path} ({len(df)} kriteria)")
    print(f"Berhasil membuat: {parquet_path}")

    return df


if __name__ == "__main__":
    generate_procurement_mcda_matrix()
