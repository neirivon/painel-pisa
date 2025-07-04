from pymongo import MongoClient
import json
from datetime import datetime

# Conectar ao MongoDB com autenticação
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["avaliacoes_rubricas_referenciais"]

# Buscar avaliações (sem _id)
avaliacoes = list(colecao.find({}, {"_id": 0}))

# Converter datetime para string ISO
for a in avaliacoes:
    if isinstance(a.get("timestamp"), datetime):
        a["timestamp"] = a["timestamp"].isoformat() + "Z"

# Salvar em JSON
CAMINHO = "dados_processados/rubricas/avaliacoes_rubricas_referenciais.json"
with open(CAMINHO, "w", encoding="utf-8") as f:
    json.dump(avaliacoes, f, ensure_ascii=False, indent=2)

client.close()
print(f"✅ Exportado para {CAMINHO}")

