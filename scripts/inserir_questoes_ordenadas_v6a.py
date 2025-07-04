from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import json
from pymongo import MongoClient

# Caminho do arquivo JSON
json_path = "dados_processadoos.path.join(s, "q")uestoeos.path.join(s, "q")uestoes_pisa_ordenadas_v6a.json"

try:
    with open(json_path, "r", encoding="utf-8") as f:
        questoes = json.load(f)

    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["rubricas"]
    colecao = db["questoes_ordenadas_v6a"]

    colecao.delete_many({})  # Limpar antes de inserir
    resultado = colecao.insert_many(questoes)
    print(f"✅ {len(resultado.inserted_ids)} questões inseridas com sucesso na coleção 'rubricas.questoes_ordenadas_v6a'.")

    client.close()  # ✅ Fecha corretamente o MongoClient

except Exception as e:
    print(f"❌ Erro ao inserir questões: {e}")

