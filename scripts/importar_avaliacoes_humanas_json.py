import json
from pymongo import MongoClient
import sys

# Verifica o argumento
if len(sys.argv) < 2:
    print("Uso: python3 scripts/importar_avaliacoes_humanas_json.py <caminho_json>")
    sys.exit(1)

json_path = sys.argv[1]

# Conexão com o MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
colecao = db["avaliacoes_humanas"]

try:
    with open(json_path, "r", encoding="utf-8") as f:
        dados = json.load(f)
        if isinstance(dados, list):
            colecao.delete_many({})  # limpa para reimportação
            colecao.insert_many(dados)
            print(f"✅ {len(dados)} documentos inseridos com sucesso na coleção 'avaliacoes_humanas'.")
        else:
            print("❌ O JSON deve conter uma lista de objetos.")
finally:
    client.close()

