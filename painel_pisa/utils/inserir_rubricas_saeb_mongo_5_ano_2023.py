# inserir_rubricas_saeb_mongo_5_ano_2023.py

import json
from utils.conexao_mongo import conectar_mongo

# === Nome da coleção e caminho do JSON ===
NOME_COLECAO = "rubricas_saeb"
CAMINHO_JSON = "rubricas_saeb_complementadas.json"

# === Conectar ao MongoDB usando função reutilizável ===
db, client = conectar_mongo(nome_banco="saeb")
colecao = db[NOME_COLECAO]

# === Carregar dados do JSON ===
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    rubricas = json.load(f)

# === Inserir no MongoDB ===
try:
    resultado = colecao.insert_many(rubricas)
    print(f"✅ {len(resultado.inserted_ids)} rubricas inseridas na coleção '{NOME_COLECAO}' do banco 'saeb'.")
finally:
    client.close()

