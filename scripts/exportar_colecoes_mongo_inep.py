import os
import json
import pandas as pd
from pymongo import MongoClient

# Configuração
URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO = "relatorios_inep"
COLECOES = ["inep_2000", "inep_2003", "inep_2006", "inep_2009", "inep_2012", "inep_2015", "inep_2018", "inep_2022"]
PASTA_SAIDA = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/relatorios_inep"

# Conexão
client = MongoClient(URI)
db = client[BANCO]

# Geração de arquivos
for colecao in COLECOES:
    dados = list(db[colecao].find({}, {"_id": 0}))  # Remove o campo _id
    if not dados:
        print(f"⚠️ Nenhum dado encontrado em {colecao}")
        continue
    
    json_path = os.path.join(PASTA_SAIDA, f"{colecao}.json")
    csv_path = os.path.join(PASTA_SAIDA, f"{colecao}.csv")

    # Exporta JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    # Exporta CSV
    try:
        df = pd.DataFrame(dados)
        df.index += 1  # Começa do 1
        df.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"❌ Erro ao exportar CSV para {colecao}: {e}")
        continue

    print(f"✅ Exportado: {colecao} → JSON + CSV")

client.close()

