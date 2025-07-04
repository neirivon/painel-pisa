# utilos.path.join(s, "e")xtrair_escs_pisa2000_v3.py

import pandas as pd
import os
import json
from pymongo import MongoClient

# Configurações
CAMINHO_SAV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")Aos.path.join(V, "E")SCS_PISA2000.sav"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_JSON_SAIDA = "pisa2000_student_escs.json"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "pisa"
COLECAO = "pisa2000_student_escs"

def extrair_escs_pisa2000():
    print("🔍 Carregando arquivo SAV...")
    df = pd.read_spss(CAMINHO_SAV)
    print("✅ Arquivo carregado.")

    # Mostrar todas as colunas reais para debug
    print("🔎 Colunas detectadas:", df.columns.tolist())

    # Detectar nomes de colunas de forma flexível
    col_country = next((c for c in df.columns if c.lower() in ["cnt", "country"]), None)
    col_schoolid = next((c for c in df.columns if "schoolid" in c.lower()), None)
    col_studentid = next((c for c in df.columns if "stidstd" in c.lower()), None)
    col_escs = next((c for c in df.columns if "escs" in c.lower()), None)

    if None in [col_country, col_schoolid, col_studentid, col_escs]:
        raise Exception("❌ Erro: Não foi possível detectar todas as colunas essenciais automaticamente.")

    print(f"✅ Mapeamento: País: {col_country} | Escola: {col_schoolid} | Estudante: {col_studentid} | ESCS: {col_escs}")

    resultados = []
    for idx, linha in df.iterrows():
        registro = {
            "pais_codigo": str(linha[col_country]).strip() if not pd.isna(linha[col_country]) else None,
            "escola_id": str(linha[col_schoolid]).strip() if not pd.isna(linha[col_schoolid]) else None,
            "estudante_id": str(linha[col_studentid]).strip() if not pd.isna(linha[col_studentid]) else None,
            "escs": float(linha[col_escs]) if not pd.isna(linha[col_escs]) else None,
            "ano": 2000,
            "origem": "SPSS_OFICIAL"
        }
        resultados.append(registro)

        if idx > 0 and idx % 10000 == 0:
            print(f"📈 {idx} registros processados...")

    print(f"✅ Total de registros extraídos: {len(resultados)}")

    # Salvar JSON para auditoria
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    caminho_saida = os.path.join(PASTA_SAIDA, ARQUIVO_JSON_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON salvo em {caminho_saida}")

    # Salvar no MongoDB
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[COLECAO]

    colecao.delete_many({})
    colecao.insert_many(resultados)
    client.close()

    print(f"✅ Coleção MongoDB '{COLECAO}' atualizada com sucesso!")

if __name__ == "__main__":
    extrair_escs_pisa2000()

