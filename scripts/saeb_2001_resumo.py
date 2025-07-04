from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

# Conexão autenticada com o MongoDB
mongo = conectar_mongo(nome_banco="saeb")[1]
db = mongo["saeb"]

# Coletas reais das rubricas
rubricas_collections = {
    "Brasil": "rubricas_2001_brasil",
    "Minas Gerais": "rubricas_2001_minasgerais",
    "Triângulo Mineiro": "rubricas_2001_micro_triangulo"
}

novo_resumo = []

for regiao, nome_colecao in rubricas_collections.items():
    doc = db[nome_colecao].find_one()
    if doc:
        resumo = {
            "regiao": regiao,
            "matematica_media": doc.get("matematica_media"),
            "leitura_media": doc.get("leitura_media"),
            "ciencias_media": doc.get("ciencias_media"),  # Pode ser None ou ausente
            "estado": "MG" if regiao != "Brasil" else None
        }
        novo_resumo.append(resumo)

# Substituir coleção antiga por dados reais
db.drop_collection("saeb_2001_resumo")
db["saeb_2001_resumo"].insert_many(novo_resumo)

print("✅ Coleção 'saeb_2001_resumo' atualizada com base nos dados reais disponíveis.")

