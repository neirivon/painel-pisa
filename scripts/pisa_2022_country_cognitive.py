from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://admin:admin123@localhost:27017")

# Acessa a coleção com dados cognitivos por país
colecao = client["pisa"]["pisa_2022_country_cognitive"]

# Busca os primeiros 50 documentos
documentos = list(colecao.find({}, {"_id": 0}).limit(50))

client.close()

# Exibe os 5 primeiros para visualização
print("\n📘 Amostra da coleção 'pisa_2022_country_cognitive':")
for doc in documentos[:5]:
    pprint(doc)
    print("-" * 60)

