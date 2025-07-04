# scripts/reimportar_student_2009_sps.py

import os
import pandas as pd
from pymongo import MongoClient

SPS_PATH = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/PISA2009_SPSS_student.txt"
TXT_PATH = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/INT_SCQ09_Dec11.txt")
CSV_PATH = "dados_processados/pisa/2009/student_sps.csv"
JSON_PATH = "dados_processados/pisa/2009/student_sps.json"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = "pisa_2009_student_sps"

def parse_sps_script(path):
    colspecs = []
    colnames = []
    with open(path, "r", encoding="latin1") as f:
        for line in f:
            line = line.strip()
            if line.startswith("DATA LIST") or line.startswith("FILE") or not line or line.startswith("*"):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            try:
                varname = parts[0]
                start = int(parts[1])
                end = int(parts[3])
                colnames.append(varname)
                colspecs.append((start - 1, end))  # Python is 0-based
            except ValueError:
                continue
    return colspecs, colnames

print("📥 Lendo metadados do SPS...")
colspecs, colnames = parse_sps_script(SPS_PATH)

print("📄 Lendo TXT com colunas fixas...")
df = pd.read_fwf(TXT_PATH, colspecs=colspecs, names=colnames, encoding="latin1")

os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
df.to_csv(CSV_PATH, index=False)
df.to_json(JSON_PATH, orient="records", lines=True, force_ascii=False)

print("📦 Gravando no MongoDB...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
collection.delete_many({})
collection.insert_many(df.to_dict(orient="records"))
client.close()

print("✅ Reimportação via SPS concluída com sucesso!")

