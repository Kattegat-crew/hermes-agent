---
name: arcgis-geospatial-analysis
description: "ArcGIS and geospatial analysis: Shapefiles (.shp), GeoJSON, KML, EPSG projections, spatial queries, and territory mapping."
license: MIT
compatibility: hermes, opencode
---

# ArcGIS & Geospatial Analysis Best Practices

Comprehensive guidelines for working with Geographic Information Systems (GIS), spatial datasets, and ArcGIS environments.

## Core Capabilities
1. **Spatial Data Formats**:
   - Vector: ESRI Shapefiles (`.shp`, `.shx`, `.dbf`, `.prj`), GeoJSON, KML/KMZ, GeoPackage (`.gpkg`).
   - Raster: GeoTIFF, DEMs, satellite imagery layers.
2. **Coordinate Reference Systems (CRS)**:
   - Always verify and document the EPSG code (e.g., `EPSG:4326` WGS84, `EPSG:3857` Web Mercator, `EPSG:3116` / `EPSG:9377` MAGNA-SIRGAS Colombia).
   - Re-project coordinates before distance or area calculations.
3. **Spatial Queries & Analytics**:
   - Point-in-Polygon (checking if casino/store locations fall within zoning boundaries).
   - Buffer analysis (e.g., 500m radius around entertainment centers).
   - Spatial join between commercial transaction data and municipal sector boundaries.
4. **Tooling & Python Ecosystem**:
   - Use `geopandas`, `shapely`, `pyproj`, and `rasterio` for headless processing.
   - Generate interactive preview maps with `folium` or export clean GeoJSON for web dashboards.
