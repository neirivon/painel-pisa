from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
collection = db["relatorio_inep_pisa_2000_analise_v2"]

# Carrega todos os documentos, excluindo o campo _id
docs = list(collection.find({}, {"_id": 0}))

# Cria DataFrame
df = pd.DataFrame(docs)

# Mostra as colunas disponíveis
print(df.columns.tolist())

# Mostra os primeiros registros para ver a estrutura
print(df.head())

