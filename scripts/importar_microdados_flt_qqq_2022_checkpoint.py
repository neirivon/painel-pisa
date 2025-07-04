import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# === CONFIGURAÇÃO ===
CAMINHO_ARQUIVO = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/SAV/CY08MSP_FLT_QQQ.SAV"
NOME_COLECAO = "pisa_2022_country_questionnaire"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BATCH_SIZE = 25000

# === FUNÇÃO DE IMPORTAÇÃO ===
def importar_sav_em_lotes():
    print(f"📥 Iniciando importação de: {CAMINHO_ARQUIVO}")
    
    # Conexão com MongoDB
    client = MongoClient(MONGO_URI)
    db = client["pisa"]
    colecao = db[NOME_COLECAO]

    # Verificação de duplicatas
    total_existente = colecao.count_documents({})
    if total_existente > 0:
        print(f"📊 Documentos já existentes na coleção: {total_existente}")
        print("✅ Nada a importar. Todos os dados já estão no MongoDB.")
        client.close()
        return

    # Leitura do arquivo .SAV
    df = pd.read_spss(CAMINHO_ARQUIVO)
    total_registros = len(df)
    print(f"📄 Total de registros no arquivo: {total_registros}")

    for i in range(0, total_registros, BATCH_SIZE):
        fim = min(i + BATCH_SIZE, total_registros)
        lote = df.iloc[i:fim].to_dict(orient="records")
        colecao.insert_many(lote)
        print(f"  ✅ {fim:,} registros inseridos até {datetime.now().strftime('%H:%M:%S')}")

    print(f"✅ Finalizado: {NOME_COLECAO} com {total_registros:,} documentos.")
    client.close()
    print("🔒 Conexão com MongoDB encerrada.")

# === EXECUÇÃO ===
if __name__ == "__main__":
    importar_sav_em_lotes()

