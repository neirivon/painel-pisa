# verificar_colecoes_edicoes_lote.py

from pymongo import MongoClient

# Conexão com MongoDB dockerizado
uri = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
client = MongoClient(uri)
db = client["pisa"]

# Dicionário com coleções por edição
edicoes = {
    "2000": [
        "pisa_2000_cog_s", "pisa_2000_cog_t", "pisa_2000_parent",
        "pisa_2000_school", "pisa_2000_student"
    ],
    "2003": [
        "pisa_2003_cog_s", "pisa_2003_cog_t", "pisa_2003_parent",
        "pisa_2003_school", "pisa_2003_student"
    ],
    "2022": [
        "pisa_2022_cog_s", "pisa_2022_cog_t", "pisa_2022_parent",
        "pisa_2022_school", "pisa_2022_student"
    ],
}

print("📊 Verificação de documentos por edição:\n")

for edicao, colecoes in edicoes.items():
    print(f"🗂️ Edição {edicao}")
    for nome in colecoes:
        try:
            total = db[nome].count_documents({})
            print(f"  📁 {nome:<25} → {total:,} documentos")
        except Exception as e:
            print(f"  ⚠️  {nome:<25} → Erro: {e}")
    print()

client.close()
print("🔒 Conexão com MongoDB encerrada.")

