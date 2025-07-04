from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# importar_agregados_saeb_2023_tmap.py

import pandas as pd
import json
from pymongo import MongoClient

CAMINHO_SAEB = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ALUNO_9EF.csv"
CAMINHO_JSON_CODIGOS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "t")map_id_municipio_2023_ibge.json"
NOME_COLECAO = "saeb_2023_tmap"

print("📥 Lendo microdados do SAEB 2023 (9º ano EF)...")
df = pd.read_csv(CAMINHO_SAEB, sep=";", encoding="latin1", low_memory=False)
df["ID_MUNICIPIO"] = df["ID_MUNICIPIO"].astype(str)

print("📥 Lendo lista de municípios TMAP...")
with open(CAMINHO_JSON_CODIGOS, "r", encoding="utf-8") as f:
    lista = json.load(f)

codigos_tmap = [str(item["codigo_ibge"]) for item in lista]

print(f"🔎 Filtrando {len(codigos_tmap)} municípios da mesorregião TMAP (ID_MUNICIPIO)...")
df_tmap = df[df["ID_MUNICIPIO"].isin(codigos_tmap)]

print("🧹 Substituindo NaNs por None...")
df_tmap = df_tmap.where(pd.notnull(df_tmap), None)

print("📦 Convertendo para dicionários...")
dados = df_tmap.to_dict(orient="records")

print(f"🧨 Limpando coleção antiga ({NOME_COLECAO}) se existir...")
cliente = conectar_mongo(nome_banco="saeb")[1]
db = cliente["saeb"]
db[NOME_COLECAO].drop()

if dados:
    print(f"🚀 Inserindo {len(dados)} documentos na coleção '{NOME_COLECAO}'...")
    db[NOME_COLECAO].insert_many(dados)
    print("✅ Importação finalizada com sucesso.")
else:
    print("⚠️ Nenhum documento encontrado para inserção. Verifique os dados.")

cliente.close()

