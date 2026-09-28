"""
Jakarta Open Data Scraper with Scrapling
Target: Halte TransJakarta datasets with pagination

Uses: Scrapling library (browser automation)
Handles: Pagination automatically
"""

import time
import json
from pathlib import Path
from scrapling import Fetcher

OUTPUT_DIR = Path("data/raw/jakarta_opendata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("JAKARTA OPEN DATA SCRAPER (Scrapling)")
print("="*60)

# Target: TransJakarta datasets page
BASE_URL = "https://data.jakarta.go.id"
SEARCH_URL = f"{BASE_URL}/search/dataset?q=transjakarta"

print(f"\nFetching: {SEARCH_URL}")

try:
    # Fetch with Scrapling
    page = Fetcher.get(SEARCH_URL)
    print("OK Page loaded")
    
    # Find all datasets
    datasets = []
    dataset_items = page.css('li.dataset-item')
    
    print(f"Found {len(dataset_items)} datasets on page 1")
    
    for item in dataset_items:
        try:
            # Title
            title_elem = item.css_first('h3.dataset-heading a')
            title = title_elem.text.strip() if title_elem else 'No title'
            
            # Link
            link = title_elem.attrib.get('href', '') if title_elem else ''
            if link and not link.startswith('http'):
                link = BASE_URL + link
            
            # Description
            desc_elem = item.css_first('div.notes')
            description = desc_elem.text.strip() if desc_elem else ''
            
            if 'halte' in title.lower() or 'halte' in description.lower():
                datasets.append({
                    'title': title,
                    'url': link,
                    'description': description
                })
                print(f"   - {title}")
        
        except Exception as e:
            continue
    
    # Handle pagination
    pagination = page.css('ul.pagination li')
    print(f"\nPagination found: {len(pagination)} items")
    
    # Try to get page 2, 3, etc
    for page_num in range(2, 5):  # Max 4 pages
        next_url = f"{SEARCH_URL}&page={page_num}"
        print(f"\nFetching page {page_num}...")
        
        try:
            next_page = Fetcher.get(next_url)
            next_items = next_page.css('li.dataset-item')
            
            if not next_items:
                print("   No more items, stopping")
                break
            
            print(f"   Found {len(next_items)} datasets")
            
            for item in next_items:
                try:
                    title_elem = item.css_first('h3.dataset-heading a')
                    title = title_elem.text.strip() if title_elem else 'No title'
                    link = title_elem.attrib.get('href', '') if title_elem else ''
                    
                    if link and not link.startswith('http'):
                        link = BASE_URL + link
                    
                    desc_elem = item.css_first('div.notes')
                    description = desc_elem.text.strip() if desc_elem else ''
                    
                    if 'halte' in title.lower() or 'halte' in description.lower():
                        datasets.append({
                            'title': title,
                            'url': link,
                            'description': description
                        })
                        print(f"   - {title}")
                
                except Exception as e:
                    continue
            
            time.sleep(2)  # Polite delay
        
        except Exception as e:
            print(f"   ERROR page {page_num}: {e}")
            break
    
    # Save catalog
    catalog_file = OUTPUT_DIR / "transjakarta_datasets.json"
    with open(catalog_file, 'w', encoding='utf-8') as f:
        json.dump(datasets, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print(f"FOUND {len(datasets)} TransJakarta Halte datasets")
    print("="*60)
    
    if datasets:
        print("\nDatasets:")
        for i, ds in enumerate(datasets, 1):
            print(f"\n{i}. {ds['title']}")
            print(f"   URL: {ds['url']}")
        
        print(f"\nOK Saved to: {catalog_file}")
        
        # Download first halte dataset
        print("\n" + "="*60)
        print("DOWNLOADING FIRST HALTE DATASET")
        print("="*60)
        
        target = datasets[0]
        print(f"\nDataset: {target['title']}")
        print(f"URL: {target['url']}")
        
        # Fetch dataset page
        dataset_page = Fetcher.get(target['url'])
        
        # Find download links
        resources = dataset_page.css('li.resource-item')
        print(f"\nFound {len(resources)} resources")
        
        for res in resources:
            try:
                format_elem = res.css_first('span.format-label')
                format_type = format_elem.text.strip().lower() if format_elem else ''
                
                link_elem = res.css_first('a.resource-url-analytics')
                download_url = link_elem.attrib.get('href', '') if link_elem else ''
                
                if download_url and not download_url.startswith('http'):
                    download_url = BASE_URL + download_url
                
                if format_type in ['csv', 'json', 'geojson', 'xlsx']:
                    print(f"\n   Downloading: {format_type.upper()}")
                    print(f"   URL: {download_url}")
                    
                    # Download file
                    import requests
                    r = requests.get(download_url, timeout=60)
                    r.raise_for_status()
                    
                    output_file = OUTPUT_DIR / f"halte_transjakarta.{format_type}"
                    with open(output_file, 'wb') as f:
                        f.write(r.content)
                    
                    size_mb = output_file.stat().st_size / (1024*1024)
                    print(f"   OK Saved: {output_file.name} ({size_mb:.2f} MB)")
                    
                    # Try to load & preview
                    if format_type == 'csv':
                        import pandas as pd
                        try:
                            df = pd.read_csv(output_file)
                            print(f"   Records: {len(df)}")
                            print(f"   Columns: {list(df.columns[:5])}")
                        except:
                            pass
                    
                    break  # Only download first file
            
            except Exception as e:
                print(f"   ERROR: {e}")
                continue
    
    else:
        print("\nWARNING: No halte datasets found")
        print("Try manual: https://data.jakarta.go.id/search/dataset?q=transjakarta")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("COMPLETE")
print("="*60)
print(f"\nLocation: {OUTPUT_DIR.absolute()}")
