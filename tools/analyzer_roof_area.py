import os
import pandas as pd
import geopandas as gpd
import osmnx as ox
import time

# Configurations
DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
DATA_PROC_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
os.makedirs(DATA_PROC_DIR, exist_ok=True)

# Projected CRS for Jakarta (UTM Zone 48S) for accurate area calculation in meters
PROJECTED_CRS = "EPSG:32748"

def load_poi_data():
    """Load MRT, LRT, and KRL data"""
    gdfs = []
    
    # 1. MRT
    mrt_path = os.path.join(DATA_RAW_DIR, 'mrt_lrt', 'mrt_stations.csv')
    if os.path.exists(mrt_path):
        df_mrt = pd.read_csv(mrt_path)
        gdf_mrt = gpd.GeoDataFrame(df_mrt, geometry=gpd.points_from_xy(df_mrt.Longitude, df_mrt.Latitude), crs="EPSG:4326")
        gdf_mrt['Tipe'] = 'MRT'
        # Set nama
        if 'Nama_Stasiun' not in gdf_mrt.columns and 'Nama' in gdf_mrt.columns:
            gdf_mrt['Nama_Stasiun'] = gdf_mrt['Nama']
        gdfs.append(gdf_mrt)

    # 2. LRT
    lrt_jkt = os.path.join(DATA_RAW_DIR, 'mrt_lrt', 'lrt_jkt_stations.geojson')
    lrt_jbd = os.path.join(DATA_RAW_DIR, 'mrt_lrt', 'lrt_jabodebek_stations.geojson')
    
    for path in [lrt_jkt, lrt_jbd]:
        if os.path.exists(path):
            gdf = gpd.read_file(path)
            gdf['geometry'] = gdf.geometry.centroid
            gdf['Tipe'] = 'LRT'
            if 'name' in gdf.columns:
                gdf['Nama_Stasiun'] = gdf['name']
            gdfs.append(gdf[['Nama_Stasiun', 'Tipe', 'geometry']])

    # 3. KRL
    krl_path = os.path.join(DATA_RAW_DIR, 'krl', 'krl_stations.csv')
    if os.path.exists(krl_path):
        df_krl = pd.read_csv(krl_path)
        gdf_krl = gpd.GeoDataFrame(df_krl, geometry=gpd.points_from_xy(df_krl.Longitude, df_krl.Latitude), crs="EPSG:4326")
        gdf_krl['Tipe'] = 'KRL'
        gdfs.append(gdf_krl)

    if not gdfs:
        print("No POI data found!")
        return gpd.GeoDataFrame()
        
    # Combine and standardize
    combined = pd.concat(gdfs, ignore_index=True)
    if 'Nama_Stasiun' not in combined.columns and 'name' in combined.columns:
         combined['Nama_Stasiun'] = combined['name']
    
    # Fill nan names with Tipe
    combined['Nama_Stasiun'] = combined['Nama_Stasiun'].fillna(combined['Tipe'])
    
    return combined[['Nama_Stasiun', 'Tipe', 'geometry']].copy()

def get_building_area(point_geom, search_dist_m=60):
    """
    Given a Point geometry (EPSG:4326), find the building roof area in sq meters.
    """
    try:
        # Buffer the point by search_dist_m in meters
        gdf_point = gpd.GeoDataFrame([{'geometry': point_geom}], crs="EPSG:4326")
        gdf_point_proj = gdf_point.to_crs(PROJECTED_CRS)
        
        buffer_proj = gdf_point_proj.buffer(search_dist_m)
        buffer_wgs = buffer_proj.to_crs("EPSG:4326").iloc[0]
        
        # Query OSMnx for buildings within this polygon
        tags = {'building': True}
        buildings = ox.features_from_polygon(buffer_wgs, tags=tags)
        
        if buildings.empty:
            return 0.0, None
            
        # We only want Polygons/MultiPolygons
        buildings = buildings[buildings.geometry.type.isin(['Polygon', 'MultiPolygon'])]
        if buildings.empty:
            return 0.0, None
            
        buildings_proj = buildings.to_crs(PROJECTED_CRS)
        point_proj = gdf_point_proj.geometry.iloc[0]
        
        # Find buildings intersecting a smaller core buffer (to ensure it's the station)
        small_buffer = point_proj.buffer(30)
        intersecting = buildings_proj[buildings_proj.intersects(small_buffer)]
        
        if not intersecting.empty:
            total_area = intersecting.area.sum()
            combined_geom = intersecting.unary_union
            combined_wgs = gpd.GeoSeries([combined_geom], crs=PROJECTED_CRS).to_crs("EPSG:4326").iloc[0]
            return total_area, combined_wgs
        else:
            # Nearest building
            buildings_proj['dist'] = buildings_proj.distance(point_proj)
            nearest = buildings_proj.loc[buildings_proj['dist'].idxmin()]
            if nearest['dist'] <= search_dist_m:
                area = nearest.geometry.area
                nearest_wgs = gpd.GeoSeries([nearest.geometry], crs=PROJECTED_CRS).to_crs("EPSG:4326").iloc[0]
                return area, nearest_wgs
            else:
                return 0.0, None
                
    except ox._errors.InsufficientResponseError:
        return 0.0, None
    except Exception as e:
        # print(f"  [Warning] {e}")
        return 0.0, None

def process_pois():
    print("Membaca data POI Fase 1...")
    pois = load_poi_data()
    print(f"Total POI MRT/LRT/KRL: {len(pois)}")
    
    areas = []
    polygons = []
    
    print("Memulai ekstraksi luasan atap (Building Footprints) via OSMnx...")
    for idx, row in pois.iterrows():
        name = row['Nama_Stasiun']
        tipe = row['Tipe']
        
        area, geom = get_building_area(row['geometry'])
        areas.append(area)
        polygons.append(geom)
        
        print(f"[{idx+1}/{len(pois)}] {tipe} - {name}: {area:.2f} m²")
        time.sleep(1) # Be nice to Overpass API
        
    pois['roof_area_m2'] = areas
    pois['roof_polygon'] = polygons
    
    # Save CSV
    out_csv = os.path.join(DATA_PROC_DIR, 'stasiun_roof_areas.csv')
    pois.drop(columns=['roof_polygon']).to_csv(out_csv, index=False)
    print(f"\nBerhasil menyimpan rekap luasan atap ke: {out_csv}")
    
    # Save GeoJSON
    valid_polygons = pois.dropna(subset=['roof_polygon']).copy()
    if not valid_polygons.empty:
        valid_polygons['geometry'] = valid_polygons['roof_polygon']
        valid_polygons = valid_polygons.drop(columns=['roof_polygon'])
        out_geojson = os.path.join(DATA_PROC_DIR, 'stasiun_roof_polygons.geojson')
        valid_polygons.to_file(out_geojson, driver='GeoJSON')
        print(f"Berhasil menyimpan geometri atap ke: {out_geojson}")

if __name__ == "__main__":
    process_pois()
