import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm
import os
import json

# ========== CONFIGURAÇÃO ==========
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"
CAMINHO_EQUIV_PAISES = "scripts/estrutura_equivalente_pais.csv"
CAMINHO_EQUIV_PONTOS = "scripts/estrutura_equivalente_pontuacoes.csv"
CAMINHO_SAIDA_CSV = "painel_pisa/dados_cloud/historico_top5_paises.csv"
CAMINHO_SAIDA_JSON = "painel_pisa/dados_cloud/historico_top5_paises.json"
TOP5 = ["Brazil", "Singapore", "Japan", "Finland", "Korea"]

# ========== CONEXÃO ==========
client = MongoClient(MONGO_URI)
db = client[BANCO]

# ========== CARREGAR EQUIVALÊNCIAS ==========
df_eq_cnt = pd.read_csv(CAMINHO_EQUIV_PAISES)
df_eq_pv = pd.read_csv(CAMINHO_EQUIV_PONTOS)

# ========== AGRUPAR DADOS ==========
registros = []

for nome_col in db.list_collection_names():
    campos_pv = df_eq_pv[df_eq_pv["colecao"] == nome_col]["campo_detectado"].tolist()
    campo_cnt = df_eq_cnt[df_eq_cnt["colecao"] == nome_col]["campo_detectado"].tolist()

    if not campos_pv or not campo_cnt:
        continue

    campo_cnt = campo_cnt[0]  # assume apenas 1 campo equivalente para CNT
    for campo_pv in campos_pv:
        try:
            cursor = db[nome_col].find(
                {campo_cnt: {"$in": TOP5}, campo_pv: {"$ne": None}},
                {campo_cnt: 1, campo_pv: 1}
            ).limit(50000)

            for doc in cursor:
                registros.append({
                    "Colecao": nome_col,
                    "Ano": int(nome_col[5:9]) if nome_col.startswith("pisa_") else None,
                    "Pais": doc[campo_cnt],
                    "Variavel": campo_pv,
                    "Valor": doc[campo_pv]
                })
        except Exception as e:
            print(f"⚠️ Erro ao acessar {nome_col}: {e}")
            continue

# ========== EXPORTAR ==========
if registros:
    df = pd.DataFrame(registros)
    df = df.dropna(subset=["Ano", "Pais", "Valor"])
    df = df.sort_values(by=["Ano", "Pais"])
    os.makedirs(os.path.dirname(CAMINHO_SAIDA_CSV), exist_ok=True)
    df.to_csv(CAMINHO_SAIDA_CSV, index=False)
    df.to_json(CAMINHO_SAIDA_JSON, orient="records", indent=2, force_ascii=False)
    print(f"✔️ Dados salvos em:\n- {CAMINHO_SAIDA_CSV}\n- {CAMINHO_SAIDA_JSON}")
else:
    print("⚠️ Nenhum dado válido foi encontrado.")

client.close()

