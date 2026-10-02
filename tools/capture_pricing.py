import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        context = await browser.new_context(viewport={"width": 1400, "height": 900}, device_scale_factor=2)
        page = await context.new_page()
        print("Opening Google Developers Environment Pricing...")
        await page.goto("https://developers.google.com/maps/billing-and-pricing/pricing#environment-pricing", wait_until="networkidle", timeout=60000)
        
        # Cari elemen environment-pricing
        header = await page.query_selector("#environment-pricing")
        if header:
            print("Found #environment-pricing header")
            await header.scroll_into_view_if_needed()
            await page.wait_for_timeout(2000)
            
            # Cari section atau tabel di dekat header
            # Biasanya table ada di parent atau sibling berikutnya
            table = await page.evaluate_handle('''(el) => {
                let node = el;
                while (node && !node.querySelector('table')) {
                    node = node.nextElementSibling || node.parentElement;
                }
                return node ? node.querySelector('table') : null;
            }''', header)
            
            if table:
                print("Found Environment Pricing Table! Capturing...")
                await table.screenshot(path="assets/google_solar_environment_pricing.png")
            else:
                print("Table not found via parent, capturing surrounding section...")
                await page.screenshot(path="assets/google_solar_environment_pricing.png")
        else:
            print("Header not found, saving viewport")
            await page.screenshot(path="assets/google_solar_environment_pricing.png")
            
        print("Success!")
        await browser.close()

asyncio.run(capture())
