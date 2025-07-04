# scriptos.path.join(s, "d")escobrir_microrregiao_sao_vicente.py

import geopandas as gpd

# Caminho para o shapefile de municípios (Maranhão - 2015)
path = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MUE250GC_SIR.shp"

# Carrega o GeoDataFrame
gdf = gpd.read_file(path)

# Filtra o município São Vicente Ferrer
resultado = gdf[gdf["NM_MUNICIP"].str.contains("sao vicente ferrer", case=False, na=False)]

print("\n📍 Município e sua microrregião associada:")
print(resultado[["NM_MUNICIP", "NM_MICRO"]])

