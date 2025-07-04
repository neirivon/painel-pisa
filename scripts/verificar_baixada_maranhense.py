# scriptos.path.join(s, "v")erificar_baixada_maranhense.py

import geopandas as gpd

# Caminho para microrregiões do Maranhão 2015
path = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MIE250GC_SIR.shp"

gdf = gpd.read_file(path)

# Filtrar por microrregiões contendo 'baixada'
resultado = gdf[gdf["NM_MICRO"].str.contains("baixada", case=False, na=False)]

print("🔍 Microrregiões com 'baixada' no nome:\n")
print(resultado[["NM_MICRO"]])

