from pymongo import MongoClient
from collections import OrderedDict

# Configuração de conexão
MONGO_URI = "mongodb://admin:admin123@localhost:27017"
DB_NAME = "rubricas"
COLLECTION_NAME = "rubrica_sinapse_ia"

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
colecao = db[COLLECTION_NAME]

# Buscar documento da versão v1.4
doc = colecao.find_one({"versao": "v1.4"})
if not doc:
    raise ValueError("❌ Rubrica v1.4 não encontrada.")

# Criar novo documento com ordem dos campos ajustada
novo_doc = OrderedDict()

# Metadados no início
for campo in ["status", "nome", "versao", "base", "modelo", "timestamp", "autor", "origem", "justificativa"]:
    if campo in doc:
        novo_doc[campo] = doc[campo]

# Campos principais
novo_doc["dimensoes"] = doc.get("dimensoes", [])
novo_doc["referencias"] = doc.get("referencias", [])

# Substituir documento mantendo o mesmo _id
colecao.replace_one({"_id": doc["_id"]}, novo_doc)

print("✅ Documento da versão v1.4 reorganizado com sucesso!")

client.close()

