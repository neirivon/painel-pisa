# scripts/exporta_rubrica_v4.py

import json
from pymongo import MongoClient
from bson import json_util

# Conexão com MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["rubrica_sinapse_ia"]

# Buscar documento da versão 1.4 ativa
rubrica = colecao.find_one({"versao": "v1.4", "status": "ativa"}, {"_id": 0})

# Caminho de saída
caminho_saida = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/rubrica_sinapase_ia_v4.json"

# Salvar usando utilitário do bson para serializar datetime
with open(caminho_saida, "w", encoding="utf-8") as f:
    f.write(json_util.dumps(rubrica, indent=2, ensure_ascii=False))

client.close()

print(f"✅ Rubrica v1.4 salva com sucesso em: {caminho_saida}")


