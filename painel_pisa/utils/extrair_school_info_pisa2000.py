# utilos.path.join(s, "e")xtrair_school_info_pisa2000.py

import os
import json
import pandas as pd
from pymongo import MongoClient

# Configurações
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSos.path.join(S, "P")ISA2000_SPSS_school_questionnaire.txt"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "pisa"
COLECAO = "pisa2000_school_info"
CAMINHO_SAIDA_JSON = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoeos.path.join(s, "p")isa2000_school_info.json"

def extrair_school_info():
    print("🔍 Lendo arquivo SPSS escolar...")

    # >>> REMOVER widths="infer" <<<
    df = pd.read_fwf(CAMINHO_ARQUIVO, encoding="latin1")

    print(f"✅ Arquivo carregado com {len(df)} registros.")

    # Detectar colunas disponíveis
    colunas = df.columns.tolist()
    print(f"🔎 Colunas detectadas: {colunas}")

    # Procurar as colunas certas
    col_country = next((col for col in colunas if col.lower() in ["country", "cnt"]), None)
    col_schoolid = next((col for col in colunas if col.lower() == "schoolid"), None)
    col_subnatio = next((col for col in colunas if col.lower() == "subnatio"), None)

    if not all([col_country, col_schoolid, col_subnatio]):
        raise Exception("Erro: Não foi possível detectar COUNTRY, SCHOOLID e SUBNATIO no arquivo.")

    # Estruturar registros
    registros = []
    for _, linha in df.iterrows():
        registro = {
            "pais_codigo": str(linha[col_country]).strip(),
            "escola_id": str(linha[col_schoolid]).zfill(5),
            "subnatio": str(linha[col_subnatio]).zfill(2),
            "ano": 2000,
            "origem": "SPSS_SCHOOL"
        }
        registros.append(registro)

    print(f"📈 {len(registros)} registros estruturados.")

    # Salvar JSON
    with open(CAMINHO_SAIDA_JSON, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=4)
    print(f"✅ JSON salvo em {CAMINHO_SAIDA_JSON}")

    # Salvar no MongoDB
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[COLECAO]
    colecao.delete_many({})
    colecao.insert_many(registros)
    client.close()
    print(f"✅ Coleção MongoDB '{COLECAO}' atualizada com sucesso!")

if __name__ == "__main__":
    extrair_school_info()

