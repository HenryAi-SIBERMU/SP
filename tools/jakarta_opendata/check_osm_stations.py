import geopandas as gpd

df = gpd.read_file('data/raw/osm/stations_jakarta.gpkg')

print(f"Total stations: {len(df)}")
print(f"\nColumns: {list(df.columns)}")

# Check for TransJakarta
if 'name' in df.columns:
    tj_halte = df[df['name'].str.contains('TransJakarta|Halte|TJ', case=False, na=False)]
    print(f"\nTransJakarta/Halte mentions: {len(tj_halte)}")

if 'amenity' in df.columns:
    print(f"\nAmenity types:\n{df['amenity'].value_counts()}")

if 'public_transport' in df.columns:
    print(f"\nPublic transport types:\n{df['public_transport'].value_counts()}")

if 'highway' in df.columns:
    print(f"\nHighway types:\n{df['highway'].value_counts()}")

print(f"\nSample data:")
print(df.head(3).T)
