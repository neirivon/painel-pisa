# scripts/importar_pisa2012_txt.py

import os
import pandas as pd
from pymongo import MongoClient

# =====================
# CONFIGURAÇÕES
# =====================
CAMINHO_PASTA = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2012"
PASTA_OUT = "dados_processados/pisa/2012"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"

ARQUIVOS = [
    "INT_COG09_S_DEC11.txt",
    "INT_COG09_TD_DEC11.txt",
    "INT_PAR09_DEC11.txt",
    "INT_SCQ09_Dec11.txt",
    "INT_STQ09_DEC11.txt"
]

# =====================
# FUNÇÃO PARA PROCESSAR
# =====================
def processar_txt(nome_arquivo):
    nome_base = os.path.splitext(nome_arquivo)[0].lower()
    caminho = os.path.join(CAMINHO_PASTA, nome_arquivo)
    print(f"📥 Lendo {nome_arquivo}...")

    try:
        df = pd.read_csv(caminho, sep='\t', encoding='latin1')
    except Exception as e:
        print(f"❌ Erro ao ler {nome_arquivo}: {e}")
        return

    os.makedirs(PASTA_OUT, exist_ok=True)
    caminho_csv = os.path.join(PASTA_OUT, f"{nome_base}.csv")
    caminho_json = os.path.join(PASTA_OUT, f"{nome_base}.json")

    df.to_csv(caminho_csv, index=False)
    print(f"✅ CSV salvo: {caminho_csv}")

    df.to_json(caminho_json, orient="records", force_ascii=False)
    print(f"✅ JSON salvo: {caminho_json}")

    # MongoDB
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[f"pisa_2012_{nome_base}"]

    dados = df.to_dict(orient="records")
    colecao.delete_many({})
    if dados:
        colecao.insert_many(dados)
        print(f"✅ Inseridos em MongoDB: pisa.pisa_2012_{nome_base}")
    client.close()

# =====================
# EXECUÇÃO
# =====================
if __name__ == "__main__":
    for nome in ARQUIVOS:
        processar_txt(nome)

