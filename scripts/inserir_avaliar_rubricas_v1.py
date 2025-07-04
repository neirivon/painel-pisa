from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_avaliar_rubricas_v1.py

import json
from pymongo import MongoClient

# Caminho do arquivo JSON com a rubrica
caminho_json = "dados_processadoos.path.join(s, "r")ubricaos.path.join(s, "a")valiar_rubricas_v1.json"

# Conectar ao MongoDB (modo local padrão)
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["avaliar_rubricas_v1"]

# Limpar coleção antes de inserir (opcional, cuidado!)
colecao.delete_many({})

# Carregar dados do JSON
with open(caminho_json, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Adicionar metadado de autoria em cada entrada
for rubrica in dados:
    rubrica["autor"] = "Professor Dr. Bruno Pereira Garcês"

# Inserir os dados
colecao.insert_many(dados)

# Fechar conexão com o MongoDB
client.close()

print("✅ Rubrica de Avaliação de Rubricas v1 inserida com sucesso no MongoDB.")
print("📁 Coleção: rubricas.avaliar_rubricas_v1")
print(f"📄 Fonte JSON: {caminho_json}")
print("👤 Criador: Professor Dr. Bruno Pereira Garcês")

