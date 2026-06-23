"""Shared sidebar component — imported by every page for consistent branding & navigation."""
import streamlit as st
import os

def render_sidebar():
    """Render CELIOS logo and solar dashboard navigation in sidebar."""
    _dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(_dir, "..", "..", "refrensi", "Celios China-Indonesia Energy Transition.png")
    logo_path = os.path.normpath(logo_path)

    with st.sidebar:
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] { display: none !important; }
        .sidebar-label {
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            color: #66BB6A;
            text-transform: uppercase;
            padding: 10px 0 4px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)

        st.markdown("""
        <div style="text-align:center; padding: 6px 0 2px 0;">
            <div style="font-size:0.85rem; font-weight:700; color:#66BB6A; letter-spacing:0.03em;">Solar Dashboard</div>
            <div style="font-size:0.7rem; color:#9E9E9E; margin-top:2px;">Teduhi Ruang Kota Kami — Jabodetabek</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.page_link("Dashboard.py", label="Overview")

        st.markdown('<div class="sidebar-label">Analisis Potensi</div>', unsafe_allow_html=True)
        st.page_link("pages/1_Pemetaan_Potensi.py",        label="Pemetaan Potensi")
        st.page_link("pages/2_Analisis_Kapasitas.py",      label="Analisis Kapasitas")
        st.page_link("pages/3_Analisis_Ekonomi.py",        label="Analisis Ekonomi")
        st.page_link("pages/4_Manfaat_Lingkungan.py",      label="Manfaat Lingkungan")
        st.page_link("pages/5_Manfaat_Sosial.py",          label="Manfaat Sosial")

        st.markdown('<div class="sidebar-label">Resources</div>', unsafe_allow_html=True)
        st.page_link("pages/6_Studi_Komparasi.py",         label="Studi Komparasi")
        st.page_link("pages/7_Rekomendasi_Roadmap.py",     label="Rekomendasi & Roadmap")
        st.page_link("pages/8_Dokumentasi_Riset.py",       label="Dokumentasi Riset")

        st.markdown("---")
        st.caption("CELIOS · Solar Dashboard · 2026")
