import pandas as pd
from pymongo import MongoClient

# Caminho para o CSV com as avaliações humanas
csv_path = "dados_processados/avaliacoes_humanas_dirceu.csv"  # ajuste conforme seu caso

# Conectando ao MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["avaliacoes_humanas"]

# Lendo o CSV
df = pd.read_csv(csv_path)

# Verificando colunas obrigatórias
if not {"juiz", "dimensao", "nota"}.issubset(df.columns):
    raise ValueError("O CSV precisa conter as colunas: 'juiz', 'dimensao' e 'nota'.")

# Convertendo os dados para dicionário
documentos = df.to_dict(orient="records")

# Inserindo no MongoDB
if documentos:
    colecao.insert_many(documentos)
    print(f"✅ Inseridos {len(documentos)} documentos na coleção 'avaliacoes_humanas'.")
else:
    print("⚠️ Nenhum documento encontrado no CSV para inserir.")

client.close()

