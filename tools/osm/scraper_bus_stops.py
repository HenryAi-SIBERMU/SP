"""
OSM Scraper - TransJakarta Bus Stops
Target: Halte TransJakarta from OpenStreetMap
"""

import osmnx as ox
import geopandas as gpd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = Path("data/raw/osm")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PLACE_NAME = "Jakarta, Indonesia"

print("="*60)
print("OSM - TRANSJAKARTA BUS STOPS")
print("="*60)

# Bus stops & platforms
print("\nDownloading bus stops...")
try:
    bus_stops = ox.features_from_place(
        PLACE_NAME,
        tags={
            'highway': 'bus_stop',
            'public_transport': ['platform', 'stop_position']
        }
    )
    
    print(f"OK Downloaded {len(bus_stops):,} bus stops")
    
    # Filter TransJakarta
    if 'name' in bus_stops.columns:
        tj_stops = bus_stops[
            bus_stops['name'].str.contains('TransJakarta|Halte|TJ', case=False, na=False)
        ]
        print(f"   TransJakarta mentions: {len(tj_stops)}")
    else:
        tj_stops = bus_stops
    
    # Save all
    output_file = OUTPUT_DIR / "bus_stops_jakarta.gpkg"
    bus_stops.to_file(output_file, driver='GPKG')
    print(f"Saved: {output_file.name} ({len(bus_stops)} stops)")
    
    # Save TJ only
    if len(tj_stops) > 0:
        tj_file = OUTPUT_DIR / "halte_transjakarta_osm.gpkg"
        tj_stops.to_file(tj_file, driver='GPKG')
        print(f"Saved: {tj_file.name} ({len(tj_stops)} halte)")
    
    # Show columns
    print(f"\nColumns: {list(bus_stops.columns[:10])}")
    
    # Preview
    print(f"\nSample:")
    if 'name' in bus_stops.columns:
        sample = bus_stops[['name', 'geometry']].head(5)
        print(sample)

except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "="*60)
print("COMPLETE")
print("="*60)
print(f"\nOutput: {OUTPUT_DIR.absolute()}")
