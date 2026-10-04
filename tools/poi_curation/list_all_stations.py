import geopandas as gpd

gdf_stn = gpd.read_file('data/raw/osm/stations_jakarta.gpkg')
print(f"Total stations in GPKG: {len(gdf_stn)}")
for idx, r in gdf_stn.iterrows():
    pt = r.geometry if r.geometry.geom_type == 'Point' else r.geometry.centroid
    print(f"[{idx}] {r.get('name')} | op: {r.get('operator')} | railway: {r.get('railway')} -> ({pt.y:.6f}, {pt.x:.6f})")
