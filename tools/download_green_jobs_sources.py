import urllib.request
import ssl
import re
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def download_file(url, target_path):
    print(f"Downloading: {url} -> {target_path}")
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp, open(target_path, 'wb') as f:
            data = resp.read()
            f.write(data)
        print(f"Success! {len(data):,} bytes written.")
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

# 1. IRENA - Leveraging Local Capacity for Solar PV (already downloaded)
irena_path = Path("data/raw/sources/irena_leveraging_local_capacity_solar_pv_official.pdf")
if not irena_path.exists() or irena_path.stat().st_size < 1000000:
    download_file(
        "https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2017/Jun/IRENA_Leveraging_for_Solar_PV_2017.pdf",
        str(irena_path)
    )

# 2. IRENA & ILO - Renewable Energy and Jobs - Annual Review 2023
irena_jobs_path = Path("data/raw/sources/irena_ilo_renewable_energy_and_jobs_annual_review_2023.pdf")
if not irena_jobs_path.exists() or irena_jobs_path.stat().st_size < 1000000:
    download_file(
        "https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2023/Sep/IRENA_ILO_Renewable_energy_and_jobs_2023.pdf",
        str(irena_jobs_path)
    )

# 3. IESR Report
iesr_url = "https://iesr.or.id/pustaka/indonesia-energy-transition-outlook-2024"
req = urllib.request.Request(iesr_url, headers=HEADERS)
try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        pdf_urls = set(re.findall(r'https?://iesr\.or\.id/wp-content/uploads/[^"\'>\s]+\.pdf', html))
        print("IESR PDF URLs:", pdf_urls)
        for p_url in pdf_urls:
            fn = p_url.split('/')[-1]
            download_file(p_url, f"data/raw/sources/iesr_{fn}")
except Exception as e:
    print(f"Error fetching IESR page: {e}")

