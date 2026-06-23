# Data Directory

Folder ini berisi semua data untuk riset PLTS atap dual-use infrastructure.

## 📂 Struktur Folder

### `raw/`
Data mentah (original) yang **TIDAK BOLEH DIUBAH**. Selalu simpan backup di sini.

- **`transjakarta/`**: Data halte TransJakarta (jumlah, lokasi, dimensi)
- **`krl/`**: Data stasiun KRL (lokasi, peron area)
- **`mrt_lrt/`**: Data stasiun MRT dan LRT
- **`satellite/`**: Satellite imagery, aerial photos
- **`demographics/`**: Data pendukung (populasi, konsumsi energi)

**Sources**:
- Government open data portals
- API downloads (TransJakarta, OpenStreetMap)
- Manual surveys
- Satellite imagery providers

### `processed/`
Data yang sudah di-clean, transform, dan siap untuk analysis.

- **`gis/`**: GIS files (shapefiles, geojson)
- **`calculations/`**: Results dari area calculation, capacity estimation
- **`aggregated/`**: Summary statistics, aggregated data

### `external/`
Data dari external API yang bisa di-refresh/update.

- PVGIS query results
- OpenStreetMap downloads
- Weather data
- PLN tariff data

## 📋 Data Inventory

### Current Datasets

| Dataset | Source | Date | Status | Location |
|---------|--------|------|--------|----------|
| Halte TransJ | - | - | 🔴 Not yet | `raw/transjakarta/` |
| Stasiun KRL | - | - | 🔴 Not yet | `raw/krl/` |
| MRT Stations | - | - | 🔴 Not yet | `raw/mrt_lrt/` |

## 🔐 Data Access & Privacy

- Semua data harus comply dengan data privacy regulations
- Sensitive data (jika ada) harus di-encrypt
- Tidak upload data pribadi ke public repository

## 📝 Data Documentation

Setiap dataset harus didokumentasikan dengan:
1. **Source**: Dari mana data berasal
2. **Date**: Kapan data dikumpulkan
3. **Format**: CSV, Shapefile, JSON, etc.
4. **Fields**: Deskripsi setiap column/field
5. **Limitations**: Keterbatasan atau bias data

Gunakan template di `docs/methodology/data-sources.md`

---

**Last Updated**: 23 Juni 2026
