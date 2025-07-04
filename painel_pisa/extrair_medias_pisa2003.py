from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# utilos.path.join(s, "e")xtrair_medias_pisa2003.py

import pymongo
import pandas as pd
from pymongo import MongoClient

# === Conexão ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["cy1mdai_stu_qqq"]  # Alunos de 2003

# === Carregar e filtrar ===
cursor = colecao.find({}, {
    "_id": 0,
    "CNT": 1,
    "PV1READ": 1,
    "PV1MATH": 1,
    "PV1SCIE": 1
})
df = pd.DataFrame(list(cursor)).dropna()

# === Calcular médias por país ===
df_medias = df.groupby("CNT")[["PV1READ", "PV1MATH", "PV1SCIE"]].mean().reset_index()
df_medias.columns = ["País", "Leitura", "Matemática", "Ciências"]

# === Mostrar na tela ===
print(df_medias.head())

# (Opcional) salvar como nova coleção
# db["pisa_2003_medias_oficiais"].delete_many({})
# db["pisa_2003_medias_oficiais"].insert_many(df_medias.to_dict("records"))

# (Opcional) exportar para CSV
# df_medias.to_csv("pisa_2003_medias_por_pais.csv", index=False)

