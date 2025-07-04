# conferir_colunas_shapefile.py

import geopandas as gpd

# Caminho atualizado com base no diretório informado
CAMINHO_SHP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "D")ADOos.path.join(S, "B")R_Microrregioes_202os.path.join(2, "B")R_Microrregioes_2022.shp"

# Carregar o shapefile
gdf = gpd.read_file(CAMINHO_SHP)

# Exibir as colunas disponíveis
print("🔍 Colunas disponíveis no shapefile:")
print(gdf.columns.tolist())

# Exibir as 5 primeiras linhas para amostra
print("\n📌 Amostra dos dados:")
print(gdf.head())

