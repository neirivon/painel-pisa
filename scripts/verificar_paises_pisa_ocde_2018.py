from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient
import pandas as pd

client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2018"]

# Amostra de documentos para inferir possíveis campos com país
amostra = list(colecao.find().limit(1000))

# Candidatos a colunas de país
colunas_possiveis = {"PAIS", "Pais", "País", "COUNTRY", "Country", "CNT", "CNTISO", "NOME", "Nation"}

# Conjunto final de países encontrados
paises = set()

for doc in amostra:
    for chave, valor in doc.items():
        if chave in colunas_possiveis and isinstance(valor, str) and len(valor) <= 50:
            paises.add(valor.strip())

# Resultado final
print(f"🌍 Número total de países encontrados: {len(paises)}")
print("📋 Lista de países encontrados:")
print(sorted(paises))

client.close()

