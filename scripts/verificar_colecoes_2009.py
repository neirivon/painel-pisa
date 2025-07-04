# scripts/verificar_colecoes_2009.py

from pymongo import MongoClient

# Configurações de autenticação e conexão
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DATABASE_NAME = "pisa"

# Coleções esperadas da edição de 2009
colecoes_2009 = [
    "pisa_2009_cog_s",
    "pisa_2009_cog_td",
    "pisa_2009_parent",
    "pisa_2009_school",
    "pisa_2009_student"
]

# Conectar ao MongoDB
cliente = MongoClient(MONGO_URI)
db = cliente[DATABASE_NAME]

print("📊 Verificação de documentos nas coleções 2009:\n")
for nome in colecoes_2009:
    total = db[nome].count_documents({})
    print(f"📁 {nome:<24} → {total:,} documentos")

# Fechar conexão
cliente.close()

