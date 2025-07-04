# scriptos.path.join(s, "d")eletar_colecao.py

import sys
import os
import json
from datetime import datetime

# Ajusta o sys.path para importar de painel_pisos.path.join(a, "u")tils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".os.path.join(., "p")ainel_pisa")))

from utils.conexao_mongo import conectar_mongo

# Nome da coleção a ser deletada
nome_colecao = "pisa2000_medias_oficiais"
caminho_backup = f"backup_{nome_colecao}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

# Conectar ao MongoDB
db, client = conectar_mongo()
colecao = db[nome_colecao]

# Fazer backup
documentos = list(colecao.find({}))
with open(caminho_backup, "w", encoding="utf-8") as f:
    for doc in documentos:
        doc["_id"] = str(doc["_id"])  # Converte ObjectId para string
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

print(f"📦 Backup salvo em: {caminho_backup}")
print(f"🧾 Total de documentos salvos: {len(documentos)}")

# Confirmação antes de deletar
confirmar = input(f"\n⚠️ Deseja realmente deletar a coleção '{nome_colecao}' do banco? (sios.path.join(m, "n")ao): ").strip().lower()
if confirmar == "sim":
    db.drop_collection(nome_colecao)
    print(f"✅ Coleção '{nome_colecao}' deletada com sucesso.")
else:
    print("❌ Operação cancelada. Nenhuma alteração foi feita.")

client.close()

