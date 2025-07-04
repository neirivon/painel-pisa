# scripts/importar_pisa2009_sas.py

import os
import pandas as pd
import pyreadstat
from pymongo import MongoClient
from datetime import datetime

# Caminhos
TXT_PATH = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/ERA_STQ09_June11.txt"
SAS_PATH = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SAS/PISA2009_SAS_student.sas"
BASE_NOME = "pisa_2009_era_stq09_june11"
OUTPUT_DIR = "dados_processados/pisa/2009"

# MongoDB
URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = BASE_NOME

# Garantir pasta de saída
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"📥 Processando {os.path.basename(TXT_PATH)} com {os.path.basename(SAS_PATH)}...")

# Ler o arquivo TXT com dicionário SAS
df, meta = pyreadstat.read_sas(TXT_PATH, metadata=SAS_PATH)

# Salvar CSV e JSON
csv_path = os.path.join(OUTPUT_DIR, f"{BASE_NOME}.csv")
json_path = os.path.join(OUTPUT_DIR, f"{BASE_NOME}.json")
df.to_csv(csv_path, index=False)
df.to_json(json_path, orient="records", force_ascii=False)

print(f"✅ CSV salvo: {csv_path}")
print(f"✅ JSON salvo: {json_path}")

# Inserir no MongoDB
client = MongoClient(URI)
try:
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    collection.delete_many({})  # Limpa dados anteriores
    collection.insert_many(df.to_dict(orient="records"))
    print(f"✅ Inseridos em MongoDB: {DB_NAME}.{COLLECTION_NAME}")
finally:
    client.close()
    print("🔒 Conexão com MongoDB encerrada.")

