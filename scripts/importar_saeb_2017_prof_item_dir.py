import os
import csv
import hashlib
from pymongo import MongoClient, errors
from datetime import datetime

MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DATABASE = "saeb"
ARQUIVOS = {
    "saeb_2017_professor": "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2017_2019/microdados_saeb_2017/DADOS/TS_PROFESSOR.csv",
    "saeb_2017_item": "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2017_2019/microdados_saeb_2017/DADOS/TS_ITEM.csv",
    "saeb_2017_diretor": "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2017_2019/microdados_saeb_2017/DADOS/TS_DIRETOR.csv"
}
ENCODING = "latin1"
TAMANHO_LOTE = 1000

def gerar_id_unico(linha: dict) -> str:
    texto = ''.join([str(v) for v in linha.values()])
    return hashlib.md5(texto.encode()).hexdigest()

def importar_arquivo(nome_colecao, caminho_csv):
    print(f"\n📥 Iniciando importação de: {caminho_csv}")
    client = MongoClient(MONGO_URI)
    db = client[DATABASE]
    colecao = db[nome_colecao]

    total = 0
    lote = []

    try:
        with open(caminho_csv, newline='', encoding=ENCODING) as csvfile:
            leitor = csv.DictReader(csvfile, delimiter=';')
            for linha in leitor:
                _id = gerar_id_unico(linha)
                linha["_id"] = _id
                lote.append(linha)

                if len(lote) >= TAMANHO_LOTE:
                    try:
                        colecao.insert_many(lote, ordered=False)
                        total += len(lote)
                        print(f"  ✅ {total:,} documentos inseridos até {datetime.now().strftime('%H:%M:%S')}")
                    except errors.BulkWriteError as bwe:
                        total += bwe.details.get('nInserted', 0)
                        print(f"  ⚠️  Inseridos com duplicatas: {total:,} até {datetime.now().strftime('%H:%M:%S')}")
                    lote = []

            if lote:
                try:
                    colecao.insert_many(lote, ordered=False)
                    total += len(lote)
                    print(f"  ✅ {total:,} documentos inseridos até {datetime.now().strftime('%H:%M:%S')}")
                except errors.BulkWriteError as bwe:
                    total += bwe.details.get('nInserted', 0)
                    print(f"  ⚠️  Inseridos com duplicatas: {total:,} até {datetime.now().strftime('%H:%M:%S')}")

    finally:
        client.close()
        print(f"🔒 Conexão com MongoDB encerrada com segurança.")

if __name__ == "__main__":
    for nome_colecao, caminho_csv in ARQUIVOS.items():
        importar_arquivo(nome_colecao, caminho_csv)

