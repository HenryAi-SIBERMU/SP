"""
Jakarta Open Data Scraper - Playwright Browser Automation
Target: data.jakarta.go.id - Halte TransJakarta datasets

Uses: Playwright (Python puppeteer equivalent)
"""

from playwright.sync_api import sync_playwright
import json
import time
from pathlib import Path

OUTPUT_DIR = Path("data/raw/jakarta_opendata")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*60)
print("JAKARTA OPEN DATA - PLAYWRIGHT SCRAPER")
print("="*60)

def scrape_jakarta_data():
    with sync_playwright() as p:
        # Launch browser
        print("\nLaunching browser...")
        browser = p.chromium.launch(headless=False)  # headless=False to see what's happening
        page = browser.new_page()
        
        # Go to search page
        search_url = "https://data.jakarta.go.id/search/dataset?q=transjakarta"
        print(f"\nNavigating to: {search_url}")
        
        page.goto(search_url, wait_until="networkidle", timeout=60000)
        time.sleep(3)  # Wait for dynamic content
        
        print("Page loaded")
        
        # Check actual URL (might redirect)
        actual_url = page.url
        print(f"Actual URL: {actual_url}")
        
        # Find dataset items
        datasets = []
        
        # Try multiple selectors
        selectors = [
            'li.dataset-item',
            '.dataset-item',
            'article.dataset-item',
            '[class*="dataset"]'
        ]
        
        for selector in selectors:
            items = page.query_selector_all(selector)
            if items:
                print(f"\nFound {len(items)} items with selector: {selector}")
                
                for item in items:
                    try:
                        # Get title
                        title_elem = item.query_selector('h3 a, .dataset-heading a, a[href*="dataset"]')
                        if title_elem:
                            title = title_elem.inner_text().strip()
                            url = title_elem.get_attribute('href')
                            
                            if url and not url.startswith('http'):
                                url = f"https://data.jakarta.go.id{url}"
                            
                            # Get description
                            desc_elem = item.query_selector('.notes, .description, p')
                            description = desc_elem.inner_text().strip() if desc_elem else ''
                            
                            # Filter halte
                            if 'halte' in title.lower() or 'transjakarta' in title.lower():
                                datasets.append({
                                    'title': title,
                                    'url': url,
                                    'description': description
                                })
                                print(f"   + {title}")
                    except Exception as e:
                        continue
                
                break  # Found items, stop trying other selectors
        
        # If no items found, save page content for debugging
        if not datasets:
            print("\nNo datasets found. Saving page HTML for inspection...")
            html = page.content()
            
            debug_file = OUTPUT_DIR / "page_debug.html"
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"Saved: {debug_file}")
            
            # Take screenshot
            screenshot_file = OUTPUT_DIR / "page_screenshot.png"
            page.screenshot(path=str(screenshot_file))
            print(f"Screenshot: {screenshot_file}")
        
        # Pagination
        if datasets:
            print("\nChecking pagination...")
            for page_num in range(2, 5):
                try:
                    next_url = f"{search_url}&page={page_num}"
                    print(f"\nPage {page_num}: {next_url}")
                    
                    page.goto(next_url, wait_until="networkidle", timeout=60000)
                    time.sleep(2)
                    
                    items = page.query_selector_all(selector)
                    if not items:
                        print("   No more items")
                        break
                    
                    print(f"   Found {len(items)} items")
                    
                    for item in items:
                        try:
                            title_elem = item.query_selector('h3 a, .dataset-heading a')
                            if title_elem:
                                title = title_elem.inner_text().strip()
                                url = title_elem.get_attribute('href')
                                
                                if url and not url.startswith('http'):
                                    url = f"https://data.jakarta.go.id{url}"
                                
                                desc_elem = item.query_selector('.notes, .description')
                                description = desc_elem.inner_text().strip() if desc_elem else ''
                                
                                if 'halte' in title.lower() or 'transjakarta' in title.lower():
                                    datasets.append({
                                        'title': title,
                                        'url': url,
                                        'description': description
                                    })
                                    print(f"   + {title}")
                        except:
                            continue
                
                except Exception as e:
                    print(f"   Error: {e}")
                    break
        
        browser.close()
        
        return datasets

# Run scraper
try:
    datasets = scrape_jakarta_data()
    
    print("\n" + "="*60)
    print(f"TOTAL: {len(datasets)} datasets found")
    print("="*60)
    
    if datasets:
        # Save catalog
        catalog_file = OUTPUT_DIR / "halte_catalog_playwright.json"
        with open(catalog_file, 'w', encoding='utf-8') as f:
            json.dump(datasets, f, indent=2, ensure_ascii=False)
        
        print(f"\nCatalog saved: {catalog_file}")
        
        # Show results
        for i, ds in enumerate(datasets, 1):
            print(f"\n{i}. {ds['title']}")
            print(f"   URL: {ds['url']}")
        
        # Download first dataset
        if datasets:
            print("\n" + "="*60)
            print("DOWNLOADING FIRST DATASET")
            print("="*60)
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                
                target = datasets[0]
                print(f"\nDataset: {target['title']}")
                print(f"URL: {target['url']}")
                
                page.goto(target['url'], wait_until="networkidle", timeout=60000)
                time.sleep(3)
                
                # Find download links
                download_links = page.query_selector_all('a[href*="download"], a.resource-url-analytics, .format-label')
                
                print(f"Found {len(download_links)} potential downloads")
                
                # Look for CSV/JSON/GeoJSON
                for link in download_links:
                    try:
                        href = link.get_attribute('href')
                        text = link.inner_text().lower()
                        
                        if href and any(fmt in text or fmt in href.lower() for fmt in ['csv', 'json', 'geojson', 'xlsx']):
                            print(f"\nDownload: {text}")
                            print(f"URL: {href}")
                            
                            # Trigger download
                            with page.expect_download() as download_info:
                                link.click()
                            
                            download = download_info.value
                            filename = download.suggested_filename
                            
                            output_file = OUTPUT_DIR / f"halte_transjakarta_{filename}"
                            download.save_as(output_file)
                            
                            print(f"Saved: {output_file}")
                            break
                    except Exception as e:
                        continue
                
                browser.close()
    
    else:
        print("\nNo datasets found. Check debug files in output directory.")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("COMPLETE")
print("="*60)
print(f"\nOutput: {OUTPUT_DIR.absolute()}")
