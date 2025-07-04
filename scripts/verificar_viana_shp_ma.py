# scriptos.path.join(s, "v")erificar_viana_shp_ma.py

import geopandas as gpd

# Caminho para o shapefile do Maranhão (2015)
path_ma = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MIE250GC_SIR.shp"

# Ler o shapefile
gdf = gpd.read_file(path_ma)

# Filtrar por microrregiões que contenham 'viana'
resultado = gdf[gdf["NM_MICRO"].str.contains("viana", case=False, na=False)]

print("\n🔍 Microrregiões encontradas com 'viana':\n")
print(resultado[["NM_MICRO"]])

