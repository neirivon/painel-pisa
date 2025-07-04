import json
from painel_pisa.utils.conexao_mongo import conectar_mongo

# ========== CONFIGURAÇÃO ==========
CAMINHO_JSON = "dados_processados/rubricas/rubrica_ctc.json"
NOME_BANCO = "rubricas"
NOME_COLECAO = "rubrica_ctc"

# ========== CONEXÃO COM MONGODB ==========
db, client = conectar_mongo(nome_banco=NOME_BANCO)
colecao = db[NOME_COLECAO]

# ========== CARREGAR JSON ==========
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

# ========== INSERIR OU ATUALIZAR ==========
total_inseridos = 0

for item in dados:
    filtro = {
        "dimensao": item.get("dimensao"),
        "nivel": item.get("nivel"),
        "versao": item.get("versao")
    }

    resultado = colecao.replace_one(filtro, item, upsert=True)

    if resultado.upserted_id or resultado.modified_count > 0:
        total_inseridos += 1

# ========== RESULTADO ==========
print("✅ Inserção/atualização concluída.")
print(f"📄 Documentos atualizados/inseridos: {total_inseridos}")

# ========== FECHAR CONEXÃO ==========
client.close()

