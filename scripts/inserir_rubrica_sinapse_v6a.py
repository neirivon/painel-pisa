from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_rubrica_sinapse_v6a.py

import json
from pymongo import MongoClient
import os

# Caminho para o arquivo JSON da versão adaptada v6a
json_path = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "d")ados_processadoos.path.join(s, "r")ubricaos.path.join(s, "r")ubrica_sinapse_v6_adaptada.json"))

# Carregar dados do JSON
with open(json_path, "r", encoding="utf-8") as f:
    rubricas = json.load(f)

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
collection = db["sinapse_todas_v6a"]

# Apagar documentos antigos e inserir novos
collection.delete_many({})
collection.insert_many(rubricas)

# Encerrar conexão
client.close()

print("✅ Rubrica SINAPSE v6a inserida com sucesso no MongoDB!")
print("🗂️ Coleção: rubricas.sinapse_todas_v6a")

