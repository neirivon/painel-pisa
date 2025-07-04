from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "f")orcar_correcao_microrregioes_geometry.py

from pymongo import MongoClient

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["saeb"]
colecao = db["ibge_microrregioes_geometry"]

# Dicionário com os nomes corretos
correcoes = {
    "Sertão de Crateús": "Sertão de Cratéus",
    "Acaraú": "Litoral de Camocim e Acaraú",
    "Camocim": "Litoral de Camocim e Acaraú"
}

atualizados = 0

for nome_antigo, nome_correto in correcoes.items():
    documentos = list(colecao.find({ "NM_MICRO": nome_antigo }))
    
    if documentos:
        for doc in documentos:
            # Atualiza apenas o campo NM_MICRO mantendo os outros (inclusive geometry)
            resultado = colecao.update_one(
                { "_id": doc["_id"] },
                { "$set": { "NM_MICRO": nome_correto } }
            )
            if resultado.modified_count > 0:
                atualizados += 1
                print(f"✅ Corrigido: {nome_antigo} → {nome_correto}")
    else:
        print(f"⚠️ Não encontrado: {nome_antigo}")

print(f"\n🚀 Atualizações concluídas. Total de documentos atualizados: {atualizados}")
client.close()

