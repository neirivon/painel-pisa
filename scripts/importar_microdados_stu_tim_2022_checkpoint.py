# scripts/importar_microdados_stu_tim_2022_checkpoint.py

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from pyreadstat import read_sav

# === CONFIGURAÇÃO ===
CAMINHO_SAV = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/SAV/CY08MSP_STU_TIM.SAV"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"
COLECAO = "pisa_2022_student_time"
LOTE = 25000

def importar_sav_em_lotes():
    print(f"📥 Iniciando importação de: {CAMINHO_SAV}")
    df, _ = read_sav(CAMINHO_SAV)
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    collection = db[COLECAO]

    if df.empty:
        print("✅ Nada a importar. Arquivo vazio.")
        print("🔒 Conexão com MongoDB encerrada.")
        client.close()
        return

    total_ja = collection.count_documents({})
    total = len(df)

    if total_ja >= total:
        print(f"📊 Documentos já existentes na coleção: {total_ja}")
        print("✅ Nada a importar. Todos os dados já estão no MongoDB.")
        print("🔒 Conexão com MongoDB encerrada.")
        client.close()
        return

    registros_faltando = df.iloc[total_ja:]

    for i in range(0, len(registros_faltando), LOTE):
        lote = registros_faltando.iloc[i:i+LOTE].to_dict(orient="records")
        collection.insert_many(lote)
        print(f"  ✅ {total_ja + i + len(lote)} registros inseridos até {datetime.now().strftime('%H:%M:%S')}")

    print(f"✅ Finalizado: {COLECAO} com {collection.count_documents({})} documentos.")
    print("🔒 Conexão com MongoDB encerrada.")
    client.close()

if __name__ == "__main__":
    importar_sav_em_lotes()

