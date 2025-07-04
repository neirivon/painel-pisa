from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
collection = db["pisa_2022"]

pipeline = [
    {"$match": {"CNT": "BRA", "AGE": 15}},
    {"$group": {"_id": "$ST003D01T", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}}
]

resultado = list(collection.aggregate(pipeline))
client.close()

df = pd.DataFrame(resultado)
df.columns = ['Ano Escolar', 'Total']
df['Ano Escolar'] = df['Ano Escolar'].fillna("Não informado")

print(df)

