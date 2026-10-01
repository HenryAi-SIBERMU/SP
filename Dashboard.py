"""
Teduhi Ruang Kota Kami
Solar Dashboard — Potensi PLTS Atap Dual-Use Infrastructure di Jabodetabek
"""
import streamlit as st
import os
import sys

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

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Teduhi Ruang Kota Kami</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Potensi Instalasi Dual-Use Infrastructure PLTS Atap di Jabodetabek</div>', unsafe_allow_html=True)

st.markdown("""
<div class="note-box">
<strong>Catatan Safety Buffer Jabodetabek (4.000 Titik Target)</strong><br>
Angka 4.000 titik merupakan estimasi batas atas (safety buffer) komprehensif se-Jabodetabek untuk pemodelan teknis dan budgeting riset. <em>Status titik saat ini merupakan estimasi awal dan belum tervalidasi 100% di lapangan</em> (sedang dalam proses validasi GIS, verifikasi satelit, dan akuisisi data stakeholder).
</div>
""", unsafe_allow_html=True)

# ─── HERO METRICS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Potensi Awal (Estimasi Safety Buffer 4.000 Titik)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Kapasitas</div>
        <div class="metric-value">~2,900 MWp</div>
        <div class="metric-desc">Dari 4.000 titik safety buffer se-Jabodetabek</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Produksi Tahunan</div>
        <div class="metric-value">~3,750 GWh</div>
        <div class="metric-desc">Estimasi produksi listrik per tahun (~1.300 kWh/kWp)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Kontribusi Regional</div>
        <div class="metric-value">~4.8%</div>
        <div class="metric-desc">Dari kebutuhan listrik Jabodetabek (~78.000 GWh)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Reduksi CO₂</div>
        <div class="metric-value">~3.1M ton</div>
        <div class="metric-desc">Emisi CO₂eq yang dapat direduksi per tahun</div>
    </div>
    """, unsafe_allow_html=True)

# ─── INFRASTRUKTUR ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">7 Kategori Infrastruktur Urban Jabodetabek (4.000 Titik)</div>', unsafe_allow_html=True)

infrastruktur = [
    ("Halte BRT & Bus Shelter", "850 shelter (TJ & Bodetabek)", "~32.0 MWp"),
    ("Stasiun KRL Commuter Line", "100 stasiun (Lintas Jabodetabek)", "~13.5 MWp"),
    ("Stasiun MRT, LRT & Bandara", "60 stasiun (MRT, LRT, Bandara, KCIC)", "~8.5 MWp"),
    ("Jembatan Penyeberangan (JPO)", "640 JPO (Arteri & Nasional)", "~4.0 MWp"),
    ("Parking Lot & Park-and-Ride", "1.850 lokasi (Komersial & TOD)", "~2.497 MWp"),
    ("Gedung Parkir (MSCP)", "440 gedung (Mall, RS, Kampus)", "~316 MWp"),
    ("Koridor Pedestrian Beratap", "60 koridor / titik TOD", "~30.0 MWp"),
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

# ─── KATEGORI TAMBAHAN FASILITAS PUBLIK ─────────────────────────────────────────
st.markdown('<div class="section-header">6 Kategori Tambahan: Fasilitas Publik (Ekspansi Riset)</div>', unsafe_allow_html=True)

fasilitas_publik = [
    ("Sekolah Negeri", "SD, SMP, SMA/SMK", "Tahap Akuisisi Data"),
    ("Universitas", "Kampus PTN / PTS", "Tahap Akuisisi Data"),
    ("RS & Puskesmas", "RSUD & Faskes", "Tahap Akuisisi Data"),
    ("Pasar Tradisional", "PD Pasar & Rakyat", "Tahap Akuisisi Data"),
    ("Bandar Udara", "Soekarno-Hatta & Halim", "Tahap Akuisisi Data"),
    ("Stadion & GOR", "Gelanggang Olahraga", "Tahap Akuisisi Data"),
]

cols_pub = st.columns(3)
for idx, (nama, lingkup, status_data) in enumerate(fasilitas_publik):
    with cols_pub[idx % 3]:
        st.markdown(f"""
        <div style="background:#1E2530; padding:1rem; border-radius:6px; margin-bottom:0.8rem; border:1px dashed #FFA726;">
            <div style="font-weight:600; color:#FFF; margin-bottom:0.3rem; font-size:0.9rem;">{nama}</div>
            <div style="font-size:0.75rem; color:#B0BEC5;">{lingkup}</div>
            <div style="font-size:0.8rem; color:#FFA726; font-weight:600; margin-top:0.5rem;">Status: {status_data}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── NEXT STEPS ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Status Riset</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<strong>Fase Saat Ini: Planning & Data Collection</strong><br><br>

<strong>Selesai:</strong><br>
Framework riset & metodologi, Data acquisition plan (43 sumber data), Struktur dashboard & dokumentasi<br><br>

<strong>Sedang Berjalan:</strong><br>
Contact stakeholder (TransJakarta, KAI, MRT), Setup PVGIS API, Download data OpenStreetMap Jabodetabek<br><br>

<strong>Next:</strong><br>
Inventarisasi area dengan GIS, Perhitungan kapasitas & produksi, Financial modeling & scenario analysis
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-size: 0.75rem; color: #616161; text-align: center;">
CELIOS Research Division · Solar Dashboard Jabodetabek · Juni 2026
</div>
""", unsafe_allow_html=True)
