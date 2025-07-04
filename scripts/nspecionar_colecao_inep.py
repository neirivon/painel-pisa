# inspecionar_colecao_inep.py

import pymongo
from collections import Counter

# Configuração do MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = "relatorios_inep_pisa_bloom_nova"

def inspecionar_colecao():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    total_documentos = collection.count_documents({})
    print(f"\n🔎 Total de documentos encontrados: {total_documentos}\n")

    # Conferir se todos possuem os campos esperados
    campos_esperados = {"ano", "texto", "nivel_bloom", "confianca", "rubrica", "area_pisa_relacionada", "media_brasil", "media_ocde", "triangulacao"}
    problemas = []
    
    niveis_detectados = Counter()
    status_triangulacao = Counter()

    for doc in collection.find():
        campos_doc = set(doc.keys())
        if not campos_esperados.issubset(campos_doc):
            problemas.append(doc.get("_id"))

        niveis_detectados[doc.get("nivel_bloom", "Indefinido")] += 1
        status_triangulacao[doc.get("triangulacao", "Indefinido")] += 1

    if problemas:
        print(f"❌ Documentos com campos faltando: {problemas}")
    else:
        print("✅ Todos os documentos possuem os campos esperados!")

    print("\n📚 Distribuição dos Níveis da Taxonomia de Bloom:")
    for nivel, count in niveis_detectados.items():
        print(f"- {nivel}: {count} documentos")

    print("\n📚 Status de Triangulação:")
    for status, count in status_triangulacao.items():
        print(f"- {status}: {count} documentos")

    client.close()

if __name__ == "__main__":
    print("🚀 Inspecionando a coleção relatorios_inep_pisa_bloom_nova...")
    inspecionar_colecao()

