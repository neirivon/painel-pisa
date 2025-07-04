# scripts/importar_pisa2006_xls.py

import os
import pandas as pd
import json
from pymongo import MongoClient

# ========================
# CONFIGURAÇÃO
# ========================
CAMINHO_PASTA = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2006"
ARQUIVOS = {
    "attitudes": "Comp_Att06_Dec07.xls",
    "cognitive": "Comp_Cogn06_Dec07.xls"
}
NOME_BANCO = "pisa"
URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DIR_OUT = "dados_processados/pisa/2006"

# ========================
# PROCESSAMENTO
# ========================
os.makedirs(DIR_OUT, exist_ok=True)
client = MongoClient(URI)
db = client[NOME_BANCO]

for nome_colecao, nome_arquivo in ARQUIVOS.items():
    caminho = os.path.join(CAMINHO_PASTA, nome_arquivo)

    print(f"📥 Lendo {nome_arquivo}...")
    df = pd.read_excel(caminho)

    # Salvar CSV
    csv_path = os.path.join(DIR_OUT, f"{nome_colecao}.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ CSV salvo: {csv_path}")

    # Salvar JSON
    json_path = os.path.join(DIR_OUT, f"{nome_colecao}.json")
    df.to_json(json_path, orient="records", force_ascii=False, indent=2)
    print(f"✅ JSON salvo: {json_path}")

    # Inserir no MongoDB
    dados = df.to_dict(orient="records")
    db[f"pisa_2006_{nome_colecao}"].delete_many({})
    db[f"pisa_2006_{nome_colecao}"].insert_many(dados)
    print(f"✅ Inseridos em MongoDB: pisa.pisa_2006_{nome_colecao}")

client.close()
print("🔒 Conexão com MongoDB encerrada.")

