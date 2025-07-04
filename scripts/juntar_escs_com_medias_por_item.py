from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "j")untar_escs_com_medias_por_item.py

import pandas as pd
from pymongo import MongoClient

# === Caminhos e conexões ===
CAMINHO_MEDIAS_ITEM = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_por_pais_por_item_pisa2022.csv"
CAMINHO_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_pais_item_escs_2022.csv"

# Conecta ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_escs = db["pisa_ocde_2022_escs_media"]

# === Carrega CSV de médias por item ===
print("📥 Lendo arquivo de médias por item...")
df_medias = pd.read_csv(CAMINHO_MEDIAS_ITEM)

# === Carrega ESCS médio por país do MongoDB ===
print("🌐 Carregando dados ESCS do MongoDB...")
dados_escs = list(colecao_escs.find({}, {"_id": 0}))
df_escs = pd.DataFrame(dados_escs)

# === Mescla os dados ===
print("🔗 Juntando as bases...")
df_final = df_escs.merge(df_medias, left_on="codigo", right_on="pais", how="inner")
df_final.drop(columns=["pais_y"], inplace=True)
df_final.rename(columns={"pais_x": "pais"}, inplace=True)

# === Salva resultado ===
df_final.to_csv(CAMINHO_SAIDA, index=False)
print(f"✅ Arquivo final salvo em: {CAMINHO_SAIDA}")

