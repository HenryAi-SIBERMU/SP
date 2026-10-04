import geopandas as gpd

gdf_pkg = gpd.read_file('data/raw/osm/parking_jakarta.gpkg')
named = gdf_pkg[gdf_pkg['name'].notna() & ~gdf_pkg['name'].str.contains('warga|motor|taman park|tempat parkir', case=False, na=False)]
print("Total named parking:", len(named))
for idx, r in named.head(30).iterrows():
    pt = r.geometry if r.geometry.geom_type == 'Point' else r.geometry.centroid
    print(f"[{idx}] {r['name']} ({r.get('parking')}) -> ({pt.y:.6f}, {pt.x:.6f})")
