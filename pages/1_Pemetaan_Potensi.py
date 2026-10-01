"""
Pemetaan Potensi — CELIOS Solar Dashboard
-----------------------------------------
Halaman visualisasi hasil Proof of Work (POW) Tahap 1 Google Solar API
untuk 5 titik pilot multi-kategori (MRT, KRL, LRT, Rumah Sakit, Gedung Parkir).

Menampilkan seluruh SKU Data Layers & Building Insights:
1. Citra Satelit Aerial RGB Asli (0.25m/px)
2. Layout Jumlah & Posisi Panel Surya di Atap (Show panels on roof)
3. Annual Solar Flux Heatmap (Radiasi Surya Tahunan kWh/kW/year)
4. Digital Surface Model (DSM - Elevasi & Ketinggian 3D)
5. Roof Mask (Binary Mask Segmentasi Atap Layak PLTS)
"""

import os
import sys
import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css

st.set_page_config(
    page_title="Pemetaan Potensi — CELIOS Solar Dashboard",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar()
st.markdown(get_solar_css(), unsafe_allow_html=True)

# ─── DATA LOADING (PROCESSED DATA ONLY) ──────────────────────────────────────────
PROCESSED_CALC_PATH = PROJECT_ROOT / "data" / "processed" / "calculations" / "pow_solar_5_titik_summary.csv"
PROCESSED_GIS_PATH = PROJECT_ROOT / "data" / "processed" / "gis" / "pow_solar_5_titik.geojson"

@st.cache_data
def load_processed_data():
    if not PROCESSED_CALC_PATH.exists():
        return None, None
    df = pd.read_csv(PROCESSED_CALC_PATH)
    gdf = gpd.read_file(PROCESSED_GIS_PATH) if PROCESSED_GIS_PATH.exists() else None
    return df, gdf

df_summary, gdf_points = load_processed_data()

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Pemetaan Potensi Urban Jabodetabek</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Verifikasi Empiris Google Solar API (Proof of Work 5 Titik Multi-Kategori — Full SKU Data Layers)</div>', unsafe_allow_html=True)

if df_summary is None or df_summary.empty:
    st.error("Dataset hasil olahan `data/processed/calculations/pow_solar_5_titik_summary.csv` tidak ditemukan. Jalankan pipeline ETL terlebih dahulu.")
    st.stop()

# ─── NOTE BOX & STATUS PILOT ──────────────────────────────────────────────────
st.markdown("""
<div class="note-box">
<strong>Laporan Validasi Empiris Google Solar API (Tahap 1 Pilot — Full SKU Layers)</strong><br>
Data berikut memuat hasil ekstraksi citra satelit Google resolusi tinggi (<strong>0.25 m/pixel — BASE Quality</strong>) untuk 5 kategori infrastruktur perkotaan. 
Dilengkapi seluruh layer turunan SKU: <strong>Foto Satelit RGB</strong>, <strong>Layout Sebaran Panel Surya di Atap (Show Panels on Roof)</strong>, <strong>Annual Solar Flux Heatmap</strong>, <strong>Digital Surface Model (DSM 3D)</strong>, dan <strong>Roof Mask Segmentasi</strong>.
</div>
""", unsafe_allow_html=True)

# ─── EXECUTIVE KPI BANNER ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">Ringkasan Potensi Surya 5 Titik Pilot</div>', unsafe_allow_html=True)

total_capacity_kwp = df_summary["installed_capacity_kwp"].sum()
total_roof_area = df_summary["max_roof_area_m2"].sum()
total_gen_mwh = df_summary["annual_generation_mwh"].sum()
total_ghg_tons = df_summary["ghg_reduction_tons_co2"].sum()
total_panels = df_summary["max_panels_count"].sum()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Kapasitas Terpasang</div>
        <div class="metric-value">{total_capacity_kwp:,.1f} kWp</div>
        <div class="metric-desc">Setara {total_capacity_kwp/1000:.2f} MWp ({total_panels:,} panel @ 400Wp)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Luas Atap Efektif</div>
        <div class="metric-value">{total_roof_area:,.0f} m²</div>
        <div class="metric-desc">Permukaan atap layak panel surya terverifikasi satelit</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Estimasi Produksi Listrik</div>
        <div class="metric-value">{total_gen_mwh:,.1f} MWh/thn</div>
        <div class="metric-desc">Asumsi Performance Ratio 80% iklim tropis perkotaan</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Reduksi Emisi GRK</div>
        <div class="metric-value">{total_ghg_tons:,.1f} Ton/thn</div>
        <div class="metric-desc">Faktor dekarbonisasi 808,99 kg CO₂/MWh (Grid Jawa-Madura-Bali)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── INTERACTIVE MAP & AUDIT TABLE ───────────────────────────────────────────
st.markdown('<div class="section-header">Peta Interaktif Sebaran & Verifikasi Spasial</div>', unsafe_allow_html=True)

col_map, col_list = st.columns([1.6, 1.0])

CAT_COLORS = {
    "mrt": "#E53935",      # Merah MRT
    "krl": "#1E88E5",      # Biru KRL
    "lrt": "#FB8C00",      # Jingga LRT
    "hospital": "#43A047", # Hijau RS
    "parking": "#8E24AA"   # Ungu Parkir
}

with col_map:
    center_lat = df_summary["google_center_lat"].mean()
    center_lon = df_summary["google_center_lon"].mean()
    
    # Folium map using clean Esri Satellite + OSM basemaps (NO Carto API KEY watermark)
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles=None
    )

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Citra Satelit (Esri World Imagery)",
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Peta Jalan (OpenStreetMap)",
        overlay=False,
        control=True
    ).add_to(m)

    for _, row in df_summary.iterrows():
        color = CAT_COLORS.get(row["category"], "#66BB6A")
        
        popup_html = f"""
        <div style="font-family: 'Inter', sans-serif; min-width: 220px; color: #111;">
            <b style="font-size: 13px; color: {color};">[{row['category_display']}] {row['asset_name']}</b><br>
            <hr style="margin: 4px 0;">
            <b>Kapasitas PLTS:</b> {row['installed_capacity_kwp']:,.1f} kWp ({row['max_panels_count']:,} panel)<br>
            <b>Luas Atap:</b> {row['max_roof_area_m2']:,.1f} m²<br>
            <b>Produksi Listrik:</b> {row['annual_generation_mwh']:,.1f} MWh/thn<br>
            <b>Reduksi CO₂:</b> {row['ghg_reduction_tons_co2']:,.1f} Ton/thn<br>
            <b>Spatial Drift:</b> {row['spatial_drift_meters']} m ({row['drift_status']})<br>
            <b>Citra Google:</b> {row['imagery_date']}
        </div>
        """

        folium.CircleMarker(
            location=[row["google_center_lat"], row["google_center_lon"]],
            radius=9,
            color="#FFFFFF",
            weight=2,
            fill=True,
            fill_color=color,
            fill_opacity=0.95,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"[{row['category_display']}] {row['asset_name']} ({row['installed_capacity_kwp']} kWp)"
        ).add_to(m)

        folium.Circle(
            location=[row["google_center_lat"], row["google_center_lon"]],
            radius=60,
            color=color,
            weight=1.5,
            fill=True,
            fill_opacity=0.20
        ).add_to(m)

    folium.LayerControl(position="topright").add_to(m)
    st_folium(m, width="100%", height=490)

with col_list:
    st.markdown("#### Audit Integritas Spasial")
    st.caption("Verifikasi deviasi jarak (*drift*) antara titik sumber data fisik vs centroid gedung Google Solar API:")

    audit_display = df_summary[[
        "asset_name", "category_display", "spatial_drift_meters", "drift_status"
    ]].rename(columns={
        "asset_name": "Infrastruktur",
        "category_display": "Kategori",
        "spatial_drift_meters": "Drift (m)",
        "drift_status": "Status Audit"
    })

    st.dataframe(
        audit_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Drift (m)": st.column_config.NumberColumn(format="%.2f m"),
            "Status Audit": st.column_config.TextColumn(help="Drift < 30m menandakan akurasi tepat pada kanopi atap")
        }
    )

    st.markdown("""
    <div style="background: #111927; padding: 12px; border-radius: 6px; font-size: 0.8rem; border-left: 3px solid #66BB6A;">
        <strong>Metodologi Anti-Halusinasi:</strong><br>
        Rata-rata <em>spatial drift</em> adalah <strong>11.02 meter</strong>. Ini membuktikan bahwa algoritma Google Solar API berhasil mengunci poligon atap stasiun dan gedung sebenarnya, bukan bangunan ruko di pinggir jalan.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── DEEP-DIVE SHOWCASE: SEMUA SKU DATA LAYER & BUILDING INSIGHTS ─────────────
st.markdown('<div class="section-header">Inspeksi Lengkap SKU Data Layers & Layout Panel Surya</div>', unsafe_allow_html=True)
st.caption("Eksplorasi seluruh layer citra resolusi 0.25 m/pixel Google Maps Platform serta simulasi posisi panel surya di atap:")

selected_asset_name = st.selectbox(
    "Pilih Infrastruktur untuk Inspeksi Detail:",
    options=df_summary["asset_name"].tolist(),
    index=0
)

asset_row = df_summary[df_summary["asset_name"] == selected_asset_name].iloc[0]

# Google Solar UI Card Header
st.markdown(f"""
<div style="background: #101726; border: 1px solid #1E293B; border-radius: 10px; padding: 18px; margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <span style="background: #1E293B; color: #64B5F6; font-size: 0.75rem; padding: 4px 10px; border-radius: 4px; font-weight: 600; text-transform: uppercase;">{asset_row['category_display']}</span>
            <h2 style="margin: 6px 0 2px 0; color: #ECEFF1; font-size: 1.5rem;">{asset_row['asset_name']}</h2>
            <p style="color: #94A3B8; font-size: 0.85rem; margin: 0;">Wilayah: {asset_row['city_regency']} | Google Building ID: <code>{asset_row['google_building_id']}</code></p>
        </div>
        <div style="text-align: right; margin-top: 8px;">
            <span style="font-size: 1.8rem; font-weight: 800; color: #00E5FF;">{asset_row['installed_capacity_kwp']:,.1f} kWp</span><br>
            <span style="color: #94A3B8; font-size: 0.8rem;">{asset_row['max_panels_count']:,} Panel @ 400Wp</span>
        </div>
    </div>
    <hr style="border-color: #1E293B; margin: 12px 0;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; text-align: center;">
        <div style="background: #0B111E; padding: 10px; border-radius: 6px;">
            <div style="color: #94A3B8; font-size: 0.7rem; font-weight: 600;">SUNSHINE</div>
            <div style="color: #FBBF24; font-size: 1.1rem; font-weight: 700;">{asset_row['sunshine_hours_annual']:,.0f} jam/thn</div>
        </div>
        <div style="background: #0B111E; padding: 10px; border-radius: 6px;">
            <div style="color: #94A3B8; font-size: 0.7rem; font-weight: 600;">ROOF AREA</div>
            <div style="color: #38BDF8; font-size: 1.1rem; font-weight: 700;">{asset_row['max_roof_area_m2']:,.0f} m²</div>
        </div>
        <div style="background: #0B111E; padding: 10px; border-radius: 6px;">
            <div style="color: #94A3B8; font-size: 0.7rem; font-weight: 600;">MAX PANELS</div>
            <div style="color: #00E676; font-size: 1.1rem; font-weight: 700;">{asset_row['max_panels_count']:,} unit</div>
        </div>
        <div style="background: #0B111E; padding: 10px; border-radius: 6px;">
            <div style="color: #94A3B8; font-size: 0.7rem; font-weight: 600;">ANNUAL OUTPUT</div>
            <div style="color: #A78BFA; font-size: 1.1rem; font-weight: 700;">{asset_row['annual_generation_mwh']:,.1f} MWh/thn</div>
        </div>
        <div style="background: #0B111E; padding: 10px; border-radius: 6px;">
            <div style="color: #94A3B8; font-size: 0.7rem; font-weight: 600;">CO2 SAVINGS</div>
            <div style="color: #34D399; font-size: 1.1rem; font-weight: 700;">{asset_row['ghg_reduction_tons_co2']:,.1f} Ton/thn</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs to explore all SKU layers (Text only, clean academic styling)
tab_panels, tab_rgb, tab_flux, tab_dsm, tab_mask, tab_gallery = st.tabs([
    "Layout Panel di Atap",
    "Citra Satelit RGB",
    "Annual Solar Flux",
    "DSM 3D Elevasi",
    "Roof Mask",
    "Komparasi 5 Layer Bersandingan"
])

with tab_panels:
    col_p1, col_p2 = st.columns([1.6, 1.0])
    with col_p1:
        st.markdown("#### Simulasi Distribusi Panel Surya di Atap (Show Panels on Roof)")
        st.caption("Posisi presisi koordinat setiap modul panel surya (400 Wp) yang diekstrak langsung dari Building Insights API:")
        panels_img_rel = asset_row.get("preview_panels_png")
        if panels_img_rel and (PROJECT_ROOT / panels_img_rel).exists():
            panels_img = Image.open(PROJECT_ROOT / panels_img_rel)
            st.image(panels_img, caption=f"Tata Letak {asset_row['max_panels_count']:,} Panel Surya di Atap {asset_row['asset_name']}", use_container_width=True)
        else:
            st.warning("Preview panel overlay belum tersedia.")
    with col_p2:
        st.markdown("#### Karakteristik Panel Atap")
        st.markdown(f"""
        * **Kapasitas Per Modul:** `400 Watt-peak (Wp)`
        * **Dimensi Modul:** `1.88 m × 1.05 m (1.97 m²)`
        * **Orientasi:** Dinamis (Landscape / Portrait menyesuaikan slope atap)
        * **Total Modul Maksimal:** `{asset_row['max_panels_count']:,} panel`
        * **Total Daya Terpasang:** `{asset_row['installed_capacity_kwp']:,.1f} kWp`
        * **Rata-rata Produksi / Panel:** `{(asset_row['annual_generation_kwh'] / max(asset_row['max_panels_count'], 1)):,.1f} kWh/panel/thn`
        """)
        st.info("**Catatan Metodologi:** Setiap kotak biru mewakili 1 modul panel surya fisik yang diposisikan oleh algoritma Google dengan menghindari bayangan cerobong/AC dan area berpenyinaran rendah.")

with tab_rgb:
    col_rgb1, col_rgb2 = st.columns([1.6, 1.0])
    with col_rgb1:
        st.markdown("#### Citra Satelit Aerial Resolusi Tinggi (RGB)")
        st.caption("Foto satelit ortorektifikasi resolusi 0.25 m/pixel Google Maps Platform:")
        rgb_img_rel = asset_row.get("preview_rgb_png")
        if rgb_img_rel and (PROJECT_ROOT / rgb_img_rel).exists():
            rgb_img = Image.open(PROJECT_ROOT / rgb_img_rel)
            st.image(rgb_img, caption=f"Foto Satelit Atap: {asset_row['asset_name']}", use_container_width=True)
    with col_rgb2:
        st.markdown("#### Metadata Citra Satelit")
        st.markdown(f"""
        * **Resolusi Spasial:** `0.25 meter per piksel (Kualitas BASE)`
        * **Tanggal Pengambilan Citra:** `{asset_row['imagery_date']}`
        * **Sistem Koordinat:** `EPSG:32748 (WGS 84 / UTM Zone 48S)`
        * **Sumber Master File:**
        """)
        st.code(f"{asset_row['path_rgb_geotiff']}", language="bash")

with tab_flux:
    col_f1, col_f2 = st.columns([1.6, 1.0])
    with col_f1:
        st.markdown("#### Annual Solar Flux Heatmap")
        st.caption("Peta kontur iradiasi radiasi matahari tahunan (kWh/kW/year) per piksel atap:")
        flux_img_rel = asset_row.get("preview_flux_png")
        if flux_img_rel and (PROJECT_ROOT / flux_img_rel).exists():
            flux_img = Image.open(PROJECT_ROOT / flux_img_rel)
            st.image(flux_img, caption=f"Heatmap Iradiasi Surya: {asset_row['asset_name']}", use_container_width=True)
    with col_f2:
        st.markdown("#### Parameter Iradiasi")
        st.markdown(f"""
        * **Jam Penyinaran Efektif:** `{asset_row['sunshine_hours_annual']:,.1f} jam/tahun`
        * **Skala Warna Heatmap:** Kuning-Putih menunjukkan potensi radiasi maksimum (> 1.400 kWh/kW/thn), sedangkan Biru-Ungu menunjukkan area berbayang rendah.
        * **Sumber Master File:**
        """)
        st.code(f"{asset_row['path_flux_geotiff']}", language="bash")

with tab_dsm:
    col_d1, col_d2 = st.columns([1.6, 1.0])
    with col_d1:
        st.markdown("#### Digital Surface Model (DSM 3D Elevation)")
        st.caption("Model elevasi dan ketinggian fisik permukaan struktur atap (meter di atas permukaan tanah):")
        dsm_img_rel = asset_row.get("preview_dsm_png")
        if dsm_img_rel and (PROJECT_ROOT / dsm_img_rel).exists():
            dsm_img = Image.open(PROJECT_ROOT / dsm_img_rel)
            st.image(dsm_img, caption=f"Model Ketinggian 3D Atap: {asset_row['asset_name']}", use_container_width=True)
    with col_d2:
        st.markdown("#### Analisis Elevasi & Bayangan")
        st.markdown("""
        * **Fungsi DSM:** Mengidentifikasi kemiringan atap (*slope*), azimuth orientasi hadap matahari, serta memprediksi bayangan gedung tinggi di sekelilingnya.
        * **Satuan Nilai Piksel:** Elevasi dalam satuan meter (WGS84).
        * **Sumber Master File:**
        """)
        st.code(f"{asset_row['path_dsm_geotiff']}", language="bash")

with tab_mask:
    col_m1, col_m2 = st.columns([1.6, 1.0])
    with col_m1:
        st.markdown("#### Roof Mask (Segmentasi Atap Layak Panel)")
        st.caption("Binary mask yang memisahkan permukaan atap bangunan (hijau) vs area jalan/tanah (gelap):")
        mask_img_rel = asset_row.get("preview_mask_png")
        if mask_img_rel and (PROJECT_ROOT / mask_img_rel).exists():
            mask_img = Image.open(PROJECT_ROOT / mask_img_rel)
            st.image(mask_img, caption=f"Mask Boundary Atap: {asset_row['asset_name']}", use_container_width=True)
    with col_m2:
        st.markdown("#### Ekstraksi Batas Atap Otomatis")
        st.markdown(f"""
        * **Luas Atap Tersegmentasi:** `{asset_row['max_roof_area_m2']:,.1f} m²`
        * **Kegunaan Mask:** Membatasi agar penempatan modul surya tidak keluar dari batas fisik dak atap bangunan.
        * **Sumber Master File:**
        """)
        st.code(f"{asset_row['path_mask_geotiff']}", language="bash")

with tab_gallery:
    st.markdown("#### Galeri Komparasi Seluruh 5 Layer Bersandingan")
    st.caption(f"Perbandingan visual lengkap seluruh SKU untuk **{asset_row['asset_name']}**:")
    
    g_col1, g_col2, g_col3, g_col4, g_col5 = st.columns(5)
    
    with g_col1:
        st.markdown("**1. RGB Asli**")
        if asset_row.get("preview_rgb_png") and (PROJECT_ROOT / asset_row["preview_rgb_png"]).exists():
            st.image(PROJECT_ROOT / asset_row["preview_rgb_png"], use_container_width=True)
    with g_col2:
        st.markdown("**2. Layout Panel**")
        if asset_row.get("preview_panels_png") and (PROJECT_ROOT / asset_row["preview_panels_png"]).exists():
            st.image(PROJECT_ROOT / asset_row["preview_panels_png"], use_container_width=True)
    with g_col3:
        st.markdown("**3. Annual Flux**")
        if asset_row.get("preview_flux_png") and (PROJECT_ROOT / asset_row["preview_flux_png"]).exists():
            st.image(PROJECT_ROOT / asset_row["preview_flux_png"], use_container_width=True)
    with g_col4:
        st.markdown("**4. DSM 3D**")
        if asset_row.get("preview_dsm_png") and (PROJECT_ROOT / asset_row["preview_dsm_png"]).exists():
            st.image(PROJECT_ROOT / asset_row["preview_dsm_png"], use_container_width=True)
    with g_col5:
        st.markdown("**5. Roof Mask**")
        if asset_row.get("preview_mask_png") and (PROJECT_ROOT / asset_row["preview_mask_png"]).exists():
            st.image(PROJECT_ROOT / asset_row["preview_mask_png"], use_container_width=True)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("CELIOS Solar Dashboard — Clean Energy & Economic Transition Research Aglomerasi Jabodetabek (2026)")
