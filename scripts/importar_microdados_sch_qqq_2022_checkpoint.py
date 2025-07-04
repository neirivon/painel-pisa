# scripts/importar_microdados_sch_qqq_2022_checkpoint.py

import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import pyreadstat

# ========================
# CONFIGURAÇÃO
# ========================
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
NOME_BANCO = "pisa"
NOME_COLECAO = "pisa_2022_school"
CAMINHO_SAV = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/SAV/CY08MSP_SCH_QQQ.SAV"
BATCH_SIZE = 25000

# ========================
# FUNÇÃO PRINCIPAL
# ========================
def importar_sav_em_lotes():
    print(f"📥 Iniciando importação de: {CAMINHO_SAV}")
    
    client = MongoClient(MONGO_URI)
    db = client[NOME_BANCO]
    colecao = db[NOME_COLECAO]

    documentos_atuais = colecao.count_documents({})
    print(f"📊 Documentos já existentes na coleção: {documentos_atuais}")

    df, meta = pyreadstat.read_sav(CAMINHO_SAV)
    total = len(df)

    df = df.iloc[documentos_atuais:]
    if df.empty:
        print("✅ Nada a importar. Todos os dados já estão no MongoDB.")
        return

    for i in range(0, len(df), BATCH_SIZE):
        fim = min(i + BATCH_SIZE, len(df))
        lote = df.iloc[i:fim].to_dict(orient="records")
        colecao.insert_many(lote)
        print(f"  ✅ {fim + documentos_atuais:,} registros inseridos até {datetime.now().strftime('%H:%M:%S')}")

    print(f"✅ Finalizado: {NOME_COLECAO} com {colecao.count_documents({}):,} documentos.")
    print("🔒 Conexão com MongoDB encerrada.")
    client.close()

if __name__ == "__main__":
    importar_sav_em_lotes()

