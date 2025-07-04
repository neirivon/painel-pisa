from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# inserir_campos_faltantes_5ano.py

from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]

# Carregar coleções
col_5ano = db["saeb_2021_municipios_5ano"]
col_9ano = db["saeb_2021_municipios_9ano"]

# Criar mapa auxiliar com dados do 9º ano
mapa = {}
for doc in col_9ano.find({}, {"_id": 0, "CO_MUNICIPIO": 1, "NO_MUNICIPIO": 1, "NO_UF": 1, "REGIAO": 1, "MESORREGIAO": 1, "MICRORREGIAO": 1}):
    mapa[doc["CO_MUNICIPIO"]] = {
        "NO_MUNICIPIO": doc["NO_MUNICIPIO"],
        "NO_UF": doc["NO_UF"],
        "REGIAO": doc.get("REGIAO"),
        "MESORREGIAO": doc.get("MESORREGIAO"),
        "MICRORREGIAO": doc.get("MICRORREGIAO")
    }

# Atualizar os documentos da coleção do 5º ano
contador = 0
for doc in col_5ano.find():
    cod_mun = doc.get("ID_MUNICIPIO")
    if cod_mun in mapa:
        dados = mapa[cod_mun]
        col_5ano.update_one(
            {"_id": doc["_id"]},
            {"$set": {
                "CO_MUNICIPIO": cod_mun,
                "NO_MUNICIPIO": dados["NO_MUNICIPIO"],
                "NO_UF": dados["NO_UF"],
                "REGIAO": dados["REGIAO"],
                "MESORREGIAO": dados["MESORREGIAO"],
                "MICRORREGIAO": dados["MICRORREGIAO"],
                "MEDIA_5_LP": doc["PROFICIENCIA_LP_SAEB"],
                "MEDIA_5_MT": doc["PROFICIENCIA_MT_SAEB"],
                "nota_geral": (doc["PROFICIENCIA_LP_SAEB"] + doc["PROFICIENCIA_MT_SAEB"])os.path.join( , " ")2
            }}
        )
        contador += 1

client.close()
print(f"✅ {contador} documentos atualizados com sucesso na coleção 'saeb_2021_municipios_5ano'")

