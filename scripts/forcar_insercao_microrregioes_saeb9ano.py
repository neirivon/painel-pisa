from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["saeb_2021_municipios_9ano"]

# Tabela de correções forçadas (baseadas no nome do município)
correcoes = {
    "Ararendá": {
        "MESORREGIAO": "Sertões Cearenses",
        "MICRORREGIAO": "Sertão de Cratéus"
    },
    "Cruz": {
        "MESORREGIAO": "Noroeste Cearense",
        "MICRORREGIAO": "Litoral de Camocim e Acaraú"
    },
    "Jijoca de Jericoacoara": {
        "MESORREGIAO": "Noroeste Cearense",
        "MICRORREGIAO": "Litoral de Camocim e Acaraú"
    },
    "Santana do Mundaú": {
        "MESORREGIAO": "Leste Alagoano",
        "MICRORREGIAO": "União dos Palmares"
    },
    "São Vicente Ferrer": {
        "MESORREGIAO": "Norte Maranhense",
        "MICRORREGIAO": "Baixada Maranhense"
    }
}

# Aplicar correções forçadas
atualizados = 0
for municipio, valores in correcoes.items():
    resultado = colecao.update_many(
        { "NO_MUNICIPIO": municipio },
        {
            "$set": {
                "MESORREGIAO": valores["MESORREGIAO"],
                "MICRORREGIAO": valores["MICRORREGIAO"]
            }
        }
    )
    print(f"✅ {municipio}: {resultado.modified_count} documento(s) atualizado(s).")
    atualizados += resultado.modified_count

client.close()
print(f"\n🚀 Atualizações forçadas concluídas. Total de documentos atualizados: {atualizados}")

