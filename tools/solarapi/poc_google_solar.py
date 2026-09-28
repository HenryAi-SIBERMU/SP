import os
import requests
import json
from dotenv import load_dotenv

# Load konfigurasi dari file .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

def check_solar_potential(lat, lon, name="Lokasi"):
    if not API_KEY or API_KEY == "MASUKKAN_API_KEY_GOOGLE_ANDA_DISINI":
        print("❌ ERROR: GOOGLE_API_KEY belum di-set di file .env")
        print("Silakan buka file .env dan masukkan API Key Anda.")
        return
        
    print(f"🔍 Mengecek potensi Solar di {name} (Lat: {lat}, Lon: {lon})...")
    
    # Memanggil endpoint buildingInsights dari Google Solar API
    url = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lon}&requiredQuality=HIGH&key={API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ BERHASIL! Ini insight ajaib dari Google Solar API:\n")
        
        solar_potential = data.get("solarPotential", {})
        
        # 1. Total Panel Maksimal yang muat di atap
        max_array = solar_potential.get("maxArrayPanelsCount", 0)
        # Asumsi 1 Panel Surya standar = ~1.6 m2
        est_area = max_array * 1.6
        
        # 2. Jam matahari efektif per tahun
        max_sunshine = solar_potential.get("maxSunshineHoursPerYear", 0)
        
        print(f"🏢 Estimasi Luas Atap Bersih : {est_area:.2f} m²")
        print(f"🟦 Kapasitas Maksimal Panel  : {max_array} Panel")
        print(f"☀️ Jam Sinar Matahari/Tahun  : {max_sunshine:.0f} Jam")
        
        # 3. Ambil skenario konfigurasi terbesar (paling bawah dari list)
        configs = solar_potential.get("solarPanelConfigs", [])
        if configs:
            best_config = configs[-1]
            energy_kwh = best_config.get("yearlyEnergyDcKwh", 0)
            print(f"⚡ Potensi Produksi Listrik  : {energy_kwh:.2f} kWh / Tahun")
            
        # Simpan JSON mentah agar kita bisa lihat data 3D shading-nya nanti
        with open("solar_api_sample_cipete.json", "w") as f:
            json.dump(data, f, indent=4)
        print("\n(Data mentah lengkap disimpan di 'solar_api_sample_cipete.json')")
            
    else:
        print(f"❌ GAGAL. HTTP Code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    # KITA UJI COBA DI 1 TITIK DULU: Stasiun MRT Cipete Raya
    cipete_lat = -6.2785
    cipete_lon = 106.7975
    
    check_solar_potential(cipete_lat, cipete_lon, "Stasiun MRT Cipete Raya")
