"""
Jakarta Open Data Scraper (CKAN API)
Target: Halte TransJakarta, JPO, Infrastructure data

Source: data.jakarta.go.id (CKAN)
Tingkat Kemudahan: MUDAH (CKAN API)
Estimated Time: 2 jam
"""

import requests
import pandas as pd
from pathlib import Path
import json
import time

# Setup
OUTPUT_DIR = Path("data/raw/jakarta_opendata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://data.jakarta.go.id/api/3/action"

print("="*60)
print("JAKARTA OPEN DATA SCRAPER (CKAN)")
print("="*60)

def search_datasets(query, limit=100):
    """Search datasets by keyword"""
    url = f"{BASE_URL}/package_search"
    params = {'q': query, 'rows': limit}
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        print(f"   Requesting: {url}")
        print(f"   Query: {query}")
        r = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"   Status: {r.status_code}")
        r.raise_for_status()
        data = r.json()
        if data.get('success'):
            return data['result']['results']
        else:
            print(f"   API returned success=False")
        return []
    except requests.exceptions.JSONDecodeError as e:
        print(f"   ERROR JSON: {e}")
        print(f"   Response text: {r.text[:200]}")
        return []
    except Exception as e:
        print(f"   ERROR: {e}")
        return []

def get_dataset_resources(package_id):
    """Get resources (files) from a dataset"""
    url = f"{BASE_URL}/package_show"
    params = {'id': package_id}
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        if data.get('success'):
            return data['result']['resources']
        return []
    except Exception as e:
        print(f"   ERROR: {e}")
        return []

def download_resource(resource_url, output_file):
    """Download resource file"""
    try:
        r = requests.get(resource_url, timeout=60, stream=True)
        r.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"   ERROR download: {e}")
        return False

# ============================================================
# 1. Search: Halte TransJakarta
# ============================================================
print("\n[1/3] Searching: Halte TransJakarta...")
halte_datasets = search_datasets("transjakarta halte", limit=50)

if halte_datasets:
    print(f"   OK Found {len(halte_datasets)} datasets")
    
    # List all found datasets
    print("\n   Available datasets:")
    for i, ds in enumerate(halte_datasets[:10], 1):
        print(f"   {i}. {ds['title']}")
        print(f"      ID: {ds['name']}")
    
    # Try to get first relevant dataset
    target_dataset = halte_datasets[0]
    print(f"\n   Fetching resources from: {target_dataset['title']}")
    
    resources = get_dataset_resources(target_dataset['name'])
    
    if resources:
        print(f"   OK Found {len(resources)} resources")
        
        # Download first CSV/JSON resource
        for res in resources:
            format_type = res.get('format', '').lower()
            if format_type in ['csv', 'json', 'geojson']:
                print(f"\n   Downloading: {res['name']} ({format_type})")
                output_file = OUTPUT_DIR / f"halte_transjakarta.{format_type}"
                
                if download_resource(res['url'], output_file):
                    print(f"   OK Saved: {output_file.name}")
                    
                    # Try to load and preview
                    if format_type == 'csv':
                        try:
                            df = pd.read_csv(output_file)
                            print(f"   Records: {len(df)}")
                            print(f"   Columns: {list(df.columns)}")
                        except:
                            pass
                    break
    else:
        print("   WARNING: No resources found")
else:
    print("   WARNING: No datasets found for 'transjakarta halte'")
    print("   Try manual: https://data.jakarta.go.id/search/dataset?q=transjakarta")

time.sleep(2)

# ============================================================
# 2. Search: JPO (Jembatan Penyeberangan Orang)
# ============================================================
print("\n[2/3] Searching: JPO...")
jpo_datasets = search_datasets("jpo jembatan penyeberangan", limit=50)

if jpo_datasets:
    print(f"   OK Found {len(jpo_datasets)} datasets")
    
    target_dataset = jpo_datasets[0]
    print(f"   Fetching resources from: {target_dataset['title']}")
    
    resources = get_dataset_resources(target_dataset['name'])
    
    if resources:
        for res in resources:
            format_type = res.get('format', '').lower()
            if format_type in ['csv', 'json', 'geojson']:
                print(f"\n   Downloading: {res['name']} ({format_type})")
                output_file = OUTPUT_DIR / f"jpo_jakarta.{format_type}"
                
                if download_resource(res['url'], output_file):
                    print(f"   OK Saved: {output_file.name}")
                    
                    if format_type == 'csv':
                        try:
                            df = pd.read_csv(output_file)
                            print(f"   Records: {len(df)}")
                        except:
                            pass
                break
else:
    print("   WARNING: No JPO datasets found")

time.sleep(2)

# ============================================================
# 3. List all transportation datasets
# ============================================================
print("\n[3/3] Searching: All transportation datasets...")
transport_datasets = search_datasets("transportasi infrastruktur", limit=20)

if transport_datasets:
    print(f"   OK Found {len(transport_datasets)} datasets")
    
    # Save catalog
    catalog = []
    for ds in transport_datasets:
        catalog.append({
            'title': ds['title'],
            'name': ds['name'],
            'url': f"https://data.jakarta.go.id/dataset/{ds['name']}"
        })
    
    catalog_file = OUTPUT_DIR / "dataset_catalog.json"
    with open(catalog_file, 'w') as f:
        json.dump(catalog, f, indent=2)
    
    print(f"   OK Saved catalog: {catalog_file.name}")

# Summary
print("\n" + "="*60)
print("DOWNLOAD COMPLETE")
print("="*60)
print(f"\nLocation: {OUTPUT_DIR.absolute()}")
print("\nFiles created:")
for file in OUTPUT_DIR.glob("*"):
    if file.is_file():
        size_mb = file.stat().st_size / (1024*1024)
        print(f"   - {file.name} ({size_mb:.2f} MB)")

print("\nOK Next steps:")
print("   1. Check data/raw/jakarta_opendata/")
print("   2. If no Halte data, visit: https://data.jakarta.go.id")
print("   3. Manual search: 'transjakarta' or 'halte'")
