# scriptos.path.join(s, "i")nspecionar_colunas_municipios_ma.py

import geopandas as gpd

path = ".os.path.join(., "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "I")BGE_201os.path.join(5, "M")A_IBGE_201os.path.join(5, "2")1MUE250GC_SIR.shp"

gdf = gpd.read_file(path)

print("🧾 Colunas disponíveis:\n")
print(gdf.columns)

print("\n🔍 Exemplo de linhas:")
print(gdf.head(5))

