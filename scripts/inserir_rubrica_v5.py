# ~/SINAPSE2.0/PISA/scripts/inserir_rubrica_v5.py

import json
import os
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

CAMINHO_JSON = "/home/neirivon/Área de Trabalho/RUBRICAS/rubrica_sinapse_ia_v5_reconstruido.json"

try:
    # Conexão com o MongoDB
    client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
    db = client["rubricas"]
    colecao = db["rubrica_sinapse_ia"]

    # Atualizar rubricas v1.4 para inativa
    resultado_update = colecao.update_many(
        {"versao": "v1.4", "status": "ativa"},
        {"$set": {"status": "inativa"}}
    )
    print(f"✔️ Rubricas v1.4 atualizadas para inativa: {resultado_update.modified_count}")

    # Carregar novo JSON (v1.5)
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Garantir que está em formato de objeto único
    if not isinstance(dados, dict):
        raise ValueError("❌ JSON inválido: o conteúdo deve ser um objeto (não lista).")

    # Remover _id se existir para evitar conflito no insert
    dados.pop("_id", None)

    # Garantir campos obrigatórios
    dados.setdefault("timestamp", datetime.utcnow().isoformat())
    dados.setdefault("versao", "v1.5")
    dados.setdefault("status", "ativa")

    resultado = colecao.insert_one(dados)
    print(f"✅ Rubrica v1.5 inserida com _id: {resultado.inserted_id}")

except Exception as e:
    print(f"❌ Erro geral: {e}")

finally:
    client.close()

