import os
import pandas as pd
from pymongo import MongoClient
import pyreadstat
from datetime import datetime

# === CONFIGURAÇÃO ===
MODO_EXECUCAO = os.environ.get("MODO_EXECUCAO", "local")  # 'local' ou 'cloud'
CAMINHO_ARQUIVO_SAV = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "P")ISA_novos.path.join(o, "D")ADOos.path.join(S, "2")01os.path.join(8, "V")Nos.path.join(M, "C")Y07_VNM_STU_COG.sav"))
NOME_COLECAO = "pisa_2018_vnm_cog_nans"
PASTA_SAIDA = "dados_processadoos.path.join(s, "2")01os.path.join(8, "V")NM"

# === GARANTIR PASTA DE SAÍDA ===
os.makedirs(PASTA_SAIDA, exist_ok=True)

# === LEITURA DO ARQUIVO .SAV ===
print("📥 Lendo o arquivo .sav...")
df, meta = pyreadstat.read_sav(CAMINHO_ARQUIVO_SAV)
print(f"✅ Total de linhas no arquivo: {len(df)}")

# === FILTRAR DADOS COM NaNs ===
df_nans = df[df.isna().any(axis=1)]
print(f"❗ Linhas com ao menos um NaN: {len(df_nans)}")

# === SALVAR EM CSV E JSON ===
csv_path = os.path.join(PASTA_SAIDA, "cog_2018_vnm_nans.csv")
json_path = os.path.join(PASTA_SAIDA, "cog_2018_vnm_nans.json")

df_nans.to_csv(csv_path, index=False)
df_nans.to_json(json_path, orient="records", lines=True, force_ascii=False)

print(f"💾 Arquivos salvos em:\n→ CSV:  {csv_path}\n→ JSON: {json_path}")

# === INSERIR NO MONGODB ===
print("🌐 Inserindo no MongoDB...")
if MODO_EXECUCAO == "local":
    mongo_uri = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
else:
    mongo_uri = os.environ.get("MONGO_CLOUD_URI")

client = MongoClient(mongo_uri)
db = client["pisa"]
colecao = db[NOME_COLECAO]

# Adiciona timestamp de extração para rastreabilidade
dados_json = df_nans.to_dict(orient="records")
for doc in dados_json:
    doc["timestamp_extracao"] = datetime.utcnow()

colecao.delete_many({})  # limpeza opcional
colecao.insert_many(dados_json)
print(f"✅ {len(dados_json)} documentos inseridos em 'pisa.{NOME_COLECAO}'.")

client.close()
print("🏁 Fim da execução.")

