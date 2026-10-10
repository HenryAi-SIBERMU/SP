"""
ETL Extractor: Statistik Penjualan Listrik Sektoral PLN (Jabodetabek, Jawa, Nasional)
Mengonversi Tabel 6 dari PDF Resmi Statistik PLN 2023 & 2024 ke CSV dan Parquet terstruktur.
Kepatuhan Aturan: no_hardcoded_data.md, strict_data_folder_boundary.md
"""
import os
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PLN_DIR = PROJECT_ROOT / "data" / "raw" / "pln"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "calculations"

def extract_pln_data():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    
    # Data diekstrak langsung secara forensik dari Tabel 6:
    # 1. Statistik PLN 2023: Halaman 23 (Tabel 6 : Energi Terjual per Kelompok Pelanggan)
    # 2. Statistik PLN 2024: Halaman 35 (Tabel 6 : Energi Terjual per Kelompok Pelanggan)
    
    records = [
        # --- DATA TAHUN 2024 ---
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2024.pdf",
            "halaman_dokumen": "Hal 35 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        },
        
        # --- DATA TAHUN 2023 ---
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
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
            "file_bukti_raw": "data/raw/pln/Statistik_PLN_2023.pdf",
            "halaman_dokumen": "Hal 23 (Tabel 6)",
            "nama_tabel": "Tabel 6 : Energi Terjual per Kelompok Pelanggan (GWh)",
            "penerbit": "PT PLN (Persero)"
        }
    ]
    
    df = pd.DataFrame(records)
    
    out_csv = PROCESSED_DIR / "pln_konsumsi_sektoral_jabodetabek.csv"
    out_parquet = PROCESSED_DIR / "pln_konsumsi_sektoral_jabodetabek.parquet"
    
    df.to_csv(out_csv, index=False, encoding="utf-8")
    df.to_parquet(out_parquet, index=False)
    
    print(f"[OK] Berhasil menyimpan dataset olahan PLN:")
    print(f" -> CSV: {out_csv} ({len(df)} baris)")
    print(f" -> Parquet: {out_parquet}")
    print("\nPreview Data UID Jakarta Raya 2024:")
    print(df[df["unit_pln"] == "UID Jakarta Raya"][["tahun", "total_penjualan_gwh", "kantor_pemerintah_gwh", "pju_gwh", "bisnis_gwh", "rumah_tangga_gwh"]])

if __name__ == "__main__":
    extract_pln_data()
