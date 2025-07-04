# utilos.path.join(s, "e")xtrair_escs_pisa2000.py

import os
import json
import pandas as pd
import pyreadstat
from pymongo import MongoClient

# Configurações
ARQUIVO_SAV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")Aos.path.join(V, "E")SCS_PISA2000.sav"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "pisa"
COLECAO = "pisa_escs_2000"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_JSON_SAIDA = "pisa_escs_2000.json"

def extrair_escs_pisa2000():
    print("🔍 Carregando arquivo SAV...")
    df, meta = pyreadstat.read_sav(ARQUIVO_SAV)

    print("✅ Arquivo carregado.")
    print(f"🔢 Número de registros: {len(df)}")

    # Detecta as colunas certas
    colunas = [col.lower() for col in df.columns]
    col_country = next((c for c in colunas if "country" in c or "cnt" in c), None)
    col_schoolid = next((c for c in colunas if "schoolid" in c), None)
    col_stidstd = next((c for c in colunas if "stidstd" in c), None)
    col_escs = next((c for c in colunas if "escs" in c or "esci" in c), None)

    if not all([col_country, col_schoolid, col_stidstd, col_escs]):
        raise Exception("🚨 Não encontrei todas as colunas necessárias automaticamente!")

    print(f"🔎 Detecção automática de colunas:\n- Country: {col_country}\n- SchoolID: {col_schoolid}\n- StudentID: {col_stidstd}\n- ESCS: {col_escs}")

    # Normaliza os dados
    dados = []
    for _, linha in df.iterrows():
        doc = {
            "pais_codigo": int(linha[col_country]) if not pd.isna(linha[col_country]) else None,
            "school_id": str(linha[col_schoolid]).strip() if not pd.isna(linha[col_schoolid]) else None,
            "student_id": str(linha[col_stidstd]).strip() if not pd.isna(linha[col_stidstd]) else None,
            "escs": float(linha[col_escs]) if not pd.isna(linha[col_escs]) else None,
            "ano": 2000,
            "origem": "ESCS_PISA2000.sav"
        }
        dados.append(doc)

    # Salva JSON
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    caminho_json = os.path.join(PASTA_SAIDA, ARQUIVO_JSON_SAIDA)
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON salvo em: {caminho_json}")

    # Salva MongoDB
    print("🚀 Inserindo dados no MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[COLECAO]
    colecao.drop()  # Zera antes de importar
    colecao.insert_many(dados)
    client.close()

    print(f"✅ Coleção '{COLECAO}' atualizada no MongoDB com sucesso!")

if __name__ == "__main__":
    extrair_escs_pisa2000()

