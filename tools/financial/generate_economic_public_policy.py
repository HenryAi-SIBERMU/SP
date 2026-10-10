import os
import pandas as pd
import numpy as np

def generate_economic_policy_dataset():
    # 1. Load baseline cumulative solar dataset
    solar_path = "data/processed/calculations/pow_solar_kumulatif_summary.csv"
    if not os.path.exists(solar_path):
        raise FileNotFoundError(f"Source file not found: {solar_path}")
    df_solar = pd.read_csv(solar_path)
    
    # 2. Load PLN tariff 2026
    tariff_path = "data/raw/pln/pln_tariff_2026.csv"
    df_tariff = pd.read_csv(tariff_path)
    tariff_p1 = float(df_tariff[df_tariff['category'] == 'P-1/TR']['tariff_rp_kwh'].values[0])
    tariff_b2 = float(df_tariff[df_tariff['category'] == 'B-2/TR']['tariff_rp_kwh'].values[0])
    
    # 3. Load CAPEX & OPEX standards
    capex_std_path = "data/processed/references/standar_capex_opex_plts_2026.csv"
    df_capex_std = pd.read_csv(capex_std_path)
    roof_capex_rp = float(df_capex_std[df_capex_std['id_standar'] == 'CAPEX-ROOF-001']['capex_per_kwp_rp'].values[0])
    carport_capex_rp = float(df_capex_std[df_capex_std['id_standar'] == 'CAPEX-CARPORT-002']['capex_per_kwp_rp'].values[0])
    
    roof_jobs_const = float(df_capex_std[df_capex_std['id_standar'] == 'CAPEX-ROOF-001']['multiplier_green_jobs_per_mwp_konstruksi'].values[0])
    roof_jobs_om = float(df_capex_std[df_capex_std['id_standar'] == 'CAPEX-ROOF-001']['multiplier_green_jobs_per_mwp_om'].values[0])
    
    carport_jobs_const = float(df_capex_std[df_capex_std['id_standar'] == 'CAPEX-CARPORT-002']['multiplier_green_jobs_per_mwp_konstruksi'].values[0])
    carport_jobs_om = float(df_capex_std[df_capex_std['id_standar'] == 'CAPEX-CARPORT-002']['multiplier_green_jobs_per_mwp_om'].values[0])
    
    # 4. Load Public Service standards
    pub_path = "data/processed/references/standar_biaya_layanan_publik.csv"
    df_pub = pd.read_csv(pub_path)
    cost_transit_pax = float(df_pub[df_pub['id_layanan'] == 'PUB-TRANS-001']['biaya_satuan_rp'].values[0])
    cost_puskesmas = float(df_pub[df_pub['id_layanan'] == 'PUB-HEALTH-001']['biaya_satuan_rp'].values[0])
    cost_kjp = float(df_pub[df_pub['id_layanan'] == 'PUB-EDU-001']['biaya_satuan_rp'].values[0])
    
    # Define roof vs carport categories
    carport_categories = {'parking', 'brt', 'krl', 'mrt_lrt', 'terminal', 'jpo', 'airport'}
    
    # Map category display and quadrant priority
    category_meta = {
        'mall': {'display': 'Pusat Perbelanjaan / Mall', 'kuadran': 'Kuadran 1: Quick Wins (Balik Modal Cepat)', 'rekomendasi': 'Skema Sewa Atap Swasta (PPA) / Solar as a Service'},
        'parking': {'display': 'Gedung & Lapangan Parkir', 'kuadran': 'Kuadran 1: Quick Wins (Balik Modal Cepat)', 'rekomendasi': 'Konsesi Solar Carport & Charging EV Berbayar'},
        'market': {'display': 'Pasar Tradisional & Modern', 'kuadran': 'Kuadran 1: Quick Wins (Balik Modal Cepat)', 'rekomendasi': 'Kerjasama Pengelola Pasar & PPA BUMD Pasar Jaya'},
        'school': {'display': 'Sekolah Dasar & Menengah', 'kuadran': 'Kuadran 2: Dividen Pelayanan Publik & Edukasi', 'rekomendasi': 'Penghematan Belanja Rutin Dialihkan ke Beasiswa KJP Plus'},
        'hospital': {'display': 'Rumah Sakit Umum Daerah (RSUD)', 'kuadran': 'Kuadran 2: Dividen Pelayanan Publik & Edukasi', 'rekomendasi': 'Efisiensi Operasional untuk Subsidi Obat & Puskesmas'},
        'university': {'display': 'Kampus & Perguruan Tinggi', 'kuadran': 'Kuadran 2: Dividen Pelayanan Publik & Edukasi', 'rekomendasi': 'Rooftop Surya sebagai Laboratorium Transisi Energi'},
        'stadium': {'display': 'Gelanggang Olahraga & Stadion', 'kuadran': 'Kuadran 2: Dividen Pelayanan Publik & Edukasi', 'rekomendasi': 'Pemanfaatan Dak Stadion untuk Fasilitas Publik Berkelanjutan'},
        'brt': {'display': 'Halte Bus TransJakarta', 'kuadran': 'Kuadran 3: Visibilitas Tinggi & Komuter', 'rekomendasi': 'Kanopi Peneduh Surya & Integrasi PSO Tiket Komuter'},
        'krl': {'display': 'Stasiun KRL Commuter Line', 'kuadran': 'Kuadran 3: Visibilitas Tinggi & Komuter', 'rekomendasi': 'Solar Canopy Overpass & Peningkatan Layanan Transit'},
        'mrt_lrt': {'display': 'Stasiun MRT & LRT', 'kuadran': 'Kuadran 3: Visibilitas Tinggi & Komuter', 'rekomendasi': 'Kanopi Modern Surya Simpul Aglomerasi Modern'},
        'terminal': {'display': 'Terminal Bus Antarkota', 'kuadran': 'Kuadran 3: Visibilitas Tinggi & Komuter', 'rekomendasi': 'Solar Carport Armada Bus & Depo Ramah Lingkungan'},
        'airport': {'display': 'Bandara Internasional (Soetta)', 'kuadran': 'Kuadran 3: Visibilitas Tinggi & Komuter', 'rekomendasi': 'Ekspansi Multi-Megawatt Meniru Benchmark T2/AOCC'},
        'jpo': {'display': 'Jembatan Penyeberangan Orang', 'kuadran': 'Kuadran 3: Visibilitas Tinggi & Komuter', 'rekomendasi': 'Kanopi Peneduh Pejalan Kaki & Penerangan Surya Mandiri'}
    }
    
    # -------------------------------------------------------------------------
    # PART A: CATEGORY LEVEL AGGREGATION
    # -------------------------------------------------------------------------
    cat_rows = []
    grouped = df_solar.groupby('category')
    
    for cat, g in grouped:
        is_carport = cat in carport_categories
        tipe_struktur = "Solar Carport & Kanopi Rangka Baja" if is_carport else "Rooftop Dak Beton Standar"
        capex_per_kwp = carport_capex_rp if is_carport else roof_capex_rp
        jobs_const_mult = carport_jobs_const if is_carport else roof_jobs_const
        jobs_om_mult = carport_jobs_om if is_carport else roof_jobs_om
        
        if cat in ['mall', 'parking', 'market', 'airport']:
            tarif_pln = tariff_b2
            gol_pln = "B-2/TR (Bisnis Menengah)"
        else:
            tarif_pln = tariff_p1
            gol_pln = "P-1/TR (Pelayanan Publik & Sosial)"
            
        points_count = len(g)
        area_m2 = round(float(g['whole_roof_area_m2'].sum()), 2)
        panels_count = int(g['max_panels_count'].sum())
        capacity_kwp = round(float(g['installed_capacity_kwp'].sum()), 2)
        annual_mwh = round(float(g['annual_generation_mwh'].sum()), 2)
        annual_kwh = annual_mwh * 1000.0
        
        capex_total_rp = capacity_kwp * capex_per_kwp
        capex_total_miliar = round(capex_total_rp / 1e9, 2)
        capex_total_triliun = round(capex_total_rp / 1e12, 4)
        
        savings_annual_rp = annual_kwh * tarif_pln
        savings_annual_miliar = round(savings_annual_rp / 1e9, 2)
        savings_annual_juta = round(savings_annual_rp / 1e6, 2)
        
        simple_payback = round(capex_total_rp / savings_annual_rp, 2) if savings_annual_rp > 0 else 0.0
        net_savings_25yr_miliar = round((savings_annual_rp * 25.0 - capex_total_rp) / 1e9, 2)
        
        capacity_mwp = capacity_kwp / 1000.0
        jobs_const = int(round(capacity_mwp * jobs_const_mult))
        jobs_om = int(round(capacity_mwp * jobs_om_mult))
        total_jobs = jobs_const + jobs_om
        
        pax_subsidized = int(round(savings_annual_rp / cost_transit_pax))
        puskesmas_funded = round(savings_annual_rp / cost_puskesmas, 1)
        kjp_funded = int(round(savings_annual_rp / cost_kjp))
        
        meta = category_meta.get(cat, {'display': cat, 'kuadran': 'Kuadran Khusus', 'rekomendasi': 'Penyusunan Rencana Aksi'})
        
        verbatim = (
            f"Kategori {meta['display']} memiliki potensi kapasitas {capacity_kwp:,.1f} kWp dengan produksi "
            f"{annual_mwh:,.2f} MWh/tahun. Kebutuhan modal Rp {capex_total_miliar:,.2f} Miliar menghasilkan penghematan "
            f"belanja listrik Rp {savings_annual_miliar:,.2f} Miliar/tahun (Simple Payback: {simple_payback} tahun, "
            f"setara {pax_subsidized:,} perjalanan komuter bersubsidi)."
        )
        
        cat_rows.append({
            'category': cat,
            'category_display': meta['display'],
            'total_points': points_count,
            'total_area_m2': area_m2,
            'total_panels_count': panels_count,
            'total_capacity_kwp': capacity_kwp,
            'total_annual_generation_mwh': annual_mwh,
            'tipe_struktur_plts': tipe_struktur,
            'capex_per_kwp_rp': capex_per_kwp,
            'total_capex_miliar': capex_total_miliar,
            'total_capex_triliun': capex_total_triliun,
            'tarif_pln_rp_per_kwh': tarif_pln,
            'golongan_tarif_pln': gol_pln,
            'total_savings_annual_miliar': savings_annual_miliar,
            'total_savings_annual_juta': savings_annual_juta,
            'simple_payback_years': simple_payback,
            'net_cumulative_savings_25yr_miliar': net_savings_25yr_miliar,
            'green_jobs_konstruksi_orang': jobs_const,
            'green_jobs_om_orang': jobs_om,
            'total_green_jobs_orang': total_jobs,
            'ekuivalensi_tiket_komuter_pax': pax_subsidized,
            'ekuivalensi_puskesmas_unit': puskesmas_funded,
            'ekuivalensi_beasiswa_siswa': kjp_funded,
            'kuadran_prioritas': meta['kuadran'],
            'rekomendasi_kebijakan': meta['rekomendasi'],
            'id_standar_capex': 'CAPEX-CARPORT-002' if is_carport else 'CAPEX-ROOF-001',
            'file_bukti_raw_capex': 'data/raw/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.html' if is_carport else 'data/raw/sources/cnbc_esdm_biaya_plts_atap_official.html',
            'file_bukti_raw_tarif': 'data/raw/pln/Statistik_PLN_2024.pdf',
            'file_sumber_solar': 'data/processed/calculations/pow_solar_kumulatif_summary.csv',
            'ringkasan_model_tekno_ekonomi': verbatim,
            'kalimat_verbatim': verbatim
        })
        
    df_summary = pd.DataFrame(cat_rows)
    df_summary = df_summary.sort_values(by='total_capacity_kwp', ascending=False).reset_index(drop=True)
    
    out_csv = "data/processed/calculations/pow_solar_ekonomi_kebijakan.csv"
    out_parquet = "data/processed/calculations/pow_solar_ekonomi_kebijakan.parquet"
    df_summary.to_csv(out_csv, index=False)
    df_summary.to_parquet(out_parquet, index=False)
    print(f"Created: {out_csv} & {out_parquet} ({len(df_summary)} categories)")
    
    # -------------------------------------------------------------------------
    # PART B: POINT-LEVEL ECONOMIC DATASET (2,100 POINTS)
    # -------------------------------------------------------------------------
    detail_records = []
    for _, row in df_solar.iterrows():
        cat = row['category']
        is_carport = cat in carport_categories
        tipe_struktur = "Solar Carport & Kanopi Rangka Baja" if is_carport else "Rooftop Dak Beton Standar"
        capex_per_kwp = carport_capex_rp if is_carport else roof_capex_rp
        jobs_const_mult = carport_jobs_const if is_carport else roof_jobs_const
        jobs_om_mult = carport_jobs_om if is_carport else roof_jobs_om
        
        if cat in ['mall', 'parking', 'market', 'airport']:
            tarif_pln = tariff_b2
            gol_pln = "B-2/TR (Bisnis Menengah)"
        else:
            tarif_pln = tariff_p1
            gol_pln = "P-1/TR (Pelayanan Publik & Sosial)"
            
        cap_kwp = float(row['installed_capacity_kwp'])
        gen_mwh = float(row['annual_generation_mwh'])
        gen_kwh = gen_mwh * 1000.0
        
        capex_rp = cap_kwp * capex_per_kwp
        capex_juta = round(capex_rp / 1e6, 2)
        
        savings_rp = gen_kwh * tarif_pln
        savings_juta = round(savings_rp / 1e6, 2)
        
        payback = round(capex_rp / savings_rp, 2) if savings_rp > 0 else 0.0
        
        cap_mwp = cap_kwp / 1000.0
        jobs_const = round(cap_mwp * jobs_const_mult, 3)
        jobs_om = round(cap_mwp * jobs_om_mult, 3)
        
        meta = category_meta.get(cat, {'display': cat, 'kuadran': 'Kuadran Khusus', 'rekomendasi': 'Penyusunan Rencana Aksi'})
        
        pax_subsidized = int(round(savings_rp / cost_transit_pax))
        
        verbatim = (
            f"Fasilitas {row['asset_name']} ({row['city_regency']}) berpotensi kapasitas {cap_kwp:.1f} kWp "
            f"dengan estimasi penghematan listrik Rp {savings_juta:,.2f} Juta/tahun dan titik impas {payback} tahun."
        )
        
        detail_records.append({
            'asset_id': row['asset_id'],
            'asset_name': row['asset_name'],
            'category': cat,
            'category_display': meta['display'],
            'city_regency': row['city_regency'],
            'postal_code': row['postal_code'],
            'lat': row['google_center_lat'],
            'lon': row['google_center_lon'],
            'quality_tier': row['quality_tier'],
            'whole_roof_area_m2': row['whole_roof_area_m2'],
            'max_panels_count': row['max_panels_count'],
            'installed_capacity_kwp': cap_kwp,
            'annual_generation_mwh': gen_mwh,
            'tipe_struktur_plts': tipe_struktur,
            'capex_per_kwp_rp': capex_per_kwp,
            'capex_total_rp': capex_rp,
            'capex_total_juta': capex_juta,
            'tarif_pln_rp_per_kwh': tarif_pln,
            'golongan_tarif_pln': gol_pln,
            'savings_annual_rp': savings_rp,
            'savings_annual_juta': savings_juta,
            'simple_payback_years': payback,
            'green_jobs_konstruksi_person_years': jobs_const,
            'green_jobs_om_permanent_jobs': jobs_om,
            'ekuivalensi_tiket_komuter_pax': pax_subsidized,
            'kuadran_prioritas': meta['kuadran'],
            'rekomendasi_kebijakan': meta['rekomendasi'],
            'id_standar_capex': 'CAPEX-CARPORT-002' if is_carport else 'CAPEX-ROOF-001',
            'file_bukti_raw_capex': 'data/raw/sources/plts_soekarno_hatta_t2_sei_ap2_ppi_official.html' if is_carport else 'data/raw/sources/cnbc_esdm_biaya_plts_atap_official.html',
            'file_bukti_raw_tarif': 'data/raw/pln/Statistik_PLN_2024.pdf',
            'ringkasan_model_tekno_ekonomi': verbatim,
            'kalimat_verbatim': verbatim
        })
        
    df_detail = pd.DataFrame(detail_records)
    out_detail_csv = "data/processed/calculations/pow_solar_2000_ekonomi_detail.csv"
    out_detail_parquet = "data/processed/calculations/pow_solar_2000_ekonomi_detail.parquet"
    df_detail.to_csv(out_detail_csv, index=False)
    df_detail.to_parquet(out_detail_parquet, index=False)
    print(f"Created: {out_detail_csv} & {out_detail_parquet} ({len(df_detail)} points)")
    
    # Summary
    print("\n=== SUMMARY REKAPITULASI SELESAI DENGAN SUKSES ===")

if __name__ == "__main__":
    generate_economic_policy_dataset()
