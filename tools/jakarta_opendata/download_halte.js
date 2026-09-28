/**
 * Jakarta Open Data - Direct Download Automation
 * Strategy: Go to dataset page → Click download button
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Output directory - ABSOLUTE PATH
const OUTPUT_DIR = path.resolve(__dirname, '..', '..', 'data', 'raw', 'jakarta_opendata');

if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log('='.repeat(60));
console.log('JAKARTA OPEN DATA - DOWNLOAD AUTOMATION');
console.log('='.repeat(60));

// Known dataset URLs from screenshot
const datasetUrls = [
    'https://satudata.jakarta.go.id/open-data/detail/jumlah-pendapatan-transjakarta-dari-tiket-penumpang',
    'https://satudata.jakarta.go.id/open-data/detail/data-halte-transjakarta',
    'https://satudata.jakarta.go.id/open-data/detail/data-rute-jalur-transjakarta',
    'https://satudata.jakarta.go.id/open-data/detail/data-halte-transjakarta-tahun-2023',
    'https://satudata.jakarta.go.id/open-data/detail/data-halte-transjakarta-triwulan-i-triwulan-iii-tahun-2023',
    'https://satudata.jakarta.go.id/open-data/detail/data-jumlah-penumpang-transjakarta',
    'https://satudata.jakarta.go.id/open-data/detail/data-rute-jalur-transjakarta-tahun-2023',
    'https://satudata.jakarta.go.id/open-data/detail/data-lokasi-transjakarta-dki-jakarta'
];

async function downloadDataset(url, downloadPath) {
    let downloaded = false;  // MOVE HERE
    
    const browser = await puppeteer.launch({
        headless: false,
        defaultViewport: { width: 1280, height: 800 }
    });
    
    const page = await browser.newPage();
    
    try {
        console.log(`\n${'='.repeat(60)}`);
        console.log(`Opening: ${url}`);
        console.log(`Download path: ${downloadPath}`);
        
        // Setup download behavior - USE ABSOLUTE PATH
        const client = await page.target().createCDPSession();
        await client.send('Page.setDownloadBehavior', {
            behavior: 'allow',
            downloadPath: downloadPath
        });
        
        // Navigate to dataset page
        await page.goto(url, { 
            waitUntil: 'networkidle2',
            timeout: 60000 
        });
        
        await page.waitForTimeout(3000);
        
        // Get page title
        const pageTitle = await page.title();
        console.log(`Page title: ${pageTitle}`);
        
        // Try to find download buttons
        const downloadSelectors = [
            'a[href*="download"]',
            'button[class*="download"]',
            '.btn-download',
            '[class*="unduh"]',
            'a:has-text("Unduh")',
            'a:has-text("Download")',
            'button:has-text("Unduh")',
            'button:has-text("Download")',
            '.fa-download',
            '[title*="Download"]',
            '[title*="Unduh"]'
        ];
        
        let foundButtons = false;
        
        for (const selector of downloadSelectors) {
            try {
                const buttons = await page.$$(selector);
                
                if (buttons.length > 0) {
                    console.log(`Found ${buttons.length} elements with selector: ${selector}`);
                    
                    for (let i = 0; i < buttons.length; i++) {
                        const button = buttons[i];
                        
                        // Get button text/attributes for debugging
                        const buttonInfo = await page.evaluate(el => {
                            return {
                                text: el.innerText || el.textContent || '',
                                href: el.href || '',
                                className: el.className || '',
                                title: el.title || ''
                            };
                        }, button);
                        
                        console.log(`\n   Button ${i + 1}:`);
                        console.log(`   Text: ${buttonInfo.text.substring(0, 50)}`);
                        console.log(`   Class: ${buttonInfo.className}`);
                        console.log(`   Href: ${buttonInfo.href}`);
                        
                        // Check if it's a download button (CSV/JSON/Excel)
                        const isDownloadButton = 
                            buttonInfo.text.toLowerCase().includes('csv') ||
                            buttonInfo.text.toLowerCase().includes('json') ||
                            buttonInfo.text.toLowerCase().includes('excel') ||
                            buttonInfo.text.toLowerCase().includes('xlsx') ||
                            buttonInfo.text.toLowerCase().includes('unduh') ||
                            buttonInfo.href.includes('download') ||
                            buttonInfo.href.includes('.csv') ||
                            buttonInfo.href.includes('.json') ||
                            buttonInfo.href.includes('.xlsx');
                        
                        if (isDownloadButton) {
                            console.log(`   → CLICKING THIS BUTTON`);
                            
                            try {
                                // Click and wait for download
                                await Promise.all([
                                    button.click(),
                                    page.waitForTimeout(2000)
                                ]);
                                
                                console.log(`   ✓ Clicked successfully`);
                                downloaded = true;
                                
                                // Wait for download to complete
                                await page.waitForTimeout(5000);
                                
                                break;
                            } catch (clickErr) {
                                console.log(`   × Click failed: ${clickErr.message}`);
                            }
                        } else {
                            console.log(`   - Not a download button`);
                        }
                    }
                    
                    if (downloaded) break;
                }
            } catch (err) {
                // Try next selector
            }
        }
        
        if (!downloaded) {
            console.log('\n⚠ No download button found. Taking screenshot...');
            const screenshotFile = path.join(downloadPath, `page_${Date.now()}.png`);
            await page.screenshot({ path: screenshotFile, fullPage: true });
            console.log(`Screenshot saved: ${screenshotFile}`);
        }
        
    } catch (error) {
        console.error(`Error: ${error.message}`);
    } finally {
        await browser.close();
    }
    
    return downloaded;
}

// Main execution
(async () => {
    console.log(`\nOutput directory: ${OUTPUT_DIR}`);
    console.log(`\nProcessing ${datasetUrls.length} datasets...\n`);
    
    let successCount = 0;
    
    for (let i = 0; i < datasetUrls.length; i++) {
        const url = datasetUrls[i];
        console.log(`\n[${i + 1}/${datasetUrls.length}] Processing dataset...`);
        
        const success = await downloadDataset(url, OUTPUT_DIR);
        if (success) successCount++;
        
        // Wait between requests
        if (i < datasetUrls.length - 1) {
            console.log('\nWaiting 3 seconds before next dataset...');
            await new Promise(resolve => setTimeout(resolve, 3000));
        }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log(`COMPLETE: ${successCount}/${datasetUrls.length} datasets downloaded`);
    console.log('='.repeat(60));
    console.log(`\nCheck files in: ${OUTPUT_DIR}`);
})();
