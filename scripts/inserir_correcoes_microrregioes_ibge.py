from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_correcoes_microrregioes_ibge.py

from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
db = client["ibge"]
collection = db["ibge_microrregioes_geometry"]

correcoes = [
    {
        "nome_original": "Litoral de Camocim e Acaraú",
        "nomes_equivalentes": ["acaraú", "camocim"]
    },
    {
        "nome_original": "Sertão de Cratéus",
        "nomes_equivalentes": ["sertão de crateús", "sertão de crateus"]
    },
    {
        "nome_original": "União dos Palmares",
        "nomes_equivalentes": ["união dos palmares"]
    },
    {
        "nome_original": "Baixada Maranhense",
        "nomes_equivalentes": ["viana"]
    }
]

atualizados = 0
for correcao in correcoes:
    for nome in correcao["nomes_equivalentes"]:
        resultado = collection.update_many(
            { "NM_MICRO": nome },
            { "$set": { "NM_MICRO": correcao["nome_original"] } }
        )
        if resultado.modified_count > 0:
            print(f"✅ {nome} → {correcao['nome_original']} ({resultado.modified_count} registros)")
            atualizados += resultado.modified_count

client.close()
print(f"\n🔁 Total de registros atualizados: {atualizados}")

