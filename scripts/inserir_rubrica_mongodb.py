from pymongo import MongoClient
import json

# Caminho do JSON no seu sistema
json_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v4.json"

# Conexão com o MongoDB dockerizado
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
collection = db["rubrica_sinapse_ia"]

# Carregar os dados JSON
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Substituir conteúdo antigo
collection.delete_many({})
if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

# Obter total de documentos antes de fechar conexão
total = collection.count_documents({})
print("✅ Rubrica SINAPSE IA v4 inserida com sucesso.")
print(f"📄 Total de documentos na coleção: {total}")

# Fechar explicitamente (opcional, mas mais seguro em scripts longos)
client.close()
