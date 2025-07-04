from pymongo import MongoClient
import json

# Configurações de conexão
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DATABASE = "rubricas"
COLECAO = "rubricas_referenciais"
CAMINHO_JSON = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubricas_referenciais_completas.json"

# Conectar ao MongoDB com autenticação
client = MongoClient(MONGO_URI)
db = client[DATABASE]
colecao = db[COLECAO]

# Carregar dados do JSON
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    rubricas = json.load(f)

# Substituir conteúdo anterior
colecao.delete_many({})
resultado = colecao.insert_many(rubricas)

client.close()

print(f"✅ Inseridos {len(resultado.inserted_ids)} documentos na coleção '{COLECAO}' do banco '{DATABASE}'.")

