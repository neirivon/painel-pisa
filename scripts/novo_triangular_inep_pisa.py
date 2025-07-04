# novo_triangular_inep_pisa.py
import pymongo

# Configuração do MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_RELATORIOS = "relatorios_inep_pisa_bloom_nova"
COLLECTION_MEDIAS = "pisa2000_medias_oficiais"

def triangular():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]

    try:
        relatorios = list(db[COLLECTION_RELATORIOS].find({}))
        medias = list(db[COLLECTION_MEDIAS].find({}))

        if not medias:
            print("❌ Não foram encontradas médias na coleção correta!")
            return

        # Criar mapa de médias por área
        mapa_medias = {}
        for doc in medias:
            area = doc.get("area")
            if area:
                mapa_medias[area.lower()] = {
                    "media_brasil": doc.get("media_brasil"),
                    "media_ocde": doc.get("media_ocde")
                }

        atualizados = 0

        for relatorio in relatorios:
            texto = relatorio.get("texto", "").lower()

            area_detectada = None
            if "ciência" in texto or "ciências" in texto:
                area_detectada = "ciencias"
            elif "matemática" in texto or "matematica" in texto:
                area_detectada = "matematica"
            elif "leitura" in texto:
                area_detectada = "leitura"

            if area_detectada and area_detectada in mapa_medias:
                update_fields = {
                    "area_pisa_relacionada": area_detectada.capitalize(),
                    "media_brasil": mapa_medias[area_detectada]["media_brasil"],
                    "media_ocde": mapa_medias[area_detectada]["media_ocde"],
                    "triangulacao": "confirma"
                }

                db[COLLECTION_RELATORIOS].update_one(
                    {"_id": relatorio["_id"]},
                    {"$set": update_fields}
                )
                atualizados += 1

        print(f"✅ Triangulação concluída! {atualizados} documentos atualizados.")

    finally:
        client.close()

if __name__ == "__main__":
    print("🚀 Iniciando triangulação correta baseada no banco do PISA...")
    triangular()

