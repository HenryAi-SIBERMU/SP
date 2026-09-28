"""
Jakarta Open Data - Direct API Scraper
Target: Halte TransJakarta via CKAN API

Updated approach: Direct API calls
"""

import requests
import json
from pathlib import Path
import time

OUTPUT_DIR = Path("data/raw/jakarta_opendata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("JAKARTA OPEN DATA - API SCRAPER")
print("="*60)

BASE_URL = "https://data.jakarta.go.id"
API_URL = f"{BASE_URL}/api/3/action"

# Try different search terms
search_terms = ["transjakarta", "halte", "tj"]

all_datasets = []

for term in search_terms:
    print(f"\nSearching: '{term}'")
    
    # Try package_search
    try:
        url = f"{API_URL}/package_search"
        params = {
            'q': term,
            'rows': 100
        }
        
        r = requests.get(url, params=params, timeout=30)
        print(f"   Status: {r.status_code}")
        
        if r.status_code == 200:
            data = r.json()
            
            if data.get('success'):
                results = data.get('result', {}).get('results', [])
                count = data.get('result', {}).get('count', 0)
                
                print(f"   Found: {count} datasets")
                
                for pkg in results:
                    title = pkg.get('title', '')
                    name = pkg.get('name', '')
                    
                    # Filter for halte/tj
                    if 'halte' in title.lower() or 'halte' in name.lower():
                        all_datasets.append({
                            'title': title,
                            'name': name,
                            'id': pkg.get('id', ''),
                            'notes': pkg.get('notes', ''),
                            'organization': pkg.get('organization', {}).get('title', ''),
                            'resources_count': len(pkg.get('resources', [])),
                            'resources': pkg.get('resources', []),
                            'url': f"{BASE_URL}/dataset/{name}"
                        })
                        print(f"      - {title} ({len(pkg.get('resources', []))} files)")
            else:
                print(f"   API error: {data.get('error', {})}")
        
        time.sleep(1)
    
    except Exception as e:
        print(f"   ERROR: {e}")

# Deduplicate
unique_datasets = {ds['id']: ds for ds in all_datasets}.values()
unique_datasets = list(unique_datasets)

print("\n" + "="*60)
print(f"TOTAL: {len(unique_datasets)} unique halte datasets")
print("="*60)

if unique_datasets:
    # Save catalog
    catalog_file = OUTPUT_DIR / "halte_transjakarta_catalog.json"
    with open(catalog_file, 'w', encoding='utf-8') as f:
        json.dump(unique_datasets, f, indent=2, ensure_ascii=False)
    
    print(f"\nCatalog saved: {catalog_file}")
    
    # Show all
    print("\nDatasets:")
    for i, ds in enumerate(unique_datasets, 1):
        print(f"\n{i}. {ds['title']}")
        print(f"   Organization: {ds['organization']}")
        print(f"   Resources: {ds['resources_count']}")
        print(f"   URL: {ds['url']}")
    
    # Download first dataset with CSV/JSON
    print("\n" + "="*60)
    print("DOWNLOADING DATA")
    print("="*60)
    
    for ds in unique_datasets:
        print(f"\nDataset: {ds['title']}")
        
        # Find CSV/JSON/GeoJSON resources
        for res in ds['resources']:
            format_type = res.get('format', '').lower()
            url = res.get('url', '')
            
            if format_type in ['csv', 'json', 'geojson', 'xlsx']:
                print(f"\n   Downloading: {format_type.upper()}")
                print(f"   URL: {url}")
                
                try:
                    r = requests.get(url, timeout=60)
                    r.raise_for_status()
                    
                    # Save
                    filename = f"halte_transjakarta_{ds['name']}.{format_type}"
                    output_file = OUTPUT_DIR / filename
                    
                    with open(output_file, 'wb') as f:
                        f.write(r.content)
                    
                    size_mb = output_file.stat().st_size / (1024*1024)
                    print(f"   OK Saved: {output_file.name} ({size_mb:.2f} MB)")
                    
                    # Preview CSV
                    if format_type == 'csv':
                        import pandas as pd
                        try:
                            df = pd.read_csv(output_file)
                            print(f"   Records: {len(df)}")
                            print(f"   Columns: {list(df.columns)}")
                            
                            # Show sample
                            if len(df) > 0:
                                print("\n   Sample (first row):")
                                print(df.iloc[0].to_dict())
                        except Exception as e:
                            print(f"   Cannot preview: {e}")
                
                except Exception as e:
                    print(f"   ERROR downloading: {e}")
        
        # Only download from first dataset
        break

else:
    print("\nWARNING: No halte datasets found via API")
    print("\nTrying alternative: Manual dataset IDs...")
    
    # Try known dataset names
    known_ids = [
        'halte-transjakarta',
        'data-halte-transjakarta',
        'transjakarta-halte'
    ]
    
    for dataset_id in known_ids:
        print(f"\nTrying: {dataset_id}")
        
        try:
            url = f"{API_URL}/package_show"
            params = {'id': dataset_id}
            
            r = requests.get(url, params=params, timeout=30)
            
            if r.status_code == 200:
                data = r.json()
                
                if data.get('success'):
                    pkg = data['result']
                    print(f"   FOUND: {pkg['title']}")
                    print(f"   Resources: {len(pkg.get('resources', []))}")
                    
                    # Download
                    for res in pkg['resources']:
                        format_type = res.get('format', '').lower()
                        url = res.get('url', '')
                        
                        if format_type in ['csv', 'json', 'geojson']:
                            print(f"\n   Downloading: {format_type.upper()}")
                            
                            r2 = requests.get(url, timeout=60)
                            r2.raise_for_status()
                            
                            filename = f"halte_transjakarta.{format_type}"
                            output_file = OUTPUT_DIR / filename
                            
                            with open(output_file, 'wb') as f:
                                f.write(r2.content)
                            
                            size_mb = output_file.stat().st_size / (1024*1024)
                            print(f"   OK Saved: {filename} ({size_mb:.2f} MB)")
                    
                    break
        
        except Exception as e:
            print(f"   Not found")

print("\n" + "="*60)
print("COMPLETE")
print("="*60)
print(f"\nOutput: {OUTPUT_DIR.absolute()}")
