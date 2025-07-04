from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")

# Procura em todos os bancos onde está a coleção com nome exato
for nome_banco in client.list_database_names():
    db = client[nome_banco]
    if "medias_pais_item_escs_2022" in db.list_collection_names():
        print(f"✔️ Encontrado: Banco '{nome_banco}' → Coleção 'medias_pais_item_escs_2022'")

client.close()  # ✅ Fecha a conexão com o MongoDB corretamente

