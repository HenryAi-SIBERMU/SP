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
PROCESSED_CALC_PATH = os.path.join(os.path.dirname(__file__), "data", "processed", "calculations", "pow_solar_5_titik_summary.csv")
if os.path.exists(PROCESSED_CALC_PATH):
    df_pilot = pd.read_csv(PROCESSED_CALC_PATH)
    fetched_kwp = df_pilot["installed_capacity_kwp"].sum()
    fetched_mwh = df_pilot["annual_generation_mwh"].sum()
    fetched_co2 = df_pilot["ghg_reduction_tons_co2"].sum()
    fetched_titik = len(df_pilot)
else:
    fetched_kwp = 5071.2
    fetched_mwh = 6682.7
    fetched_co2 = 5406.3
    fetched_titik = 5

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Teduhi Ruang Kota Kami</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Potensi Instalasi Dual-Use Infrastructure PLTS Atap di Jabodetabek</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Catatan Titik Target Riset Jabodetabek (2.260 Titik)</strong><br>
Angka target riset mencakup <strong>2.260 titik</strong> lintas <strong>13 kategori infrastruktur</strong> se-Jabodetabek. <em>Status saat ini: {fetched_titik} titik pilot multi-kategori (KRL Manggarai Sentral, MRT Cipete Raya, LRT Dukuh Atas, RSUD Tarakan, Pondok Indah Mall 1) telah selesai di-fetch dan terverifikasi 100% menggunakan Google Solar API ({fetched_kwp:,.1f} kWp / {fetched_mwh:,.1f} MWh/thn)</em>.
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
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Produksi Tahunan</div>
        <div class="metric-value">~785 GWh</div>
        <div class="metric-desc">Estimasi produksi listrik per tahun (~1.330 kWh/kWp)</div>
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
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Reduksi CO₂</div>
        <div class="metric-value">~635k ton</div>
        <div class="metric-desc">Emisi CO₂eq yang dapat direduksi per tahun (~809 kg/MWh)</div>
    </div>
    """, unsafe_allow_html=True)

# ─── 13 KATEGORI INFRASTRUKTUR URBAN ──────────────────────────────────────────
st.markdown('<div class="section-header">13 Kategori Infrastruktur Urban Jabodetabek (2.260 Titik)</div>', unsafe_allow_html=True)

infrastruktur = [
    ("Halte BRT & Bus Shelter", "400 shelter (TJ & Bodetabek)", "~12.0 MWp"),
    ("Stasiun KRL Commuter Line", "80 stasiun (Lintas Jabodetabek)", "~64.0 MWp"),
    ("Stasiun MRT & LRT", "40 stasiun (MRT & LRT Jabodebek)", "~20.0 MWp"),
    ("Jembatan Penyeberangan (JPO)", "300 JPO (Arteri & Nasional)", "~3.0 MWp"),
    ("Parking Lot & Park-and-Ride", "750 lokasi (Komersial & TOD)", "~300.0 MWp"),
    ("Gedung Parkir (MSCP)", "180 gedung (Mall, RS, Kampus)", "~45.0 MWp"),
    ("Koridor Pedestrian Beratap", "50 koridor / titik TOD", "~7.5 MWp"),
    ("Sekolah Negeri", "200 sekolah (SD, SMP, SMA/SMK)", "~30.0 MWp"),
    ("Universitas", "50 kampus (PTN / PTS Jabodetabek)", "~25.0 MWp"),
    ("RS & Puskesmas", "100 faskes (RSUD & Puskesmas)", "~15.0 MWp"),
    ("Pasar Tradisional", "70 pasar (PD Pasar & Rakyat)", "~21.0 MWp"),
    ("Bandar Udara", "20 fasilitas (Soetta & Halim)", "~30.0 MWp"),
    ("Stadion & GOR", "20 fasilitas (Gelanggang Olahraga)", "~20.0 MWp"),
]

cols = st.columns(4)
for idx, (nama, jumlah, kapasitas) in enumerate(infrastruktur):
    with cols[idx % 4]:
        st.markdown(f"""
        <div style="background:#1A1F2B; padding:1rem; border-radius:6px; margin-bottom:0.8rem; border:1px solid #333;">
            <div style="font-weight:600; color:#ECEFF1; margin-bottom:0.3rem; font-size:0.9rem;">{nama}</div>
            <div style="font-size:0.75rem; color:#9E9E9E;">{jumlah}</div>
            <div style="font-size:0.9rem; color:#66BB6A; font-weight:700; margin-top:0.5rem;">{kapasitas}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── NEXT STEPS ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Status Riset</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="info-box">
<strong>Fase Saat Ini: Validasi Spasial Empiris & Ekspansi Dataset</strong><br><br>

<strong>Selesai (Tahap 1 Pilot):</strong><br>
Akuisisi data {fetched_titik} titik pilot multi-kategori (KRL Manggarai Sentral, MRT Cipete Raya, LRT Dukuh Atas, RSUD Tarakan, Pondok Indah Mall 1) via Google Solar API Full SKU ({fetched_kwp:,.1f} kWp / {fetched_mwh:,.1f} MWh/thn). Verifikasi spasial, segmentasi 3D atap, dan visualisasi citra satelit di halaman Pemetaan Potensi.<br><br>

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
