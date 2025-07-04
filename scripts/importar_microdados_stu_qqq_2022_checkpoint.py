# salvar como: importar_microdados_stu_qqq_2022_checkpoint.py
import os
import pandas as pd
import pyreadstat
from pymongo import MongoClient
import gc
from datetime import datetime

# Configurações
CAMINHO_ARQUIVO = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/SAV/CY08MSP_STU_QQQ.SAV"
NOME_COLECAO = "pisa_2022_student_qqq"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
TAMANHO_LOTE = 25000

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client["pisa"]
colecao = db[NOME_COLECAO]

# Verificar documentos existentes
total_existente = colecao.count_documents({})
print(f"📥 Iniciando importação de: {CAMINHO_ARQUIVO}")
print(f"📊 Documentos já existentes na coleção: {total_existente}")

# Leitura e inserção fragmentada
chunk_size = TAMANHO_LOTE
rows_lidos = 0

for df, meta in pyreadstat.read_file_in_chunks(pyreadstat.read_sav, CAMINHO_ARQUIVO, chunksize=chunk_size):
    if rows_lidos < total_existente:
        rows_lidos += len(df)
        continue

    documentos = df.to_dict(orient="records")
    colecao.insert_many(documentos)
    rows_lidos += len(documentos)
    tempo = datetime.now().strftime("%H:%M:%S")
    print(f"  ✅ {rows_lidos:,} registros inseridos até {tempo}")
    gc.collect()

client.close()
print("🔒 Conexão com MongoDB encerrada.")

