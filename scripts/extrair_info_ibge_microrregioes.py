# scriptos.path.join(s, "e")xtrair_info_ibge_microrregioes.py

import geopandas as gpd
import pandas as pd
import os

# Caminho do shapefile de microrregiões
CAMINHO_SHP = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "I")BGos.path.join(E, "D")ADOos.path.join(S, "B")R_Microrregioes_202os.path.join(2, "B")R_Microrregioes_2022.shp"

# Caminho de saída atualizado
CAMINHO_CSV_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "i")bge_microrregioes_geometry.csv"

# Criar diretório se não existir (precaução, mas ele já existe)
os.makedirs(os.path.dirname(CAMINHO_CSV_SAIDA), exist_ok=True)

# Ler o shapefile
gdf = gpd.read_file(CAMINHO_SHP)

# Converter geometria para WKT (formato textual)
gdf["geometry"] = gdf["geometry"].apply(lambda geom: geom.wkt)

# Selecionar colunas desejadas
colunas_utilizadas = ["CD_MICRO", "NM_MICRO", "SIGLA_UF", "AREA_KM2", "geometry"]

# Exportar para CSV
gdf[colunas_utilizadas].to_csv(CAMINHO_CSV_SAIDA, index=False)

print(f"✅ Arquivo CSV exportado com sucesso: {CAMINHO_CSV_SAIDA}")

