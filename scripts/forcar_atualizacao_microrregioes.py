from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# forcar_atualizacao_microrregioes.py

from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_9ano"]

# Dicionário de correções forçadas
correcoes = {
    "Ararendá": {
        "REGIAO": "Nordeste",
        "MESORREGIAO": "Sertões Cearenses",
        "MICRORREGIAO": "Sertão de Crateús"
    },
    "Cruz": {
        "REGIAO": "Nordeste",
        "MESORREGIAO": "Noroeste Cearense",
        "MICRORREGIAO": "Acaraú"
    },
    "Jijoca de Jericoacoara": {
        "REGIAO": "Nordeste",
        "MESORREGIAO": "Noroeste Cearense",
        "MICRORREGIAO": "Camocim"
    },
    "Santana do Mundaú": {
        "REGIAO": "Nordeste",
        "MESORREGIAO": "Leste Alagoano",
        "MICRORREGIAO": "União dos Palmares"
    },
    "São Vicente Ferrer": {
        "REGIAO": "Nordeste",
        "MESORREGIAO": "Norte Maranhense",
        "MICRORREGIAO": "Viana"
    }
}

total_atualizados = 0

for municipio, dados in correcoes.items():
    resultado = colecao.update_many(
        { "NO_MUNICIPIO": municipio },
        { "$set": dados }
    )
    print(f"✅ {municipio}: {resultado.modified_count} documento(s) atualizado(s).")
    total_atualizados += resultado.modified_count

print(f"\n🚀 Atualizações forçadas concluídas. Total de documentos atualizados: {total_atualizados}")

client.close()

