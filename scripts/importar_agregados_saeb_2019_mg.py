from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# importar_agregados_saeb_2019_mg.py

import pandas as pd
from pymongo import MongoClient

CAMINHO_ARQUIVO = (
    "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")017_2019/"
    "microdados_saeb_201os.path.join(9, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_UF.xlsx"
)
CODIGO_MG = 31
NOME_COLECAO = "saeb_2019_mg"

print("📥 Lendo arquivo Excel...")
df = pd.read_excel(CAMINHO_ARQUIVO)

print("🔎 Filtrando estado de Minas Gerais (CO_UF == 31)...")
df_mg = df[df["CO_UF"] == CODIGO_MG]

print("🧹 Substituindo NaNs por None...")
df_mg = df_mg.where(pd.notnull(df_mg), None)

print("📦 Convertendo para dicionários...")
dados = df_mg.to_dict(orient="records")

print(f"🧨 Limpando coleção antiga ({NOME_COLECAO}) se existir...")
cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]
db[NOME_COLECAO].drop()

print(f"🚀 Inserindo {len(dados)} documentos na coleção '{NOME_COLECAO}'...")
db[NOME_COLECAO].insert_many(dados)
cliente.close()

print("✅ Importação dos dados de Minas Gerais (SAEB 2019) finalizada com sucesso.")

