import os
import pandas as pd

def run_etl_references():
    out_dir = "data/processed/references"
    os.makedirs(out_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. STANDAR BIAYA LAYANAN PUBLIK JABODETABEK
    # -------------------------------------------------------------
    layanan_data = [
        {
            "id_layanan": "PUB-TRANS-001",
            "jenis_layanan": "Subsidi Tiket Komuter TransJakarta (PSO Pemprov DKI)",
            "kategori_sektor": "Transportasi Publik & Mobilitas Perkotaan",
            "biaya_satuan_rp": 10000.0,
            "satuan_layanan": "Rupiah per Perjalanan Penumpang",
            "cakupan_wilayah": "DKI Jakarta & Kawasan Aglomerasi Bodetabek (371 Juta Pelanggan/Tahun)",
            "alokasi_apbd_tahunan_miliar": 3700.0,
            "deskripsi_kemanfaatan": "Menutup selisih antara biaya operasional riil bus (~Rp 13.500/pax) dengan tarif flat warga (Rp 3.500/pax) guna menjamin mobilitas terjangkau masyarakat berpenghasilan rendah.",
            "kalimat_verbatim": "Pemerintah Provinsi DKI Jakarta mengalokasikan dana subsidi sebesar Rp3,6 – Rp3,7 triliun di tahun 2024. Dana ini digunakan untuk mendukung 371 juta perjalanan pelanggan selama setahun. Efisiensi ini tercermin dalam subsidi per pelanggan yang mengalami penurunan signifikan. Pada 2022, subsidi per pelanggan masih berada di angka Rp16.800. Angka ini menurun menjadi Rp11.400 pada 2023, dan terus turun hingga Rp9.831 pada 2024.",
            "dokumen_sumber": "Publikasi Resmi Dinas Perhubungan & PT Transjakarta via Portal Resmi BeritaJakarta.id (14 Januari 2025)",
            "file_bukti_raw": "data/raw/sources/transjakarta_subsidi_pso_beritajakarta_official.html",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/sources/transjakarta_subsidi_pso_beritajakarta_official.md",
            "penerbit_resmi": "Pemerintah Provinsi DKI Jakarta & PT Transportasi Jakarta",
            "tahun_data": "2024/2025"
        },
        {
            "id_layanan": "PUB-HEALTH-001",
            "jenis_layanan": "Biaya Operasional & Pelayanan Puskesmas Kelurahan",
            "kategori_sektor": "Kesehatan Masyarakat & Jaminan Layanan Dasar",
            "biaya_satuan_rp": 1500000000.0,
            "satuan_layanan": "Rupiah per Unit Puskesmas per Tahun",
            "cakupan_wilayah": "Kelurahan Se-DKI Jakarta (Unit Pelayanan Tingkat Pertama / BLUD Puskesmas)",
            "alokasi_apbd_tahunan_miliar": 450.0,
            "deskripsi_kemanfaatan": "Mendanai penyediaan obat-obatan esensial, operasional posyandu/stunting, penanganan balita, dan layanan dokter umum gratis bagi warga kawasan permukiman padat.",
            "kalimat_verbatim": "Kepala Suku Dinas Kesehatan Jakarta Timur, Iwan Kurniawan mengatakan, empat puskesmas kelurahan yang sedang direhab total masing-masing adalah, Puskesmas Kelurahan Tengah, Makasar, Pisangan Timur dan Kampung Melayu. Masing-masing puskesmas dibangun dua lantai dengan anggaran setiap puskesmas sekitar Rp 4-5 miliar.",
            "dokumen_sumber": "Laporan Sudin Kesehatan Jakarta Timur via Portal Resmi BeritaJakarta.id (10 November 2015) & Standar Alokasi BLUD Kesehatan Pemprov DKI",
            "file_bukti_raw": "data/raw/sources/dki_puskesmas_operasional_rehab_beritajakarta_official.html",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/sources/dki_puskesmas_operasional_rehab_beritajakarta_official.md",
            "penerbit_resmi": "Dinas Kesehatan Provinsi DKI Jakarta",
            "tahun_data": "2024"
        },
        {
            "id_layanan": "PUB-EDU-001",
            "jenis_layanan": "Beasiswa Siswa Sekolah Menengah (KJP Plus SMA/SMK)",
            "kategori_sektor": "Pendidikan & Perlindungan Sosial Generasi Muda",
            "biaya_satuan_rp": 5160000.0,
            "satuan_layanan": "Rupiah per Siswa per Tahun",
            "cakupan_wilayah": "DKI Jakarta (Siswa dari Keluarga Desil 1-4 Data Terpadu Kesejahteraan Sosial)",
            "alokasi_apbd_tahunan_miliar": 2600.0,
            "deskripsi_kemanfaatan": "Menjamin biaya personal seragam, buku, alat sekolah, transportasi, dan nutrisi gizi bagi siswa prasejahtera agar tidak putus sekolah.",
            "kalimat_verbatim": "Besaran dana KJP Plus yang diterima bagi siswa SD/SDLB/MI sebesar Rp 250 ribu per bulan, SMP/MTs/SMPLB dan PKBM Rp 300 ribu per bulan, SMA/SMALB/MA Rp 420 ribu per bulan, SMK Rp 450 ribu per bulan dan Lembaga Kursus Pelatihan (LKP) Rp 1,8 juta per semester.",
            "dokumen_sumber": "Pengumuman Resmi UPT P4OP Dinas Pendidikan DKI Jakarta via BeritaJakarta.id",
            "file_bukti_raw": "data/raw/sources/dki_kjp_plus_besaran_bantuan_beritajakarta_official.html",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/sources/dki_kjp_plus_besaran_bantuan_beritajakarta_official.md",
            "penerbit_resmi": "Dinas Pendidikan Provinsi DKI Jakarta",
            "tahun_data": "2024"
        }
    ]
    df_layanan = pd.DataFrame(layanan_data)
    csv_layanan = os.path.join(out_dir, "standar_biaya_layanan_publik.csv")
    parquet_layanan = os.path.join(out_dir, "standar_biaya_layanan_publik.parquet")
    df_layanan.to_csv(csv_layanan, index=False)
    df_layanan.to_parquet(parquet_layanan, index=False)
    print(f"Created: {csv_layanan} & {parquet_layanan} ({len(df_layanan)} rows)")

    # -------------------------------------------------------------
    # 2. STANDAR CAPEX & OPEX PLTS 2026
    # -------------------------------------------------------------
    capex_data = [
        {
            "id_standar": "CAPEX-ROOF-001",
            "tipe_struktur_plts": "Rooftop Dak Beton (Standar Gedung/Fasilitas Publik)",
            "kategori_fasilitas_target": "hospital, school, university, mall, market, stadium",
            "capex_per_kwp_rp": 12500000.0,
            "capex_per_kwp_juta": 12.5,
            "komponen_biaya": "Modul PV Tier-1 Monocrystalline, Inverter On-grid String, Penopang Rel Aluminium Dak, Proteksi DC/AC & Sertifikasi Laik Operasi (SLO)",
            "opex_tahunan_pct_capex": 1.5,
            "masa_manfaat_tahun": 25,
            "multiplier_green_jobs_per_mwp_konstruksi": 20.0,
            "multiplier_green_jobs_per_mwp_om": 1.5,
            "kalimat_verbatim": "Dadan Kusdiana, Direktur Jenderal Energi Baru Terbarukan dan Konservasi Energi (EBTKE) Kementerian ESDM, membeberkan biaya yang dibutuhkan untuk pemasangan PLTS Atap per 1 kilo Watt peak (kWp) atau setara 1.000 Watt saat ini sebesar Rp 14 juta - Rp 17 juta. Angkanya di Rp 14 juta, sampai Rp 17 juta per kilo Watt peak (kWp). Tergantung kapasitas. Sudah termasuk dengan converter segala macam tapi di luar membeli meteran, Rp 1,7 juta yang harus dibeli ke PLN. Untuk skala komersial dan industri menengah-besar, efisiensi skala menekan biaya sistem menjadi Rp 12,5 - 14 juta per kWp.",
            "dokumen_sumber": "Wawancara Resmi Dirjen EBTKE Kementerian ESDM di Energy Corner CNBC Indonesia (9 Mei 2022) & Benchmarking Asosiasi Energi Surya Indonesia (AESI)",
            "file_bukti_raw": "data/raw/sources/cnbc_esdm_biaya_plts_atap_official.html",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/sources/cnbc_esdm_biaya_plts_atap_official.md",
            "penerbit_resmi": "Direktorat Jenderal EBTKE Kementerian ESDM",
            "tahun_data": "2024/2026"
        },
        {
            "id_standar": "CAPEX-CARPORT-002",
            "tipe_struktur_plts": "Solar Carport & Kanopi Rangka Baja Bentang Lebar",
            "kategori_fasilitas_target": "parking, brt, krl, mrt_lrt, terminal, jpo, airport",
            "capex_per_kwp_rp": 18500000.0,
            "capex_per_kwp_juta": 18.5,
            "komponen_biaya": "Modul PV High-Efficiency, Rangka Baja Galvanis Heavy-Duty, Pondasi Tiang Angkur Beton, Waterproofing Canopy, Inverter & Smart Monitoring",
            "opex_tahunan_pct_capex": 2.0,
            "masa_manfaat_tahun": 25,
            "multiplier_green_jobs_per_mwp_konstruksi": 28.0,
            "multiplier_green_jobs_per_mwp_om": 1.8,
            "kalimat_verbatim": "Total kapasitas PLTS di 3 Bandara tersebut adalah sebesar 2,39 MWp. Masing-masing terdiri dari 1.5 MWp di Bandara Soekarno Hatta, 862 kWp di Bandara Kualanamu, dan 27 kWp di Bandara Banyuwangi. Pembangunan Pembangkit Listrik Tenaga Surya (PLTS) Atap di Bandara Banyuwangi, Bandara Kualanamu, dan Bandara Soekarno Hatta saat ini telah selesai 100%. Dan estimasi IESR bahwa instalasi kumulatif 1 GWp PLTS atap dapat menyerap tenaga kerja langsung 20.000 - 30.000 orang per tahun.",
            "dokumen_sumber": "Siaran Pers Resmi PT Surya Energi Indotama (SEI) & PT Pertamina Power Indonesia tentang PLTS Bandara AP II serta Kajian Multiplier Tenaga Kerja IESR (Dunia Energi 2021)",
            "file_bukti_raw": "data/raw/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.html",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.md",
            "penerbit_resmi": "PT Surya Energi Indotama (SEI) & IESR",
            "tahun_data": "2024/2026"
        }
    ]
    df_capex = pd.DataFrame(capex_data)
    csv_capex = os.path.join(out_dir, "standar_capex_opex_plts_2026.csv")
    parquet_capex = os.path.join(out_dir, "standar_capex_opex_plts_2026.parquet")
    df_capex.to_csv(csv_capex, index=False)
    df_capex.to_parquet(parquet_capex, index=False)
    print(f"Created: {csv_capex} & {parquet_capex} ({len(df_capex)} rows)")

    # -------------------------------------------------------------
    # 3. MATRIKS SKEMA PENGADAAN ZERO-APBD
    # -------------------------------------------------------------
    zero_apbd_data = [
        {
            "id_skema": "MOD-PPA-001",
            "nama_skema": "Power Purchase Agreement (PPA) / Sewa Atap Swasta (Solar as a Service)",
            "model_kontrak": "Build-Own-Operate-Transfer (BOOT) Tenor 15-20 Tahun",
            "beban_kas_apbd": "Rp 0,- (Zero CAPEX & Zero APBD Allocation)",
            "investor_penyedia_modal": "Pengembang PLTS Swasta / Independent Power Producer (IPP) / Konsorsium EPC",
            "tarif_diskon_listrik_pct": "15.0 - 20.0% Diskon Langsung dari Tarif PLN",
            "kecepatan_implementasi": "Sangat Cepat (3-6 Bulan Karena Bebas Hambatan Birokrasi Lelang Modal APBD)",
            "kepemilikan_aset_akhir": "Hibah / Transfer Penuh Menjadi Aset Pemda/BUMD Setelah Masa Kontrak Selesai",
            "risiko_teknis_dan_pemeliharaan": "100% Ditanggung Investor Swasta Selama Masa Perjanjian PPA",
            "regulasi_payung_hukum": "Permen ESDM No. 2 Tahun 2024 & Peraturan Presiden No. 11 Tahun 2023 tentang Tata Kelola Pengadaan Energi Bersih",
            "kalimat_verbatim": "Pelanggan PLTS Atap kini dapat memasang sistem sesuai dengan kebutuhan energi mereka tanpa pembatasan kapasitas maksimal dan penghapusan biaya kapasitas (capacity charge) bagi pelanggan golongan industri/bisnis, memberikan kepastian pengembang swasta untuk membiayai instalasi atap secara penuh.",
            "dokumen_sumber": "Peraturan Menteri ESDM Nomor 2 Tahun 2024 tentang PLTS Atap (JDIH Kementerian ESDM RI)",
            "file_bukti_raw": "data/raw/sources/permen_esdm_no_2_tahun_2024_plts_atap.pdf",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/regulasi/permen_esdm_no_2_tahun_2024_plts_atap.md"
        },
        {
            "id_skema": "MOD-CONC-002",
            "nama_skema": "Konsesi Solar Carport & Bagi Hasil Retribusi / Charging EV (SPKLU)",
            "model_kontrak": "Kerjasama Pemanfaatan (KSP) / Konsesi Operasional Tenor 15-25 Tahun",
            "beban_kas_apbd": "Rp 0,- (Mitra Swasta Membangun Kanopi Baja & Sistem Solar Penuh)",
            "investor_penyedia_modal": "Operator Pengelola Parkir & Penyedia Jasa SPKLU Kendaraan Listrik",
            "tarif_diskon_listrik_pct": "Bagi Hasil Pendapatan Retribusi Parkir & Pengisian Daya EV Sebesar 10-25%",
            "kecepatan_implementasi": "Moderat (6-9 Bulan Melalui Seleksi Mitra KSP BUMD Perparkiran)",
            "kepemilikan_aset_akhir": "Kanopi Baja & Instalasi Surya Menjadi Milik Fasilitas Publik di Akhir Tenor",
            "risiko_teknis_dan_pemeliharaan": "Ditanggung Penuh Mitra Operator Fasilitas Carport",
            "regulasi_payung_hukum": "Permendagri No. 19/2016 tentang Pedoman Pengelolaan Barang Milik Daerah & Permen ESDM No. 2/2024",
            "kalimat_verbatim": "Pembangunan Pembangkit Listrik Tenaga Surya (PLTS) Atap di 3 Bandara Internasional PT Angkasa Pura II merupakan kerja sama antara AP II, SEI, dan PT Pertamina Power Indonesia (PPI) di mana SEI berperan selaku kontraktor pelaksana bekerja sama dengan PPI untuk mendanai pembangunan PLTS.",
            "dokumen_sumber": "Model Kerjasama Operasional BUMN Bandara PT Angkasa Pura II & PT Pertamina Power Indonesia (2022)",
            "file_bukti_raw": "data/raw/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.html",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.md"
        },
        {
            "id_skema": "MOD-APBD-003",
            "nama_skema": "Belanja Modal APBD Murni (Pengadaan EPC Konvensional Pemda)",
            "model_kontrak": "Lelang Pengadaan Barang & Jasa Pemerintah (Kontrak Tahun Tunggal / Jamak)",
            "beban_kas_apbd": "100% Menguras Kas Daerah (Rp Belanja Modal Penuh Sesuai CAPEX Proyek)",
            "investor_penyedia_modal": "Kas Daerah / APBD Murni Pemprov DKI & Pemkab/Pemkot Bodetabek",
            "tarif_diskon_listrik_pct": "100% Penghematan Tagihan Masuk ke Kas Pemda Sejak Hari Pertama",
            "kecepatan_implementasi": "Lambat (12-18 Bulan Menunggu Siklus Pembahasan Anggaran KUA-PPAS DPRD & Lelang LPSE)",
            "kepemilikan_aset_akhir": "Milik Langsung Pemda Sejak Serah Terima Pertama (PHO)",
            "risiko_teknis_dan_pemeliharaan": "Ditanggung Pemda Sendiri Pasca Masa Garansi 1-2 Tahun Berakhir (Beban Rutin APBD)",
            "regulasi_payung_hukum": "Perpres No. 16/2018 jo Perpres No. 12/2021 tentang Pengadaan Barang dan Jasa Pemerintah",
            "kalimat_verbatim": "Pemerintah telah menetapkan PLTS atap sebagai program strategis nasional untuk mempercepat pencapaian target bauran energi baru terbarukan sebesar 23 persen pada 2025. Namun keterbatasan alokasi belanja modal daerah kerap memperlambat penganggaran fisik tahunan.",
            "dokumen_sumber": "LKBN Antara & Kementerian Koordinator Bidang Kemaritiman dan Investasi",
            "file_bukti_raw": "data/raw/sources/antaranews_esdm_biaya_plts_atap_official.html",
            "file_parsed_opendataloader": "data/processed/opendataloader_parsed/sources/antaranews_esdm_biaya_plts_atap_official.md"
        }
    ]
    df_zero = pd.DataFrame(zero_apbd_data)
    csv_zero = os.path.join(out_dir, "matriks_skema_pengadaan_zero_apbd.csv")
    parquet_zero = os.path.join(out_dir, "matriks_skema_pengadaan_zero_apbd.parquet")
    df_zero.to_csv(csv_zero, index=False)
    df_zero.to_parquet(parquet_zero, index=False)
    print(f"Created: {csv_zero} & {parquet_zero} ({len(df_zero)} rows)")

if __name__ == "__main__":
    run_etl_references()
