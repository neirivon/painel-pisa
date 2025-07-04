from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
import os
from pymongo import MongoClient

CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")017_201os.path.join(9, "m")icrodados_saeb_201os.path.join(9, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_UF.xlsx"
NOME_COLECAO = "saeb_2019_uf"

cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]

print("📥 Lendo arquivo Excel...")
df = pd.read_excel(CAMINHO_ARQUIVO)

print("🧹 Substituindo NaNs por None...")
df = df.where(pd.notnull(df), None)

print("📦 Convertendo para dicionários...")
dados = df.to_dict(orient="records")

print(f"🧨 Limpando coleção antiga ({NOME_COLECAO}) se existir...")
db[NOME_COLECAO].drop()

print(f"🚀 Inserindo {len(dados)} documentos na coleção '{NOME_COLECAO}'...")
db[NOME_COLECAO].insert_many(dados)

print("✅ Importação finalizada com sucesso.")
cliente.close()

