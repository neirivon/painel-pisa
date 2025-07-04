from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_nivel_lp_saeb2021.py

from pymongo import MongoClient

# === Conexão com o MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_9ano"]

# === Função de classificação da rubrica de LP ===
def classificar_nivel_lp(media):
    if media is None:
        return None
    elif media < 225:
        return "0"
    elif media < 250:
        return "1 a 3"
    elif media < 275:
        return "4 a 5"
    elif media < 300:
        return "6 a 7"
    else:
        return "8"

# === Atualização em lote ===
contador = 0
for doc in colecao.find({"MEDIA_9_LP": {"$exists": True}}):
    media_lp = doc.get("MEDIA_9_LP")
    nivel = classificar_nivel_lp(media_lp)

    if nivel:
        colecao.update_one(
            {"_id": doc["_id"]},
            {"$set": {"nivel_lp": nivel}}
        )
        contador += 1

# === Fechar conexão ===
client.close()

print(f"✅ {contador} documentos atualizados com o campo 'nivel_lp'.")

