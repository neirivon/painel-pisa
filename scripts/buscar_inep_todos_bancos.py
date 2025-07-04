# scripts/buscar_inep_todos_bancos.py

from pymongo import MongoClient

# Conexão local autenticada
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
client = MongoClient(MONGO_URI)

print("🔍 Buscando coleções com 'inep' em TODOS os bancos MongoDB...\n")

bancos = client.list_database_names()
achados = []

for banco in bancos:
    db = client[banco]
    try:
        colecoes = db.list_collection_names()
        for colecao in colecoes:
            if "inep" in colecao.lower():
                achados.append((banco, colecao))
    except Exception as e:
        print(f"⚠️ Erro ao acessar banco '{banco}': {e}")

if achados:
    for idx, (banco, colecao) in enumerate(achados, start=1):
        print(f"{idx:02d}. Banco: {banco} | Coleção: {colecao}")
else:
    print("❌ Nenhuma coleção com 'inep' foi encontrada em nenhum banco.")

client.close()

