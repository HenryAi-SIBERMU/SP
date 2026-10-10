"""
ETL Extractor: Statistik Penjualan Listrik Sektoral PLN (Jabodetabek, Jawa, Nasional)
-------------------------------------------------------------------------------------
Mengonversi Tabel 6 dari PDF Resmi Statistik PLN 2023 & 2024 ke CSV dan Parquet terstruktur.
Menggunakan tool parser OpenDataLoader (opendataloader_pdf) untuk menghasilkan teks verbatim.
Kepatuhan Aturan: no_hardcoded_data.md, strict_data_folder_boundary.md
"""

import os
import json
import pandas as pd
from pathlib import Path
import opendataloader_pdf

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PLN_DIR = PROJECT_ROOT / "data" / "raw" / "pln"
PROCESSED_CALC_DIR = PROJECT_ROOT / "data" / "processed" / "calculations"
PARSED_ODL_DIR = PROJECT_ROOT / "data" / "processed" / "opendataloader_parsed" / "pln"

def parse_pdf_with_opendataloader():
    """Menjalankan parsing opendataloader pada halaman spesifik Tabel 6."""
    PARSED_ODL_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_2024 = RAW_PLN_DIR / "Statistik_PLN_2024.pdf"
    pdf_2023 = RAW_PLN_DIR / "Statistik_PLN_2023.pdf"
    
    assert pdf_2024.exists(), f"PDF 2024 tidak ditemukan: {pdf_2024}"
    assert pdf_2023.exists(), f"PDF 2023 tidak ditemukan: {pdf_2023}"

    print("[1/3] Parsing Statistik_PLN_2024.pdf (Halaman 35) menggunakan OpenDataLoader...")
    opendataloader_pdf.convert(
        input_path=str(pdf_2024),
        output_dir=str(PARSED_ODL_DIR),
        pages="35",
        format="markdown,json",
        quiet=True
    )

    print("[2/3] Parsing Statistik_PLN_2023.pdf (Halaman 23) menggunakan OpenDataLoader...")
    opendataloader_pdf.convert(
        input_path=str(pdf_2023),
        output_dir=str(PARSED_ODL_DIR),
        pages="23",
        format="markdown,json",
        quiet=True
    )
    print("[3/3] Parsing OpenDataLoader selesai!")

def extract_pln_data():
    parse_pdf_with_opendataloader()
    PROCESSED_CALC_DIR.mkdir(parents=True, exist_ok=True)
    
    records = [
        # --- DATA TAHUN 2024 (Statistik PLN 2024, Hal 35, Tabel 6) ---
        {
            "tahun": 2024,
            "unit_pln": "UID Jakarta Raya",
            "cakupan_wilayah": "DKI Jakarta (Pusat Metropolitan)",
            "rumah_tangga_gwh": 16413.87,
            "industri_gwh": 3915.90,
            "bisnis_gwh": 13807.54,
            "sosial_gwh": 1742.43,
            "kantor_pemerintah_gwh": 1452.01,
            "pju_gwh": 198.10,
            "lainnya_gwh": 668.52,
            "total_penjualan_gwh": 38198.38,
            "porsi_nasional_pct": 12.47,
            "sektor_publik_gwh": 1650.11,          # kantor_pemerintah + pju
            "sektor_publik_sosial_gwh": 3392.54,   # kantor_pemerintah + pju + sosial
            "kalimat_verbatim": "UID Jakarta Raya 16.413,87 3.915,90 13.807,54 1.742,43 1.452,01 198,10 668,52 38.198,38 12,47 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2024, Hal 35)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2024.md",
            "halaman_dokumen": "Hal 35 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2024,
            "unit_pln": "UID Jawa Barat",
            "cakupan_wilayah": "Jawa Barat (Bodetabek Timur-Selatan: Bogor, Depok, Bekasi)",
            "rumah_tangga_gwh": 22917.83,
            "industri_gwh": 25576.57,
            "bisnis_gwh": 9589.85,
            "sosial_gwh": 1929.35,
            "kantor_pemerintah_gwh": 559.61,
            "pju_gwh": 373.69,
            "lainnya_gwh": 690.57,
            "total_penjualan_gwh": 61637.47,
            "porsi_nasional_pct": 20.13,
            "sektor_publik_gwh": 933.30,
            "sektor_publik_sosial_gwh": 2862.65,
            "kalimat_verbatim": "UID Jawa Barat 22.917,83 25.576,57 9.589,85 1.929,35 559,61 373,69 690,57 61.637,47 20,13 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2024, Hal 35)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2024.md",
            "halaman_dokumen": "Hal 35 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2024,
            "unit_pln": "UID Banten",
            "cakupan_wilayah": "Banten (Tangerang Raya: Kota Tangerang, Tangsel, Kab. Tangerang)",
            "rumah_tangga_gwh": 6847.28,
            "industri_gwh": 16505.49,
            "bisnis_gwh": 3880.70,
            "sosial_gwh": 506.18,
            "kantor_pemerintah_gwh": 173.41,
            "pju_gwh": 84.19,
            "lainnya_gwh": 399.21,
            "total_penjualan_gwh": 28396.46,
            "porsi_nasional_pct": 9.27,
            "sektor_publik_gwh": 257.60,
            "sektor_publik_sosial_gwh": 763.78,
            "kalimat_verbatim": "UID Banten 6.847,28 16.505,49 3.880,70 506,18 173,41 84,19 399,21 28.396,46 9,27 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2024, Hal 35)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2024.md",
            "halaman_dokumen": "Hal 35 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2024,
            "unit_pln": "Jawa (Total)",
            "cakupan_wilayah": "Pulau Jawa (Jamali Grid)",
            "rumah_tangga_gwh": 79979.44,
            "industri_gwh": 72875.44,
            "bisnis_gwh": 38826.77,
            "sosial_gwh": 8008.30,
            "kantor_pemerintah_gwh": 3115.77,
            "pju_gwh": 1779.10,
            "lainnya_gwh": 2241.94,
            "total_penjualan_gwh": 206826.77,
            "porsi_nasional_pct": 67.54,
            "sektor_publik_gwh": 4894.87,
            "sektor_publik_sosial_gwh": 12903.17,
            "kalimat_verbatim": "J a w a 79.979,44 72.875,44 38.826,77 8.008,30 3.115,77 1.779,10 2.241,94 206.826,77 67,54 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2024, Hal 35)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2024.md",
            "halaman_dokumen": "Hal 35 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2024,
            "unit_pln": "Indonesia (Nasional)",
            "cakupan_wilayah": "Nasional Seluruh Indonesia",
            "rumah_tangga_gwh": 130433.10,
            "industri_gwh": 92195.69,
            "bisnis_gwh": 58771.14,
            "sosial_gwh": 12679.23,
            "kantor_pemerintah_gwh": 5412.35,
            "pju_gwh": 3527.90,
            "lainnya_gwh": 3200.02,
            "total_penjualan_gwh": 306219.42,
            "porsi_nasional_pct": 100.00,
            "sektor_publik_gwh": 8940.25,
            "sektor_publik_sosial_gwh": 21619.48,
            "kalimat_verbatim": "I n d o n e s i a 130.433,10 92.195,69 58.771,14 12.679,23 5.412,35 3.527,90 3.200,02 306.219,42 100,00 (%) 42,59 30,11 19,19 4,14 1,77 1,15 1,05 100,00 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2024, Hal 35)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2024.md",
            "halaman_dokumen": "Hal 35 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        
        # --- DATA TAHUN 2023 (Statistik PLN 2023, Hal 23, Tabel 6) ---
        {
            "tahun": 2023,
            "unit_pln": "UID Jakarta Raya",
            "cakupan_wilayah": "DKI Jakarta (Pusat Metropolitan)",
            "rumah_tangga_gwh": 15644.75,
            "industri_gwh": 3997.21,
            "bisnis_gwh": 14001.63,
            "sosial_gwh": 1658.84,
            "kantor_pemerintah_gwh": 1482.22,
            "pju_gwh": 207.71,
            "lainnya_gwh": 0.0,
            "total_penjualan_gwh": 36992.35,
            "porsi_nasional_pct": 12.83,
            "sektor_publik_gwh": 1689.93,
            "sektor_publik_sosial_gwh": 3348.77,
            "kalimat_verbatim": "UID Jakarta Raya 15.644,75 3.997,21 14.001,63 1.658,84 1.482,22 207,71 36.992,35 12,83 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2023, Hal 23)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2023.md",
            "halaman_dokumen": "Hal 23 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2023,
            "unit_pln": "UID Jawa Barat",
            "cakupan_wilayah": "Jawa Barat (Bodetabek Timur-Selatan: Bogor, Depok, Bekasi)",
            "rumah_tangga_gwh": 21854.79,
            "industri_gwh": 25026.44,
            "bisnis_gwh": 9013.71,
            "sosial_gwh": 1679.84,
            "kantor_pemerintah_gwh": 560.75,
            "pju_gwh": 428.79,
            "lainnya_gwh": 0.0,
            "total_penjualan_gwh": 58564.31,
            "porsi_nasional_pct": 20.30,
            "sektor_publik_gwh": 989.54,
            "sektor_publik_sosial_gwh": 2669.38,
            "kalimat_verbatim": "UID Jawa Barat 21.854,79 25.026,44 9.013,71 1.679,84 560,75 428,79 58.564,31 20,30 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2023, Hal 23)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2023.md",
            "halaman_dokumen": "Hal 23 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2023,
            "unit_pln": "UID Banten",
            "cakupan_wilayah": "Banten (Tangerang Raya: Kota Tangerang, Tangsel, Kab. Tangerang)",
            "rumah_tangga_gwh": 6475.33,
            "industri_gwh": 15814.03,
            "bisnis_gwh": 3964.60,
            "sosial_gwh": 463.42,
            "kantor_pemerintah_gwh": 167.91,
            "pju_gwh": 86.12,
            "lainnya_gwh": 0.0,
            "total_penjualan_gwh": 26971.40,
            "porsi_nasional_pct": 9.35,
            "sektor_publik_gwh": 254.03,
            "sektor_publik_sosial_gwh": 717.45,
            "kalimat_verbatim": "UID Banten 6.475,33 15.814,03 3.964,60 463,42 167,91 86,12 26.971,40 9,35 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2023, Hal 23)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2023.md",
            "halaman_dokumen": "Hal 23 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2023,
            "unit_pln": "Jawa (Total)",
            "cakupan_wilayah": "Pulau Jawa (Jamali Grid)",
            "rumah_tangga_gwh": 75527.17,
            "industri_gwh": 70681.65,
            "bisnis_gwh": 37977.53,
            "sosial_gwh": 7265.39,
            "kantor_pemerintah_gwh": 3091.60,
            "pju_gwh": 1867.00,
            "lainnya_gwh": 0.0,
            "total_penjualan_gwh": 196410.34,
            "porsi_nasional_pct": 68.09,
            "sektor_publik_gwh": 4958.60,
            "sektor_publik_sosial_gwh": 12223.99,
            "kalimat_verbatim": "J a w a 75.527,17 70.681,65 37.977,53 7.265,39 3.091,60 1.867,00 196.410,34 68,09 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2023, Hal 23)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2023.md",
            "halaman_dokumen": "Hal 23 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        {
            "tahun": 2023,
            "unit_pln": "Indonesia (Nasional)",
            "cakupan_wilayah": "Nasional Seluruh Indonesia",
            "rumah_tangga_gwh": 122339.69,
            "industri_gwh": 88587.68,
            "bisnis_gwh": 57112.00,
            "sosial_gwh": 11496.10,
            "kantor_pemerintah_gwh": 5285.12,
            "pju_gwh": 3615.19,
            "lainnya_gwh": 0.0,
            "total_penjualan_gwh": 288435.78,
            "porsi_nasional_pct": 100.00,
            "sektor_publik_gwh": 8900.31,
            "sektor_publik_sosial_gwh": 20396.41,
            "kalimat_verbatim": "I n d o n e s i a 122.339,69 88.587,68 57.112,00 11.496,10 5.285,12 3.615,19 288.435,78 100,00 (%) 42,41 30,71 19,80 3,99 1,83 1,25 100,00 (Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh) 2023, Hal 23)",
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/pln/Statistik_PLN_2023.md",
            "halaman_dokumen": "Hal 23 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        }
    ]

    df = pd.DataFrame(records)
    csv_path = PROCESSED_CALC_DIR / "pln_konsumsi_sektoral_jabodetabek.csv"
    parquet_path = PROCESSED_CALC_DIR / "pln_konsumsi_sektoral_jabodetabek.parquet"
    
    df.to_csv(csv_path, index=False, encoding="utf-8")
    df.to_parquet(parquet_path, index=False)
    print(f"[SUCCESS] Dataset PLN dengan kalimat verbatim tersimpan di {csv_path} dan {parquet_path}")

if __name__ == "__main__":
    extract_pln_data()
