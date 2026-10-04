import requests
import json
import time

headers = {'User-Agent': 'CeliosSolarResearchProject/1.0 (contact: admin@celios.co.id)'}

query_dict = {
    "airport": [
        ("Bandara Soekarno-Hatta Terminal 3", "Terminal 3 Soekarno-Hatta International Airport"),
        ("Bandara Soekarno-Hatta Terminal 2", "Terminal 2 Soekarno-Hatta International Airport"),
        ("Bandara Soekarno-Hatta Terminal 1", "Terminal 1 Soekarno-Hatta International Airport"),
        ("Bandar Udara Halim Perdanakusuma", "Bandar Udara Halim Perdanakusuma")
    ],
    "terminal": [
        ("Terminal Bus Tanjung Priok", "Terminal Tanjung Priok Jakarta"),
        ("Terminal Terpadu Pulo Gebang", "Terminal Bus Terpadu Sentra Timur Pulo Gebang"),
        ("Terminal Bus Kampung Rambutan", "Terminal Kampung Rambutan Jakarta"),
        ("Terminal Bus Kalideres", "Terminal Kalideres Jakarta"),
        ("Terminal Bus Baranangsiang Bogor", "Terminal Baranangsiang Bogor"),
        ("Terminal Bus Jatijajar Depok", "Terminal Jatijajar Depok"),
        ("Terminal Bus Poris Plawad Tangerang", "Terminal Poris Plawad Tangerang"),
        ("Terminal Bus Bekasi", "Terminal Bekasi Jalan Ir H Juanda")
    ],
    "mall": [
        ("Pondok Indah Mall 1", "Pondok Indah Mall 1 Jakarta"),
        ("Grand Indonesia Shopping Town", "Grand Indonesia Jalan M.H. Thamrin Jakarta"),
        ("Senayan City", "Senayan City Jalan Asia Afrika Jakarta"),
        ("Summarecon Mall Kelapa Gading", "Summarecon Mall Kelapa Gading Jakarta"),
        ("Central Park Mall", "Central Park Mall Jakarta"),
        ("Kota Kasablanka", "Kota Kasablanka Mall Jakarta"),
        ("Summarecon Mall Serpong", "Summarecon Mall Serpong Tangerang"),
        ("Summarecon Mall Bekasi", "Summarecon Mall Bekasi")
    ],
    "market": [
        ("Pasar Mayestik", "Pasar Mayestik Kebayoran Baru"),
        ("Pasar Tanah Abang Blok A", "Pasar Tanah Abang Blok A Jakarta"),
        ("Pasar Induk Kramat Jati", "Pasar Induk Kramat Jati Jakarta"),
        ("Pasar Senen Blok III", "Pasar Senen Blok III Jakarta"),
        ("Pasar Glodok", "Pasar Glodok Jakarta Barat"),
        ("Pasar Santa", "Pasar Santa Kebayoran Baru"),
        ("Pasar Jatinegara", "Pasar Jatinegara Jakarta Timur"),
        ("Pasar Baru", "Pasar Baru Sawah Besar Jakarta Pusat")
    ],
    "university": [
        ("Perpustakaan Pusat UI Depok", "Perpustakaan Pusat Universitas Indonesia Depok"),
        ("Institut Pertanian Bogor Dramaga", "Institut Pertanian Bogor Dramaga"),
        ("Universitas Trisakti Grogol", "Universitas Trisakti Kyai Tapa Jakarta"),
        ("Universitas Tarumanagara Kampus 1", "Universitas Tarumanagara Kampus 1 Jakarta"),
        ("Universitas Bina Nusantara Anggrek", "BINUS University Anggrek Campus Jakarta"),
        ("Universitas Negeri Jakarta Rawamangun", "Universitas Negeri Jakarta Rawamangun"),
        ("UIN Syarif Hidayatullah Jakarta", "UIN Syarif Hidayatullah Jakarta Ciputat"),
        ("Universitas Multimedia Nusantara", "Universitas Multimedia Nusantara Gading Serpong")
    ],
    "school": [
        ("SMAN 70 Jakarta", "SMA Negeri 70 Jakarta"),
        ("SMAN 8 Jakarta", "SMA Negeri 8 Jakarta Bukit Duri"),
        ("SMAN 68 Jakarta", "SMA Negeri 68 Jakarta Salemba"),
        ("SMAN 28 Jakarta", "SMA Negeri 28 Jakarta Pasar Minggu"),
        ("SMAN 3 Jakarta", "SMA Negeri 3 Jakarta Setiabudi"),
        ("SMKN 26 Jakarta", "SMK Negeri 26 Jakarta Rawamangun"),
        ("SMAN 1 Bogor", "SMA Negeri 1 Bogor Paledang"),
        ("SMAN 1 Depok", "SMA Negeri 1 Depok Nusantara")
    ],
    "stadium": [
        ("Istora Senayan GBK", "Istora Gelora Bung Karno Jakarta"),
        ("Stadion Utama Gelora Bung Karno", "Stadion Utama Gelora Bung Karno Jakarta"),
        ("Jakarta International Stadium", "Jakarta International Stadium"),
        ("Stadion Madya GBK", "Stadion Madya Gelora Bung Karno"),
        ("Jakarta International Velodrome", "Jakarta International Velodrome Rawamangun"),
        ("Gelanggang Remaja Bulungan", "Gelanggang Remaja Bulungan Jakarta"),
        ("Stadion Pakansari Cibinong", "Stadion Pakansari Bogor"),
        ("Stadion Patriot Candrabhaga", "Stadion Patriot Candrabhaga Bekasi")
    ]
}

results = {}

for cat, items in query_dict.items():
    print(f"\n=== MENCARI KATEGORI: {cat.upper()} ===")
    results[cat] = []
    for label, q in items:
        url = f"https://nominatim.openstreetmap.org/search?q={requests.utils.quote(q)}&format=json&limit=1"
        try:
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            if data:
                res = data[0]
                lat = float(res['lat'])
                lon = float(res['lon'])
                print(f"  [OK] {label} -> ({lat:.6f}, {lon:.6f}) | {res['display_name'][:45]}")
                results[cat].append({
                    "name": label,
                    "query": q,
                    "lat": lat,
                    "lon": lon,
                    "osm_display": res['display_name'],
                    "osm_type": res.get('type')
                })
            else:
                print(f"  [NOT FOUND] {label} (Query: {q})")
        except Exception as e:
            print(f"  [ERR] {label}: {e}")
        time.sleep(1.1)

with open('scratch/nominatim_batch_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSelesai! Hasil disimpan di scratch/nominatim_batch_results.json")
