from pymongo import MongoClient
import json
from datetime import datetime
import os

# Caminho do arquivo JSON
json_path = os.path.expanduser("~/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_v6a_complementar.json")

# Carregar os dados
with open(json_path, "r", encoding="utf-8") as f:
    rubrica_data = json.load(f)

# Garantir timestamps
for item in rubrica_data:
    if "timestamp" not in item:
        item["timestamp"] = datetime.utcnow().isoformat()

# Conexão MongoDB segura com context manager
with MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin") as client:
    db = client["rubricas"]
    collection = db["rubrica_sinapse_v6a"]

    for doc in rubrica_data:
        filtro = {
            "dimensao": doc["dimensao"],
            "nivel": doc["nivel"],
            "versao": doc["versao"]
        }
        collection.update_one(filtro, {"$set": doc}, upsert=True)

    total = collection.count_documents({})
    print("✅ Total de documentos após inserção:", total)

