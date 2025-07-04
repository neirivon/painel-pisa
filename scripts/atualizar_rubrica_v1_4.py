from pymongo import MongoClient
from datetime import datetime

# Configurações de conexão
MONGO_URI = "mongodb://admin:admin123@localhost:27017"
DB_NAME = "rubricas"
COLLECTION = "rubrica_sinapse_ia"

# Conecta ao MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
colecao = db[COLLECTION]

# Atualiza a versão v1.4 com os metadados padronizados
resultado = colecao.update_one(
    {"versao": "v1.4"},
    {
        "$set": {
            "nome": "rubrica_sinapse_ia",
            "status": "ativa",
            "base": "SAEB 2017 + PISA 2022",
            "modelo": "LLAMA3 + análise pedagógica",
            "timestamp": datetime(2025, 6, 7, 14, 0, 0),
            "autor": "neirivon",
            "origem": "Rubrica base utilizada para triangulação com dados SAEB/PISA e validação por IA",
            "justificativa": "Estrutura original da versão 1.4 mantida como referência primária após análise crítica qualitativa e validação automatizada."
        }
    }
)

# Resultado do processo
if resultado.modified_count > 0:
    print("✅ Rubrica v1.4 atualizada com sucesso.")
else:
    print("⚠️ Nenhum documento foi modificado. Verifique se a versão v1.4 existe.")

client.close()

