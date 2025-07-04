import json
from pymongo import MongoClient

# Caminhos
CAMINHO_JSON = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/modelo_extracao_pisa_2022.json"
CAMINHO_SAIDA = CAMINHO_JSON.replace(".json", "_com_trecho_e_hash.json")

# Mongo
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

for item in dados:
    fonte = item.get("fonte")
    colecao = item.get("colecao_mongodb")
    if not (fonte and colecao):
        continue

    # Atualizado para refletir renomeações
    nome_colecao_final = f"protocolo_pisa_2022_{colecao.replace('pisa_', '').replace('_2022', '')}"
    doc = db[nome_colecao_final].find_one({"fonte": fonte})

    if doc:
        if "trecho_do_conteudo" in doc:
            item["trecho_do_conteudo"] = doc["trecho_do_conteudo"]
        if "hash_conteudo" in doc:
            item["hash_conteudo"] = doc["hash_conteudo"]

with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

client.close()
print(f"✅ JSON atualizado salvo como: {CAMINHO_SAIDA}")

