# preencher_rubricas_saeb_mongo.py

import pandas as pd
import geopandas as gpd
import os
import sys

# === Importar função de conexão MongoDB do projeto
sys.path.append("/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "u")tils")
from conexao_mongo import conectar_mongo

print("🔌 Iniciando conexão com o MongoDB...")
db, cliente = conectar_mongo(uri="mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin", nome_banco="saeb")
colecao = db["saeb_2021_municipios_9ano"]
print("✅ Conectado com sucesso ao banco 'saeb'.")

# === Caminhos
csv_saida = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "d")adoos.path.join(s, "m")icrorregioes_rubricas.csv"
shapefile_municipios = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "d")adoos.path.join(s, "I")BGos.path.join(E, "2")02os.path.join(4, "B")R_Municipios_202os.path.join(4, "B")R_Municipios_2024.shp"

# === Carregar dados do MongoDB
print("📥 Lendo dados do SAEB 2021 dos municípios...")
dados_mongo = list(colecao.find({}, {
    "CO_MUNICIPIO": 1,
    "nota_geral": 1
}))
df_saeb = pd.DataFrame(dados_mongo)
df_saeb.rename(columns={"CO_MUNICIPIO": "CD_MUN", "nota_geral": "proficiencia"}, inplace=True)
print(f"📊 Registros carregados do MongoDB: {len(df_saeb)}")

# === Carregar shapefile do IBGE
print("🗺️ Lendo shapefile dos municípios do IBGE...")
gdf_mun = gpd.read_file(shapefile_municipios)
gdf_mun = gdf_mun.to_crs(epsg=4326)

campos = list(gdf_mun.columns)
assert "CD_MUN" in campos and "CD_MICRO" in campos and "NM_MICRO" in campos and "SIGLA_UF" in campos, \
    "❌ Campos obrigatórios não encontrados no shapefile."

df_mun = gdf_mun[["CD_MUN", "CD_MICRO", "NM_MICRO", "SIGLA_UF", "geometry"]].copy()
df_mun["lat"] = df_mun.geometry.centroid.y
df_mun["lon"] = df_mun.geometry.centroid.x
print(f"📌 Municípios do shapefile carregados: {len(df_mun)}")

# === Juntar dados SAEB + IBGE
print("🔗 Cruzando municípios entre SAEB e IBGE...")
df_merged = pd.merge(df_mun, df_saeb, on="CD_MUN", how="inner")
print(f"🔄 Total de municípios com dados combinados: {len(df_merged)}")

# === Agregar por microrregião
print("📊 Calculando médias de proficiência por microrregião...")
df_grouped = df_merged.groupby(["CD_MICRO", "NM_MICRO", "SIGLA_UF"]).agg({
    "proficiencia": "mean",
    "lat": "mean",
    "lon": "mean"
}).reset_index()

# === Função de classificação de rubricas
def classificar_rubrica(p):
    if p <= 225:
        return {
            "nivel": "Muito Baixo",
            "bloom": "Lembrar e Compreender",
            "metodologia": "Contação + Apoio visual",
            "dua": "Leitura oral com reforço visual"
        }
    elif p <= 275:
        return {
            "nivel": "Básico",
            "bloom": "Compreender e Aplicar",
            "metodologia": "Resolução de problemas + Pares",
            "dua": "Mediação estruturada com repetição guiada"
        }
    elif p <= 325:
        return {
            "nivel": "Proficiente",
            "bloom": "Analisar e Avaliar",
            "metodologia": "Gamificação + Projetos",
            "dua": "Feedback imediato e avaliação formativa"
        }
    else:
        return {
            "nivel": "Avançado",
            "bloom": "Avaliar e Criar",
            "metodologia": "Projetos interdisciplinares",
            "dua": "Produções multimodais e autonomia"
        }

# === Aplicar classificações
print("📘 Classificando rubricas pedagógicas por microrregião...")
df_grouped[["nivel", "bloom", "metodologia", "dua"]] = df_grouped["proficiencia"].apply(
    lambda p: pd.Series(classificar_rubrica(p))
)

# === Preparar saída final
df_grouped.rename(columns={
    "NM_MICRO": "microrregiao",
    "SIGLA_UF": "uf"
}, inplace=True)

df_final = df_grouped[[
    "microrregiao", "uf", "lat", "lon", "proficiencia", "nivel", "bloom", "metodologia", "dua"
]]

# === Salvar CSV final
print(f"💾 Salvando arquivo final em: {csv_saida}")
os.makedirs(os.path.dirname(csv_saida), exist_ok=True)
df_final.to_csv(csv_saida, index=False, encoding="utf-8")

# === Fechar conexão
cliente.close()
print("✅ Conexão com MongoDB encerrada.")
print(f"🎉 Arquivo gerado com sucesso: {csv_saida}")
print(f"🔢 Total de microrregiões com dados: {len(df_final)}")

