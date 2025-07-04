# scripts/importar_sav_2022_em_blocos.py

import os
import pyreadstat
from pymongo import MongoClient
from tqdm import tqdm

# ==========================
# CONFIGURAÇÃO DO AMBIENTE
# ==========================
CAMINHO_SAV = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2022/SAV"
ARQUIVOS_SAV = {
    "pisa_2022_student": "CY08MSP_STU_QQQ.SAV",
    "pisa_2022_school":  "CY08MSP_SCH_QQQ.SAV",
    "pisa_2022_cog_s":   "CY08MSP_STU_COG.SAV",
    "pisa_2022_cog_t":   "CY08MSP_CRT_COG.SAV",
    "pisa_2022_teacher": "CY08MSP_TCH_QQQ.SAV"
}

# ================================
# CONEXÃO COM MONGODB DOCKERIZADO
# ================================
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# ============================
# FUNÇÃO PARA IMPORTAR EM LOTE
# ============================
def importar_em_blocos(nome_colecao, caminho_arquivo, batch_size=10000):
    print(f"\n📥 Lendo arquivo: {caminho_arquivo}")

    # Leitura completa (sem chunk nativo do pyreadstat), depois iteração em blocos
    df, meta = pyreadstat.read_sav(caminho_arquivo)
    total = len(df)
    print(f"📦 Total de registros: {total}")

    colecao = db[nome_colecao]
    colecao.drop()

    for i in tqdm(range(0, total, batch_size), desc=f"Inserindo em '{nome_colecao}'"):
        lote = df.iloc[i:i+batch_size].to_dict(orient="records")
        colecao.insert_many(lote)

    print(f"✅ Coleção '{nome_colecao}' importada com sucesso!\n")

# =======================
# EXECUÇÃO DO LOTE TODO
# =======================
for nome_colecao, nome_arquivo in ARQUIVOS_SAV.items():
    caminho = os.path.join(CAMINHO_SAV, nome_arquivo)
    if os.path.exists(caminho):
        importar_em_blocos(nome_colecao, caminho)
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho}")

# =======================
# FINALIZAÇÃO
# =======================
client.close()
print("🔒 Conexão com MongoDB encerrada.")

