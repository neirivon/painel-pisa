# scriptos.path.join(s, "a")tualizar_matematica_resumo.py

from pymongo import MongoClient

# === Conexão MongoDB ===
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
client = MongoClient(MONGO_URI)

db = client["saeb"]

# === Mapeamento de fontes ===
fontes = {
    "Brasil": db["rubricas_2001_brasil"],
    "Minas Gerais": db["rubricas_2001_minasgerais"],
    "Triângulo Mineiro": db["rubricas_2001_micro_triangulo"]
}

# === Atualizar a coleção resumo ===
for regiao, colecao in fontes.items():
    doc = colecao.find_one()
    if doc and "media_proficiencia" in doc:
        media = doc["media_proficiencia"]
        resultado = db["saeb_2001_resumo"].update_one(
            {"regiao": regiao},
            {"$set": {"matematica_media": media}}
        )
        print(f"✅ Atualizado {regiao}: média = {media} | {resultado.modified_count} doc(s) modificados.")
    else:
        print(f"⚠️ Nenhum dado encontrado para {regiao} ou campo 'media_proficiencia' ausente.")

client.close()

