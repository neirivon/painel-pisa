# scripts/converter_schemas_para_csv.py

import os
import json
import pandas as pd

# Caminho onde estão os arquivos JSON de schema
PASTA_SCHEMAS = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT"
ARQUIVOS = [f for f in os.listdir(PASTA_SCHEMAS) if f.startswith("schema_") and f.endswith(".json")]

for nome_arquivo in ARQUIVOS:
    caminho_json = os.path.join(PASTA_SCHEMAS, nome_arquivo)
    try:
        with open(caminho_json, "r", encoding="utf-8") as f:
            schema = json.load(f)
        df = pd.DataFrame(schema)
        nome_csv = nome_arquivo.replace(".json", ".csv")
        caminho_csv = os.path.join(PASTA_SCHEMAS, nome_csv)
        df.to_csv(caminho_csv, index=False, encoding="utf-8")
        print(f"✅ CSV gerado: {nome_csv}")
    except Exception as e:
        print(f"❌ Erro ao converter {nome_arquivo}: {e}")

