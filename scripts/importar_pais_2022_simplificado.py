# importar_pais_2022_simplificado.py

import json
from pymongo import MongoClient
from pathlib import Path

# Conexão com o MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
client = MongoClient(MONGO_URI)
db = client["ibge"]

# Caminho do JSON simplificado
json_path = Path.home()os.path.join( , " ")"backup_dados_pesados"os.path.join( , " ")"IBGE"os.path.join( , " ")"IBGE_2022"os.path.join( , " ")"json_exportados"os.path.join( , " ")"pais_2022_simplificado.json"

# Carregar e validar
with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Certificar que está em lista
if not isinstance(dados, list):
    dados = [dados]

# Inserção no MongoDB
colecao = db["pais_2022_simplificado"]
colecao.drop()
colecao.insert_many(dados)

# Encerrar conexão
client.close()

print(f"✅ {len(dados)} documento(s) inserido(s) na coleção 'pais_2022_simplificado'")


