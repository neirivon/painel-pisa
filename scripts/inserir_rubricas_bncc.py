from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_rubricas_bncc.py

import json
from pymongo import MongoClient
import os

# Caminho absoluto do JSON
CAMINHO_JSON = os.path.join(
    os.path.dirname(__file__),
    ".os.path.join(., "p")ainel_pisos.path.join(a, "u")tilos.path.join(s, "d")ados_clouos.path.join(d, "r")ubricaos.path.join(s, "r")ubricas_bncc_9ano.json"
)

# Conexão direta com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["bncc_9ano"]

try:
    # Limpa a coleção antes de inserir os novos dados
    colecao.delete_many({})

    # Carrega o conteúdo do JSON
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Insere os documentos na coleção
    resultado = colecao.insert_many(dados)
    print(f"✅ {len(resultado.inserted_ids)} documentos inseridos com sucesso na coleção 'bncc_9ano' do banco 'rubricas'.")

finally:
    client.close()

