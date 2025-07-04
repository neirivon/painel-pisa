import json
from pymongo import MongoClient
from datetime import datetime

# === CONFIGURAÇÕES ===
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "rubricas"
COLECAO = "rubrica_sinapse_ia"
CAMINHO_JSON = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_padronizada.json"

try:
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        rubrica = json.load(f)
except Exception as e:
    print(f"❌ Erro ao ler o JSON: {e}")
    exit(1)

# === INSERÇÃO NO MONGODB ===
cliente = None
try:
    cliente = MongoClient(MONGO_URI)
    db = cliente[BANCO]
    colecao = db[COLECAO]

    # Remove entradas antigas da mesma versão
    versao_atual = rubrica.get("versao", "desconhecida")
    colecao.delete_many({"versao": versao_atual})

    # Insere nova rubrica
    rubrica["inserido_em"] = datetime.now().isoformat()
    resultado = colecao.insert_one(rubrica)

    print("✅ Rubrica salva com sucesso no MongoDB!")
    print(f"🆔 ID inserido: {resultado.inserted_id}")
    print(f"📂 Banco: {BANCO} | Coleção: {COLECAO} | Versão: {versao_atual}")

except Exception as e:
    print(f"❌ Erro ao salvar no MongoDB: {e}")

finally:
    if cliente:
        cliente.close()
        print("🔒 Conexão com MongoDB encerrada.")

