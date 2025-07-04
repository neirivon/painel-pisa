from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# importar_agregados_saeb_2021_tmap.py

import pandas as pd
from pymongo import MongoClient

# === Caminho para o arquivo Excel de municípios do SAEB 2021 ===
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(1, "m")icrodados_saeb_2021_ensino_fundamental_e_medios.path.join(o, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_MUNICIPIO.xlsx"
NOME_COLECAO = "saeb_2021_tmap"

# === Códigos IBGE dos 74 municípios da mesorregião TMAP ===
CODIGOS_TMAP = [
    3100104, 3100203, 3100302, 3100500, 3100708, 3100906, 3101508, 3101607,
    3101706, 3101904, 3102001, 3102100, 3102209, 3102308, 3102407, 3102506,
    3102803, 3103108, 3103207, 3103306, 3103504, 3103702, 3103801, 3103900,
    3104007, 3104205, 3104403, 3104601, 3104908, 3105004, 3105103, 3105301,
    3105509, 3105608, 3105905, 3106002, 3106101, 3106200, 3106507, 3106655,
    3106705, 3106804, 3107000, 3107109, 3107307, 3107406, 3107604, 3107802,
    3108008, 3108107, 3108404, 3108503, 3108602, 3108909, 3109006, 3109105,
    3109204, 3109253, 3109303, 3109451, 3109600, 3109709, 3109907, 3110004,
    3110103, 3110202, 3110301, 3110400, 3110509, 3110608, 3110707, 3110806,
    3110905, 3111002
]

# === Leitura do arquivo Excel ===
print("📥 Lendo arquivo Excel...")
df = pd.read_excel(CAMINHO_ARQUIVO)

# === Filtragem da mesorregião TMAP ===
print("🔎 Filtrando 74 municípios da mesorregião TMAP...")
df_tmap = df[df["CO_MUNICIPIO"].isin(CODIGOS_TMAP)]

# === Substituir NaN por None para compatibilidade com MongoDB ===
print("🧹 Substituindo NaNs por None...")
df_tmap = df_tmap.where(pd.notnull(df_tmap), None)

# === Converter para dicionários ===
print("📦 Convertendo para dicionários...")
dados = df_tmap.to_dict(orient="records")

# === Inserção no MongoDB ===
cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]

print(f"🧨 Limpando coleção antiga ({NOME_COLECAO}) se existir...")
db[NOME_COLECAO].drop()

print(f"🚀 Inserindo {len(dados)} documentos na coleção '{NOME_COLECAO}'...")
db[NOME_COLECAO].insert_many(dados)

print("✅ Importação dos dados TMAP 2021 finalizada com sucesso.")
cliente.close()

