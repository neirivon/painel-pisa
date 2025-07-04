from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_dados_ibge_5ano.py

from pymongo import MongoClient

# === Conexão com MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao_saeb = db["saeb_2021_municipios_5ano"]

# === Base simplificada do IBGE (pode expandir se quiser)
municipios_ibge = [
    {
        "CO_MUNICIPIO": 6322170,
        "NO_MUNICIPIO": "Porto Velho",
        "NO_UF": "Rondônia",
        "REGIAO": "Norte",
        "MESORREGIAO": "Leste Rondoniense",
        "MICRORREGIAO": "Porto Velho"
    },
    {
        "CO_MUNICIPIO": 1100015,
        "NO_MUNICIPIO": "Alta Floresta D'Oeste",
        "NO_UF": "Rondônia",
        "REGIAO": "Norte",
        "MESORREGIAO": "Leste Rondoniense",
        "MICRORREGIAO": "Cacoal"
    },
    # 🔁 Adicione mais municípios conforme necessário
]

# === Atualização no MongoDB ===
atualizados = 0
for municipio in municipios_ibge:
    resultado = colecao_saeb.update_many(
        {"ID_MUNICIPIO": municipio["CO_MUNICIPIO"]},
        {
            "$set": {
                "NO_MUNICIPIO": municipio["NO_MUNICIPIO"],
                "NO_UF": municipio["NO_UF"],
                "REGIAO": municipio["REGIAO"],
                "MESORREGIAO": municipio["MESORREGIAO"],
                "MICRORREGIAO": municipio["MICRORREGIAO"]
            }
        }
    )
    atualizados += resultado.modified_count

print(f"✅ {atualizados} documentos atualizados com sucesso na coleção 'saeb_2021_municipios_5ano'.")
client.close()

