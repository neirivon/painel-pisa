from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_questoes_pisa_ordenadas.py

import json
import os
from pymongo import MongoClient

try:
    print("🔄 Conectando ao MongoDB...")

    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["rubricas"]
    colecao = db["questoes_ordenadas_v6a"]

    # Caminho do arquivo JSON
    caminho_json = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "d")ados_processadoos.path.join(s, "q")uestoeos.path.join(s, "q")uestoes_pisa_ordenadas.json"))

    if not os.path.exists(caminho_json):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_json}")

    # Carregar e inserir
    with open(caminho_json, "r", encoding="utf-8") as f:
        questoes = json.load(f)

    if not isinstance(questoes, list):
        raise ValueError("O JSON deve conter uma lista de questões.")

    # Limpa a coleção anterior (opcional)
    colecao.delete_many({})

    # Insere as novas questões
    result = colecao.insert_many(questoes)
    print(f"✅ {len(result.inserted_ids)} questões inseridas com sucesso na coleção 'rubricas.questoes_ordenadas_v6a'.")

except Exception as e:
    print("❌ Erro ao inserir no MongoDB:")
    print(e)
finally:
    client.close()

