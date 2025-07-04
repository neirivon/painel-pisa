# importar_microdados_student_2000.py

import os
import json
from pymongo import MongoClient

# === Configurações ===
ARQUIVOS = {
    "math": {
        "txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intstud_math_v3.txt",
        "schema": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_student_math_2000.json",
        "colecao": "pisa_2000_student_math"
    },
    "read": {
        "txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intstud_read_v3.txt",
        "schema": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_student_read_2000.json",
        "colecao": "pisa_2000_student_read"
    },
    "scie": {
        "txt": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/INT/intstud_scie_v3.txt",
        "schema": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_student_scie_2000.json",
        "colecao": "pisa_2000_student_scie"
    }
}

MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"

def carregar_schema(caminho_json):
    with open(caminho_json, "r", encoding="utf-8") as f:
        return json.load(f)

def importar_txt_para_mongo(caminho_txt, schema, nome_colecao, client):
    colecao = client[BANCO][nome_colecao]
    documentos = []

    with open(caminho_txt, "r", encoding="latin1") as f:
        for linha in f:
            doc = {}
            for campo in schema:
                nome = campo["nome"]
                inicio = campo["inicio"] - 1
                fim = campo["fim"]
                tipo = campo["tipo"]

                valor = linha[inicio:fim].strip()

                if tipo == "int":
                    try:
                        valor = int(valor)
                    except:
                        valor = None
                elif tipo == "float":
                    try:
                        valor = float(valor)
                    except:
                        valor = None
                doc[nome] = valor
            documentos.append(doc)

    if documentos:
        colecao.delete_many({})
        colecao.insert_many(documentos)
        print(f"✅ Coleção '{nome_colecao}' importada com sucesso: {len(documentos):,} documentos")
    else:
        print(f"⚠️ Nenhum documento válido encontrado para {nome_colecao}")

def main():
    client = MongoClient(MONGO_URI)

    for chave, info in ARQUIVOS.items():
        print(f"\n📥 Lendo arquivo: {info['txt']}")
        try:
            schema = carregar_schema(info["schema"])
            importar_txt_para_mongo(info["txt"], schema, info["colecao"], client)
        except Exception as e:
            print(f"❌ Erro ao importar '{info['txt']}': {e}")

    client.close()
    print("\n🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    main()

