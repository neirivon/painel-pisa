from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# verificar_integridade_ibge_geometry.py

from pymongo import MongoClient
from collections import Counter

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
collection = db["ibge_microrregioes_geometry"]

# 1️⃣ Verificar registros com geometry ausente ou vazio
faltantes = list(collection.find(
    { "$or": [ { "geometry": { "$exists": False } }, { "geometry": "" } ] },
    { "_id": 0, "NM_MICRO": 1, "SIGLA_UF": 1 }
))

print("🔍 Verificação de registros com geometry ausente ou vazio:")
if faltantes:
    for doc in faltantes:
        print(f"❌ {doc['NM_MICRO']} - {doc['SIGLA_UF']}")
else:
    print("✅ Todos os documentos possuem geometry válido.\n")

# 2️⃣ Verificar duplicatas por NM_MICRO + SIGLA_UF
todos = list(collection.find({}, { "_id": 0, "NM_MICRO": 1, "SIGLA_UF": 1 }))
chaves = [ (d["NM_MICRO"], d["SIGLA_UF"]) for d in todos ]
contador = Counter(chaves)
duplicatas = [ key for key, count in contador.items() if count > 1 ]

print("🔁 Verificação de microrregiões duplicadas:")
if duplicatas:
    for micro, uf in duplicatas:
        print(f"⚠️ Duplicado: {micro} - {uf}")
else:
    print("✅ Nenhuma duplicata encontrada.\n")

# Encerrar conexão
client.close()

