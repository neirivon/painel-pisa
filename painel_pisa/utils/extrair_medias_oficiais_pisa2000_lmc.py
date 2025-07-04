from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# utilos.path.join(s, "e")xtrair_medias_oficiais_pisa2000_lmc.py

from pymongo import MongoClient

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa2000_comparativo_lmc"]

# Dados a serem inseridos
dados = [
    {"area": "Leitura", "tipo": "geral", "nota_brasil": 422, "nota_ocde": 500, "ano": 2000},
    {"area": "Leitura", "tipo": "publica", "nota_brasil": 385, "nota_ocde": 491, "ano": 2000},
    {"area": "Matemática", "tipo": "geral", "nota_brasil": 334, "nota_ocde": 500, "ano": 2000},
    {"area": "Matemática", "tipo": "publica", "nota_brasil": 322, "nota_ocde": 488, "ano": 2000},
    {"area": "Ciências", "tipo": "geral", "nota_brasil": 390, "nota_ocde": 500, "ano": 2000},
    {"area": "Ciências", "tipo": "publica", "nota_brasil": 366, "nota_ocde": 493, "ano": 2000},
]

# Limpar antes de inserir
colecao.delete_many({})
colecao.insert_many(dados)
client.close()
print("✅ Dados inseridos com sucesso no MongoDB (com campo 'ano')!")

