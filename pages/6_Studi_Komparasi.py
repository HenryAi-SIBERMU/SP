"""
Studi Komparasi
"""
import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css

st.set_page_config(
    page_title="Studi Komparasi — CELIOS Solar Dashboard",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
)

render_sidebar()
st.markdown(get_solar_css(), unsafe_allow_html=True)

st.markdown('<div class="page-title">Studi Komparasi</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Implementasi Dual-Use Solar Infrastructure di Berbagai Negara</div>', unsafe_allow_html=True)

st.markdown("""
<div class="dev-placeholder">
    <h2>Halaman Dalam Pengembangan</h2>
    <p>Halaman <strong>Studi Komparasi</strong> sedang dalam tahap development.</p>
</div>
""", unsafe_allow_html=True)
