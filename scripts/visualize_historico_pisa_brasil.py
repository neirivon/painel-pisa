from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]
col = db["historico_pisa_brasil"]
df = pd.DataFrame(list(col.find({}, {"_id": 0})))

print(df.columns.tolist())
client.close()

