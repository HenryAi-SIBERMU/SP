"""
Script untuk download data OpenStreetMap jakarta
- Building footprints
- POI (mall, hospital, campus, office)
- Parking areas
- Roads & administrative boundaries

Source: OpenStreetMap via OSMnx
Tingkat Kemudahan: ðŸŸ¢ SANGAT MUDAH
Estimated Time: 1-2 jam
"""

import osmnx as ox
import geopandas as gpd
import pandas as pd
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Setup directories
OUTPUT_DIR = Path("data/raw/osm")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Jakarta DKI - Use place name (simpler & more reliable)
PLACE_NAME = "Jakarta, Indonesia"

print("="*60)
print("OSM DATA DOWNLOAD - JAKARTA")
print("="*60)

# ============================================================
# 1. Download Building Footprints
# ============================================================
print("\n[1/5] Downloading building footprints...")
try:
    buildings = ox.features_from_place(
        PLACE_NAME,
        tags={'building': True}
    )
    
    # Save as GeoPackage (better than shapefile)
    buildings_file = OUTPUT_DIR / "buildings_jakarta.gpkg"
    buildings.to_file(buildings_file, driver='GPKG')
    
    print(f"   âœ… Downloaded {len(buildings):,} buildings")
    print(f"   ðŸ“ Saved to: {buildings_file}")
    
except Exception as e:
    print(f"   âŒ Error: {e}")

# ============================================================
# 2. Download POI - Mall & Shopping Centers
# ============================================================
print("\n[2/5] Downloading mall & shopping centers...")
try:
    malls = ox.features_from_bbox(
        PLACE_NAME,
        tags={'shop': 'mall'}
    )
    
    shopping = ox.features_from_bbox(
        PLACE_NAME,
        tags={'building': 'retail'}
    )
    
    # Combine
    all_retail = pd.concat([malls, shopping], ignore_index=True)
    
    retail_file = OUTPUT_DIR / "retail_mall_jakarta.gpkg"
    all_retail.to_file(retail_file, driver='GPKG')
    
    print(f"   âœ… Downloaded {len(all_retail):,} retail/mall locations")
    print(f"   ðŸ“ Saved to: {retail_file}")
    
except Exception as e:
    print(f"   âš ï¸  Warning: {e}")
    print(f"   Note: Mungkin sedikit data, akan gunakan alternatif method")

# ============================================================
# 3. Download POI - Hospitals
# ============================================================
print("\n[3/5] Downloading hospitals...")
try:
    hospitals = ox.features_from_bbox(
        PLACE_NAME,
        tags={'amenity': 'hospital'}
    )
    
    hospital_file = OUTPUT_DIR / "hospitals_jakarta.gpkg"
    hospitals.to_file(hospital_file, driver='GPKG')
    
    print(f"   âœ… Downloaded {len(hospitals):,} hospitals")
    print(f"   ðŸ“ Saved to: {hospital_file}")
    
except Exception as e:
    print(f"   âŒ Error: {e}")

# ============================================================
# 4. Download POI - Universities & Campuses
# ============================================================
print("\n[4/5] Downloading universities...")
try:
    universities = ox.features_from_bbox(
        PLACE_NAME,
        tags={'amenity': 'university'}
    )
    
    uni_file = OUTPUT_DIR / "universities_jakarta.gpkg"
    universities.to_file(uni_file, driver='GPKG')
    
    print(f"   âœ… Downloaded {len(universities):,} universities")
    print(f"   ðŸ“ Saved to: {uni_file}")
    
except Exception as e:
    print(f"   âŒ Error: {e}")

# ============================================================
# 5. Download POI - Parking Areas
# ============================================================
print("\n[5/5] Downloading parking areas...")
try:
    parking = ox.features_from_bbox(
        PLACE_NAME,
        tags={'amenity': 'parking'}
    )
    
    parking_file = OUTPUT_DIR / "parking_jakarta.gpkg"
    parking.to_file(parking_file, driver='GPKG')
    
    print(f"   âœ… Downloaded {len(parking):,} parking locations")
    print(f"   ðŸ“ Saved to: {parking_file}")
    
except Exception as e:
    print(f"   âŒ Error: {e}")

# ============================================================
# 6. Download Road Network (for context)
# ============================================================
print("\n[BONUS] Downloading road network...")
try:
    # Download road network
    graph = ox.graph_from_bbox(
        PLACE_NAME,
        network_type='drive'
    )
    
    # Convert to GeoDataFrame
    edges = ox.graph_to_gdfs(graph, nodes=False)
    
    roads_file = OUTPUT_DIR / "roads_jakarta.gpkg"
    edges.to_file(roads_file, driver='GPKG')
    
    print(f"   âœ… Downloaded road network")
    print(f"   ðŸ“ Saved to: {roads_file}")
    
except Exception as e:
    print(f"   âš ï¸  Warning: {e}")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("DOWNLOAD COMPLETE!")
print("="*60)
print(f"\nðŸ“ All data saved to: {OUTPUT_DIR.absolute()}")
print("\nðŸ“Š Files created:")
for file in OUTPUT_DIR.glob("*.gpkg"):
    size_mb = file.stat().st_size / (1024*1024)
    print(f"   - {file.name} ({size_mb:.1f} MB)")

print("\nâœ… Next steps:")
print("   1. Check data/raw/osm/ folder")
print("   2. Open in QGIS untuk visualisasi")
print("   3. Run 02_process_osm.py untuk cleaning")




