from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# verificar_codigos_escs.py

from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]

docs = list(db["pisa_ocde_2022_escs_media"].find({}, {"_id": 0, "codigo": 1}))
codigos_escs = sorted({doc["codigo"] for doc in docs})
print(f"\n✅ Códigos ESCS (total: {len(codigos_escs)}):")
print(codigos_escs)

client.close()

