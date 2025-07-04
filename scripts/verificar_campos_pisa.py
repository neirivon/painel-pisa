# scripts/verificar_campos_pisa.py

from pymongo import MongoClient
import pandas as pd

MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
client = MongoClient(MONGO_URI)

banco = "pisa"
colecoes = client[banco].list_collection_names()
dados = []

for nome_col in colecoes:
    doc = client[banco][nome_col].find_one()
    if doc:
        for campo in doc.keys():
            dados.append((nome_col, campo))

df = pd.DataFrame(dados, columns=["Coleção", "Campo"])
df.to_csv("dados_processados/estrutura_campos_banco_pisa.csv", index=False)

client.close()
print("✔️ Estrutura salva em: dados_processados/estrutura_campos_banco_pisa.csv")

