import pandas as pd
import requests
import os
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
os.makedirs(os.path.join(DATA_RAW_DIR, "transjakarta"), exist_ok=True)
os.makedirs(os.path.join(DATA_RAW_DIR, "krl"), exist_ok=True)
os.makedirs(os.path.join(DATA_RAW_DIR, "mrt_lrt"), exist_ok=True)

geolocator = Nominatim(user_agent="celios8_solarpanel_research")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5)

def get_coordinates(name, context="Jakarta"):
    try:
        query = f"{name} {context}"
        location = geocode(query)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Error geocoding {name}: {e}")
        return None, None

def scrape_transjakarta():
    print("Downloading official TransJakarta GTFS from transjakarta.co.id...")
    url = "https://gtfs.transjakarta.co.id/files/file_gtfs.zip"
    try:
        import io, zipfile
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            with z.open('stops.txt') as f:
                df = pd.read_csv(f)
                
        print(f"Found {len(df)} TransJakarta stops.")
        df_out = df[['stop_name', 'stop_lat', 'stop_lon']].copy()
        df_out.columns = ['Nama_Halte', 'Latitude', 'Longitude']
        
        # Deduplikasi berdasarkan nama halte
        df_out = df_out.drop_duplicates(subset=['Nama_Halte'])
        
        out_path = os.path.join(DATA_RAW_DIR, "transjakarta", "transjakarta_stations.csv")
        df_out.to_csv(out_path, index=False)
        print(f"Saved TransJakarta to {out_path}\n")
    except Exception as e:
        print(f"Error: {e}")

def scrape_mrt():
    print("Scraping MRT Jakarta...")
    mrt_stations = [
        "Lebak Bulus Grab", "Fatmawati Indomaret", "Cipete Raya", "Haji Nawi",
        "Blok A", "Blok M BCA", "ASEAN", "Senayan Mastercard", "Istora Mandiri",
        "Bendungan Hilir", "Setiabudi Astra", "Dukuh Atas BNI", "Bundaran HI Bank DKI"
    ]
    df_out = pd.DataFrame({'Nama_Stasiun': mrt_stations})
    
    print("Geocoding MRT stations...")
    lats, lons = [], []
    for s in mrt_stations:
        lat, lon = get_coordinates(s + " Stasiun MRT", "Jakarta")
        lats.append(lat)
        lons.append(lon)
    df_out['Latitude'] = lats
    df_out['Longitude'] = lons
    
    out_path = os.path.join(DATA_RAW_DIR, "mrt_lrt", "mrt_stations.csv")
    df_out.to_csv(out_path, index=False)
    print(f"Saved MRT to {out_path}\n")

def scrape_krl():
    print("Scraping KRL from Wikipedia Category...")
    url = "https://id.wikipedia.org/wiki/Kategori:Stasiun_kereta_api_di_Jakarta"
    try:
        import bs4
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Celios8_SolarPanel_Research/1.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        links = soup.select('.mw-category li a')
        all_stations = [a.text for a in links if 'Stasiun' in a.text and 'KAI' not in a.text and 'MRT' not in a.text and 'LRT' not in a.text and 'Bekas' not in a.text and 'Rintisan' not in a.text]
        
        print(f"Found {len(all_stations)} unique KRL stations.")
        df_out = pd.DataFrame({'Nama_Stasiun': all_stations})
        
        print("Geocoding KRL stations...")
        lats, lons = [], []
        for s in all_stations:
            lat, lon = get_coordinates(s, "Jakarta")
            lats.append(lat)
            lons.append(lon)
        df_out['Latitude'] = lats
        df_out['Longitude'] = lons
        
        out_path = os.path.join(DATA_RAW_DIR, "krl", "krl_stations.csv")
        df_out.to_csv(out_path, index=False)
        print(f"Saved KRL to {out_path}\n")
    except Exception as e:
        print(f"Error scraping KRL: {e}")

if __name__ == "__main__":
    # scrape_mrt() # Sudah sukses ditarik
    # scrape_krl() # Sudah sukses ditarik
    scrape_transjakarta()
