from pymongo import MongoClient
from bson import ObjectId

try:
    client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
    db = client["rubricas"]
    colecao = db["rubrica_sinapse"]

    id_rubrica_v1_4 = ObjectId("685071433ed68cd846778401")
    resultado = colecao.update_one(
        {"_id": id_rubrica_v1_4},
        {"$set": {"status": "inativa"}}
    )

    if resultado.modified_count == 1:
        print("✅ Rubrica v1.4 agora está marcada como INATIVA.")
    else:
        print("⚠️ Nenhuma modificação. A rubrica já pode estar inativa ou o ID está incorreto.")

except Exception as e:
    print("❌ Erro ao atualizar rubrica:", e)
finally:
    client.close()

