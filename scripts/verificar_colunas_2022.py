import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
df = pd.DataFrame(list(client["pisa"]["historico_pisa_brasil"].find({}, {"_id": 0})))
df_2022 = df[df["Ano"] == 2022]
print(df_2022["Variavel"].unique())
client.close()
