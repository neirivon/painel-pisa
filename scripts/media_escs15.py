from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
import numpy as np
from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
col = client.pisa.pisa_pfd_alunos

df = pd.DataFrame(list(col.find({}, {"ESCS15": 1, "_id": 0})))
df_clean = df[np.isfinite(df["ESCS15"])]

print("✅ Média ESCS15:", df_clean["ESCS15"].mean())
client.close()
