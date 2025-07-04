# scripts/copiar_colecoes_inep_para_pisa.py

from pymongo import MongoClient

# URI autenticada do MongoDB local
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"

# Conecta ao Mongo
client = MongoClient(MONGO_URI)
db_origem = client["relatorios_inep"]
db_destino = client["pisa"]

# Lista as coleções de interesse
colecoes_origem = db_origem.list_collection_names()
colecoes_filtradas = [c for c in colecoes_origem if c.startswith("relatorio_inep_")]

print("🔁 Copiando coleções do banco 'relatorios_inep' → 'pisa':\n")

for nome_colecao in colecoes_filtradas:
    nova_colecao = nome_colecao.replace("relatorio_inep_", "relatorio_inep_pisa_")
    print(f"✔ {nome_colecao} → {nova_colecao}")

    docs = list(db_origem[nome_colecao].find())
    if docs:
        db_destino[nova_colecao].insert_many(docs)
    else:
        print(f"⚠️ Coleção '{nome_colecao}' está vazia.")

client.close()
print("\n✅ Migração concluída com sucesso.")

