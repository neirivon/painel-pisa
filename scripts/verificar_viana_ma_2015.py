# scriptos.path.join(s, "v")erificar_viana_ma_2015.py

import geopandas as gpd

# Caminho para o shapefile de microrregiões do Maranhão 2015
path = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MIE250GC_SIR.shp"

# Carrega o GeoDataFrame
gdf = gpd.read_file(path)

# Filtra por microrregiões que contenham 'viana'
resultado = gdf[gdf["NM_MICRO"].str.contains("viana", case=False, na=False)]

# Mostra o resultado
print("🔎 Microrregiões que contêm 'viana':\n")
print(resultado[["NM_MICRO"]])

