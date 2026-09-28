"""
Jakarta Smart City API (JAKGO API)
Alternative API endpoint untuk data Jakarta
"""

import requests
import json
from pathlib import Path

OUTPUT_DIR = Path("data/raw/jakarta_opendata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("JAKGO API TEST")
print("="*60)

# API Token from GitHub repo
API_TOKEN = "q06qb1eTOimT7sc9nMQfkzCKBYEzePXwYbWpEaEk"
BASE_URL = "http://api-jakgo.fzlrhmn.com/api/v1"

# Test endpoints
endpoints = {
    'hospital_general': f"{BASE_URL}/rs-umum",
    'hospital_specialty': f"{BASE_URL}/rs-khusus",
    'clinic': f"{BASE_URL}/puskesmas",
    'cctv': f"{BASE_URL}/cctv"
}

print(f"\nAPI Token: {API_TOKEN[:20]}...")
print(f"Base URL: {BASE_URL}")

for name, url in endpoints.items():
    print(f"\nTesting: {name}")
    print(f"URL: {url}")
    
    try:
        params = {
            'api_token': API_TOKEN,
            'format': 'json'
        }
        
        r = requests.get(url, params=params, timeout=30)
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            try:
                data = r.json()
                
                if isinstance(data, dict):
                    if 'features' in data:
                        count = len(data['features'])
                        print(f"   Features: {count}")
                    elif 'data' in data:
                        count = len(data['data'])
                        print(f"   Data: {count}")
                    else:
                        print(f"   Keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"   Records: {len(data)}")
                
                # Save sample
                output_file = OUTPUT_DIR / f"jakgo_{name}_sample.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"   OK Saved: {output_file.name}")
            
            except json.JSONDecodeError:
                print(f"   ERROR: Invalid JSON")
                print(f"   Response: {r.text[:200]}")
        else:
            print(f"   ERROR: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
    
    except Exception as e:
        print(f"   ERROR: {e}")

print("\n" + "="*60)
print("COMPLETE")
print("="*60)
print(f"\nOutput: {OUTPUT_DIR.absolute()}")
