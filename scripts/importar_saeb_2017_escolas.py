# scripts/importar_saeb_2017_escolas.py

import csv
import hashlib
from pymongo import MongoClient
from datetime import datetime

# Conexão direta com MongoDB (dockerizado)
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"

CAMINHO_CSV = "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2017_2019/microdados_saeb_2017/DADOS/TS_ESCOLA.csv"
NOME_COLECAO = "saeb_2017_escolas"
TAMANHO_LOTE = 1000

def gerar_id_unico(linha):
    texto = "".join([str(v).strip() for v in linha.values() if v.strip()])
    return hashlib.md5(texto.encode("utf-8")).hexdigest()

def importar_csv_em_lotes():
    client = MongoClient(MONGO_URI)
    db = client["saeb"]
    colecao = db[NOME_COLECAO]

    total = 0
    lote = []

    with open(CAMINHO_CSV, "r", encoding="latin1") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=",")
        for linha in leitor:
            if not any(valor.strip() for valor in linha.values()):
                continue  # Ignora linha totalmente vazia

            doc = dict(linha)
            doc["_id"] = gerar_id_unico(doc)
            lote.append(doc)

            if len(lote) >= TAMANHO_LOTE:
                try:
                    colecao.insert_many(lote, ordered=False)
                    total += len(lote)
                    print(f"  ✅ {total:,} documentos inseridos até {datetime.now().strftime('%H:%M:%S')}")
                except Exception as e:
                    print(f"⚠️  Erro em lote: {e}")
                lote = []

        # Último lote
        if lote:
            try:
                colecao.insert_many(lote, ordered=False)
                total += len(lote)
                print(f"  ✅ {total:,} documentos inseridos até {datetime.now().strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"⚠️  Erro final em lote: {e}")

    print("🔒 Conexão com MongoDB encerrada.")
    client.close()

if __name__ == "__main__":
    print(f"📥 Iniciando importação de: {CAMINHO_CSV}")
    importar_csv_em_lotes()

