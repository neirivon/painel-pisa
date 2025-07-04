# utilos.path.join(s, "e")xtrair_mapeamento_subnatio_pisa2000_v2.py

import pandas as pd
import os
from pymongo import MongoClient

# Caminhos
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSos.path.join(S, "P")ISA2000_SPSS_school_questionnaire.txt"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_SAIDA_JSON = "pisa2000_school_subnatio.json"

# MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "pisa"
COLECAO = "pisa2000_school_subnatio"

def extrair_mapeamento_subnatio():
    print("🔍 Lendo arquivo escolar para detectar SUBNATIO...")

    # Lendo somente os campos fixos: COUNTRY (2-4), SCHOOLID (5-9), SUBNATIO (11-12)
    colspecs = [(1, 4), (4, 9), (10, 12)]  # Atenção: Python indexa do zero, por isso 1-4 etc.
    nomes_colunas = ["country", "schoolid", "subnatio"]

    df = pd.read_fwf(CAMINHO_ARQUIVO, colspecs=colspecs, names=nomes_colunas, encoding="latin1")

    print(f"✅ Arquivo carregado: {len(df)} registros.")

    # Filtrar apenas escolas do Brasil (country == 'BRA')
    df_brasil = df[df["country"] == "BRA"]

    print(f"✅ Total de escolas brasileiras encontradas: {len(df_brasil)}")

    # Montar lista para salvar
    registros = []
    for _, linha in df_brasil.iterrows():
        registro = {
            "pais_codigo": linha["country"],
            "escola_id": str(linha["schoolid"]).zfill(5),
            "subnatio_codigo": str(linha["subnatio"]).zfill(2),
            "ano": 2000,
            "origem": "SPSS_OFICIAL"
        }
        registros.append(registro)

    # Garantir que pasta de saída exista
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    # Salvar JSON
    caminho_saida = os.path.join(PASTA_SAIDA, ARQUIVO_SAIDA_JSON)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        import json
        json.dump(registros, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON salvo em {caminho_saida}")

    # Inserir no MongoDB
    if registros:
        client = MongoClient(MONGO_URI)
        db = client[BANCO]
        db[COLECAO].delete_many({})  # Limpar se existir
        db[COLECAO].insert_many(registros)
        client.close()
        print(f"✅ Coleção MongoDB '{COLECAO}' atualizada com sucesso!")
    else:
        print("⚠️ Nenhum registro brasileiro para inserir.")

if __name__ == "__main__":
    extrair_mapeamento_subnatio()

