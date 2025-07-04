# scripts/verificar_colecoes_2003.py

from pymongo import MongoClient

# Conexão direta com o MongoDB local dockerizado
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

colecoes_2003 = [
    "pisa_2003_student",
    "pisa_2003_school",
    "pisa_2003_cognitive_item"
]

print("📊 Verificação de documentos nas coleções da edição 2003:\n")

for colecao in colecoes_2003:
    total = db[colecao].count_documents({})
    print(f"📁 {colecao:<28} → {total:,} documentos")

# Encerrar a conexão
client.close()

