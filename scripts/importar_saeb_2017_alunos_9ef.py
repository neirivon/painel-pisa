# scripts/importar_saeb_2017_alunos_9ef.py

import csv
import hashlib
import time
from pymongo import MongoClient

# Caminho do arquivo CSV
CAMINHO_CSV = "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2017_2019/microdados_saeb_2017/DADOS/TS_ALUNO_9EF.csv"
NOME_COLECAO = "saeb_2017_alunos_9ef"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BATCH_SIZE = 1000

def gerar_id_unico(linha_dict):
    texto = "|".join([linha_dict.get(k, "") for k in sorted(linha_dict.keys())])
    return hashlib.md5(texto.encode("utf-8")).hexdigest()

def importar_csv_em_lotes():
    client = MongoClient(MONGO_URI)
    db = client["saeb"]
    colecao = db[NOME_COLECAO]

    total = 0
    lote = []
    hora_inicio = time.strftime("%H:%M:%S")

    print(f"📥 Iniciando importação de: {CAMINHO_CSV}")

    with open(CAMINHO_CSV, "r", encoding="latin1") as f:
        leitor = csv.DictReader(f, delimiter=";")
        for linha in leitor:
            _id = gerar_id_unico(linha)
            linha["_id"] = _id
            lote.append(linha)

            if len(lote) >= BATCH_SIZE:
                try:
                    colecao.insert_many(lote, ordered=False)
                except Exception as e:
                    pass  # Ignorar duplicatas ou erros pontuais
                total += len(lote)
                print(f"  ✅ {total:,} documentos inseridos até {time.strftime('%H:%M:%S')}")
                lote = []

        # Inserir o restante
        if lote:
            try:
                colecao.insert_many(lote, ordered=False)
            except Exception as e:
                pass
            total += len(lote)
            print(f"  ✅ {total:,} documentos inseridos até {time.strftime('%H:%M:%S')}")

    client.close()
    print("🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    importar_csv_em_lotes()

