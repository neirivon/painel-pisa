# scripts/importar_microdados_stu_cog_2022_checkpoint.py

import os
import gc
import datetime
from pymongo import MongoClient
import pyreadstat

# === CONFIGURAÇÃO ===
CAMINHO_ARQUIVO = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/SAV/CY08MSP_STU_COG.SAV"
NOME_COLECAO = "pisa_2022_student_cog"
BLOCO = 25000  # Tamanho do chunk
URI_MONGO = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
NOME_BANCO = "pisa"

# === CONEXÃO COM MONGO ===
client = MongoClient(URI_MONGO)
db = client[NOME_BANCO]
colecao = db[NOME_COLECAO]

# === CONTADOR GLOBAL ===
total_inseridos = colecao.count_documents({})

print(f"📥 Iniciando importação de: {CAMINHO_ARQUIVO}")
print(f"📊 Documentos já existentes na coleção: {total_inseridos}")

# === IMPORTAÇÃO POR BLOCOS ===
try:
    reader = pyreadstat.read_file_in_chunks(pyreadstat.read_sav, CAMINHO_ARQUIVO, chunksize=BLOCO)
    for i, (df, meta) in enumerate(reader):
        registros = df.to_dict(orient="records")
        colecao.insert_many(registros)
        total_inseridos += len(registros)
        horario = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"  ✅ {total_inseridos:,} registros inseridos até {horario}")
        del registros, df
        gc.collect()
except Exception as e:
    print(f"❌ ERRO durante importação: {e}")
finally:
    print(f"🔒 Conexão com MongoDB encerrada.")
    client.close()

