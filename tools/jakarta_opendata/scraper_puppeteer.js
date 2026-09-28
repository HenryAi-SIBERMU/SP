/**
 * Jakarta Open Data Scraper - Puppeteer
 * Target: data.jakarta.go.id - Halte TransJakarta datasets
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Output directory
const OUTPUT_DIR = path.join(__dirname, '..', '..', 'data', 'raw', 'jakarta_opendata');

// Create output directory if not exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log('='.repeat(60));
console.log('JAKARTA OPEN DATA - PUPPETEER SCRAPER');
console.log('='.repeat(60));

async function scrapeJakartaData() {
    const datasets = [];
    
    // Launch browser
    console.log('\nLaunching browser...');
    const browser = await puppeteer.launch({
        headless: false,  // Show browser
        defaultViewport: { width: 1280, height: 800 }
    });
    
    const page = await browser.newPage();
    
    try {
        // Navigate to search page (NEW URL: satudata.jakarta.go.id)
        const searchUrl = 'https://satudata.jakarta.go.id/search?q=transjakarta';
        console.log(`\nNavigating to: ${searchUrl}`);
        
        await page.goto(searchUrl, { 
            waitUntil: 'networkidle2',
            timeout: 60000 
        });
        
        await page.waitForTimeout(3000);  // Wait for dynamic content
        
        const actualUrl = page.url();
        console.log(`Actual URL: ${actualUrl}`);
        
        // Try to find dataset items (NEW WEBSITE SELECTORS)
        const selectors = [
            '.card',  // satudata uses cards
            '.dataset-card',
            '[class*="card"]',
            '[class*="result"]',
            'li.dataset-item',  // old selectors as fallback
            '.dataset-item',
            'article.dataset-item',
            '[class*="dataset"]'
        ];
        
        let foundItems = false;
        
        for (const selector of selectors) {
            const items = await page.$$(selector);
            
            if (items.length > 0) {
                console.log(`\nFound ${items.length} items with selector: ${selector}`);
                foundItems = true;
                
                // Extract data from each item
                for (const item of items) {
                    try {
                        // Debug: get all text
                        const itemText = await page.evaluate(el => el.innerText, item);
                        console.log(`\n   Item text preview: ${itemText.substring(0, 100)}...`);
                        
                        // Get title and URL (NEW SELECTORS)
                        const titleElem = await item.$('a[href*="dataset"], a[href*="detail"], h3 a, .card-title a, .dataset-heading a, a');
                        
                        if (titleElem) {
                            const title = await page.evaluate(el => el.innerText.trim(), titleElem);
                            let url = await page.evaluate(el => el.getAttribute('href'), titleElem);
                            
                            console.log(`   Title found: ${title}`);
                            console.log(`   URL: ${url}`);
                            
                            if (url && !url.startsWith('http')) {
                                url = `https://satudata.jakarta.go.id${url}`;
                            }
                            
                            // Get description (NEW SELECTORS)
                            const descElem = await item.$('.card-text, .description, .notes, p');
                            const description = descElem 
                                ? await page.evaluate(el => el.innerText.trim(), descElem)
                                : '';
                            
                            // Filter for halte/transjakarta
                            if (title.toLowerCase().includes('halte') || 
                                title.toLowerCase().includes('transjakarta') ||
                                description.toLowerCase().includes('halte')) {
                                
                                datasets.push({ title, url, description });
                                console.log(`   + ADDED: ${title}`);
                            } else {
                                console.log(`   - SKIP: no halte/transjakarta keyword`);
                            }
                        } else {
                            console.log(`   No title element found`);
                        }
                    } catch (err) {
                        console.log(`   Error: ${err.message}`);
                    }
                }
                
                break;  // Found items, stop trying other selectors
            }
        }
        
        // If no items found, save debug info
        if (!foundItems) {
            console.log('\nNo datasets found. Saving debug info...');
            
            // Save HTML
            const html = await page.content();
            const debugFile = path.join(OUTPUT_DIR, 'page_debug.html');
            fs.writeFileSync(debugFile, html);
            console.log(`HTML saved: ${debugFile}`);
            
            // Take screenshot
            const screenshotFile = path.join(OUTPUT_DIR, 'page_screenshot.png');
            await page.screenshot({ path: screenshotFile, fullPage: true });
            console.log(`Screenshot saved: ${screenshotFile}`);
        }
        
        // Try pagination if datasets found
        if (datasets.length > 0) {
            console.log('\nChecking pagination...');
            
            for (let pageNum = 2; pageNum <= 4; pageNum++) {
                try {
                    const nextUrl = `${searchUrl}&page=${pageNum}`;
                    console.log(`\nPage ${pageNum}: ${nextUrl}`);
                    
                    await page.goto(nextUrl, { 
                        waitUntil: 'networkidle2',
                        timeout: 60000 
                    });
                    
                    await page.waitForTimeout(2000);
                    
                    const items = await page.$$(selectors[0] || '.card');
                    
                    if (items.length === 0) {
                        console.log('   No more items');
                        break;
                    }
                    
                    console.log(`   Found ${items.length} items`);
                    
                    for (const item of items) {
                        try {
                            const titleElem = await item.$('a[href*="dataset"], a[href*="detail"], h3 a, .card-title a');
                            if (titleElem) {
                                const title = await page.evaluate(el => el.innerText.trim(), titleElem);
                                let url = await page.evaluate(el => el.getAttribute('href'), titleElem);
                                
                                if (url && !url.startsWith('http')) {
                                    url = `https://satudata.jakarta.go.id${url}`;
                                }
                                
                                const descElem = await item.$('.card-text, .description, .notes');
                                const description = descElem 
                                    ? await page.evaluate(el => el.innerText.trim(), descElem)
                                    : '';
                                
                                if (title.toLowerCase().includes('halte') || 
                                    title.toLowerCase().includes('transjakarta')) {
                                    datasets.push({ title, url, description });
                                    console.log(`   + ${title}`);
                                }
                            }
                        } catch (err) {
                            // Skip
                        }
                    }
                } catch (err) {
                    console.log(`   Error: ${err.message}`);
                    break;
                }
            }
        }
        
    } catch (error) {
        console.error(`\nERROR: ${error.message}`);
    } finally {
        await browser.close();
    }
    
    return datasets;
}

// Run scraper
(async () => {
    try {
        const datasets = await scrapeJakartaData();
        
        console.log('\n' + '='.repeat(60));
        console.log(`TOTAL: ${datasets.length} datasets found`);
        console.log('='.repeat(60));
        
        if (datasets.length > 0) {
            // Save catalog
            const catalogFile = path.join(OUTPUT_DIR, 'halte_catalog_puppeteer.json');
            fs.writeFileSync(catalogFile, JSON.stringify(datasets, null, 2));
            
            console.log(`\nCatalog saved: ${catalogFile}`);
            
            // Show results
            datasets.forEach((ds, i) => {
                console.log(`\n${i + 1}. ${ds.title}`);
                console.log(`   URL: ${ds.url}`);
            });
            
            console.log('\nTo download datasets, visit URLs manually or extend script.');
        } else {
            console.log('\nNo datasets found. Check debug files in output directory.');
        }
        
        console.log('\n' + '='.repeat(60));
        console.log('COMPLETE');
        console.log('='.repeat(60));
        console.log(`\nOutput: ${OUTPUT_DIR}`);
        
    } catch (error) {
        console.error(`\nFATAL ERROR: ${error.message}`);
        process.exit(1);
    }
})();
