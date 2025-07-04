# scripts/importar_microdados_int_2003_fragmentado.py

import os
import json
from pymongo import MongoClient
from datetime import datetime

# === CONFIGURAÇÃO ===
ARQUIVOS = [
    {
        "nome": "student",
        "arquivo_txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/INT/INT_stui_2003_v2.txt",
        "schema_json": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/SCHEMAS/schema_student_2003.json",
        "colecao_mongo": "pisa_2003_student"
    },
    {
        "nome": "school",
        "arquivo_txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/INT/INT_schi_2003.txt",
        "schema_json": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/SCHEMAS/schema_school_2003.json",
        "colecao_mongo": "pisa_2003_school"
    },
    {
        "nome": "cognitive_item",
        "arquivo_txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/INT/INT_cogn_2003_v2.txt",
        "schema_json": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003/SCHEMAS/schema_cognitive_item_2003.json",
        "colecao_mongo": "pisa_2003_cognitive_item"
    }
]

MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"

# === FUNÇÃO PRINCIPAL ===
def importar_txt_fixo_em_blocos(caminho_arquivo, schema, colecao, nome, bloco=10000):
    total = 0
    with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as f:
        buffer = []
        for linha in f:
            doc = {}
            for campo in schema:
                try:
                    valor = linha[campo["start"] - 1: campo["end"]].strip()
                    doc[campo["name"]] = valor
                except Exception as e:
                    doc[campo["name"]] = None
            buffer.append(doc)
            total += 1
            if len(buffer) >= bloco:
                colecao.insert_many(buffer)
                print(f"📦 {nome}: {total} registros importados...")
                buffer.clear()
        if buffer:
            colecao.insert_many(buffer)
            print(f"📦 {nome}: {total} registros importados (final)...")
    return total

# === EXECUÇÃO EM LOTE ===
client = MongoClient(MONGO_URI)
db = client[BANCO]

for item in ARQUIVOS:
    nome = item["nome"]
    print(f"\n📥 Lendo arquivo: {item['arquivo_txt']}")
    if not os.path.exists(item["schema_json"]):
        print(f"❌ Schema não encontrado: {item['schema_json']}")
        continue
    if not os.path.exists(item["arquivo_txt"]):
        print(f"❌ Arquivo TXT não encontrado: {item['arquivo_txt']}")
        continue

    with open(item["schema_json"], "r", encoding="utf-8") as f:
        schema = json.load(f)

    colecao = db[item["colecao_mongo"]]
    colecao.drop()  # limpa antes de inserir novamente

    total = importar_txt_fixo_em_blocos(
        caminho_arquivo=item["arquivo_txt"],
        schema=schema,
        colecao=colecao,
        nome=nome,
        bloco=10000
    )

    print(f"✅ Coleção '{item['colecao_mongo']}' importada com {total:,} documentos.")

client.close()
print("🔒 Conexão com MongoDB encerrada.")

