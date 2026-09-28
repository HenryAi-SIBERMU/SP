"""
Jakarta Open Data - BeautifulSoup Scraper
Target: Halte TransJakarta datasets
"""

import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import time
import pandas as pd

OUTPUT_DIR = Path("data/raw/jakarta_opendata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("JAKARTA OPEN DATA SCRAPER (BeautifulSoup)")
print("="*60)

BASE_URL = "https://data.jakarta.go.id"

# Search for transjakarta datasets
search_urls = [
    f"{BASE_URL}/search/dataset?q=transjakarta",
    f"{BASE_URL}/search/dataset?q=halte"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

all_datasets = []

for search_url in search_urls:
    print(f"\nSearching: {search_url}")
    
    try:
        r = requests.get(search_url, headers=headers, timeout=30)
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # Find dataset items
            items = soup.find_all('li', class_='dataset-item')
            print(f"Found: {len(items)} items")
            
            for item in items:
                try:
                    # Title & link
                    title_tag = item.find('h3', class_='dataset-heading')
                    if title_tag:
                        link_tag = title_tag.find('a')
                        if link_tag:
                            title = link_tag.get_text(strip=True)
                            url = link_tag.get('href', '')
                            
                            if url and not url.startswith('http'):
                                url = BASE_URL + url
                            
                            # Description
                            desc_tag = item.find('div', class_='notes')
                            description = desc_tag.get_text(strip=True) if desc_tag else ''
                            
                            # Filter halte
                            if 'halte' in title.lower() or 'halte' in description.lower():
                                dataset = {
                                    'title': title,
                                    'url': url,
                                    'description': description
                                }
                                
                                # Skip duplicates
                                if dataset not in all_datasets:
                                    all_datasets.append(dataset)
                                    print(f"   + {title}")
                except Exception as e:
                    continue
            
            # Pagination
            pagination = soup.find('ul', class_='pagination')
            if pagination:
                pages = pagination.find_all('li')
                print(f"Pagination: {len(pages)} items")
        
        time.sleep(2)
    
    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "="*60)
print(f"TOTAL: {len(all_datasets)} halte datasets")
print("="*60)

if all_datasets:
    # Save catalog
    catalog_file = OUTPUT_DIR / "halte_catalog.json"
    with open(catalog_file, 'w', encoding='utf-8') as f:
        json.dump(all_datasets, f, indent=2, ensure_ascii=False)
    
    print(f"\nCatalog: {catalog_file}")
    
    # Show datasets
    for i, ds in enumerate(all_datasets, 1):
        print(f"\n{i}. {ds['title']}")
        print(f"   URL: {ds['url']}")
    
    # Download first dataset
    print("\n" + "="*60)
    print("DOWNLOADING DATASET")
    print("="*60)
    
    target = all_datasets[0]
    print(f"\nDataset: {target['title']}")
    print(f"Fetching: {target['url']}")
    
    try:
        r = requests.get(target['url'], headers=headers, timeout=30)
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            
            # Find resources
            resources = soup.find_all('li', class_='resource-item')
            print(f"Resources: {len(resources)}")
            
            for res in resources:
                try:
                    # Format
                    format_tag = res.find('span', class_='format-label')
                    format_type = format_tag.get_text(strip=True).lower() if format_tag else ''
                    
                    # Download link
                    link_tag = res.find('a', class_='resource-url-analytics')
                    if not link_tag:
                        link_tag = res.find('a', href=True)
                    
                    if link_tag:
                        download_url = link_tag.get('href', '')
                        
                        if download_url and not download_url.startswith('http'):
                            download_url = BASE_URL + download_url
                        
                        if format_type in ['csv', 'json', 'geojson', 'xlsx']:
                            print(f"\n   Format: {format_type.upper()}")
                            print(f"   URL: {download_url}")
                            
                            # Download
                            r2 = requests.get(download_url, headers=headers, timeout=60)
                            r2.raise_for_status()
                            
                            filename = f"halte_transjakarta.{format_type}"
                            output_file = OUTPUT_DIR / filename
                            
                            with open(output_file, 'wb') as f:
                                f.write(r2.content)
                            
                            size_mb = output_file.stat().st_size / (1024*1024)
                            print(f"   OK Saved: {filename} ({size_mb:.2f} MB)")
                            
                            # Preview CSV
                            if format_type == 'csv':
                                try:
                                    df = pd.read_csv(output_file)
                                    print(f"\n   Records: {len(df)}")
                                    print(f"   Columns: {list(df.columns)}")
                                    
                                    # Check for coordinates
                                    coord_cols = [c for c in df.columns if any(x in c.lower() for x in ['lat', 'lon', 'coord', 'x', 'y'])]
                                    if coord_cols:
                                        print(f"   Coordinates: {coord_cols}")
                                    
                                    print(f"\n   Sample:")
                                    print(df.head(3).to_string())
                                except Exception as e:
                                    print(f"   Preview error: {e}")
                            
                            break  # Only first file
                
                except Exception as e:
                    print(f"   Resource error: {e}")
                    continue
    
    except Exception as e:
        print(f"ERROR downloading: {e}")

else:
    print("\nWARNING: No halte datasets found")
    print("Manual check: https://data.jakarta.go.id")

print("\n" + "="*60)
print("COMPLETE")
print("="*60)
print(f"\nOutput: {OUTPUT_DIR.absolute()}")
