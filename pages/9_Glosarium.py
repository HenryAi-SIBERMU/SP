"""
Glosarium Ilmiah & Parameter Baku PLTS
Kamus acuan parameter teknis, rumus fisika radiasi surya, terminologi standar,
dan kriteria kelayakan PLTS Atap (NREL, ASHRAE, SNI 8395:2017).
"""
import streamlit as st
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.components.sidebar import render_sidebar
from src.utils.styling import get_solar_css

st.set_page_config(
    page_title="Glosarium — CELIOS Solar Dashboard",
    page_icon="refrensi/Celios China-Indonesia Energy Transition.png",
    layout="wide",
)

render_sidebar()
st.markdown(get_solar_css(), unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.title("Glosarium Ilmiah & Parameter Baku")
st.markdown(
    "Kamus parameter teknis, rumus fisika radiasi surya, terminologi standar, "
    "dan kondisi batas evaluasi potensi PLTS Atap berdasarkan **NREL PVWatts V5**, "
    "**NREL Solar Position Algorithm (SPA)**, **ASHRAE Fundamentals**, dan **SNI 8395:2017**."
)

st.markdown("---")

# ─── SECTION 1: PRINSIP FISIKA & TEORI BAKU ──────────────────────────────────
st.subheader("1. Prinsip Fisika & Teori Baku")

st.markdown("""
* **Sudut Datang Sinar (*Angle of Incidence* / AOI - NREL Eq. 1):**  
  Sudut antara berkas sinar matahari langsung dengan garis tegak lurus bidang modul dihitung matematis berdasarkan persamaan geometris:
""")
st.latex(r"\alpha_{\text{fixed}} = \cos^{-1}\left[\sin(\theta_{\text{sun}}) \cos(\gamma - \gamma_{\text{sun}}) \sin(\beta) + \cos(\theta_{\text{sun}}) \cos(\beta)\right]")
st.markdown("""
  Di mana:
  - $\\beta$: Sudut kemiringan atap (*tilt*)
  - $\\gamma$: Azimuth arah hadap atap
  - $\\theta_{\\text{sun}}$: Sudut zenith matahari
  - $\\gamma_{\\text{sun}}$: Azimuth posisi matahari di cakrawala

* **Total Iradiansi Bidang Panel (*Plane-of-Array* / POA - NREL Eq. 2):**
""")
st.latex(r"I_{\text{poa}} = I_b + I_{d,\text{sky}} + I_{d,\text{ground}}")
st.markdown("""
  Energi yang diterima modul surya merupakan penjumlahan dari:
  - Radiasi langsung (*beam* $I_b$)
  - Radiasi bauran atmosfer (*diffuse sky* $I_{d,\\text{sky}}$ via model Perez)
  - Pantulan permukaan tanah/atap (*ground-reflected albedo* $I_{d,\\text{ground}}$ dengan nilai default 0.20)

* **Orientasi Optimum Belahan Bumi Selatan (Jakarta Lintang $\\approx -6.2^\\circ\\text{ LS}$):**  
  Sesuai NREL PVWatts (Tabel 2), sistem PLTS di belahan bumi selatan memiliki orientasi azimuth tahunan optimum baku **$0^\\circ$ (Menghadap Utara)** dengan sudut kemiringan mendekati lintang wilayah ($5^\\circ–10^\\circ$) untuk memaksimalkan tangkapan energi tahunan.
""")

st.markdown("---")

# ─── SECTION 2: TERMINOLOGI STANDAR TEKNIK ───────────────────────────────────
st.subheader("2. Terminologi Standar Teknik")

col_term1, col_term2 = st.columns(2)

with col_term1:
    st.markdown("""
    * **Azimuth Bidang Atap ($\\gamma$):**  
      Sudut hadap bidang permukaan atap yang diukur searah jarum jam dari arah Utara geografis:
      - $0^\\circ = \\text{Utara}$
      - $90^\\circ = \\text{Timur}$
      - $180^\\circ = \\text{Selatan}$
      - $270^\\circ = \\text{Barat}$  
      *(Sesuai konvensi baku NREL Solar Position Algorithm / SPA)*.

    * **Kemiringan / Pitch / Tilt ($\\beta$):**  
      Sudut inklinasi bidang permukaan atap terhadap bidang horizontal bumi ($0^\\circ = \\text{bidang datar}$, $90^\\circ = \\text{fasad vertikal}$).

    * **Sudut Zenith Matahari ($\\theta_{\\text{sun}}$):**  
      Sudut antara garis vertikal tepat di atas kepala pengamat (*zenith*) dengan posisi matahari ($0^\\circ = \\text{matahari tepat di atas kepala}$, $90^\\circ = \\text{matahari di cakrawala}$).
    """)

with col_term2:
    st.markdown("""
    * **Solar Noon (Kulminasi Matahari):**  
      Waktu saat matahari mencapai titik elevasi harian tertinggi pada meridian bujur lokasi (berbeda dengan jam 12.00 siang waktu lokal karena pengaruh persamaan waktu / *Equation of Time*).

    * **Ambang Batas Pembersihan Mandiri (*Self-Cleaning Threshold*):**  
      Kemiringan fisik modul minimal $\\ge 10^\\circ$ yang disyaratkan secara teknis agar air hujan dapat meluruhkan kotoran dan debu secara gravitasi tanpa meninggalkan endapan air di bingkai bawah modul (*soiling losses*).

    * **Faktor Kapasitas (*Capacity Factor* / CF):**  
      Rasio antara energi listrik riil yang dihasilkan dalam satu tahun terhadap energi teoritis jika sistem beroperasi pada daya nominal penuh selama 8.760 jam non-stop.
    """)

st.markdown("---")

# ─── SECTION 3: SATUAN & METRIK TERSTANDARISASI ──────────────────────────────
st.subheader("3. Satuan & Metrik Terstandarisasi")

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    st.markdown("""
    **Daya & Energi:**
    * **$\\text{Watt-peak (Wp) / kWp}$:**  
      Kapasitas daya nominal modul PV pada Kondisi Uji Standar (*Standard Test Conditions* / STC: iradiansi $1.000\\text{ W/m}^2$, temperatur sel $25^\\circ\\text{C}$, massa udara AM 1.5).
    * **$\\text{MWh/tahun}$:**  
      Total produksi energi listrik bolak-balik (AC) netto yang diestimasikan dapat disalurkan ke sistem beban gedung dalam satu tahun operasional (8.760 jam).
    """)

with col_m2:
    st.markdown("""
    **Radiasi & Fluks:**
    * **$\\text{W/m}^2$ (Watt per meter persegi):**  
      Satuan fluks daya iradiansi matahari seketika yang jatuh pada suatu bidang datar.
    * **$\\text{kWh/m}^2/\\text{hari}$ (Peak Sun Hours / PSH):**  
      Akumulasi energi radiasi harian. Wilayah Jabodetabek rata-rata berkisar antara $4.2–4.8\\text{ kWh/m}^2/\\text{hari}$.
    """)

with col_m3:
    st.markdown("""
    **Geometri & Dimensi:**
    * **Derajat Busur ($^\\circ$):**  
      Satuan besaran sudut untuk Azimuth ($0^\\circ–360^\\circ$) dan Kemiringan ($0^\\circ–90^\\circ$).
    * **Meter Persegi ($\\text{m}^2$):**  
      Luas bidang atap 3D (*Plane Area*) yang memperhitungkan sudut kemiringan terhadap luas tapak horizontal (*Ground Area*).
    """)

st.markdown("---")

# ─── SECTION 4: DASAR SAINS HUBUNGAN PITCH & AZIMUTH ─────────────────────────
st.subheader("4. Dasar Sains PLTS: Hubungan Kemiringan (Pitch) & Azimuth")
st.markdown("Dalam perancangan PLTS atap, kemiringan dan arah hadap atap harus selalu dianalisis berpasangan:")

col_sc1, col_sc2 = st.columns(2)

with col_sc1:
    st.markdown("""
    ##### Kemiringan Menentukan Efisiensi & Drainase
    1. **Atap Datar ($< 3^\\circ$):**  
       Tangkapan radiasi simetris harian, namun air hujan dan debu cenderung menggenang. Perlu struktur penopang (*mounting rack*) miring $8^\\circ–10^\\circ$.
    2. **Atap Miring ($10^\\circ–25^\\circ$):**  
       Ideal untuk pembersihan alami (*self-cleaning*) oleh air hujan di wilayah beriklim tropis monsun seperti Indonesia.
    3. **Kemiringan Ekstrem ($> 60^\\circ$):**  
       Tidak layak dipasang modul karena sudut datang sinar matahari sangat miring dan risiko beban angin tinggi.
    """)

with col_sc2:
    st.markdown("""
    ##### Azimuth Menentukan Jam Puncak Produksi
    * **Miring ke Timur (Azimuth $\\sim 90^\\circ$):**  
      Memproduksi listrik maksimal di **pagi hari (07.00 – 11.00)**. Sangat selaras dengan profil beban gedung sekolah dan perkantoran.
    * **Miring ke Barat (Azimuth $\\sim 270^\\circ$):**  
      Memproduksi listrik maksimal di **siang–sore (12.00 – 16.00)**. Sangat selaras dengan puncak penggunaan pendingin udara (AC) komersial.
    * **Miring ke Utara (Azimuth $\\sim 0^\\circ$):**  
      Orientasi optimum di belahan bumi selatan dengan yield total tahunan paling tinggi.
    * **Miring ke Selatan (Azimuth $\\sim 180^\\circ$):**  
      Penalti yield minor di belahan bumi selatan, tetap layak dengan profil produksi simetris di sekitar solar noon.
    """)

st.markdown("---")

# ─── SECTION 5: STANDAR ORIENTASI SURYA INTERNASIONAL & SNI ──────────────────
st.subheader("5. Tabel Rujukan Orientasi Surya (NREL PVWatts & SNI 8395:2017)")

ref_csv_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data", "processed", "references", "standar_orientasi_surya_nrel_sni.csv"
)

if os.path.exists(ref_csv_path):
    try:
        ref_df = pd.read_csv(ref_csv_path)
        display_df = ref_df[[
            "kode_mata_angin", "arah_mata_angin", "rentang_azimuth_derajat",
            "karakteristik_radiasi_surya", "jam_puncak_indikatif",
            "standar_primer_internasional", "standar_nasional_sni"
        ]].rename(columns={
            "kode_mata_angin": "Kode",
            "arah_mata_angin": "Arah",
            "rentang_azimuth_derajat": "Rentang Azimuth",
            "karakteristik_radiasi_surya": "Karakteristik Radiasi",
            "jam_puncak_indikatif": "Jam Puncak",
            "standar_primer_internasional": "Standar Internasional",
            "standar_nasional_sni": "Standar Nasional"
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.caption(f"Tabel referensi tersedia di repositori: `data/processed/references/standar_orientasi_surya_nrel_sni.csv`")

st.markdown("---")

# ─── SECTION 6: KONDISI BATAS & KRITERIA PENERAPAN PRAKTIS ───────────────────
st.subheader("6. Kondisi Batas & Kriteria Eliminasi")

st.markdown("""
* **Karakteristik Atap Datar (*Flat Roof*, Kemiringan $< 3^\\circ$):**  
  Tangkapan radiasi simetris dengan puncak di jam 11.00–13.00. Deviasi energi tahunan sangat tipis ($< 1.5\\%$) terhadap kemiringan optimum, namun di lapangan tetap disarankan memasang struktur penopang (*mounting rack*) miring minimal $8^\\circ–10^\\circ$ demi drainase air hujan dan pencegahan *soiling loss*.

* **Kriteria Eliminasi Google Solar API (Segmen 0 Panel):**  
  Google Solar API secara otomatis tidak menempatkan panel pada segmen atap tertentu jika:
  1. Ukuran bidang terlalu sempit untuk modul standar ($< 1.97\\text{ m}^2$).
  2. Kemiringan ekstrim ($> 60^\\circ$) seperti dinding lisplang/parapet vertikal.
  3. Mengalami bayangan rintangan permanen (*heavy shading*) dari struktur bertingkat sekitar.
  4. Terletak di zona batas aman tepi perimeter (*setback clearance*).

* **Arsip Dokumen Acuan di Repositori:**
  - Berkas PDF NREL PVWatts V5 Manual: `data/processed/references/nrel_pvwatts_version5_manual.pdf` (NREL/TP-6A20-62641).
  - Berkas PDF NREL SPA Technical Report: `data/processed/references/nrel_spa_technical_report_34302.pdf` (NREL/TP-560-34302).
  - Kamus Acuan Metadata: `data/processed/references/standar_orientasi_surya_nrel_sni.csv`.
""")
