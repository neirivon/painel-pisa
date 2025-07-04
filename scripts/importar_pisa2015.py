# scripts/importar_pisa2015.py

import os
import pandas as pd
import pyreadstat
from pymongo import MongoClient
from datetime import datetime
import json

# ========================
# CONFIGURAÇÃO PRINCIPAL
# ========================
CAMINHO_PASTA = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2015"
PASTA_OUT = "dados_processados/pisa/2015"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"

# ========================
# FUNÇÃO PRINCIPAL
# ========================
def processar_sav(caminho_arquivo):
    nome_base = os.path.splitext(os.path.basename(caminho_arquivo))[0].lower()
    nome_colecao = f"pisa_2015_{nome_base}"
    print(f"📥 Lendo {os.path.basename(caminho_arquivo)}...")

    df, _ = pyreadstat.read_sav(caminho_arquivo)

    # Exportar CSV
    os.makedirs(PASTA_OUT, exist_ok=True)
    caminho_csv = os.path.join(PASTA_OUT, f"{nome_base}.csv")
    df.to_csv(caminho_csv, index=False)
    print(f"✅ CSV salvo: {caminho_csv}")

    # Exportar JSON
    caminho_json = os.path.join(PASTA_OUT, f"{nome_base}.json")
    df.to_json(caminho_json, orient="records", force_ascii=False)
    print(f"✅ JSON salvo: {caminho_json}")

    # Inserir no MongoDB
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[nome_colecao]
    dados = df.to_dict(orient="records")
    colecao.delete_many({})
    if dados:
        colecao.insert_many(dados)
        print(f"✅ Inseridos em MongoDB: {BANCO}.{nome_colecao}")
    client.close()

# ========================
# EXECUÇÃO
# ========================
if __name__ == "__main__":
    arquivos = [f for f in os.listdir(CAMINHO_PASTA) if f.lower().endswith(".sav")]
    if not arquivos:
        print("❌ Nenhum arquivo .sav encontrado.")
    else:
        for nome_arquivo in arquivos:
            caminho = os.path.join(CAMINHO_PASTA, nome_arquivo)
            try:
                processar_sav(caminho)
            except Exception as e:
                print(f"⚠️ Erro ao processar {nome_arquivo}: {e}")

