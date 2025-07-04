import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
colecao = db["historico_pisa_brasil"]

# Carregar todos os dados
df = pd.DataFrame(list(colecao.find({}, {"_id": 0})))

# Mostrar países únicos especificamente no ano 2022
df_2022 = df[df["Ano"] == 2022]
paises_2022 = df_2022["Pais"].dropna().unique()

print("🌎 Países no ano 2022 encontrados na base:")
print(paises_2022)

client.close()

