import os
import pandas as pd
from pymongo import MongoClient

# === CONFIGURAÇÕES ===
CAMINHO_BASE = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT")
ARQUIVO_DADOS = os.path.join(CAMINHO_BASE, "INT_SCQ09_Dec11.txt")
ARQUIVO_MASCARA = os.path.join(CAMINHO_BASE, "PISA2009_SPSS_cognitive_item.txt")
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = "pisa_2009_sps"

# === Função para carregar máscara de colunas fixas ===
def carregar_mascara_spss(arquivo_mascara):
    col_names = []
    col_specs = []
    with open(arquivo_mascara, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split()
            if len(partes) >= 3:
                nome = partes[0]
                inicio = int(partes[1]) - 1  # início 0-based
                fim = int(partes[2])         # fim exclusivo
                col_names.append(nome)
                col_specs.append((inicio, fim))
    return col_names, col_specs

# === Função principal ===
def importar_para_mongodb():
    print("📥 Lendo metadados do SPS...")
    col_names, col_specs = carregar_mascara_spss(ARQUIVO_MASCARA)

    print("📄 Lendo TXT com colunas fixas...")
    df = pd.read_fwf(ARQUIVO_DADOS, names=col_names, colspecs=col_specs, encoding='latin1')

    print("📦 Gravando no MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    collection.drop()  # Apagar se já existir
    registros = df.to_dict(orient="records")
    collection.insert_many(registros)

    print(f"✅ {len(registros)} registros importados com sucesso na coleção '{COLLECTION_NAME}'.")

# === Execução ===
if __name__ == "__main__":
    importar_para_mongodb()

