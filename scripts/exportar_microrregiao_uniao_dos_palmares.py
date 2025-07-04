import geopandas as gpd
import os

# Caminhos dos shapefiles
path_mun = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "A")L_IBGE_201os.path.join(5, "2")7MUE250GC_SIR.shp"))
path_micro = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "A")L_IBGE_201os.path.join(5, "2")7MIE250GC_SIR.shp"))

# Carregar GeoDataFrames
gdf_mun = gpd.read_file(path_mun)
gdf_micro = gpd.read_file(path_micro)

# Garantir mesmo sistema de coordenadas
gdf_mun = gdf_mun.to_crs("EPSG:4326")
gdf_micro = gdf_micro.to_crs("EPSG:4326")

# Procurar o município de interesse
alvo = "santana do mundaú"
gdf_alvo = gdf_mun[gdf_mun.apply(lambda row: alvo in str(row).lower(), axis=1)]

if gdf_alvo.empty:
    print("❌ Município 'Santana do Mundaú' não encontrado no shapefile de municípios.")
else:
    print(f"✅ Município encontrado: {gdf_alvo.iloc[0]['NM_MUNICIP']}")

    # Fazer o spatial join para descobrir a microrregião
    joined = gpd.sjoin(gdf_alvo, gdf_micro, how="left", predicate="intersects")

    # Mostrar resultado
    print("\n🏷️ Microrregião associada:")
    print(joined[["NM_MUNICIP", "NM_MICRO"]])

