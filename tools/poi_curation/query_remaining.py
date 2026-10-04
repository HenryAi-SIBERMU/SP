import requests
import time

headers = {'User-Agent': 'CeliosSolarResearchProject/1.0 (contact: admin@celios.co.id)'}

remaining = [
    ("Grand Indonesia", "Grand Indonesia"),
    ("Pasar Tanah Abang", "Pasar Tanah Abang"),
    ("Pasar Senen", "Pasar Senen"),
    ("Terminal Bekasi", "Terminal Bekasi"),
    ("BINUS University", "Bina Nusantara Kebon Jeruk"),
    ("UIN Syarif Hidayatullah", "UIN Syarif Hidayatullah"),
    ("Bandara Soetta T1", "Soekarno-Hatta Airport Terminal 1"),
    ("Bandara Soetta T2", "Soekarno-Hatta Airport Terminal 2")
]

for label, q in remaining:
    url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(q)}&format=json&limit=1"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        if data:
            res = data[0]
            lat = float(res['lat'])
            lon = float(res['lon'])
            print(f"[OK] {label} -> ({lat:.6f}, {lon:.6f}) | {res['display_name'][:50]}")
        else:
            print(f"[NOT FOUND] {label} ({q})")
    except Exception as e:
        print(f"[ERR] {label}: {e}")
    time.sleep(1.1)
