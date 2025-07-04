import geopandas as gpd
import json

# Caminho base do shapefile (sem extensão)
CAMINHO_SHAPEFILE = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "m")unicipios_tmap"

# Nomes das colunas reais do shapefile
COL_CODIGO = 'CD_MUN'
COL_NOME = 'NM_MUN'

print("📍 Lendo shapefile da mesorregião TMAP...")
gdf = gpd.read_file(f"{CAMINHO_SHAPEFILE}.shp")

print("\n📋 Colunas disponíveis:")
print(gdf.columns)

# Selecionar e renomear colunas relevantes
municipios = gdf[[COL_CODIGO, COL_NOME]].copy()
municipios = municipios.rename(columns={COL_CODIGO: "codigo_ibge", COL_NOME: "nome"})

# Remover duplicatas
municipios = municipios.drop_duplicates(subset="codigo_ibge")

# Salvar como JSON
json_path = f"{CAMINHO_SHAPEFILE}_lista.json"
print(f"💾 Salvando JSON: {json_path}")
municipios.to_json(json_path, orient="records", force_ascii=False)

# Salvar como CSV
csv_path = f"{CAMINHO_SHAPEFILE}_lista.csv"
print(f"💾 Salvando CSV: {csv_path}")
municipios.to_csv(csv_path, index=False)

print("✅ Exportação da lista de municípios TMAP finalizada com sucesso.")

