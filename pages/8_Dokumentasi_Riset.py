"""
Dokumentasi Riset
Menampilkan dokumen-dokumen riset dalam format markdown
"""
import streamlit as st
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css

st.set_page_config(
    page_title="Dokumentasi Riset — CELIOS Solar Dashboard",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
)

render_sidebar()
st.markdown(get_solar_css(), unsafe_allow_html=True)

# ─── CUSTOM CSS FOR DOCUMENTATION PAGE ────────────────────────────────────
st.markdown("""
<style>
.doc-nav-card {
    background: #1A1F2B;
    border: 1px solid #2E7D32;
    border-radius: 6px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    cursor: pointer;
    transition: all 0.2s;
}
.doc-nav-card:hover {
    border: 2px solid #2E7D32;
}
.doc-nav-title {
    font-size: 1rem;
    font-weight: 700;
    color: #66BB6A;
    margin-bottom: 0.3rem;
}
.doc-nav-desc {
    font-size: 0.85rem;
    color: #9E9E9E;
    line-height: 1.4;
}
.doc-content {
    background: #1A1F2B;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 2rem;
    margin-top: 1.5rem;
}
blockquote {
    border-left: 4px solid #2E7D32 !important;
    background: #1A2F2A;
    padding: 0.8rem 1.2rem;
    border-radius: 4px;
    color: #ECEFF1;
    margin: 1rem 0;
}
h1, h2, h3 { color: #ECEFF1; }
h1 { 
    color: #66BB6A;
    border-bottom: 2px solid #2E7D32; 
    padding-bottom: 0.5rem; 
}
h2 { 
    color: #66BB6A; 
    margin-top: 2rem; 
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}
table th {
    background: #1A2F2A;
    color: #66BB6A;
    padding: 0.6rem;
    text-align: left;
    font-weight: 600;
    border: 1px solid #333;
}
table td {
    border: 1px solid #333;
    padding: 0.6rem;
    color: #ECEFF1;
}
table tr:hover {
    background: #232B3B;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Dokumentasi Riset</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Dokumen Lengkap Riset PLTS Atap Dual-Use Infrastructure</div>', unsafe_allow_html=True)

# ─── NAVIGATION ────────────────────────────────────────────────────────────
st.markdown("""
<div class="note-box">
<strong>Dokumen Riset Tersedia</strong><br>
Pilih dokumen di bawah untuk membaca konten lengkap.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="doc-nav-card">
        <div class="doc-nav-title">Data Acquisition Plan</div>
        <div class="doc-nav-desc">
            Master log untuk semua sumber data yang dibutuhkan dalam riset. 
            43 sumber data teridentifikasi dari 10 kategori berbeda.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="doc-nav-card">
        <div class="doc-nav-title">Framework Awal - Feedback & Analisis</div>
        <div class="doc-nav-desc">
            Analisis mendalam terhadap framework riset, metodologi, 
            dan feedback komprehensif untuk pengembangan riset.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── DOCUMENT SELECTOR ─────────────────────────────────────────────────────
st.markdown("---")

doc_choice = st.radio(
    "Pilih Dokumen untuk Ditampilkan:",
    [
        "Data Acquisition Plan",
        "Framework Awal - Feedback & Analisis"
    ],
    horizontal=True
)

# ─── HELPER FUNCTION ───────────────────────────────────────────────────────
def strip_emoji(text: str) -> str:
    """Hapus karakter emoji dan simbol non-ASCII untuk rendering yang lebih stabil."""
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)

# ─── DOCUMENT DISPLAY ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if "Data Acquisition Plan" in doc_choice:
    doc_path = os.path.join(BASE_DIR, "docs", "DATA-ACQUISITION-PLAN.md")
    doc_name = "DATA-ACQUISITION-PLAN.md"
    
elif "Framework Awal" in doc_choice:
    doc_path = os.path.join(BASE_DIR, "docs", "project-plan", "Framework Awal - Feedback & Analisis.md")
    doc_name = "Framework Awal - Feedback & Analisis.md"

# Read and display the document
if os.path.exists(doc_path):
    with open(doc_path, "r", encoding="utf-8") as f:
        raw_content = f.read()
    
    # Clean emoji untuk rendering yang lebih stabil
    clean_content = strip_emoji(raw_content)
    
    # Display in a styled container
    st.markdown('<div class="doc-content">', unsafe_allow_html=True)
    st.markdown(clean_content)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Download button
    st.markdown("---")
    with open(doc_path, "rb") as f:
        st.download_button(
            label=f"Unduh {doc_name}",
            data=f,
            file_name=doc_name,
            mime="text/markdown",
        )
else:
    st.error(f"❌ File tidak ditemukan: {doc_path}")

# ─── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-size: 0.75rem; color: #616161; text-align: center;">
CELIOS Research Division · Dokumentasi Riset · Juni 2026
</div>
""", unsafe_allow_html=True)
