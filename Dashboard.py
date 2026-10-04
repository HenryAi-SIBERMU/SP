"""
Teduhi Ruang Kota Kami
Solar Dashboard — Potensi PLTS Atap Dual-Use Infrastructure di Jabodetabek
"""
import streamlit as st
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css

st.set_page_config(
    page_title="CELIOS — Solar Dashboard Jabodetabek",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_solar_css(), unsafe_allow_html=True)

# ─── DATA EMPIRIS PILOT YANG SUDAH DI-FETCH ──────────────────────────────────
CALC_DIR = os.path.join(os.path.dirname(__file__), "data", "processed", "calculations")
PROCESSED_CALC_PATH = os.path.join(CALC_DIR, "pow_solar_13_titik_summary.csv")
if not os.path.exists(PROCESSED_CALC_PATH):
    PROCESSED_CALC_PATH = os.path.join(CALC_DIR, "pow_solar_5_titik_summary.csv")

if os.path.exists(PROCESSED_CALC_PATH):
    df_pilot = pd.read_csv(PROCESSED_CALC_PATH)
    fetched_kwp = df_pilot["installed_capacity_kwp"].sum()
    fetched_mwh = df_pilot["annual_generation_mwh"].sum()
    fetched_co2 = df_pilot["ghg_reduction_tons_co2"].sum()
    fetched_titik = len(df_pilot)
else:
    df_pilot = pd.DataFrame()
    fetched_kwp = 6648.0
    fetched_mwh = 8759.4
    fetched_co2 = 7086.3
    fetched_titik = 13

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Teduhi Ruang Kota Kami</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Potensi Instalasi Dual-Use Infrastructure PLTS Atap di Jabodetabek</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Catatan Titik Target Riset Jabodetabek (2.260 Titik)</strong><br>
Angka target riset mencakup <strong>2.260 titik</strong> lintas <strong>13 kategori infrastruktur</strong> se-Jabodetabek. <em>Status saat ini: {fetched_titik} titik pilot lintas 13 kategori infrastruktur lengkap telah selesai di-fetch dan terverifikasi 100% valid spasial menggunakan Google Solar API ({fetched_kwp:,.1f} kWp / {fetched_mwh:,.1f} MWh/thn / {fetched_co2:,.1f} Ton CO₂/thn)</em>.
</div>
""", unsafe_allow_html=True)

# ─── HERO METRICS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Potensi Estimasi (2.260 Titik Target se-Jabodetabek)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Kapasitas</div>
        <div class="metric-value">~590 MWp</div>
        <div class="metric-desc">Dari 2.260 titik target se-Jabodetabek ({fetched_kwp/1000:.2f} MWp terverifikasi pilot)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Produksi Tahunan</div>
        <div class="metric-value">~785 GWh</div>
        <div class="metric-desc">Estimasi produksi per tahun ({fetched_mwh:,.1f} MWh terverifikasi pilot)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Kontribusi Regional</div>
        <div class="metric-value">~1.0%</div>
        <div class="metric-desc">Dari kebutuhan listrik Jabodetabek (~78.000 GWh)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Reduksi CO₂</div>
        <div class="metric-value">~635k ton</div>
        <div class="metric-desc">Emisi CO₂eq yang direduksi per tahun ({fetched_co2:,.1f} ton terverifikasi pilot)</div>
    </div>
    """, unsafe_allow_html=True)

# ─── 13 KATEGORI INFRASTRUKTUR URBAN ──────────────────────────────────────────
st.markdown('<div class="section-header">13 Kategori Infrastruktur Urban Jabodetabek (2.260 Titik)</div>', unsafe_allow_html=True)

pilot_by_cat = {}
if not df_pilot.empty and "category" in df_pilot.columns:
    for _, row in df_pilot.iterrows():
        pilot_by_cat[str(row["category"]).strip().lower()] = row

infrastruktur = [
    {
        "cat_key": "brt",
        "nama": "Halte BRT TransJakarta",
        "target": "400 shelter (TJ & Busway)",
        "est_kapasitas": "~12.0 MWp",
        "default_pilot": "Halte CSW Integrasi (174.4 kWp)",
    },
    {
        "cat_key": "krl",
        "nama": "Stasiun KRL Commuter Line",
        "target": "80 stasiun (Lintas Jabodetabek)",
        "est_kapasitas": "~64.0 MWp",
        "default_pilot": "Stasiun KRL Manggarai Sentral (1,771.6 kWp)",
    },
    {
        "cat_key": "mrt",
        "nama": "Stasiun MRT",
        "target": "20 stasiun (MRT Jakarta Koridor 1 & 2)",
        "est_kapasitas": "~13.0 MWp",
        "default_pilot": "Stasiun MRT Cipete Raya (656.8 kWp)",
    },
    {
        "cat_key": "lrt",
        "nama": "Stasiun LRT",
        "target": "20 stasiun (LRT Jabodebek & Jakarta)",
        "est_kapasitas": "~7.0 MWp",
        "default_pilot": "Stasiun LRT Dukuh Atas (310.8 kWp)",
    },
    {
        "cat_key": "terminal",
        "nama": "Terminal Bus",
        "target": "25 terminal (Terminal Antarkota & Tipe A)",
        "est_kapasitas": "~4.5 MWp",
        "default_pilot": "Terminal Bus Tanjung Priok (128.8 kWp)",
    },
    {
        "cat_key": "airport",
        "nama": "Bandar Udara",
        "target": "20 fasilitas (Soetta & Halim)",
        "est_kapasitas": "~30.0 MWp",
        "default_pilot": "Bandara Soekarno-Hatta T3 (325.2 kWp)",
    },
    {
        "cat_key": "parking",
        "nama": "Gedung Parkir (MSCP)",
        "target": "180 gedung (Mall, RS, Kampus)",
        "est_kapasitas": "~45.0 MWp",
        "default_pilot": "Gedung Parkir Binus University (288.0 kWp)",
    },
    {
        "cat_key": "mall",
        "nama": "Pusat Perbelanjaan / Mall",
        "target": "150 mall (Kawasan Komersial & Retail)",
        "est_kapasitas": "~300.0 MWp",
        "default_pilot": "Pondok Indah Mall 1 (2,173.2 kWp)",
    },
    {
        "cat_key": "hospital",
        "nama": "Rumah Sakit & Faskes",
        "target": "100 faskes (RSUD & Puskesmas)",
        "est_kapasitas": "~15.0 MWp",
        "default_pilot": "RSUD Tarakan Jakarta (158.8 kWp)",
    },
    {
        "cat_key": "university",
        "nama": "Universitas / Kampus",
        "target": "50 kampus (Perguruan Tinggi Jabodetabek)",
        "est_kapasitas": "~25.0 MWp",
        "default_pilot": "Perpustakaan Pusat UI Depok (419.2 kWp)",
    },
    {
        "cat_key": "school",
        "nama": "Sekolah Negeri",
        "target": "200 sekolah (SD, SMP, SMA/SMK)",
        "est_kapasitas": "~30.0 MWp",
        "default_pilot": "SMAN 70 Jakarta Bulungan (28.8 kWp)",
    },
    {
        "cat_key": "market",
        "nama": "Pasar Tradisional",
        "target": "70 pasar (Pasar Rakyat Jabodetabek)",
        "est_kapasitas": "~21.0 MWp",
        "default_pilot": "Pasar Mayestik Kebayoran Baru (37.2 kWp)",
    },
    {
        "cat_key": "stadium",
        "nama": "Stadion & GOR",
        "target": "20 fasilitas (Gelanggang Olahraga)",
        "est_kapasitas": "~20.0 MWp",
        "default_pilot": "Istora Senayan GBK (175.2 kWp)",
    },
]

cols = st.columns(4)
for idx, item in enumerate(infrastruktur):
    cat_key = item["cat_key"]
    nama = item["nama"]
    target = item["target"]
    est_kap = item["est_kapasitas"]

    if cat_key in pilot_by_cat:
        p_row = pilot_by_cat[cat_key]
        p_name = p_row.get("asset_name", "")
        p_kwp = p_row.get("installed_capacity_kwp", 0.0)
        pilot_text = f"Pilot: {p_name} ({p_kwp:,.1f} kWp)"
    else:
        pilot_text = f"Pilot: {item['default_pilot']}"

    with cols[idx % 4]:
        st.markdown(f"""
        <div style="background:#1A1F2B; padding:1rem; border-radius:6px; margin-bottom:0.8rem; border:1px solid #333;">
            <div style="font-weight:600; color:#ECEFF1; margin-bottom:0.3rem; font-size:0.9rem;">{nama}</div>
            <div style="font-size:0.75rem; color:#9E9E9E; margin-bottom:0.4rem;">{target}</div>
            <div style="font-size:0.75rem; color:#4FC3F7; margin-bottom:0.3rem;">{pilot_text}</div>
            <div style="font-size:0.9rem; color:#66BB6A; font-weight:700;">{est_kap}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── NEXT STEPS ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Status Riset</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="info-box">
<strong>Fase Saat Ini: Validasi Spasial Empiris & Ekspansi Dataset</strong><br><br>

<strong>Selesai (Tahap 1 Pilot):</strong><br>
Akuisisi data {fetched_titik} titik pilot lintas 13 kategori infrastruktur lengkap (Halte BRT CSW, KRL Manggarai, MRT Cipete Raya, LRT Dukuh Atas, Terminal Tj. Priok, Bandara Soetta T3, Gedung Parkir Binus, Pondok Indah Mall 1, RSUD Tarakan, Perpustakaan UI Depok, SMAN 70 Bulungan, Pasar Mayestik, Istora Senayan GBK) via Google Solar API Full SKU ({fetched_kwp:,.1f} kWp / {fetched_mwh:,.1f} MWh/thn / {fetched_co2:,.1f} Ton CO₂/thn). Verifikasi spasial 100% valid (rata-rata drift spasial hanya 5,8 meter), segmentasi 3D atap, dan visualisasi citra satelit resolusi tinggi di halaman Pemetaan Potensi.<br><br>

<strong>Sedang Berjalan (Tahap 2):</strong><br>
Persiapan ekspansi 110 titik ikonik se-Jabodetabek lintas 13 kategori infrastruktur.<br><br>

<strong>Target Akhir (Tahap 3):</strong><br>
Inventarisasi penuh 2.260 titik infrastruktur urban Jabodetabek lintas 13 kategori, perhitungan agregat kapasitas dan produksi listrik kota, pemodelan reduksi emisi, dan mitigasi Urban Heat Island (UHI).
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-size: 0.75rem; color: #616161; text-align: center;">
CELIOS Research Division · Solar Dashboard Jabodetabek · 2026
</div>
""", unsafe_allow_html=True)
