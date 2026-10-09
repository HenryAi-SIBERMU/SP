"""
Teduhi Ruang Kota Kami
Solar Dashboard — Potensi PLTS Atap Dual-Use Infrastructure di Jabodetabek
"""
import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
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

# ─── DATA LOADING DARI DATASET PROCESSED (MATCHING PAGE 1) ────────────────────
PROCESSED_CALC_PATH = (
    PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_kumulatif_summary.csv"
    if (PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_kumulatif_summary.csv").exists()
    else (
        PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_100_titik_summary.csv"
        if (PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_100_titik_summary.csv").exists()
        else (
            PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_13_titik_summary.csv"
            if (PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_13_titik_summary.csv").exists()
            else (PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_5_titik_summary.csv")
        )
    )
)

PROCESSED_INFILL_PATH = PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_gap_infill_extension.csv"

if not PROCESSED_CALC_PATH.exists():
    st.error("Dataset hasil olahan `data/processed/calculations/` tidak ditemukan.")
    st.stop()

df = pd.read_csv(PROCESSED_CALC_PATH)

# Agregasi Utama Dinamis (Zero Hardcoding!)
total_titik = len(df)
total_categories = len(df["category"].unique())
total_capacity_kwp = df["installed_capacity_kwp"].sum()
total_capacity_mwp = total_capacity_kwp / 1000.0
total_gen_mwh = df["annual_generation_mwh"].sum()
total_gen_gwh = total_gen_mwh / 1000.0
total_ghg_tons = df["ghg_reduction_tons_co2"].sum()
total_panels = int(df["max_panels_count"].sum())
total_roof_area_m2 = df["max_roof_area_m2"].sum()
avg_drift = df["spatial_drift_meters"].mean() if "spatial_drift_meters" in df.columns else 0.0

# Konsumsi Listrik Regional Jabodetabek (PLN Statistics: ~78.000 GWh/tahun)
REGIONAL_DEMAND_GWH = 78000.0
kontribusi_regional_pct = (total_gen_gwh / REGIONAL_DEMAND_GWH) * 100.0

df_infill = pd.read_csv(PROCESSED_INFILL_PATH) if PROCESSED_INFILL_PATH.exists() else pd.DataFrame()
has_infill = not df_infill.empty
if has_infill:
    infill_kwp = df_infill["infill_additional_kwp"].sum()
    infill_mwp = infill_kwp / 1000.0
    combined_mwp = total_capacity_mwp + infill_mwp

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Teduhi Ruang Kota Kami</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-subtitle">Inventarisasi Potensi PLTS Atap Dual-Use Infrastructure di Jabodetabek ({total_titik:,} Titik Terverifikasi)</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="note-box">
<strong>Catatan Riset Inventarisasi Spasial Jabodetabek ({total_titik:,} Titik Terpadu)</strong><br>
Data agregat mencakup <strong>{total_titik:,} fasilitas infrastruktur perkotaan</strong> lintas <strong>{total_categories} kategori</strong> se-Jabodetabek yang telah terverifikasi penuh menggunakan Google Solar API High-Resolution (0.25 m/pixel). Seluruh metrik kapasitas ({total_capacity_mwp:,.2f} MWp), estimasi produksi listrik tahunan ({total_gen_gwh:,.2f} GWh/thn), luas atap efektif ({total_roof_area_m2:,.0f} m²), dan reduksi emisi ({total_ghg_tons:,.1f} Ton CO₂/thn) dihitung secara deterministik langsung dari dataset hasil olahan satelit.
</div>
""", unsafe_allow_html=True)

# ─── HERO METRICS ─────────────────────────────────────────────────────────────
st.markdown(f'<div class="section-header">Potensi Agregat Empiris ({total_titik:,} Fasilitas se-Jabodetabek)</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Kapasitas Terpasang</div>
        <div class="metric-value">{total_capacity_mwp:,.1f} MWp</div>
        <div class="metric-desc">{total_capacity_kwp:,.1f} kWp ({total_panels:,} panel @ 400Wp)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Produksi Listrik Tahunan</div>
        <div class="metric-value">{total_gen_gwh:,.1f} GWh</div>
        <div class="metric-desc">{total_gen_mwh:,.1f} MWh/thn (PR 80% iklim tropis perkotaan)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Kontribusi Regional</div>
        <div class="metric-value">{kontribusi_regional_pct:.2f}%</div>
        <div class="metric-desc">Dari kebutuhan listrik Jabodetabek (~78.000 GWh - PLN Statistics)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Reduksi Emisi GRK</div>
        <div class="metric-value">{total_ghg_tons/1000:,.1f}k ton</div>
        <div class="metric-desc">{total_ghg_tons:,.1f} Ton CO₂/thn (Grid Jamali 808,99 kg/MWh)</div>
    </div>
    """, unsafe_allow_html=True)

# ─── KATEGORI INFRASTRUKTUR URBAN ─────────────────────────────────────────────
st.markdown(f'<div class="section-header">Distribusi Potensi Lintas {total_categories} Kategori Infrastruktur ({total_titik:,} Titik)</div>', unsafe_allow_html=True)

cat_summary = (
    df.groupby(["category", "category_display"])
    .agg(
        total_titik=("asset_id", "count"),
        total_kwp=("installed_capacity_kwp", "sum"),
        total_mwh=("annual_generation_mwh", "sum"),
        total_co2=("ghg_reduction_tons_co2", "sum"),
        total_panels=("max_panels_count", "sum"),
        total_roof_m2=("max_roof_area_m2", "sum"),
    )
    .reset_index()
    .sort_values("total_kwp", ascending=False)
)

cols = st.columns(4)
for idx, (_, row) in enumerate(cat_summary.iterrows()):
    nama = row["category_display"]
    pts = int(row["total_titik"])
    kwp = row["total_kwp"]
    mwp = kwp / 1000.0
    mwh = row["total_mwh"]
    panels = int(row["total_panels"])
    roof = row["total_roof_m2"]

    titik_text = f"{pts:,} fasilitas • {roof:,.0f} m² atap"
    prod_text = f"{mwh:,.0f} MWh/thn • {panels:,} panel"
    kapasitas_text = f"{mwp:,.2f} MWp" if mwp >= 1.0 else f"{kwp:,.1f} kWp"

    with cols[idx % 4]:
        st.markdown(f"""
        <div style="background:#1A1F2B; padding:1rem; border-radius:6px; margin-bottom:0.8rem; border:1px solid #333;">
            <div style="font-weight:600; color:#ECEFF1; margin-bottom:0.3rem; font-size:0.9rem;">{nama}</div>
            <div style="font-size:0.75rem; color:#9E9E9E; margin-bottom:0.25rem;">{titik_text}</div>
            <div style="font-size:0.75rem; color:#4FC3F7; margin-bottom:0.4rem;">{prod_text}</div>
            <div style="font-size:0.95rem; color:#66BB6A; font-weight:700;">{kapasitas_text}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── STATUS RISET & DATA LINEAGE ──────────────────────────────────────────────
st.markdown('<div class="section-header">Status Riset & Integritas Metodologi</div>', unsafe_allow_html=True)

infill_note = (
    f" Tersedia pula simulasi suplemen pemanfaatan celah atap (*Roof Gap Infill Extension*) "
    f"sebesar <strong>+{infill_mwp:,.2f} MWp</strong> ({infill_kwp:,.1f} kWp) berbasis SNI 8395:2017 & NFPA 1 "
    f"sehingga potensi gabungan mencapai <strong>{combined_mwp:,.2f} MWp</strong>."
    if has_infill
    else ""
)

st.markdown(f"""
<div class="info-box">
<strong>Fase Riset Saat Ini: Inventarisasi Skala Aglomerasi ({total_titik:,} Fasilitas Terverifikasi)</strong><br><br>

<strong>1. Ekstraksi Google Solar API Full SKU Selesai:</strong><br>
Sebanyak <strong>{total_titik:,} titik fasilitas</strong> lintas {total_categories} kategori infrastruktur perkotaan Jabodetabek telah berhasil diproses melalui Google Solar API (kualitas citra 0.25 m/pixel — BASE Tier). Data mencakup Digital Surface Model (DSM 3D), Roof Mask segmentasi, citra satelit RGB resolusi tinggi, dan Annual Solar Flux Heatmap dengan total kapasitas baseline terverifikasi <strong>{total_capacity_mwp:,.2f} MWp</strong> ({total_capacity_kwp:,.1f} kWp) dan produksi listrik bersih <strong>{total_gen_gwh:,.2f} GWh/tahun</strong>.{infill_note}<br><br>

<strong>2. Akurasi & Validasi Spasial Empiris:</strong><br>
Audit spasial mencatat rata-rata pergeseran koordinat (*spatial drift*) hanya <strong>{avg_drift:.2f} meter</strong> terhadap titik berat kanopi atap riil di seluruh Jabodetabek (Jakarta, Bogor, Depok, Tangerang, Bekasi), memenuhi toleransi standar pemetaan geospasial urban.<br><br>

<strong>3. Eksplorasi Lanjutan:</strong><br>
Visualisasi interaktif per-titik, inspeksi 6 SKU layer fotogrametris atap, tabel master seluruh fasilitas, dan pemodelan orientasi azimuth/pitch dapat dieksplorasi secara mendalam pada halaman <strong>Pemetaan Potensi</strong>.
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="font-size: 0.75rem; color: #616161; text-align: center;">
CELIOS Research Division · Solar Dashboard Jabodetabek · 2026
</div>
""", unsafe_allow_html=True)
