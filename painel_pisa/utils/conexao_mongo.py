# utils/conexao_mongo.py

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import pandas as pd
import os

from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.paths import LOGOS_DIR

# ✅ Caminho completo para o logo (caso seja reutilizado)
logo_path = os.path.join(LOGOS_DIR, "IFTM_360.png")

def conectar_mongo(uri=None, nome_banco=None):
    """
    Conecta ao MongoDB com URI autenticada e retorna o banco e o client.
    """
    try:
        uri = uri or CONFIG.get("MONGO_URI")
        nome_banco = nome_banco or CONFIG.get("MONGO_BANCO", "pisa")
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")  # Testa conexão
        db = client[nome_banco]
        return db, client
    except Exception as e:
        raise ConnectionError(f"❌ Erro ao conectar ao MongoDB: {e}")

def salvar_mongodb(dados, nome_colecao, nome_banco="pisa", uri=None):
    """
    Salva dados (lista de dicionários ou DataFrame) em uma coleção MongoDB.
    """
    if isinstance(dados, pd.DataFrame):
        dados = dados.to_dict(orient="records")

    if not isinstance(dados, list):
        raise ValueError("❌ Os dados devem ser uma lista de dicionários ou DataFrame.")

    db, client = conectar_mongo(uri=uri, nome_banco=nome_banco)
    try:
        colecao = db[nome_colecao]
        if dados:
            colecao.insert_many(dados)
            print(f"✅ {len(dados)} documentos inseridos em '{nome_colecao}'.")
        else:
            print("⚠️ Nenhum dado para inserir.")
    except BulkWriteError as bwe:
        print("❌ Erro de inserção em massa:", bwe.details)
    finally:
        client.close()

