# OpenStreetMap Data Scraper

Download building footprints, POI, dan parking data dari OpenStreetMap untuk Jabodetabek.

## 📊 Data Source
- **Source**: OpenStreetMap (OSM)
- **URL**: https://www.openstreetmap.org
- **API**: Overpass API via OSMnx Python library
- **Tingkat Kemudahan**: 🟢 SANGAT MUDAH

## 🎯 Output Data

| File | Description | Size (approx) |
|------|-------------|---------------|
| `buildings_jabodetabek.gpkg` | Building footprints | ~500 MB |
| `parking_jabodetabek.gpkg` | Parking areas (`amenity=parking`) | ~10 MB |
| `hospitals_jabodetabek.gpkg` | Hospitals (`amenity=hospital`) | ~1 MB |
| `universities_jabodetabek.gpkg` | Universities (`amenity=university`) | ~500 KB |
| `retail_mall_jabodetabek.gpkg` | Malls & retail buildings | ~5 MB |
| `roads_jabodetabek.gpkg` | Road network | ~100 MB |

All saved to: `data/raw/osm/`

## 🚀 Usage

```bash
# Install dependencies
pip install osmnx geopandas

# Run scraper
python tools/osm/scraper.py
```

## ⚙️ Configuration

Edit `scraper.py` to change bounding box:

```python
JABODETABEK_BBOX = {
    'north': -5.9,   # Northern limit
    'south': -6.7,   # Southern limit
    'east': 107.2,   # Eastern limit
    'west': 106.4    # Western limit
}
```

## 📈 Estimated Time
- Buildings: 30-60 minutes (large dataset)
- POI data: 5-10 minutes each
- Total: **1-2 hours**

## ⚠️ Notes
- OSM servers kadang lambat, tunggu saja
- Download ~600 MB total data
- Requires stable internet connection
- Data format: GeoPackage (.gpkg) - compatible with QGIS, Python, R

## 📚 Data Fields

### Buildings
- `building`: building type
- `geometry`: polygon coordinates
- `addr:*`: address information (if available)

### Parking
- `amenity`: parking
- `parking`: surface/underground/multi-storey
- `capacity`: number of spots (if available)
- `geometry`: point/polygon

### Hospitals/Universities
- `name`: facility name
- `amenity`: hospital/university
- `geometry`: point/polygon
- `addr:*`: address

## 🔗 References
- OSMnx Documentation: https://osmnx.readthedocs.io/
- OpenStreetMap Wiki: https://wiki.openstreetmap.org/
