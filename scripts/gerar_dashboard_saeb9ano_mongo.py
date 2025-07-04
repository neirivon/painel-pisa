from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# 🔹 gerar_dashboard_saeb9ano_mongo.py

import pandas as pd
from pymongo import MongoClient

# Caminho para o Excel do SAEB 2021 (9º ano)
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(1, "m")icrodados_saeb_2021_ensino_fundamental_e_medios.path.join(o, "P")LANILHAS DE RESULTADOos.path.join(S, "T")S_MUNICIPIO.xlsx"

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_9ano"]

# Leitura e filtragem
df = pd.read_excel(CAMINHO_ARQUIVO)
df = df[(df["DEPENDENCIA_ADM"] == "Total - Federal, Estadual, Municipal e Privada") & 
        (df["LOCALIZACAO"] == "Total")]

df_filtrado = df[[
    "CO_UF", "NO_UF", "CO_MUNICIPIO", "NO_MUNICIPIO",
    "MEDIA_9_LP", "MEDIA_9_MT"
]].dropna()

df_filtrado["nota_geral"] = df_filtrado[["MEDIA_9_LP", "MEDIA_9_MT"]].mean(axis=1)

# Inserção no MongoDB
colecao.delete_many({})
colecao.insert_many(df_filtrado.to_dict(orient="records"))
client.close()

print("✅ Dados do 9º ano inseridos com sucesso no MongoDB (coleção: saeb_2021_municipios_9ano)")

