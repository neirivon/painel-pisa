from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# importar_agregados_saeb_2023_mg.py

import pandas as pd
from pymongo import MongoClient

CAMINHO_ARQUIVO = (
    "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"
)
CODIGO_MG = 31  # ID_UF para Minas Gerais
NOME_COLECAO = "saeb_2023_mg"

print("📥 Lendo microdados do SAEB 2023 (9º ano EF)...")
df = pd.read_csv(CAMINHO_ARQUIVO, sep=";", encoding="latin1")

print("🔎 Filtrando apenas alunos de Minas Gerais (ID_UF == 31)...")
df_mg = df[df["ID_UF"] == CODIGO_MG]

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

print("✅ Importação dos dados de Minas Gerais (SAEB 2023) finalizada com sucesso.")

