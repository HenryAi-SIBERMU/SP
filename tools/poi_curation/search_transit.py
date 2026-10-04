import pandas as pd
import geopandas as gpd

print("=== KRL STATIONS ===")
df_krl = pd.read_csv('data/raw/krl/krl_stations.csv')
print(df_krl.head(10)[['Nama_Stasiun', 'Latitude', 'Longitude']])

print("\n=== MRT STATIONS ===")
df_mrt = pd.read_csv('data/raw/mrt_lrt/mrt_stations.csv')
print(df_mrt[['Nama_Stasiun', 'Latitude', 'Longitude']])

print("\n=== LRT JABODEBEK ===")
gdf_lrt_jab = gpd.read_file('data/raw/mrt_lrt/lrt_jabodebek_stations.geojson')
for idx, r in gdf_lrt_jab.head(8).iterrows():
    pt = r.geometry if r.geometry.geom_type == 'Point' else r.geometry.centroid
    print(f"{r.get('name', r.get('id'))} -> ({pt.y:.6f}, {pt.x:.6f})")

print("\n=== LRT JAKARTA ===")
gdf_lrt_jkt = gpd.read_file('data/raw/mrt_lrt/lrt_jkt_stations.geojson')
for idx, r in gdf_lrt_jkt.head(8).iterrows():
    pt = r.geometry if r.geometry.geom_type == 'Point' else r.geometry.centroid
    print(f"{r.get('name', r.get('id'))} -> ({pt.y:.6f}, {pt.x:.6f})")

print("\n=== BRT TRANSJAKARTA (SAMPLE CORRIDORS) ===")
df_tj = pd.read_csv('data/raw/transjakarta/transjakarta_stations.csv')
kw_brt = ['csw', 'tosari', 'bundaran senayan', 'monas', 'harmoni', 'ragunan', 'kampung melayu', 'pulo gadung']
for kw in kw_brt:
    m = df_tj[df_tj['Nama_Halte'].astype(str).str.contains(kw, case=False, na=False)]
    if not m.empty:
        r = m.iloc[0]
        print(f"BRT [{kw}]: {r['Nama_Halte']} -> ({r['Latitude']}, {r['Longitude']})")
