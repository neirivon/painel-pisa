# scripts/verificar_edicoes_inep.py

from pymongo import MongoClient

# URI local com autenticação (forçado)
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
NOME_BANCO = "pisa"

# Conecta diretamente
client = MongoClient(MONGO_URI)
db = client[NOME_BANCO]

# Lista as coleções do banco
colecoes = db.list_collection_names()
colecoes_inep = sorted([c for c in colecoes if "inep" in c.lower()])

print("📄 Coleções INEP encontradas no MongoDB:\n")
for idx, nome in enumerate(colecoes_inep, start=1):
    print(f"{idx:02d}. {nome}")

client.close()

