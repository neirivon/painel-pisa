# scripts/copiar_colecoes_saeb_para_pisa.py

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# Conexão com autenticação
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
client = MongoClient(MONGO_URI)

db_origem = client["saeb"]
db_destino = client["pisa"]

# Filtrar coleções desejadas
colecoes = db_origem.list_collection_names()
colecoes_relevantes = [c for c in colecoes if c.startswith("saeb_") or c.startswith("escala_saeb_")]

print("🔁 Copiando coleções grandes por lotes...\n")

for nome_colecao in colecoes_relevantes:
    nova_colecao = nome_colecao
    print(f"➡️ Copiando: {nome_colecao} → {nova_colecao}")

    origem = db_origem[nome_colecao]
    destino = db_destino[nova_colecao]
    destino.drop()  # Apaga a coleção destino se já existir

    batch_size = 1000
    batch = []
    total_inseridos = 0

    try:
        cursor = origem.find({}, no_cursor_timeout=True).batch_size(batch_size)
        for doc in cursor:
            batch.append(doc)
            if len(batch) >= batch_size:
                destino.insert_many(batch)
                total_inseridos += len(batch)
                print(f"   ✔ {total_inseridos} documentos inseridos...")
                batch = []

        if batch:
            destino.insert_many(batch)
            total_inseridos += len(batch)
            print(f"   ✔ {total_inseridos} documentos inseridos no total.")

        cursor.close()
    except BulkWriteError as bwe:
        print(f"❌ Erro de inserção em lote: {bwe.details}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

print("\n✅ Cópia por lote finalizada com sucesso.")
client.close()

