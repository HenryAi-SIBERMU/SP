/**
 * Jakarta Open Data - Extract JSON from Preview
 * Strategy: Click "Lihat JSON" → Extract data from popup/tab
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const OUTPUT_DIR = path.resolve(__dirname, '..', '..', 'data', 'raw', 'jakarta_opendata');

if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log('='.repeat(60));
console.log('JAKARTA OPEN DATA - JSON EXTRACTOR');
console.log('='.repeat(60));

const datasets = [
    { 
        name: 'data-halte-transjakarta',
        url: 'https://satudata.jakarta.go.id/open-data/detail/data-halte-transjakarta'
    },
    { 
        name: 'data-halte-transjakarta-2023',
        url: 'https://satudata.jakarta.go.id/open-data/detail/data-halte-transjakarta-tahun-2023'
    },
    { 
        name: 'data-halte-transjakarta-triwulan-2023',
        url: 'https://satudata.jakarta.go.id/open-data/detail/data-halte-transjakarta-triwulan-i-triwulan-iii-tahun-2023'
    },
    { 
        name: 'data-rute-jalur-transjakarta',
        url: 'https://satudata.jakarta.go.id/open-data/detail/data-rute-jalur-transjakarta'
    },
    { 
        name: 'data-lokasi-transjakarta',
        url: 'https://satudata.jakarta.go.id/open-data/detail/data-lokasi-transjakarta-dki-jakarta'
    }
];

async function extractData(dataset) {
    const browser = await puppeteer.launch({
        headless: true,  // Run in background
        defaultViewport: { width: 1280, height: 800 }
    });
    
    const page = await browser.newPage();
    
    try {
        console.log(`\n${'='.repeat(60)}`);
        console.log(`Dataset: ${dataset.name}`);
        console.log(`URL: ${dataset.url}`);
        
        await page.goto(dataset.url, { 
            waitUntil: 'networkidle2',
            timeout: 60000 
        });
        
        await page.waitForTimeout(3000);
        
        // Find JSON button - PROPER SELECTOR
        const jsonButton = await page.evaluateHandle(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            return buttons.find(btn => 
                btn.textContent.includes('Lihat JSON') || 
                btn.textContent.includes('JSON') ||
                btn.classList.contains('button-download')
            );
        });
        
        if (jsonButton && jsonButton.asElement()) {
            console.log('Found JSON button, clicking...');
            
            const buttonElement = jsonButton.asElement();
            
            // Listen for new tab/popup
            const newPagePromise = new Promise(resolve => 
                browser.once('targetcreated', target => resolve(target.page()))
            );
            
            await buttonElement.click();
            await page.waitForTimeout(2000);
            
            // Check if new tab opened
            const pages = await browser.pages();
            let jsonPage = null;
            
            if (pages.length > 1) {
                jsonPage = pages[pages.length - 1];
                console.log('New tab opened');
            } else {
                // Check for modal/div with JSON
                jsonPage = page;
                console.log('Checking current page for JSON data');
            }
            
            await jsonPage.waitForTimeout(2000);
            
            // Try to extract JSON data
            const jsonData = await jsonPage.evaluate(() => {
                // Try pre tag (common for JSON display)
                const preTag = document.querySelector('pre');
                if (preTag) {
                    try {
                        return JSON.parse(preTag.textContent);
                    } catch (e) {
                        return preTag.textContent;
                    }
                }
                
                // Try body text
                const bodyText = document.body.innerText;
                try {
                    return JSON.parse(bodyText);
                } catch (e) {
                    return bodyText;
                }
            });
            
            if (jsonData) {
                // Save to file
                const outputFile = path.join(OUTPUT_DIR, `${dataset.name}.json`);
                fs.writeFileSync(outputFile, JSON.stringify(jsonData, null, 2));
                
                console.log(`✓ Saved: ${path.basename(outputFile)}`);
                
                // Show preview
                if (Array.isArray(jsonData)) {
                    console.log(`  Records: ${jsonData.length}`);
                } else if (jsonData.data && Array.isArray(jsonData.data)) {
                    console.log(`  Records: ${jsonData.data.length}`);
                } else if (typeof jsonData === 'object') {
                    console.log(`  Keys: ${Object.keys(jsonData).join(', ')}`);
                }
                
                return true;
            } else {
                console.log('× No JSON data found');
                
                // Save screenshot for debugging
                const screenshotFile = path.join(OUTPUT_DIR, `${dataset.name}_error.png`);
                await jsonPage.screenshot({ path: screenshotFile });
                console.log(`  Screenshot: ${path.basename(screenshotFile)}`);
                
                return false;
            }
            
        } else {
            console.log('× JSON button not found');
            return false;
        }
        
    } catch (error) {
        console.error(`Error: ${error.message}`);
        return false;
    } finally {
        await browser.close();
    }
}

// Main execution
(async () => {
    console.log(`\nOutput directory: ${OUTPUT_DIR}`);
    console.log(`\nProcessing ${datasets.length} datasets...\n`);
    
    let successCount = 0;
    
    for (let i = 0; i < datasets.length; i++) {
        const dataset = datasets[i];
        console.log(`\n[${i + 1}/${datasets.length}]`);
        
        const success = await extractData(dataset);
        if (success) successCount++;
        
        if (i < datasets.length - 1) {
            console.log('\nWaiting 2 seconds...');
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log(`COMPLETE: ${successCount}/${datasets.length} datasets extracted`);
    console.log('='.repeat(60));
    console.log(`\nFiles saved in: ${OUTPUT_DIR}`);
})();
