import os
import pandas as pd
from pymongo import MongoClient

# === CAMINHOS DOS ARQUIVOS ===
CAMINHO_MASCARA = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SAS")
ARQUIVO_DADOS = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/INT_SCQ09_Dec11.txt")
ARQUIVO_MASCARA = os.path.join(CAMINHO_MASCARA, "mascara_school_2009.txt")

# === CONEXÃO MONGODB COM AUTENTICAÇÃO ===
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = "pisa_2009_school"

# === Função para carregar a máscara ===
def carregar_mascara_colunas(arquivo_mascara):
    col_names = []
    col_specs = []
    with open(arquivo_mascara, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split()
            if len(partes) == 3:
                nome = partes[0]
                inicio = int(partes[1]) - 1  # 0-based
                fim = int(partes[2])
                col_names.append(nome)
                col_specs.append((inicio, fim))
    return col_names, col_specs

# === Função principal ===
def importar_para_mongo():
    print("📥 Lendo máscara...")
    col_names, col_specs = carregar_mascara_colunas(ARQUIVO_MASCARA)

    print("📄 Lendo dados formatados...")
    df = pd.read_fwf(ARQUIVO_DADOS, names=col_names, colspecs=col_specs, encoding="latin1")

    print("📊 Primeiras 3 linhas dos dados:")
    print(df.head(3).to_string(index=False))

    print("📦 Gravando no MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    collection.drop()  # limpa se já existir
    collection.insert_many(df.to_dict(orient="records"))

    print(f"✅ Importação concluída com {len(df)} registros em '{COLLECTION_NAME}'.")

# === Execução ===
if __name__ == "__main__":
    importar_para_mongo()

