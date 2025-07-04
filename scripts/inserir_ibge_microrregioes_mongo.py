from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_ibge_microrregioes_mongo.py

import pandas as pd
from pymongo import MongoClient

# Caminho do arquivo CSV
CAMINHO_CSV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")utputs_tmaos.path.join(p, "i")bge_microrregioes_geometry.csv"

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["ibge_microrregioes_geometry"]

# Ler CSV
df = pd.read_csv(CAMINHO_CSV)

# Converter DataFrame em dicionário
documentos = df.to_dict(orient="records")

# Inserir no MongoDB (remove antes se já existir)
colecao.drop()
colecao.insert_many(documentos)

client.close()
print(f"✅ {len(documentos)} documentos inseridos com sucesso na coleção 'ibge_microrregioes_geometry'.")

