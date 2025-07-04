import pymongo

# Configuração MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_ANALISE = "relatorios_inep_pisa_bloom"
COLLECTION_MEDIAS = "pisa_2000_medias"

# Função melhorada para detectar a área
def detectar_area(texto):
    texto = texto.lower()

    # Palavras relacionadas a Leitura
    palavras_leitura = ["leitura", "ler", "interpretação", "texto", "compreensão", "compreender"]
    if any(p in texto for p in palavras_leitura):
        return "leitura"

    # Palavras relacionadas a Matemática
    palavras_matematica = ["matemática", "matematica", "problema", "cálculo", "calculo", "equação", "número", "quantitativo"]
    if any(p in texto for p in palavras_matematica):
        return "matematica"

    # Palavras relacionadas a Ciências
    palavras_ciencias = ["ciência", "ciências", "natureza", "experimento", "científico", "cientifica", "biologia", "física", "química"]
    if any(p in texto for p in palavras_ciencias):
        return "ciencias"

    return None

# Função para definir a triangulação
def definir_triangulacao(media_brasil, media_ocde):
    if media_brasil is None or media_ocde is None:
        return "inconclusivo"
    if media_brasil < (media_ocde - 20):
        return "confirma"
    elif media_brasil > (media_ocde + 20):
        return "diverge"
    else:
        return "inconclusivo"

# Função principal
def triangular():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]

    docs = list(db[COLLECTION_ANALISE].find({"ano": 2000}))
    medias_docs = list(db[COLLECTION_MEDIAS].find({"ano": 2000, "pais": "BRA"}))

    mapa_medias = {}
    if medias_docs:
        areas_brasil = medias_docs[0]["areas"]
        mapa_medias = {
            "leitura": areas_brasil.get("leitura", {}).get("media"),
            "matematica": areas_brasil.get("matematica", {}).get("media"),
            "ciencias": areas_brasil.get("ciencias", {}).get("media")
        }

    total_triangulado = 0

    for doc in docs:
        area_detectada = detectar_area(doc["texto"])
        if area_detectada:
            media_brasil = mapa_medias.get(area_detectada.lower(), None)
            media_ocde = 500  # Definido no PISA 2000
            triangulacao = definir_triangulacao(media_brasil, media_ocde)

            db[COLLECTION_ANALISE].update_one(
                {"_id": doc["_id"]},
                {"$set": {
                    "area_pisa_relacionada": area_detectada.title(),
                    "media_brasil": media_brasil,
                    "media_ocde": 500,
                    "triangulacao": triangulacao
                }}
            )
            total_triangulado += 1

    client.close()
    print(f"✅ Triangulação concluída! {total_triangulado} documentos atualizados.")

if __name__ == "__main__":
    print("🚀 Iniciando triangulação com análise melhorada...")
    triangular()

