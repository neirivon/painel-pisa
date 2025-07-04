from pymongo import MongoClient
import json

# Conexão MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["rubrica_sinapse"]

# Caminho do arquivo JSON da nova rubrica
caminho_json = "/home/neirivon/Downloads/rubrica_sinapse_ia_v1_5.json"

# Atualiza v1.4 para inativa
resultado = colecao.update_many({"versao": "v1.4"}, {"$set": {"status": "inativa"}})
print(f"📉 Rubrica v1.4 modificada: {resultado.modified_count} documento(s)")

# Carrega nova rubrica (como lista)
with open(caminho_json, "r", encoding="utf-8") as f:
    lista_rubricas = json.load(f)

# Se for uma lista, pega o primeiro item
nova_rubrica = lista_rubricas[0] if isinstance(lista_rubricas, list) else lista_rubricas
nova_rubrica["status"] = "ativa"

# Insere no banco
inserido = colecao.insert_one(nova_rubrica)
print("✅ Rubrica v1.5 inserida com sucesso!")
print("🧾 ID do novo documento:", inserido.inserted_id)

# Fecha conexão
client.close()

