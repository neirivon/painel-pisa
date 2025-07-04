import os
import json
from pymongo import MongoClient

# ==========================
# CONFIGURAÇÃO DO BANCO
# ==========================
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
NOME_BANCO = "pisa"

# ==========================
# ARQUIVOS E SCHEMAS
# ==========================
ARQUIVOS = [
    {
        "arquivo_txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intcogn_v4.txt",
        "schema_json": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_cognitive_item_2000.json",
        "colecao": "pisa_2000_cognitive_item"
    },
    {
        "arquivo_txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intscho.txt",
        "schema_json": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_school_2000.json",
        "colecao": "pisa_2000_school"
    }
]

# ==========================
# FUNÇÃO DE IMPORTAÇÃO
# ==========================
def importar_txt_fixo(arquivo_txt, schema_json, colecao):
    print(f"📥 Lendo arquivo: {arquivo_txt}")

    # Carregar schema
    with open(schema_json, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    # Conectar ao MongoDB
    client = MongoClient(MONGO_URI)
    db = client[NOME_BANCO]
    col = db[colecao]

    documentos = []
    with open(arquivo_txt, 'r', encoding='latin1') as f:
        for linha in f:
            doc = {}
            for campo in schema:
                nome = campo["name"]
                inicio = campo["start"] - 1  # Corrigir índice
                fim = campo["end"]
                doc[nome] = linha[inicio:fim].strip()
            documentos.append(doc)

    # Inserir documentos
    if documentos:
        col.insert_many(documentos)
        print(f"✅ Coleção '{colecao}' importada com {len(documentos):,} documentos.")
    else:
        print(f"⚠️ Nenhum documento válido para '{colecao}'.")

    client.close()
    print("🔒 Conexão com MongoDB encerrada.\n")

# ==========================
# EXECUÇÃO EM LOTE
# ==========================
if __name__ == "__main__":
    for item in ARQUIVOS:
        if os.path.exists(item["arquivo_txt"]) and os.path.exists(item["schema_json"]):
            try:
                importar_txt_fixo(item["arquivo_txt"], item["schema_json"], item["colecao"])
            except Exception as e:
                print(f"❌ Erro ao importar '{item['arquivo_txt']}': {e}")
        else:
            print(f"❌ Caminho não encontrado: {item['arquivo_txt']} ou {item['schema_json']}")

