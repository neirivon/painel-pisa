import pandas as pd
from pymongo import MongoClient
import pyreadstat
import os
import math
import json
from datetime import datetime

# === CONFIGURAÇÕES ===
CAMINHO_SAV = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/SAV/CY08MSP_STU_COG.SAV"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"
COLECAO = "pisa_2022_cog"
TAMANHO_BLOCO = 50000
CAMINHO_CHECKPOINT = "checkpoint_stu_cog_2022.json"

# === CONEXÃO COM MONGODB ===
client = MongoClient(MONGO_URI)
db = client[BANCO]
colecao = db[COLECAO]

# === LER CHECKPOINT ===
inicio = 0
if os.path.exists(CAMINHO_CHECKPOINT):
    with open(CAMINHO_CHECKPOINT, "r") as f:
        dados = json.load(f)
        inicio = dados.get("ultimo_indice", 0)
        print(f"🔁 Retomando do índice {inicio} com checkpoint.")

# === CARREGAR DADOS ===
print(f"📥 Lendo arquivo: {CAMINHO_SAV}")
df, meta = pyreadstat.read_sav(CAMINHO_SAV)
total = len(df)
print(f"📊 Total de registros no arquivo: {total}")

# === INSERÇÃO EM BLOCOS COM PROGRESSO E CHECKPOINT ===
for i in range(inicio, total, TAMANHO_BLOCO):
    bloco = df.iloc[i:i + TAMANHO_BLOCO].fillna(None).to_dict(orient="records")
    colecao.insert_many(bloco)

    # Atualizar checkpoint
    with open(CAMINHO_CHECKPOINT, "w") as f:
        json.dump({"ultimo_indice": i + TAMANHO_BLOCO}, f)

    progresso = min(i + TAMANHO_BLOCO, total)
    percentual = round((progresso / total) * 100, 2)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Inserido {progresso} / {total} ({percentual}%)")

print(f"🏁 Concluído! {total} registros inseridos com sucesso na coleção '{COLECAO}'.")
client.close()
print("🔒 Conexão com MongoDB encerrada.")

