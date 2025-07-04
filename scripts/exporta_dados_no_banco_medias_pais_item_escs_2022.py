from pymongo import MongoClient
import json
import os

# ========== CONEXÃO ==========
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
colecao = db["medias_pais_item_escs_2022"]

# ========== EXPORTAÇÃO ==========
documentos = list(colecao.find({}, {"_id": 0}))  # remove o ObjectId

# Cria diretório se não existir
os.makedirs("/home/neirivon/SINAPSE2.0/PISA/dados_processados/exportados", exist_ok=True)
CAMINHO_TXT = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/exportados/medias_pais_item_escs_2022.txt"

with open(CAMINHO_TXT, "w", encoding="utf-8") as f:
    for doc in documentos:
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

client.close()

print(f"✅ Exportado com sucesso para: {CAMINHO_TXT}")

