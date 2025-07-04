from pymongo import MongoClient

# Conexão com autenticação
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

colecoes_2006 = [
    "pisa_2006_cog_s",
    "pisa_2006_cog_t",
    "pisa_2006_parent",
    "pisa_2006_school",
    "pisa_2006_student",
]

print("📊 Verificação de documentos nas coleções 2006:\n")

for nome_colecao in colecoes_2006:
    try:
        total = db[nome_colecao].count_documents({})
        print(f"📁 {nome_colecao:<25} → {total:,} documentos")
    except Exception as e:
        print(f"❌ Erro ao acessar '{nome_colecao}': {e}")

# Encerrar conexão
client.close()

