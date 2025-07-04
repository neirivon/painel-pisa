import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
cliente = MongoClient(MONGO_URI)
db = cliente["pisa"]
col = db["historico_pisa_brasil"]

# Carrega apenas o ano 2022 e Brasil
dados = list(col.find({"Ano": 2022, "Pais": {"$in": ["Brazil", "BR", "Brasil"]}}, {"_id": 0}))
df_2022 = pd.DataFrame(dados)

# Mostra os nomes das variáveis encontradas
print("📌 Variáveis encontradas no ano 2022:")
print(df_2022["Variavel"].unique())

cliente.close()

