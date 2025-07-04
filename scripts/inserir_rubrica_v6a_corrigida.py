from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_rubrica_v6a_corrigida.py

import json
from pymongo import MongoClient
import os

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARQUIVO_JSON = os.path.join(BASE_DIR, "dados_processados", "rubricas", "rubrica_sinapse_v6a_corrigida.json")

# Verificação
if not os.path.exists(ARQUIVO_JSON):
    raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO_JSON}")

# Leitura do arquivo
with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["sinapse_todas_v6a"]

# Limpa e insere
colecao.delete_many({})
colecao.insert_many(rubrica)
client.close()

print("✅ Rubrica v6a corrigida inserida com sucesso no MongoDB!")
print("🗂️ Coleção: rubricas.sinapse_todas_v6a")
