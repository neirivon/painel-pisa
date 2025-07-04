# scripts/importar_cognitive_item_2009_spss.py

import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# === Configurações ===
ARQUIVO_TEXTO = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/INT_COG09_TD_DEC11.txt"
ARQUIVO_LAYOUT = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/PISA2009_SPSS_cognitive_item.txt"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "pisa"
COLECAO = "pisa_2009_cognitive_item"

# === Função para ler layout SPS ===
def ler_layout_sps(arquivo_layout):
    colspecs = []
    nomes = []
    with open(arquivo_layout, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("*") or linha.startswith("DATA LIST"):
                continue
            partes = linha.split()
            if len(partes) >= 4:
                nome = partes[0]
                ini_fim = partes[1]
                if "-" in ini_fim:
                    ini, fim = ini_fim.split("-")
                    colspecs.append((int(ini)-1, int(fim)))
                    nomes.append(nome)
    return colspecs, nomes

# === Conectar ao MongoDB ===
cliente = MongoClient(MONGO_URI)
db = cliente[BANCO]
db[COLECAO].drop()

# === Ler layout e arquivo de dados ===
try:
    colspecs, nomes = ler_layout_sps(ARQUIVO_LAYOUT)
    if not colspecs or not nomes:
        raise ValueError("❌ SPS inválido: nenhum campo lido")
    df = pd.read_fwf(ARQUIVO_TEXTO, colspecs=colspecs, names=nomes, encoding="latin1")
    df = df.fillna("")  # Limpar NaNs
    registros = df.to_dict(orient="records")
    db[COLECAO].insert_many(registros)
    print(f"✅ Importado com sucesso: {len(registros)} registros para '{COLECAO}'")
except Exception as e:
    print(f"❌ Erro ao importar '{ARQUIVO_TEXTO}': {e}")
finally:
    cliente.close()

