"""
CELIOS8: Teduhi Ruang Kota Kami
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
<strong>Dashboard dalam Pengembangan</strong><br>
Halaman ini menampilkan overview riset yang sedang berjalan. Data masih dalam proses pengumpulan.
Untuk detail progress riset, lihat halaman <strong>Dokumentasi Riset</strong>.
</div>
""", unsafe_allow_html=True)

# ─── HERO METRICS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">Potensi Awal (Estimasi)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Kapasitas</div>
        <div class="metric-value">~857 MWp</div>
        <div class="metric-desc">Dari 7,200+ lokasi infrastruktur urban</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Produksi Tahunan</div>
        <div class="metric-value">~1,105 GWh</div>
        <div class="metric-desc">Estimasi produksi listrik per tahun</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Kontribusi</div>
        <div class="metric-value">~1.4%</div>
        <div class="metric-desc">Dari kebutuhan listrik Jabodetabek</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Reduksi CO₂</div>
        <div class="metric-value">~940k ton</div>
        <div class="metric-desc">Emisi CO₂ yang dapat dikurangi per tahun</div>
    </div>
    """, unsafe_allow_html=True)

# ─── INFRASTRUKTUR ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">7 Kategori Infrastruktur Potensial</div>', unsafe_allow_html=True)

infrastruktur = [
    ("Halte TransJakarta", "284 halte", "~10.7 MWp"),
    ("Stasiun KRL", "80+ stasiun", "~10.8 MWp"),
    ("Stasiun MRT & LRT", "31 stasiun", "~4.5 MWp"),
    ("Jembatan Penyeberangan (JPO)", "~300 JPO", "~1.9 MWp"),
    ("Koridor Pedestrian", "20 km prioritas", "~10 MWp"),
    ("Parking Lot Terbuka", "500+ lokasi", "~675 MWp"),
    ("Gedung Parkir (MSCP)", "200 gedung", "~144 MWp"),
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

st.markdown("""
<div class="info-box">
<strong>Fase Saat Ini: Planning & Data Collection</strong><br><br>

✅ <strong>Selesai:</strong><br>
Framework riset & metodologi, Data acquisition plan (43 sumber data), Struktur dashboard & dokumentasi<br><br>

⏳ <strong>Sedang Berjalan:</strong><br>
Contact stakeholder (TransJakarta, KAI, MRT), Setup PVGIS API, Download data OpenStreetMap Jabodetabek<br><br>

📋 <strong>Next:</strong><br>
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
