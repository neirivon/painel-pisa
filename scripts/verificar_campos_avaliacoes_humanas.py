from pymongo import MongoClient
import pandas as pd

# Conectar ao MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["avaliacoes_humanas"]

# Buscar os primeiros documentos
documentos = list(colecao.find().limit(5))

# Transformar em DataFrame
df = pd.DataFrame(documentos)

# Mostrar colunas e amostra
print("📌 Colunas disponíveis:", df.columns.tolist())
print("\n📊 Amostra de dados:")
print(df[["juiz", "dimensao", "nota"]].head())

client.close()

