from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")mportar_agregados_saeb_2019_tmap.py

import pandas as pd
from pymongo import MongoClient

CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")017_201os.path.join(9, "m")icrodados_saeb_201os.path.join(9, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_MUNICIPIO.xlsx"

# Códigos dos 74 municípios da mesorregião TMAP
CODIGOS_TMAP = [
    3100104, 3100203, 3100708, 3100906, 3101508, 3102100, 3102407, 3102803, 3103405, 3104007,
    3104304, 3105103, 3105301, 3105400, 3106002, 3106606, 3107604, 3109006, 3109709, 3110004,
    3110152, 3110202, 3110707, 3110905, 3112307, 3113008, 3113107, 3113404, 3113701, 3114204,
    3115300, 3115409, 3116902, 3117009, 3117603, 3118304, 3118700, 3119500, 3119807, 3119906,
    3120102, 3120151, 3120201, 3120706, 3120805, 3120904, 3121100, 3121605, 3122009, 3122108,
    3122504, 3122702, 3122801, 3123205, 3123403, 3124104, 3124203, 3124401, 3124906, 3125200,
    3125408, 3125507, 3126208, 3126505, 3126901, 3127008, 3127107, 3127305, 3127909, 3128006,
    3128105, 3128303, 3128402, 3128709
]

print("📥 Lendo arquivo Excel...")
df = pd.read_excel(CAMINHO_ARQUIVO)

print("🔎 Filtrando 74 municípios da mesorregião TMAP...")
df_tmap = df[df["CO_MUNICIPIO"].isin(CODIGOS_TMAP)].copy()

print("🧹 Substituindo NaNs por None...")
df_tmap = df_tmap.where(pd.notnull(df_tmap), None)

print("📦 Convertendo para dicionários...")
dados = df_tmap.to_dict(orient="records")

print("🧨 Limpando coleção antiga (saeb_2019_tmap) se existir...")
cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]
db["saeb_2019_tmap"].drop()

print(f"🚀 Inserindo {len(dados)} documentos na coleção 'saeb_2019_tmap'...")
db["saeb_2019_tmap"].insert_many(dados)

cliente.close()
print("✅ Importação dos dados TMAP 2019 finalizada com sucesso.")

