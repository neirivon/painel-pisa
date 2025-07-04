from pymongo import MongoClient
import json
import os

CAMINHO_ALUNO = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/rubrica_sinapse_pedagogica_aluno.json"
CAMINHO_PROF = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/rubrica_sinapse_pedagogica_professor.json"

MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
NOME_BANCO = "rubricas"
NOME_COLECAO = "rubricas_pedagogicas"

def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def inserir_mongodb(documento):
    client = MongoClient(MONGO_URI)
    db = client[NOME_BANCO]
    colecao = db[NOME_COLECAO]
    filtro = {
        "nome": documento["nome"],
        "versao": documento["versao"],
        "publico": documento["publico"]
    }
    colecao.replace_one(filtro, documento, upsert=True)
    client.close()
    print(f"✅ Inserido no MongoDB: {documento['nome']} ({documento['publico']})")

if __name__ == "__main__":
    doc_aluno = carregar_json(CAMINHO_ALUNO)
    doc_prof = carregar_json(CAMINHO_PROF)
    inserir_mongodb(doc_aluno)
    inserir_mongodb(doc_prof)

