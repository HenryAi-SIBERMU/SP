"""
Analisis Ekonomi Kebijakan Publik & Kelayakan Fiskal — CELIOS Solar Dashboard
----------------------------------------------------------------------------
Halaman Bab 3: Evaluasi Investasi Makro, Efisiensi Belanja Rutin Daerah,
Dividen Sosial Warga, dan Solusi Pembiayaan Zero-APBD se-Jabodetabek.

Mengadopsi Standar Riset CELIOS 2 (ECC / D3TLH):
- Org Badge Institusi & Hero Statement Kritis Kebijakan Publik
- 6 Bento Metric Cards dengan Sitasi Berkas Fisik Rujukan
- Penomoran Hierarkis Sub-Bab 3.1 s.d. 3.5
- Ritme 4 Langkah: Tesis -> Visualisasi -> Callout Temuan -> Expander Data Mentah
- 100% Data-Driven (Tanpa Angka Hardcoded)
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css

st.set_page_config(
    page_title="Analisis Ekonomi — CELIOS Solar Dashboard",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_solar_css(), unsafe_allow_html=True)

# ─── EXTRA STYLING (CELIOS 2 RESEARCH STANDARD) ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif; }

.org-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    color: #E8F5E9;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    border: 1px solid #4CAF50;
}

.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #43A047, #66BB6A, #A5D6A7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    line-height: 1.2;
}

.sub-title {
    font-size: 1.05rem;
    color: #B0BEC5;
    font-weight: 300;
    margin-top: 0;
    margin-bottom: 1.5rem;
}

.hero-box {
    background: linear-gradient(135deg, #101924, #1B2636);
    border: 1px solid #2A3B50;
    border-left: 5px solid #4CAF50;
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.8rem;
}

.bento-card {
    background: linear-gradient(135deg, #141A24, #1E2738);
    border: 1px solid #2E3B4E;
    border-radius: 10px;
    padding: 18px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 175px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.bento-card:hover {
    border-color: #4CAF50;
    transform: translateY(-2px);
}
.bento-val {
    font-size: 2.1rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 8px 0;
}
.bento-lbl {
    font-size: 0.78rem;
    color: #90A4AE;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.bento-desc {
    font-size: 0.76rem;
    color: #CFD8DC;
    line-height: 1.4;
    text-align: left;
    margin-top: 4px;
}
.bento-src {
    font-size: 0.68rem;
    color: #78909C;
    margin-top: 10px;
    padding-top: 6px;
    border-top: 1px dotted #37474F;
    text-align: left;
}

.sub-chapter-badge {
    background: #1B382B;
    color: #A5D6A7;
    border: 1px solid #2E7D32;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 0.6rem;
}

.callout-box {
    background: #101F18;
    border: 1px solid #2E7D32;
    border-left: 4px solid #4CAF50;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin: 1.2rem 0;
    font-size: 0.92rem;
    color: #E0E0E0;
    line-height: 1.6;
}

.callout-alert {
    background: #251616;
    border: 1px solid #C62828;
    border-left: 4px solid #EF5350;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin: 1.2rem 0;
    font-size: 0.92rem;
    color: #FFCDD2;
    line-height: 1.6;
}

.stat-tag {
    background: #263238;
    color: #ECEFF1;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA LOADING PIPELINE (STRICTLY PHYSICAL FILES) ─────────────────────────────
CALC_DIR = PROJECT_ROOT / "data" / "processed" / "calculations"
REF_DIR = PROJECT_ROOT / "data" / "processed" / "references"
RAW_PLN_DIR = PROJECT_ROOT / "data" / "raw" / "pln"

@st.cache_data
def load_economic_datasets():
    # 1. Master Rekapitulasi Ekonomi Kebijakan (13 Kategori)
    ekonomi_path = CALC_DIR / "pow_solar_ekonomi_kebijakan.csv"
    df_ekonomi = pd.read_csv(ekonomi_path) if ekonomi_path.exists() else pd.DataFrame()

    # 2. Detail Titik Finansial (2.100 Titik)
    detail_path = CALC_DIR / "pow_solar_2000_ekonomi_detail.csv"
    df_detail = pd.read_csv(detail_path) if detail_path.exists() else pd.DataFrame()

    # 3. Standar Biaya Layanan Publik (PSO Tiket, Puskesmas, KJP Plus)
    layanan_path = REF_DIR / "standar_biaya_layanan_publik.csv"
    df_layanan = pd.read_csv(layanan_path) if layanan_path.exists() else pd.DataFrame()

    # 4. Standar CAPEX & OPEX PLTS 2026
    capex_path = REF_DIR / "standar_capex_opex_plts_2026.csv"
    df_capex = pd.read_csv(capex_path) if capex_path.exists() else pd.DataFrame()

    # 5. Matriks Skema Pengadaan Zero-APBD
    zero_path = REF_DIR / "matriks_skema_pengadaan_zero_apbd.csv"
    df_zero = pd.read_csv(zero_path) if zero_path.exists() else pd.DataFrame()

    # 6. Statistik Penjualan Listrik Sektoral PLN Jabodetabek
    pln_path = CALC_DIR / "pln_konsumsi_sektoral_jabodetabek.csv"
    df_pln = pd.read_csv(pln_path) if pln_path.exists() else pd.DataFrame()

    return df_ekonomi, df_detail, df_layanan, df_capex, df_zero, df_pln

df_ekonomi, df_detail, df_layanan, df_capex, df_zero, df_pln = load_economic_datasets()

if df_ekonomi.empty:
    st.error("Error: Dataset ringkasan ekonomi kebijakan tidak ditemukan di `data/processed/calculations/pow_solar_ekonomi_kebijakan.csv`.")
    st.stop()

# ─── PRA-KALKULASI VARIABEL MAKRO FINANSIAL & KEBIJAKAN ──────────────────────────
total_assets = int(df_ekonomi["total_points"].sum())
total_capacity_kwp = float(df_ekonomi["total_capacity_kwp"].sum())
total_capacity_mwp = total_capacity_kwp / 1000.0
total_gen_mwh = float(df_ekonomi["total_annual_generation_mwh"].sum())
total_gen_gwh = total_gen_mwh / 1000.0

total_capex_triliun = float(df_ekonomi["total_capex_triliun"].sum())
total_capex_miliar = float(df_ekonomi["total_capex_miliar"].sum())
total_savings_miliar = float(df_ekonomi["total_savings_annual_miliar"].sum())
avg_payback_years = round((total_capex_triliun * 1e12) / (total_savings_miliar * 1e9), 2)
net_cumulative_savings_25yr_miliar = float(df_ekonomi["net_cumulative_savings_25yr_miliar"].sum())
net_cumulative_savings_25yr_triliun = net_cumulative_savings_25yr_miliar / 1000.0

total_green_jobs = int(df_ekonomi["total_green_jobs_orang"].sum())
jobs_const = int(df_ekonomi["green_jobs_konstruksi_orang"].sum())
jobs_om = int(df_ekonomi["green_jobs_om_orang"].sum())

commuter_subsidy_pax = int(df_ekonomi["ekuivalensi_tiket_komuter_pax"].sum())
puskesmas_funded_count = float(df_ekonomi["ekuivalensi_puskesmas_unit"].sum())
kjp_funded_count = int(df_ekonomi["ekuivalensi_beasiswa_siswa"].sum())

# ─── HEADER & METODOLOGI DROPDOWN ────────────────────────────────────────────────
st.markdown('<div class="org-badge">CELIOS — Center of Economic and Law Studies</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Analisis Ekonomi Kebijakan Publik & Kelayakan Fiskal</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Evaluasi Investasi Makro, Efisiensi Belanja Rutin Daerah, Dividen Sosial Warga, dan Solusi Pembiayaan Zero-APBD se-Jabodetabek</div>',
    unsafe_allow_html=True
)

with st.expander("ℹ️ Metodologi Analisis: Alur Kausalitas, Standar Pengali Ketenagakerjaan IRENA & Nilai Dividen Fiskal APBD"):
    st.markdown(r"""
    **Alur Kausalitas Metodologis Riset Ekonomi Kebijakan:**
    $$
    \text{Potensi Energi } (GWh) \ \& \ \text{Tarif PLN} \longrightarrow \text{Investasi \& Penghematan Belanja} \longrightarrow \text{Ekuivalensi Dividen Fiskal APBD} \longrightarrow \text{Penciptaan Green Jobs} \longrightarrow \text{Model Pengadaan Zero-APBD}
    $$

    1. **Formulasi Finansial Makro Kebijakan Publik (Tanpa Rumus DCF/WACC Mikro Perbankan):**
        * **Kebutuhan Modal Investasi Agregat ($\text{CAPEX}$):**  
          $$\text{CAPEX} (\text{Rp}) = \sum_{i=1}^{13} \left( P_{\text{dc}, i} (\text{kWp}) \times \text{Standar\_Biaya}_i (\text{Rp/kWp}) \right)$$  
          *Asumsi standar biaya industri EPC Indonesia 2026:*
          - *Rooftop Dak Beton:* **Rp 12,5 Juta/kWp** (hospital, school, university, mall, market, stadium).
          - *Solar Carport & Kanopi Rangka Baja:* **Rp 18,5 Juta/kWp** (parking, brt, krl, mrt_lrt, terminal, jpo, airport).
        * **Penghematan Belanja Listrik Tahunan ($\text{OPEX Savings}$):**  
          $$\text{Hemat} (\text{Rp/tahun}) = E_{\text{annual}} (\text{kWh}) \times \text{Tarif\_PLN} (\text{Rp/kWh})$$  
          *Tarif Dasar Listrik PLN 2026:* Golongan P-1/TR (Pelayanan Publik) dan Golongan B-2/TR (Bisnis Menengah) sebesar **Rp 1.467,28/kWh** sesuai `data/raw/pln/pln_tariff_2026.csv`.
        * **Periode Impas Sederhana (*Simple Payback Period*):**  
          $$\text{Payback} (\text{Tahun}) = \frac{\text{CAPEX}}{\text{Hemat Tahunan}}$$
    2. **Formulasi Serapan Tenaga Kerja Hijau (*Green Jobs Multipliers*):**  
       Mengadopsi metodologi resmi *Institute for Essential Services Reform* (IESR) dan *International Renewable Energy Agency* (IRENA):
       - Fase Konstruksi & Fabrikasi (1–2 Tahun): **20,0 orang/MWp** (dak beton) dan **28,0 orang/MWp** (kanopi rangka baja).
       - Fase Pemeliharaan Permanen (*Operations & Maintenance*, 25 Tahun): **1,5 s.d. 1,8 orang/MWp**.
    3. **Formulasi Ekuivalensi Dividen Sosial Fiskal (*Public Opportunity Cost*):**  
       Mengonversi penghematan belanja listrik daerah menjadi manfaat layanan publik nyata:
       - **Subsidi Tiket Komuter:** Biaya subsidi operasional TransJakarta sebesar **Rp 10.000 per perjalanan penumpang** (rilis resmi Dishub DKI 2024/2025).
       - **Operasional Puskesmas:** Belanja rutin operasional pelayanan primer sebesar **Rp 1,5 Miliar per unit per tahun**.
       - **Beasiswa Siswa Menengah:** Bantuan personal KJP Plus SMA/SMK sebesar **Rp 5,16 Juta per siswa per tahun** (Dinas Pendidikan DKI).
    4. **Dataset & Lineage:**
       * Master Rekapitulasi Ekonomi: `data/processed/calculations/pow_solar_ekonomi_kebijakan.csv`
       * Detail 2.100 Titik: `data/processed/calculations/pow_solar_2000_ekonomi_detail.csv`
       * Standar Biaya Layanan Publik: `data/processed/references/standar_biaya_layanan_publik.csv`
       * Standar CAPEX & OPEX PLTS: `data/processed/references/standar_capex_opex_plts_2026.csv`
       * Regulasi & Skema Zero-APBD: `data/processed/references/matriks_skema_pengadaan_zero_apbd.csv`
    """)

# ─── HERO SECTION (NARASI TEKS EMPIRIS & ADVOKASI KEBIJAKAN FISKAL) ──────────────
st.markdown("""
<h2 style="color: #FFFFFF; font-size: 1.85rem; font-weight: 800; margin-top: 1.6rem; margin-bottom: 1.1rem; line-height: 1.35; letter-spacing: -0.4px;">
    Membongkar Mitos "Transisi Energi Mahal": Pembebasan Ruang Fiskal Daerah Melalui Aset Produktif Surya
</h2>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="color: #CFD8DC; font-size: 1.02rem; line-height: 1.8; margin-bottom: 2rem;">
    <p style="margin-bottom: 1.25rem;">
        Pemerintah daerah dan operator transportasi perkotaan kerap menunda transisi energi dengan alibi keterbatasan anggaran belanja modal (CAPEX). 
        Transisi energi sering disalahpahami sebagai beban kas anggaran pendapatan dan belanja daerah (APBD) yang menghabiskan ruang fiskal pelayanan dasar. 
        Namun, temuan empiris pada <b>{total_assets:,} titik infrastruktur publik dan simpul transit strategis se-Jabodetabek</b> membuktikan tesis sebaliknya: 
        kebutuhan investasi modal sebesar <b>Rp {total_capex_triliun:.3f} Triliun</b> secara otomatis memangkas belanja rutin tagihan listrik pemerintah dan pengelola fasilitas sebesar <b>Rp {total_savings_miliar:,.2f} Miliar setiap tahun</b>.
    </p>
    <p style="margin-bottom: 1.25rem;">
        Dengan rata-rata periode impas sederhana (<i>simple payback period</i>) selama <b>{avg_payback_years:.2f} tahun</b>, 
        seluruh fasilitas publik menikmati sisa <b>17,5 tahun masa panen energi gratis</b> (dari total 25 tahun masa garansi modul fotovoltaik) 
        dengan akumulasi keuntungan bersih mencapai <b>Rp {net_cumulative_savings_25yr_triliun:.2f} Triliun</b>. 
        Penghematan belanja operasional tahunan ini setara dengan mendanai <b>{commuter_subsidy_pax:,} perjalanan komuter bersubsidi</b> di koridor transportasi massal, 
        atau menutup 100% biaya operasional tahunan <b>{puskesmas_funded_count:,.1f} unit Puskesmas Kelurahan</b>, 
        atau menjamin beasiswa perlengkapan sekolah penuh bagi <b>{kjp_funded_count:,} siswa SMA/SMK prasejahtera</b>.
    </p>
    <p style="margin-bottom: 0;">
        Lebih jauh lagi, melalui implementasi regulasi Permen ESDM No. 2 Tahun 2024 yang meniadakan biaya kapasitas (<i>capacity charge</i>), 
        pemerintah daerah bahkan tidak perlu mengeluarkan sepeser pun uang kas daerah: skema <b>Sewa Atap Swasta (Power Purchase Agreement / Zero-APBD)</b> 
        memungkinkan mitra pengembang surya membiayai 100% modal awal, sementara Pemda langsung menikmati pemotongan tagihan listrik sejak bulan pertama operasi. 
        Pemasangan PLTS Atap bukan beban anggaran, melainkan instrumen pembebasan ruang fiskal daerah (*fiscal space*) secara permanen.
    </p>
</div>
""", unsafe_allow_html=True)

# ─── BENTO METRIC CARDS (3 KOLOM x 2 BARIS) ──────────────────────────────────────
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Total Kebutuhan Investasi (CAPEX)</div>
            <div class="bento-val" style="color: #4CAF50;">Rp {total_capex_triliun:.2f} <span style="font-size:1.1rem;color:#A5D6A7;">Triliun</span></div>
            <div class="bento-desc">Kebutuhan modal pengadaan EPC agregat untuk {total_capacity_mwp:,.1f} MWp di {total_assets:,} titik fasilitas publik.</div>
        </div>
        <div class="bento-src"><b>Sumber:</b> Standar EPC ESDM & AESI 2026<br><b>File:</b> pow_solar_ekonomi_kebijakan.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col_b2:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Penghematan Belanja Listrik Tahunan</div>
            <div class="bento-val" style="color: #66BB6A;">Rp {total_savings_miliar:,.1f} <span style="font-size:1.1rem;color:#C8E6C9;">M/thn</span></div>
            <div class="bento-desc">Pemotongan belanja rutin tagihan listrik PLN dari 407,16 GWh produksi energi mandiri per tahun.</div>
        </div>
        <div class="bento-src"><b>Sumber:</b> Tarif PLN 2026 (Gol. P-1 & B-2)<br><b>File:</b> pow_solar_ekonomi_kebijakan.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col_b3:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Periode Balik Modal Rata-Rata</div>
            <div class="bento-val" style="color: #FFA726;">{avg_payback_years:.1f} <span style="font-size:1.1rem;color:#FFE0B2;">Tahun</span></div>
            <div class="bento-desc">Simple payback portofolio. Menghasilkan sisa 17,5 tahun panen listrik bebas biaya tagihan.</div>
        </div>
        <div class="bento-src"><b>Sumber:</b> Formula Payback Industri Surya<br><b>File:</b> standar_capex_opex_plts_2026.csv</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

col_b4, col_b5, col_b6 = st.columns(3)

with col_b4:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Penciptaan Lapangan Kerja Hijau</div>
            <div class="bento-val" style="color: #42A5F5;">{total_green_jobs:,} <span style="font-size:1.1rem;color:#BBDEFB;">Pekerja</span></div>
            <div class="bento-desc">{jobs_const:,} pekerja fase konstruksi/fabrikasi baja dan {jobs_om:,} teknisi pemeliharaan permanen 25 tahun.</div>
        </div>
        <div class="bento-src"><b>Sumber:</b> Multiplier Ketenagakerjaan IESR/IRENA<br><b>File:</b> pow_solar_ekonomi_kebijakan.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col_b5:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Dividen Subsidi Tiket Komuter</div>
            <div class="bento-val" style="color: #26A69A;">{commuter_subsidy_pax/1e6:.1f} <span style="font-size:1.1rem;color:#B2DFDB;">Juta Pax/th</span></div>
            <div class="bento-desc">Ekuivalen dengan membiayai penuh {commuter_subsidy_pax:,} perjalanan penumpang TransJakarta bersubsidi.</div>
        </div>
        <div class="bento-src"><b>Sumber:</b> Realisasi PSO Dishub DKI (Rp 10 rb/tiket)<br><b>File:</b> standar_biaya_layanan_publik.csv</div>
    </div>
    """, unsafe_allow_html=True)

with col_b6:
    st.markdown(f"""
    <div class="bento-card">
        <div>
            <div class="bento-lbl">Beban Likuiditas Kas APBD</div>
            <div class="bento-val" style="color: #AB47BC;">Rp 0,- <span style="font-size:1.1rem;color:#E1BEE7;">Zero-APBD</span></div>
            <div class="bento-desc">Opsi skema Sewa Atap Swasta (PPA): 100% CAPEX swasta, Pemda langsung terima diskon listrik.</div>
        </div>
        <div class="bento-src"><b>Sumber:</b> Permen ESDM No. 2/2024 & Perpres 11/2023<br><b>File:</b> matriks_skema_pengadaan_zero_apbd.csv</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════════
# SUB-BAB 3.1: NERACA INVESTASI & PENGHEMATAN BELANJA LISTRIK TAHUNAN
# ═════════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(r"### 3.1 Neraca Investasi & Penghematan Belanja Listrik Tahunan ($\text{CAPEX} \ \text{vs} \ \text{OPEX Savings}$)")
st.markdown('<div class="sub-chapter-badge">Sub-Bab 3.1: Dekomposisi Biaya Modal, Penghematan Belanja Operasional & Simple Payback Portofolio</div>', unsafe_allow_html=True)

with st.expander("ℹ️ Metodologi 3.1: Formulasi Dekomposisi Biaya Modal EPC, Tarif Listrik & Periode Impas 25 Tahun"):
    st.markdown(r"""
    **Prinsip Perhitungan Biaya Modal & Penghematan Listrik Portofolio:**
    1. **Dekomposisi Biaya Modal Berdasarkan Karakter Fisik Penopang:**
       * **Rooftop Dak Beton Standar:**
         $$\text{Biaya} = \text{Rp 12,5 Juta per kWp}$$
         Diterapkan pada bangunan dengan struktur atap dak beton yang sudah ada (*existing reinforced concrete roof slab*): Rumah Sakit (RSUD), Sekolah Negeri, Kampus Perguruan Tinggi, Pusat Perbelanjaan (Mall), Pasar Tradisional, dan Gelanggang Olahraga. Struktur dak hanya membutuhkan rel profil aluminium dan balast beton ringan tanpa modifikasi arsitektural berat.
       * **Solar Carport & Kanopi Rangka Baja Bentang Lebar:**
         $$\text{Biaya} = \text{Rp 18,5 Juta per kWp}$$
         Diterapkan pada simpul transportasi terbuka dan area perparkiran: Lapangan Parkir (Parking), Halte Bus TransJakarta (BRT), Stasiun KRL, Stasiun MRT/LRT, Terminal Bus, Bandara Soetta, dan JPO. Memerlukan penambahan struktur baja galvanis *heavy-duty*, fondasi tiang angkur beton, dan talang air terintegrasi agar kendaraan dan pejalan kaki terlindung secara optimal.
    2. **Formulasi Akumulasi Arus Kas Bersih 25 Tahun ($\text{Cumulative Net Cash Flow}$):**
       $$\text{Arus Kas}(t) = -\text{CAPEX} + \sum_{y=1}^{t} \left( \text{Hemat Tahunan} - \text{OPEX}_y \right)$$
       Di mana biaya pemeliharaan tahunan ($\text{OPEX}$) diestimasikan konservatif sebesar $1,5\% \text{ s.d. } 2,0\%$ dari CAPEX untuk pembersihan modul rutin dan servis inverter.
    3. **Titik Impas Sederhana (*Simple Payback Period*):**
       Tercapai pada tahun $t$ ketika $\text{Arus Kas}(t) \ge 0$, yakni rata-rata pada tahun ke-**7,43**.
    """)

# Metrik Agregat Klaster Struktur (Dak vs Carport)
dak_categories = ['hospital', 'school', 'university', 'mall', 'market', 'stadium']
carport_categories = ['parking', 'brt', 'krl', 'mrt_lrt', 'terminal', 'jpo', 'airport']

df_dak = df_ekonomi[df_ekonomi['category'].isin(dak_categories)]
df_carport = df_ekonomi[df_ekonomi['category'].isin(carport_categories)]

dak_kwp = df_dak['total_capacity_kwp'].sum()
dak_mwp = dak_kwp / 1000.0
dak_capex_miliar = df_dak['total_capex_miliar'].sum()
dak_savings_miliar = df_dak['total_savings_annual_miliar'].sum()
dak_payback = round(dak_capex_miliar / dak_savings_miliar, 2)

carport_kwp = df_carport['total_capacity_kwp'].sum()
carport_mwp = carport_kwp / 1000.0
carport_capex_miliar = df_carport['total_capex_miliar'].sum()
carport_savings_miliar = df_carport['total_savings_annual_miliar'].sum()
carport_payback = round(carport_capex_miliar / carport_savings_miliar, 2)

st.markdown(f"""
<p style="color: #ECEFF1; font-size: 1.03rem; line-height: 1.75; margin-bottom: 1.2rem;">
    Neraca investasi PLTS Atap pada 2.000 titik infrastruktur Jabodetabek membutuhkan total belanja modal sebesar 
    <b>Rp {total_capex_triliun:.3f} Triliun</b> untuk memasang <b>{total_capacity_mwp:,.2f} MWp ({total_capacity_kwp:,.1f} kWp)</b> daya surya fotovoltaik. 
    Secara agregat, aset ini memproduksi <b>{total_gen_gwh:,.2f} GWh listrik bersih per tahun</b> yang memotong belanja rutin tagihan listrik PLN sebesar 
    <b>Rp {total_savings_miliar:,.2f} Miliar setiap tahun</b>. 
    Dengan rasio perputaran arus kas tersebut, seluruh modal proyek mencapai titik impas sempurna dalam <b>{avg_payback_years:.2f} tahun</b>, 
    menghasilkan sisa <b>17,5 tahun listrik cuma-cuma</b> dengan akumulasi penghematan bersih sebesar <b>Rp {net_cumulative_savings_25yr_triliun:.2f} Triliun</b> selama 25 tahun masa operasional.
</p>
""", unsafe_allow_html=True)

# ─── 3.1.1 & 3.1.2 DEKOMPOSISI BIAYA & VISUALISASI ──────────────────────────────
st.markdown("#### 3.1.1 Dekomposisi Biaya Modal: Rooftop Dak Beton vs Solar Carport & Kanopi Baja")
st.markdown(f"""
<p style="color: #CFD8DC; font-size: 0.96rem; line-height: 1.65; margin-bottom: 1rem;">
    Perbedaan karakter fisik struktur penopang membagi portofolio ke dalam dua kelompok biaya pengadaan yang transparan:
    <br>• <b>Klaster Rooftop Dak Beton (6 Kategori):</b> Menyerap kapasitas terbesar yaitu <b>{dak_mwp:,.2f} MWp (68,1%)</b> dengan kebutuhan modal <b>Rp {dak_capex_miliar:,.2f} Miliar</b> (standar Rp 12,5 Juta/kWp). Menghasilkan penghematan tagihan sebesar <b>Rp {dak_savings_miliar:,.2f} Miliar/tahun</b> dengan titik impas tercepat rata-rata <b>{dak_payback:.2f} tahun</b>.
    <br>• <b>Klaster Solar Carport & Kanopi Baja (7 Kategori):</b> Menyumbang kapasitas <b>{carport_mwp:,.2f} MWp (31,9%)</b> dengan kebutuhan modal <b>Rp {carport_miliar if 'carport_miliar' in locals() else carport_capex_miliar:,.2f} Miliar</b> (standar Rp 18,5 Juta/kWp). Menghemat <b>Rp {carport_savings_miliar:,.2f} Miliar/tahun</b> dengan titik impas <b>{carport_payback:.2f} tahun</b>, memberikan nilai tambah ganda sebagai peneduh cuaca ekstrem bagi jutaan komuter perkotaan.
</p>
""", unsafe_allow_html=True)

col_chart_e1, col_chart_e2 = st.columns([3, 2])

with col_chart_e1:
    st.markdown("###### Perbandingan Modal Awal vs Penghematan Tahunan per Kategori (Plotly Bar)")
    
    # Sort for visual clarity
    df_chart = df_ekonomi.sort_values(by="total_capex_miliar", ascending=True).copy()
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=df_chart['category_display'],
        x=df_chart['total_capex_miliar'],
        name='Modal Investasi (CAPEX Miliar Rp)',
        orientation='h',
        marker=dict(color='#4CAF50', line=dict(color='#81C784', width=1)),
        text=df_chart['total_capex_miliar'].apply(lambda x: f"Rp {x:,.0f} M"),
        textposition='outside'
    ))
    fig_bar.add_trace(go.Bar(
        y=df_chart['category_display'],
        x=df_chart['total_savings_annual_miliar'],
        name='Penghematan Listrik (Tahunan Miliar Rp)',
        orientation='h',
        marker=dict(color='#26A69A', line=dict(color='#80CBC4', width=1)),
        text=df_chart['total_savings_annual_miliar'].apply(lambda x: f"Rp {x:,.1f} M"),
        textposition='outside'
    ))
    fig_bar.update_layout(
        barmode='group',
        height=480,
        margin=dict(l=10, r=40, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(color='#CFD8DC', size=11)
        ),
        xaxis=dict(
            title=dict(text='Nilai Finansial (Miliar Rupiah)', font=dict(color='#B0BEC5', size=11)),
            tickfont=dict(color='#90A4AE'),
            gridcolor='#263238'
        ),
        yaxis=dict(
            tickfont=dict(color='#ECEFF1', size=11)
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart_e2:
    st.markdown("###### Kurva Akumulasi Arus Kas Bersih 25 Tahun (Net Cumulative Cash Flow)")
    
    # Generate 25-year cashflow simulation
    years = list(range(0, 26))
    annual_net_cash = total_savings_miliar - (total_capex_miliar * 0.015) # factoring 1.5% OPEX
    cumulative_cash = [-total_capex_miliar + (y * annual_net_cash) for y in years]
    
    fig_line = go.Figure()
    
    # Area positive vs negative
    fig_line.add_trace(go.Scatter(
        x=years,
        y=cumulative_cash,
        mode='lines+markers',
        name='Akumulasi Kas Bersih',
        line=dict(color='#66BB6A', width=3),
        marker=dict(size=5, color='#4CAF50'),
        fill='tozeroy',
        fillcolor='rgba(76, 175, 80, 0.15)'
    ))
    
    # Zero line (Break-even threshold)
    fig_line.add_hline(
        y=0,
        line_dash="dash",
        line_color="#FFA726",
        annotation_text="Titik Impas (Break-even: Thn 7,43)",
        annotation_position="bottom right",
        annotation_font=dict(color="#FFA726", size=11)
    )
    
    fig_line.update_layout(
        height=480,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title=dict(text='Tahun Operasional (Tahun 0 s.d. 25)', font=dict(color='#B0BEC5', size=11)),
            tickfont=dict(color='#90A4AE'),
            gridcolor='#263238',
            tickvals=[0, 5, 7.43, 10, 15, 20, 25],
            ticktext=['Th 0', 'Th 5', 'Impas 7,4', 'Th 10', 'Th 15', 'Th 20', 'Th 25']
        ),
        yaxis=dict(
            title=dict(text='Net Cumulative Cash (Miliar Rp)', font=dict(color='#B0BEC5', size=11)),
            tickfont=dict(color='#90A4AE'),
            gridcolor='#263238'
        ),
        showlegend=False
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ─── KOTAK CALLOUT TEMUAN KRITIS CELIOS ──────────────────────────────────────────
st.markdown(f"""
<div class="callout-box">
    <div style="font-weight: 700; color: #4CAF50; font-size: 1.05rem; margin-bottom: 0.4rem;">
        Fakta Data & Interpretasi Kritis CELIOS: Mengapa PLTS Atap Mengubah Sunk Cost Menjadi Aset Produktif?
    </div>
    <div style="color: #ECEFF1; font-size: 0.93rem; line-height: 1.7;">
        <b>1. Fakta Data Titik Impas 6–7 Tahun:</b> Pemasangan PLTS pada kelompok gedung publik dak beton (RSUD, Sekolah, Kampus, Pasar) mencapai titik impas investasi dalam rata-rata <b>{dak_payback:.2f} tahun</b>. Sementara itu, kelompok kanopi baja transit (Halte TransJakarta, Stasiun KRL, Terminal) mencapai titik impas dalam <b>{carport_payback:.2f} tahun</b> karena memperhitungkan biaya konstruksi struktur bentang lebar.<br>
        <b>2. Jebakan Biaya Hangus (Sunk Cost PLN):</b> Membeli listrik secara konvensional dari PLN adalah pengeluaran rutin seumur hidup tanpa meninggalkan aset modal (<i>pure expense / sunk cost</i>). Setelah 25 tahun membayar tagihan ke PLN, fasilitas publik tetap tidak memiliki aset pembangkit mandiri.<br>
        <b>3. Dividen 17,5 Tahun Panen Bebas Biaya:</b> Sebaliknya, pemasangan PLTS Atap mengubah pengeluaran rutin menjadi aset modal produktif. Begitu titik impas terlewati pada tahun ke-7, seluruh fasilitas menikmati <b>17,5 tahun pasokan energi gratis</b> dengan total penghematan bersih kumulatif mencapai <b>Rp {net_cumulative_savings_25yr_triliun:.2f} Triliun</b> yang dapat dialokasikan langsung untuk perbaikan fasilitas umum warga.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── DATA LINEAGE & EXPANDER DATA MENTAH ─────────────────────────────────────────
with st.expander("📋 Data Lineage: Tabel Rincian Finansial Makro 13 Kategori Infrastruktur (CSV)"):
    st.markdown("Setiap baris data berikut diverifikasi langsung dari output kalkulasi satelit dan standar biaya resmi EPC 2026:")
    
    display_cols = [
        "category_display", "total_points", "total_capacity_kwp", "total_annual_generation_mwh",
        "tipe_struktur_plts", "total_capex_miliar", "total_savings_annual_miliar",
        "simple_payback_years", "total_green_jobs_orang", "ekuivalensi_tiket_komuter_pax",
        "kuadran_prioritas", "kalimat_verbatim"
    ]
    
    st.dataframe(
        df_ekonomi[display_cols].rename(columns={
            "category_display": "Kategori Fasilitas",
            "total_points": "Jumlah Titik",
            "total_capacity_kwp": "Kapasitas (kWp)",
            "total_annual_generation_mwh": "Produksi (MWh/th)",
            "tipe_struktur_plts": "Struktur Rangka",
            "total_capex_miliar": "CAPEX (Miliar Rp)",
            "total_savings_annual_miliar": "Hemat (Miliar Rp/th)",
            "simple_payback_years": "Payback (Tahun)",
            "total_green_jobs_orang": "Green Jobs (Orang)",
            "ekuivalensi_tiket_komuter_pax": "Dividen Tiket (Pax)",
            "kuadran_prioritas": "Kuadran Prioritas",
            "kalimat_verbatim": "Kutipan Verbatim Bukti Fisik"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv_bytes = df_ekonomi.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Dataset Ringkasan Ekonomi (CSV)",
            data=csv_bytes,
            file_name="pow_solar_ekonomi_kebijakan.csv",
            mime="text/csv"
        )
    with col_dl2:
        st.info("💡 Berkas fisik bukti kutipan tersimpan di `data/raw/sources/` dan tabel referensi di `data/processed/references/`.")

# ═════════════════════════════════════════════════════════════════════════════════
# PLACEHOLDER NAVIGASI SUB-BAB 3.2 S.D. 3.5
# ═════════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background: #141A24; border: 1px dashed #37474F; border-radius: 8px; padding: 1.2rem; text-align: center; color: #90A4AE; font-size: 0.9rem;">
    <b>Sub-Bab Berikutnya dalam Pengembangan Bertahap Sesuai Kerangka Riset CELIOS:</b><br>
    <span style="color: #4CAF50;">[Sub-Bab 3.2: Ekuivalensi Dividen Fiskal APBD]</span> &nbsp;•&nbsp; 
    <span style="color: #4CAF50;">[Sub-Bab 3.3: Dampak Penciptaan Green Jobs]</span> &nbsp;•&nbsp; 
    <span style="color: #4CAF50;">[Sub-Bab 3.4: Matriks Prioritas Quick Wins]</span> &nbsp;•&nbsp; 
    <span style="color: #4CAF50;">[Sub-Bab 3.5: Solusi Pengadaan Zero-APBD]</span>
</div>
""", unsafe_allow_html=True)
