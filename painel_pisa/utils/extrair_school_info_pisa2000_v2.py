# utilos.path.join(s, "e")xtrair_school_info_pisa2000_v2.py

import pandas as pd
import os
import json
from pymongo import MongoClient

# Configurações
CAMINHO_ARQUIVO = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSos.path.join(S, "P")ISA2000_SPSS_school_questionnaire.txt"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLECAO = "pisa2000_school_info"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_JSON = "pisa2000_school_info.json"

def extrair_school_info():
    print("🔍 Lendo arquivo SPSS escolar...")
    
    # Como o TXT é uma transcrição livre do SPSS, vamos ler como texto puro
    with open(CAMINHO_ARQUIVO, "r", encoding="latin1") as f:
        linhas = f.readlines()

    escolas = []

    for linha in linhas:
        linha = linha.strip()
        
        # Filtro para pegar apenas linhas que contenham SCHOOLID e SUBNATIO
        # Padrão típico: "  BRA  01001  31"  (país, schoolid, subnatio)
        partes = linha.split()
        
        if len(partes) >= 3:
            pais_codigo = partes[0]
            escola_id = partes[1]
            subnatio = partes[2]

            # Só queremos Brasil por enquanto
            if pais_codigo == "BRA":
                escolas.append({
                    "pais_codigo": pais_codigo,
                    "escola_id": escola_id,
                    "subnatio": subnatio,
                    "ano": 2000,
                    "origem": "SPSS_OFICIAL"
                })

    print(f"✅ Total de escolas brasileiras encontradas: {len(escolas)}")

    # Salvando JSON para auditoria
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
    
    caminho_json = os.path.join(PASTA_SAIDA, ARQUIVO_JSON)
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(escolas, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON salvo em {caminho_json}")

    # Salvando no MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    db[COLECAO].drop()  # Apaga coleção antiga, se houver
    db[COLECAO].insert_many(escolas)
    client.close()

    print(f"✅ Coleção MongoDB '{COLECAO}' atualizada com sucesso!")

if __name__ == "__main__":
    extrair_school_info()

