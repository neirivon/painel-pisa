from pymongo import MongoClient
from pymongo.errors import OperationFailure
from bson.json_util import dumps
from pathlib import Path

# === Configurações ===
MONGO_URI = "mongodb://admin:admin123@localhost:27017"
BANCO = "pisa"
ARQUIVO_SAIDA = Path("relatorio_colecoes_com_pv1.txt")
TERMO_PESQUISA = ["PV1READ", "PV1MATH", "PV1SCIE", "READ", "MATH", "SCIE"]

# === Conexão ===
client = MongoClient(MONGO_URI)
db = client[BANCO]

# === Listar coleções do banco PISA
colecoes = db.list_collection_names(filter={"name": {"$regex": "^pisa_2022_"}})
relatorio = []

print("🔍 Iniciando varredura nas coleções do PISA 2022...\n")

for nome_col in colecoes:
    print(f"➡️ Verificando: {nome_col}")
    colecao = db[nome_col]

    try:
        # Buscar um documento do Brasil
        doc = colecao.find_one({"CNT": {"$in": ["BRA", "BR"]}})
        if not doc:
            print(f"   ⛔ Nenhum documento com CNT=BRA/BR encontrado.\n")
            continue

        campos_encontrados = [k for k in doc.keys() if any(term in k for term in TERMO_PESQUISA)]
        if campos_encontrados:
            print(f"   ✅ Campos cognitivos encontrados: {campos_encontrados}\n")
            relatorio.append({
                "colecao": nome_col,
                "campos": campos_encontrados,
                "exemplo": {k: doc[k] for k in campos_encontrados if k in doc}
            })
        else:
            print(f"   ⚠️ Nenhum campo cognitivo presente neste documento.\n")

    except OperationFailure as e:
        print(f"   ❌ Erro ao acessar {nome_col}: {e}")

client.close()

# Salvar relatório
texto = dumps(relatorio, indent=2, ensure_ascii=False)
ARQUIVO_SAIDA.write_text(texto, encoding="utf-8")
print(f"\n✅ Relatório final salvo em: {ARQUIVO_SAIDA.resolve()}")

