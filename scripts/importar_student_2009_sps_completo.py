# scripts/importar_student_2009_sps_completo.py

import os
import pandas as pd
from pymongo import MongoClient

SPS_PATH = "backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/PISA2009_SPSS_student.txt"
TXT_PATH = "backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/INT_SCQ09_Dec11.txt"
CSV_OUT = "dados_processados/pisa/2009/student.csv"
JSON_OUT = "dados_processados/pisa/2009/student.json"
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "pisa"
COLLECTION_NAME = "pisa_2009_student"

def parse_sps_script(path):
    colspecs = []
    colnames = []
    with open(path, "r", encoding="latin1") as f:
        for line in f:
            if line.strip().startswith("DATA LIST"):
                continue
            if "/" in line or "SET" in line or "*" in line:
                continue
            parts = line.strip().split()
            if len(parts) >= 4:
                name = parts[0]
                start = int(parts[1])
                end = int(parts[3])
                colnames.append(name)
                colspecs.append((start - 1, end))
    return colspecs, colnames

# === Execução principal ===
print("📥 Lendo metadados do SPS...")
colspecs, colnames = parse_sps_script(SPS_PATH)

print("📄 Lendo TXT com colunas fixas...")
df = pd.read_fwf(TXT_PATH, colspecs=colspecs, names=colnames, encoding="latin1")

print("💾 Salvando CSV e JSON...")
os.makedirs(os.path.dirname(CSV_OUT), exist_ok=True)
df.to_csv(CSV_OUT, index=False)
df.to_json(JSON_OUT, orient="records", lines=True)

print("📦 Gravando no MongoDB...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))

print("✅ Reimportação via SPS concluída com sucesso!")

