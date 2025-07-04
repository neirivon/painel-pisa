from pymongo import MongoClient
import json

CAMINHO_JSON_ENTRADA = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/modelo_extracao_pisa_2022.json"
CAMINHO_JSON_SAIDA = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/modelo_extracao_pisa_2022_preenchido.json"

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

with open(CAMINHO_JSON_ENTRADA, "r", encoding="utf-8") as f:
    dados = json.load(f)

for doc in dados:
    colecao_original = doc["colecao_mongodb"]
    
    if colecao_original.startswith("pisa_") and "_2022" in colecao_original:
        colecao_real = "protocolo_pisa_2022_" + colecao_original.replace("pisa_", "").replace("_2022", "")
    elif colecao_original == "pisa_revenue_stats_2025":
        colecao_real = "protocolo_pisa_2022_revenue_stats_2025"
    elif colecao_original == "pisa_econ_outlook_2025":
        colecao_real = "protocolo_pisa_2022_econ_outlook_2025"
    else:
        colecao_real = colecao_original

    encontrado = db[colecao_real].find_one({"arquivo_original": doc["arquivo_original"]})
    if encontrado:
        doc["trecho_do_conteudo"] = encontrado.get("trecho_do_conteudo", "")
        doc["hash_conteudo"] = encontrado.get("hash_conteudo", "")
    else:
        print(f"❌ Documento não encontrado no MongoDB: {doc['arquivo_original']}")

with open(CAMINHO_JSON_SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)

client.close()  # 👈 Fecha a conexão com o MongoDB

print("✅ Arquivo atualizado salvo como:", CAMINHO_JSON_SAIDA)

