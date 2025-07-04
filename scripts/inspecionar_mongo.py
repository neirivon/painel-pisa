from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]

print("📂 Bancos disponíveis:", client.list_database_names())

db = client["pisa"]  # substitua se for outro nome
colecoes = db.list_collection_names()
print("\n📁 Coleções no banco 'pisa':", colecoes)

for colecao in colecoes:
    print(f"\n📄 Amostra da coleção: {colecao}")
    doc = db[colecao].find_one()
    if doc:
        print("🔑 Campos disponíveis:", list(doc.keys()))
    else:
        print("⚠️ Nenhum documento encontrado.")

