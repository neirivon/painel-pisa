import json
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from painel_pisa.utils.config import CONFIG  # ajuste se necessário
from painel_pisa.utils.conexao_mongo import conectar_mongo

# =====================
# CONFIGURAÇÃO
# =====================
NOME_BANCO = "relatorios_inep"
NOME_COLECAO = "inep_2022"
CAMINHO_CSV = "dados_processados/rotulagem/paragrafos_inep2022_rotulagem.csv"
CAMINHO_JSON = "dados_processados/rotulagem/paragrafos_inep2022_rotulagem.json"

# =====================
# CONEXÃO COM MONGODB
# =====================
db, client = conectar_mongo(nome_banco=NOME_BANCO)
colecao = db[NOME_COLECAO]

# =====================
# BUSCA DE DOCUMENTOS
# =====================
print("🔍 Buscando documentos validados pela IA...")
documentos = list(colecao.find({
    "erro": None,
    "resposta": { "$exists": True }
}).sort("ordem", 1))

print(f"✅ Total de parágrafos encontrados: {len(documentos)}")

# =====================
# PROCESSAR DOCUMENTOS
# =====================
linhas = []
for doc in documentos:
    linhas.append({
        "id_mongo": str(doc["_id"]),
        "ano": doc.get("ano", ""),
        "ordem": doc.get("ordem", ""),
        "paragrafo": doc.get("paragrafo", ""),
        "resposta_ia": doc.get("resposta", "")
    })

# =====================
# EXPORTAR PARA CSV
# =====================
df = pd.DataFrame(linhas)
df.to_csv(CAMINHO_CSV, index=False, encoding="utf-8")
print(f"📁 CSV exportado para: {CAMINHO_CSV}")

# =====================
# EXPORTAR PARA JSON
# =====================
with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
    json.dump(linhas, f, ensure_ascii=False, indent=2)

client.close()

print(f"📁 JSON exportado para: {CAMINHO_JSON}")

