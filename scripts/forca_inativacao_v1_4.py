from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

try:
    # Conexão com o MongoDB
    client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
    db = client["rubricas"]
    colecao = db["rubrica_sinapse"]

    # ID da versão 1.4 a ser inativada
    id_alvo = ObjectId("685071433ed68cd846778401")

    # Atualização forçada
    resultado = colecao.update_one(
        {"_id": id_alvo},
        {"$set": {"status": "inativa", "timestamp": datetime.utcnow()}}
    )

    if resultado.modified_count == 1:
        print("✅ Rubrica v1.4 atualizada com sucesso para 'inativa'.")
    else:
        print("⚠️ Nenhuma modificação. A rubrica já estava inativa ou o ID não foi localizado.")

except Exception as e:
    print("❌ Erro ao atualizar a rubrica:", str(e))
finally:
    client.close()
