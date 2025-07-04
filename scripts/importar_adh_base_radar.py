# scriptos.path.join(s, "i")mportar_adh_base_radar.py

import pandas as pd
from pymongo import MongoClient
import os

# === Caminho do arquivo CSV ===
caminho_csv = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "A")DH_BASE_RADAR_2012-202os.path.join(1, "A")DH_BASE_RADAR_2012-2021(COR_B).csv"))

# === Conexão MongoDB ===
mongo_uri = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
nome_banco = "indicadores"
nome_colecao = "adh_base_radar"

# === Leitura do CSV ===
print(f"📂 Lendo CSV: {caminho_csv}")
df = pd.read_csv(caminho_csv, sep=';', encoding='latin1')

# Verificar se há coluna de código de município
possiveis_codigos = [col for col in df.columns if "cod" in col.lower()]
print("🔍 Colunas com código encontradas:", possiveis_codigos)

# Padronizar nome da coluna de código de município, se existir
for nome in possiveis_codigos:
    if "mun" in nome.lower():
        df.rename(columns={nome: "CD_MUNICIPIO"}, inplace=True)
        break

# === Inserção no MongoDB ===
client = MongoClient(mongo_uri)
db = client[nome_banco]
colecao = db[nome_colecao]

colecao.drop()  # Limpar coleção antiga
colecao.insert_many(df.to_dict(orient="records"))

print(f"✅ {len(df)} documentos inseridos em '{nome_colecao}' no banco '{nome_banco}'.")
client.close()

