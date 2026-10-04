import requests
import time

headers = {'User-Agent': 'CeliosSolarResearchProject/1.0 (contact: admin@celios.co.id)'}

places = [
    "Grand Indonesia Jakarta",
    "Senayan City Jakarta",
    "Mall Kelapa Gading Jakarta",
    "Central Park Mall Jakarta",
    "Pasar Tanah Abang Jakarta",
    "Pasar Induk Kramat Jati",
    "Universitas Indonesia Depok",
    "Institut Pertanian Bogor",
    "SMAN 8 Jakarta",
    "SMAN 68 Jakarta",
    "Stadion Utama Gelora Bung Karno",
    "Jakarta International Stadium",
    "Terminal Pulo Gebang",
    "Terminal Kampung Rambutan",
    "Bandara Halim Perdanakusuma"
]

for p in places:
    url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(p)}&format=json&limit=1"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data:
            item = data[0]
            print(f"{p} -> Lat: {item['lat']}, Lon: {item['lon']}, Display: {item['display_name'][:50]}")
        else:
            print(f"{p} -> NOT FOUND")
    except Exception as e:
        print(f"{p} -> Error: {e}")
    time.sleep(1.1)  # Respect Nominatim rate limit (1 req/sec)
