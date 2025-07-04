import os
import json
from pymongo import MongoClient
from datetime import datetime

# ========== CONFIGURAÇÃO ==========
ARQUIVOS = {
    "student": {
        "arquivo": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/INT/INT_stui_2003_v2.txt",
        "schema": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/SCHEMAS/schema_student_2003.json",
        "colecao": "pisa_2003_student"
    },
    "school": {
        "arquivo": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/INT/INT_schi_2003.txt",
        "schema": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/SCHEMAS/schema_school_2003.json",
        "colecao": "pisa_2003_school"
    },
    "cognitive": {
        "arquivo": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/INT/INT_cogn_2003_v2.txt",
        "schema": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/SCHEMAS/schema_cognitive_item_2003.json",
        "colecao": "pisa_2003_cognitive_item"
    }
}
CHECKPOINT_DIR = "checkpoints"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# ========== CONEXÃO MONGODB ==========
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# ========== FUNÇÕES ==========

def carregar_schema(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def carregar_checkpoint(nome_colecao):
    caminho = os.path.join(CHECKPOINT_DIR, f"{nome_colecao}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            return int(f.read().strip())
    return 0

def salvar_checkpoint(nome_colecao, linha_atual):
    with open(os.path.join(CHECKPOINT_DIR, f"{nome_colecao}.txt"), "w") as f:
        f.write(str(linha_atual))

def importar_txt_fixo(arquivo, schema, colecao_mongo, nome_colecao):
    print(f"\n📥 Iniciando importação: {arquivo}")
    total_inseridos = 0
    checkpoint = carregar_checkpoint(nome_colecao)
    campos = schema

    with open(arquivo, "r", encoding="latin1") as f:
        for i, linha in enumerate(f):
            if i < checkpoint:
                continue

            doc = {}
            for campo in campos:
                nome = campo["name"]
                ini = campo["start"] - 1
                fim = campo["end"]
                doc[nome] = linha[ini:fim].strip()

            colecao_mongo.insert_one(doc)
            total_inseridos += 1

            if total_inseridos % 100000 == 0:
                print(f"  ✅ {total_inseridos:,} registros inseridos até {datetime.now().strftime('%H:%M:%S')}")

            if total_inseridos % 1000 == 0:
                salvar_checkpoint(nome_colecao, i + 1)

    salvar_checkpoint(nome_colecao, i + 1)
    print(f"✅ Finalizado: {nome_colecao} com {total_inseridos:,} documentos.\n")

# ========== EXECUÇÃO ==========

for chave, dados in ARQUIVOS.items():
    try:
        schema = carregar_schema(dados["schema"])
        colecao = db[dados["colecao"]]
        importar_txt_fixo(dados["arquivo"], schema, colecao, dados["colecao"])
    except Exception as e:
        print(f"❌ Erro ao importar {dados['arquivo']}: {e}")

client.close()
print("🔒 Conexão com MongoDB encerrada.")

