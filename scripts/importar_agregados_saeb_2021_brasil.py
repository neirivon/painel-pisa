from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# importar_agregados_saeb_2021_brasil.py

import pandas as pd
from pymongo import MongoClient

CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(1, "m")icrodados_saeb_2021_ensino_fundamental_e_medios.path.join(o, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_BRASIL.xlsx"
NOME_COLECAO = "saeb_2021_brasil"

print("📥 Lendo arquivo Excel...")
df = pd.read_excel(CAMINHO_ARQUIVO)

print("🧹 Substituindo NaNs por None...")
df = df.where(pd.notnull(df), None)

print("📦 Convertendo para dicionários...")
dados = df.to_dict(orient="records")

print(f"🧨 Limpando coleção antiga ({NOME_COLECAO}) se existir...")
cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]
db[NOME_COLECAO].drop()

print(f"🚀 Inserindo {len(dados)} documentos na coleção '{NOME_COLECAO}'...")
db[NOME_COLECAO].insert_many(dados)
cliente.close()

print("✅ Importação dos dados do Brasil (SAEB 2021) finalizada com sucesso.")

