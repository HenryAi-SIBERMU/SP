import geopandas as gpd

gdf = gpd.read_file('data/raw/osm/buildings_jakarta.gpkg')
print(f"Total buildings in GPKG: {len(gdf)}")
named_bldg = gdf[gdf['name'].notna()]
print(f"Total named buildings: {len(named_bldg)}")

categories = {
    'mall': ['mall', 'plaza', 'square', 'grand indonesia', 'senayan', 'kelapa gading', 'kasablanka', 'puri'],
    'market': ['pasar', 'market'],
    'school': ['sma', 'smk', 'smp', 'sekolah', 'school'],
    'university': ['universitas', 'univ', 'institut', 'kampus', 'college', 'academy', 'akadem'],
    'stadium': ['stadion', 'gor', 'stadium', 'sport', 'velodrome', 'istora'],
    'terminal': ['terminal', 'halte', 'station'],
    'airport': ['bandara', 'airport', 'aeroway', 'terminal 1', 'terminal 2', 'terminal 3']
}

for cat, kw_list in categories.items():
    print(f"\n=== MENCARI {cat.upper()} ===")
    pattern = '|'.join(kw_list)
    matches = named_bldg[named_bldg['name'].str.contains(pattern, case=False, na=False)]
    print(f"Ditemukan {len(matches)} gedung:")
    for idx, r in matches.head(10).iterrows():
        pt = r.geometry if r.geometry.geom_type == 'Point' else r.geometry.centroid
        print(f"  [{r['name']}] -> ({pt.y:.6f}, {pt.x:.6f})")
