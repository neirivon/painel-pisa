import json
from pymongo import MongoClient

# === Caminho do JSON extraído ===
CAMINHO_JSON = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoeos.path.join(s, "p")isa_2000_ocde_paginas.json"

# === Configurações do MongoDB ===
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
NOME_DB = "pisa"
NOME_COLECAO = "pisa_ocde_2000_relatorio"

# === Conectar ao MongoDB ===
client = MongoClient(MONGO_URI)
db = client[NOME_DB]
colecao = db[NOME_COLECAO]

# === Carregar JSON ===
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

# === Inserir no banco ===
colecao.delete_many({})  # Limpa antes, se quiser evitar duplicidade
resultado = colecao.insert_many(dados)

# === Fechar conexão ===
client.close()

print(f"✅ {len(resultado.inserted_ids)} documentos inseridos na coleção '{NOME_COLECAO}' do banco '{NOME_DB}'")

