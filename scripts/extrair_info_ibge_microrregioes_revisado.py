# extrair_info_ibge_microrregioes_revisado.py

import geopandas as gpd
import pandas as pd
import os

# Caminho para o shapefile
CAMINHO_SHP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "D")ADOos.path.join(S, "B")R_Microrregioes_202os.path.join(2, "B")R_Microrregioes_2022.shp"

# Caminho de saída do CSV
CAMINHO_CSV_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "i")bge_microrregioes_geometry_corrigido.csv"

# Carregar shapefile
gdf = gpd.read_file(CAMINHO_SHP)

# Garantir que a geometria seja convertida para WKT (texto)
gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom.wkt if geom else None)

# Selecionar apenas as colunas de interesse
colunas_utilizadas = ["NM_MICRO", "SIGLA_UF", "geometry"]
gdf_final = gdf[colunas_utilizadas].copy()

# Criar diretório se não existir
os.makedirs(os.path.dirname(CAMINHO_CSV_SAIDA), exist_ok=True)

# Exportar para CSV
gdf_final.to_csv(CAMINHO_CSV_SAIDA, index=False)

print(f"✅ CSV exportado com sucesso: {CAMINHO_CSV_SAIDA}")

