# scriptos.path.join(s, "e")xtrair_info_ibge_shp.py

import geopandas as gpd
import pandas as pd

# Caminho para o shapefile nacional de microrregiões
CAMINHO_SHP = ".os.path.join(., "d")ados_geograficoos.path.join(s, "B")R_Microrregioes_202os.path.join(2, "B")R_Microrregioes_2022.shp"

# Nome do arquivo de saída
CAMINHO_CSV = "dados_ibge_municipios_2022.csv"

# Carregar shapefile com Geopandas
gdf = gpd.read_file(CAMINHO_SHP)

# Selecionar colunas úteis e renomear
df = gdf[[
    "CD_MUN",     # Código do município
    "NM_MUN",     # Nome do município
    "NM_UF",      # Nome da UF
    "NM_REGIAO",  # Região do Brasil
    "NM_MESO",    # Mesorregião
    "NM_MICRO"    # Microrregião
]].rename(columns={
    "CD_MUN": "ID_MUNICIPIO",
    "NM_MUN": "NO_MUNICIPIO",
    "NM_UF": "NO_UF",
    "NM_REGIAO": "REGIAO",
    "NM_MESO": "MESORREGIAO",
    "NM_MICRO": "MICRORREGIAO"
})

# Remover duplicatas (por segurança)
df = df.drop_duplicates(subset=["ID_MUNICIPIO"])

# Salvar CSV
df.to_csv(CAMINHO_CSV, index=False, encoding="utf-8-sig")

print(f"✅ Arquivo salvo com sucesso: {CAMINHO_CSV}")

