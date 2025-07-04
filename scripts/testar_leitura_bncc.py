from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "t")estar_leitura_bncc.py

import sys
import os
import json
from pymongo import MongoClient

# 🔗 Conexão direta com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["bncc_9ano"]

print("\n📚 Rubricas da BNCC - 9º ano (coleção 'bncc_9ano'):\n")

# 📤 Exibe cada rubrica formatada
for doc in colecao.find({}, {"_id": 0}):  # Exclui o _id da visualização
    print(json.dumps(doc, indent=2, ensure_ascii=False))
    print("-" * 80)

# 🔒 Fecha a conexão com segurança
client.close()

