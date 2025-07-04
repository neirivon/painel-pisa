from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]

# Quais países existem na coleção 'cy1mdai_stu_qqq'?
paises = db.cy1mdai_stu_qqq.distinct("CNT")
print(f"Número de países encontrados: {len(paises)}")
print(f"Lista de países encontrados: {paises}")
