import requests
import json

overpass_url = "https://overpass-api.de/api/interpreter"
headers = {
    'User-Agent': 'CeliosSolarResearch/1.0 (contact: admin@celios.co.id)'
}
# Bounding box for Jakarta: south, west, north, east
# -6.37, 106.68, -6.10, 106.98
query = """
[out:json][timeout:25];
(
  nwr["shop"="mall"]["name"](-6.37, 106.68, -6.10, 106.98);
);
out center 20;
"""

try:
    resp = requests.post(overpass_url, data={'data': query}, headers=headers, timeout=30)
    print("Status code:", resp.status_code)
    data = resp.json()
    elements = data.get("elements", [])
    print(f"Total elements returned: {len(elements)}")
    for el in elements:
        name = el.get("tags", {}).get("name", "Unknown")
        lat = el.get("lat") or el.get("center", {}).get("lat")
        lon = el.get("lon") or el.get("center", {}).get("lon")
        print(f"Mall: {name} -> ({lat:.6f}, {lon:.6f})")
except Exception as e:
    print("Error querying Overpass:", e)
