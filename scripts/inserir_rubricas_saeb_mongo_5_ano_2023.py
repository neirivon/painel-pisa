# inserir_rubricas_saeb_mongo_5_ano_2023.py

import json
import sys
from pathlib import Path

# Adiciona o diretório base ao sys.path (para acessar painel_pisa.utils)
sys.path.append(str(Path(__file__).resolve().parents[1]))

from painel_pisa.utils.conexao_mongo import conectar_mongo

# === Configuração ===
NOME_COLECAO = "rubricas_saeb"
CAMINHO_JSON = "rubricas_saeb_complementadas.json"

# === Conectar ao MongoDB usando função reutilizável ===
db, client = conectar_mongo(nome_banco="saeb")
colecao = db[NOME_COLECAO]

# === Carregar rubricas do JSON ===
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    rubricas = json.load(f)

# === Inserir no MongoDB ===
try:
    resultado = colecao.insert_many(rubricas)
    print(f"✅ {len(resultado.inserted_ids)} rubricas inseridas na coleção '{NOME_COLECAO}' do banco 'saeb'.")
finally:
    client.close()

