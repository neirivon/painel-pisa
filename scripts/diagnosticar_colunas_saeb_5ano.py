from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# diagnosticar_colunas_saeb_5ano.py

import pandas as pd
from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
collection = db["saeb_2021_municipios_5ano"]

# Buscar uma amostra pequena
df = pd.DataFrame(list(collection.find({}, {'_id': 0}).limit(5)))
client.close()

print("🔍 Colunas disponíveis na coleção saeb_2021_municipios_5ano:")
print(df.columns.tolist())

