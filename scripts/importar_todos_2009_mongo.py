# scripts/importar_todos_2009_mongo.py

import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
BANCO = "pisa"

PASTA_SAS = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SAS"
PASTA_TXT = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/TXT"
PASTA_SAIDA = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/2009"

ARQUIVOS = [
    ("PISA2009_SAS_scored_cognitive_item.sas", "ERA_COG09_S_June11.txt", "pisa_2009_score_cognitive_item"),
    ("PISA2009_SAS_cognitive_item.sas",        "ERA_COG09_TD_June11.txt", "pisa_2009_cognitive_item"),
    ("PISA2009_SAS_school.sas",                "ERA_SCQ09_June11.txt",    "pisa_2009_school"),
    ("PISA2009_SAS_student.sas",               "ERA_STQ09_June11.txt",    "pisa_2009_student"),
]

def extrair_mascara(sas_path):
    col_specs = []
    col_names = []
    with open(sas_path, encoding="latin1") as f:
        for linha in f:
            if "INPUT" in linha or "input" in linha:
                continue
            partes = linha.strip().replace(';', '').split()
            if len(partes) >= 3 and partes[1].isdigit() and '-' in partes[1]:
                nome = partes[0]
                ini, fim = partes[1].split('-')
                col_names.append(nome)
                col_specs.append((int(ini) - 1, int(fim)))
    return col_names, col_specs

def importar_arquivo(txt_path, sas_path, nome_colecao):
    print(f"\n📂 Importando: {os.path.basename(txt_path)} → coleção '{nome_colecao}'")
    try:
        col_names, col_specs = extrair_mascara(sas_path)
        df = pd.read_fwf(txt_path, names=col_names, colspecs=col_specs, encoding="latin1")
        df["importado_em"] = datetime.utcnow()

        # Exportar CSV e JSON para nuvem
        os.makedirs(PASTA_SAIDA, exist_ok=True)
        csv_path = os.path.join(PASTA_SAIDA, f"{nome_colecao}.csv")
        json_path = os.path.join(PASTA_SAIDA, f"{nome_colecao}.json")

        df.to_csv(csv_path, index=False)
        df.to_json(json_path, orient="records", force_ascii=False)

        # Enviar para MongoDB
        docs = df.to_dict(orient="records")
        client[BANCO][nome_colecao].delete_many({})
        client[BANCO][nome_colecao].insert_many(docs)
        print(f"✅ {len(docs)} registros inseridos com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao importar '{txt_path}': {e}")

def main():
    global client
    client = MongoClient(MONGO_URI)

    for sas_file, txt_file, nome_colecao in ARQUIVOS:
        sas_path = os.path.join(PASTA_SAS, sas_file)
        txt_path = os.path.join(PASTA_TXT, txt_file)
        importar_arquivo(txt_path, sas_path, nome_colecao)

    client.close()
    print("\n🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    main()

