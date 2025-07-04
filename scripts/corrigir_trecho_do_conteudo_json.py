import json
from pymongo import MongoClient

CAMINHO_JSON_ENTRADA = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/modelo_extracao_pisa_2022.json"
CAMINHO_JSON_SAIDA = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/modelo_extracao_pisa_2022_corrigido_com_trechos.json"

client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

print("🚀 Mapeando trechos disponíveis no MongoDB...")

# Mapa: {arquivo_original → trecho_do_conteudo}
mapa_trechos = {}

for nome_col in db.list_collection_names():
    if not nome_col.startswith("protocolo_pisa_2022_"):
        continue

    print(f"🔍 Verificando coleção: {nome_col}")
    for doc in db[nome_col].find(
        {"trecho_do_conteudo": {"$exists": True}},
        {"arquivo_original": 1, "trecho_do_conteudo": 1}
    ):
        mapa_trechos[doc["arquivo_original"]] = doc["trecho_do_conteudo"]

print(f"✅ Total de trechos coletados: {len(mapa_trechos)}")

# Carrega o JSON original
with open(CAMINHO_JSON_ENTRADA, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Corrige cada entrada do JSON
corrigidos = 0
nao_encontrados = 0

print("🛠️ Corrigindo entradas do JSON...")
for idx, item in enumerate(dados, start=1):
    nome = item["arquivo_original"]
    print(f"🔄 [{idx}/{len(dados)}] Corrigindo: {nome}")

    if not item.get("trecho_do_conteudo"):
        trecho = mapa_trechos.get(nome)
        if trecho:
            item["trecho_do_conteudo"] = trecho
            corrigidos += 1
        else:
            print(f"⚠️  Trecho não encontrado no MongoDB para: {nome}")
            nao_encontrados += 1

# Salva resultado corrigido
with open(CAMINHO_JSON_SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

client.close()

print("\n🎯 Conclusão:")
print(f"✔️  Entradas corrigidas com trecho: {corrigidos}")
print(f"❌ Sem trecho no MongoDB: {nao_encontrados}")
print(f"📁 Arquivo salvo em: {CAMINHO_JSON_SAIDA}")

