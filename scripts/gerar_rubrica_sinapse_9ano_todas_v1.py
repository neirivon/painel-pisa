import json
import csv
import os
from pymongo import MongoClient
from datetime import datetime

# === Configurações ===
CAMINHOS_JSON = [
    "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_matematica_v1.json",
    "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_lingua_portuguesa_v1.json",
    "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_ciencias_v1.json"
]
CAMINHO_SAIDA_JSON = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v1.json"
CAMINHO_SAIDA_CSV = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v1.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
MONGO_DB = "rubricas"
MONGO_COLLECTION = "sinapse_9ano_todas"

# === Unificação ===
rubricas_unificadas = []
for caminho in CAMINHOS_JSON:
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        rubricas_unificadas.extend(dados)

# === Detectar todos os campos únicos ===
todos_campos = set()
for doc in rubricas_unificadas:
    todos_campos.update(doc.keys())
todos_campos = sorted(list(todos_campos))

# === Salvar JSON unificado ===
os.makedirs(os.path.dirname(CAMINHO_SAIDA_JSON), exist_ok=True)
with open(CAMINHO_SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(rubricas_unificadas, f, ensure_ascii=False, indent=2)

# === Salvar CSV unificado ===
with open(CAMINHO_SAIDA_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=todos_campos)
    writer.writeheader()
    for doc in rubricas_unificadas:
        linha = {campo: doc.get(campo, "") for campo in todos_campos}
        writer.writerow(linha)

# === Inserção no MongoDB ===
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
colecao = db[MONGO_COLLECTION]
colecao.drop()
for doc in rubricas_unificadas:
    doc["timestamp_insercao"] = datetime.utcnow()
colecao.insert_many(rubricas_unificadas)
client.close()

# === Fim ===
print("✅ Rubrica SINAPSE unificada gerada e armazenada com sucesso.")
print(f"📄 JSON: {CAMINHO_SAIDA_JSON}")
print(f"📄 CSV:  {CAMINHO_SAIDA_CSV}")
print(f"🌐 MongoDB: {MONGO_DB}.{MONGO_COLLECTION}")

