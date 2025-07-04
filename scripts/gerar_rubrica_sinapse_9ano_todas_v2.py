from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import json
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# Arquivos de entrada das três disciplinas
arquivos = {
    "matematica": "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_matematica_v1.json",
    "lp": "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_lingua_portuguesa_v1.json",
    "ciencias": "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_ciencias_v1.json"
}

# Carregar os dados
rubricas_unificadas = []
for nome, caminho in arquivos.items():
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
        for d in dados:
            d["timestamp_versao"] = datetime.utcnow()
        rubricas_unificadas.extend(dados)

# Salvar como JSON
os.makedirs("dados_processadoos.path.join(s, "b")ncc", exist_ok=True)
json_path = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v2.json"
with open(json_path, "w", encoding="utf-8") as jf:
    json.dump(rubricas_unificadas, jf, ensure_ascii=False, indent=2, default=str)

# Salvar como CSV (removendo colunas com tipos não suportados)
df = pd.DataFrame(rubricas_unificadas)
df["timestamp_versao"] = df["timestamp_versao"].astype(str)
csv_path = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v2.csv"
df.to_csv(csv_path, index=False)

# Inserir no MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
db["sinapse_9ano_todas"].drop()  # remover coleção anterior
db["sinapse_9ano_todas"].insert_many(rubricas_unificadas)
client.close()

print("✅ Rubrica SINAPSE unificada V2 gerada e armazenada com sucesso.")
print(f"📄 JSON: {json_path}")
print(f"📄 CSV:  {csv_path}")
print("🌐 MongoDB: rubricas.sinapse_9ano_todas")

