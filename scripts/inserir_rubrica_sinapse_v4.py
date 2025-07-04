from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_rubrica_sinapse_v4.py

import json
from pymongo import MongoClient
import os

# Caminho do arquivo JSON gerado anteriormente
caminho_json = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v4.json"

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["sinapse_9ano_todas_v4"]

# Verifica se o arquivo existe
if not os.path.exists(caminho_json):
    print(f"❌ Arquivo não encontrado: {caminho_json}")
    exit()

# Carregar os dados do JSON
with open(caminho_json, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# Transformar para estrutura achatada para inserção em MongoDB
documentos = []
for dim in rubrica:
    for nivel in dim["niveis"]:
        doc = {
            "dimensao": dim["dimensao"],
            "icone": dim["icone"],
            "versao": dim["versao"],
            "fonte": dim["fonte"],
            "timestamp_versao": dim["timestamp_versao"],
            "nivel": nivel["nivel"],
            "nome_nivel": nivel["nome"],
            "descricao": nivel["descricao"],
            "exemplo": nivel["exemplo"]
        }
        documentos.append(doc)

# Apagar dados antigos antes de reinserir (se desejar sobrescrever)
colecao.delete_many({})

# Inserir no MongoDB
colecao.insert_many(documentos)

# Fechar conexão
client.close()

# Confirmação
print("✅ Rubrica SINAPSE v4 inserida com sucesso no MongoDB.")
print("📁 Coleção: rubricas.sinapse_9ano_todas_v4")
print(f"📄 Fonte JSON: {caminho_json}")

