# pyrefly: ignore [missing-import]
import osmnx as ox
import geopandas as gpd
import os

# Konfigurasi Lokasi
PLACE_NAME = "Jakarta, Indonesia"

# Path Output
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")

def clean_columns_for_geojson(gdf):
    """
    GeoJSON tidak mendukung tipe data list, jadi kita konversi list menjadi string.
    """
    for col in gdf.columns:
        if gdf[col].apply(lambda x: isinstance(x, list)).any():
            gdf[col] = gdf[col].astype(str)
    return gdf

def fetch_and_save_stations(network_name, tag_dict, out_dir_name, out_filename):
    print(f"Mencari titik/poligon untuk: {network_name}...")
    out_dir = os.path.join(DATA_RAW_DIR, out_dir_name)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, out_filename)
    
    try:
        # Menggunakan fitur terbaru dari osmnx (features_from_place)
        gdf = ox.features_from_place(PLACE_NAME, tags=tag_dict)
        
        if len(gdf) == 0:
            print(f" ❌ Data kosong untuk {network_name}")
            return
            
        print(f" ✅ Ditemukan {len(gdf)} data untuk {network_name}")
        
        # Bersihkan kolom tipe list agar bisa di-save ke GeoJSON
        gdf = clean_columns_for_geojson(gdf)
        
        # Simpan
        gdf.to_file(out_path, driver="GeoJSON")
        print(f" 💾 Berhasil disimpan di: {out_path}\n")
        
    except Exception as e:
        print(f" ⚠️ Error saat menarik data {network_name}: {e}\n")

if __name__ == "__main__":
    print("=== Memulai Scraping Stasiun KRL, MRT, LRT via OSMnx ===")
    
    # 1. KAI Commuter (KRL)
    fetch_and_save_stations(
        network_name="KAI Commuter", 
        tag_dict={'network': 'KAI Commuter'}, 
        out_dir_name="krl", 
        out_filename="krl_stations.geojson"
    )
    
    # 2. MRT Jakarta
    fetch_and_save_stations(
        network_name="MRT Jakarta", 
        tag_dict={'network': 'MRT Jakarta'}, 
        out_dir_name="mrt_lrt", 
        out_filename="mrt_stations.geojson"
    )
    
    # 3. LRT Jakarta
    fetch_and_save_stations(
        network_name="LRT Jakarta", 
        tag_dict={'network': 'LRT Jakarta'}, 
        out_dir_name="mrt_lrt", 
        out_filename="lrt_jkt_stations.geojson"
    )
    
    # 4. LRT Jabodebek
    fetch_and_save_stations(
        network_name="LRT Jabodebek", 
        tag_dict={'network': 'LRT Jabodebek'}, 
        out_dir_name="mrt_lrt", 
        out_filename="lrt_jabodebek_stations.geojson"
    )
    
    print("=== Scraping OSMnx Selesai ===")
