from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_correcoes_microrregioes_ibge_normalizado.py

from pymongo import MongoClient
import unicodedata
import re

# Função para remover acentuação
def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower()

# Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["ibge"]
collection = db["ibge_microrregioes_geometry"]

# Correções desejadas
correcoes = [
    {
        "nome_correcao": "Litoral de Camocim e Acaraú",
        "equivalentes": ["acaraú", "camocim"]
    },
    {
        "nome_correcao": "Sertão de Cratéus",
        "equivalentes": ["sertão de crateús", "sertão de crateus"]
    },
    {
        "nome_correcao": "União dos Palmares",
        "equivalentes": ["união dos palmares"]
    },
    {
        "nome_correcao": "Baixada Maranhense",
        "equivalentes": ["viana"]
    }
]

# Percorrer documentos e aplicar correções baseadas na equivalência
atualizados = 0
docs = list(collection.find({}))
for correcao in correcoes:
    nome_correcao = correcao["nome_correcao"]
    nomes_equivalentes = [normalizar(n) for n in correcao["equivalentes"]]

    for doc in docs:
        nome_microrregiao = doc.get("NM_MICRO", "")
        if normalizar(nome_microrregiao) in nomes_equivalentes:
            resultado = collection.update_one(
                { "_id": doc["_id"] },
                { "$set": { "NM_MICRO": nome_correcao } }
            )
            if resultado.modified_count > 0:
                print(f"✅ Atualizado: {nome_microrregiao} → {nome_correcao}")
                atualizados += 1

client.close()
print(f"\n🔁 Total de registros atualizados com sucesso: {atualizados}")

