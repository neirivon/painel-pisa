# scripts/importar_pisa2009_txt_com_sas.py

import os
import pandas as pd
from pymongo import MongoClient
from scripts.sas7bdat_parser import parse_sas_script

# === Caminhos ===
TXT_PATH = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/TXT/ERA_STQ09_June11.txt"
SAS_PATH = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SAS/PISA2009_SAS_student.sas"
OUT_CSV = "dados_processados/pisa/2009/student.csv"
OUT_JSON = "dados_processados/pisa/2009/student.json"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
MONGO_DB = "pisa"
MONGO_COLLECTION = "pisa_2009_student"

# === Etapa 1: Extrair Metadados ===
print("📥 Extraindo metadados SAS...")
colspecs, colnames = parse_sas_script(SAS_PATH)

# === Etapa 2: Ler TXT ===
print("📄 Lendo TXT com colunas fixas...")
df = pd.read_fwf(TXT_PATH, colspecs=colspecs, names=colnames, encoding='latin1')

# === Etapa 3: Exportar CSV e JSON ===
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
df.to_csv(OUT_CSV, index=False)
print(f"✅ CSV salvo: {OUT_CSV}")
df.to_json(OUT_JSON, orient="records", force_ascii=False)
print(f"✅ JSON salvo: {OUT_JSON}")

# === Etapa 4: Inserir no MongoDB ===
print("📦 Gravando no MongoDB...")
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))
client.close()
print("✅ Importação concluída com sucesso!")

