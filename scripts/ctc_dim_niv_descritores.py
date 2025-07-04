from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["sinapse_todas_v6a"]

# Busca fuzzy
cursor = colecao.find({"dimensao": {"$regex": "territorial", "$options": "i"}}, {"_id": 0, "dimensao": 1}).limit(10)
dimensoes_encontradas = list(cursor)

for item in dimensoes_encontradas:
    print(item)

client.close()

