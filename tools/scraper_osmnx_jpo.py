import osmnx as ox
import geopandas as gpd
import os

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
os.makedirs(os.path.join(DATA_RAW_DIR, 'jpo'), exist_ok=True)

def scrape_jpo():
    print("Scraping JPO (Pedestrian Overpass) dari OpenStreetMap menggunakan OSMnx...")
    
    # Tag untuk Jembatan Penyeberangan Orang (JPO)
    tags = {
        'highway': ['footway', 'pedestrian'],
        'bridge': ['yes', 'footway']
    }
    
    # Lokasi pusat Monas dengan radius 25km (mencakup seluruh DKI Jakarta)
    center_point = (-6.175392, 106.827153)
    
    try:
        jpo_gdf = ox.features_from_point(center_point, tags=tags, dist=25000)
        
        # Filter out linestrings/polygons to get centroids if they are lines
        jpo_centroids = jpo_gdf.copy()
        jpo_centroids['geometry'] = jpo_centroids['geometry'].centroid
        
        # Ekstrak nama jika ada, jika tidak isi dengan 'JPO Tanpa Nama'
        if 'name' in jpo_centroids.columns:
            jpo_centroids['Nama_JPO'] = jpo_centroids['name'].fillna('JPO Tanpa Nama')
        else:
            jpo_centroids['Nama_JPO'] = 'JPO Tanpa Nama'
            
        jpo_centroids['Latitude'] = jpo_centroids.geometry.y
        jpo_centroids['Longitude'] = jpo_centroids.geometry.x
        
        # Bersihkan dari kolom-kolom OSM yang terlalu kompleks agar ringan disimpan ke CSV
        df_out = jpo_centroids[['Nama_JPO', 'Latitude', 'Longitude']].copy()
        df_out = df_out.drop_duplicates()
        
        # Filter valid latitude/longitude
        df_out = df_out.dropna(subset=['Latitude', 'Longitude'])
        
        print(f"Berhasil menemukan {len(df_out)} JPO di area Jakarta.")
        
        out_path = os.path.join(DATA_RAW_DIR, 'jpo', 'jpo_jakarta.csv')
        df_out.to_csv(out_path, index=False)
        
        print(f"Data JPO berhasil disimpan di: {out_path}")
        
    except Exception as e:
        print(f"Error saat scraping JPO: {e}")

if __name__ == "__main__":
    scrape_jpo()
