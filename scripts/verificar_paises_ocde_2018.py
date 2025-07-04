from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# arquivo: listar_campos_ocde_2018.py

from pymongo import MongoClient

# Conectar no MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2018"]

# Buscar um único documento para inspecionar os campos
exemplo = colecao.find_one()

if exemplo:
    print("🔍 Campos encontrados no documento:")
    for campo in exemplo.keys():
        print(f"- {campo}")
else:
    print("⚠️ Nenhum documento encontrado na coleção.")

client.close()

