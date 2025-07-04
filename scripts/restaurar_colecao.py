# scriptos.path.join(s, "r")estaurar_colecao.py

import sys
import os
import json
from bson import ObjectId

# Ajusta o sys.path para importar painel_pisos.path.join(a, "u")tils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".os.path.join(., "p")ainel_pisa")))

from utils.conexao_mongo import conectar_mongo

# Configurações
arquivo_backup = "backup_pisa2000_medias_oficiais_20250501_194210.json"  # Altere para o nome real do seu backup
nome_colecao_destino = "pisa2000_medias_oficiais"

# Conectar ao MongoDB
db, client = conectar_mongo()
colecao = db[nome_colecao_destino]

# Restaurar documentos
documentos = []
with open(arquivo_backup, "r", encoding="utf-8") as f:
    for linha in f:
        doc = json.loads(linha)
        # Você pode manter o _id original convertendo de volta, ou removê-lo
        # doc["_id"] = ObjectId(doc["_id"])  # Se quiser restaurar o mesmo _id
        doc.pop("_id", None)  # Se preferir gerar novos _id
        documentos.append(doc)

if documentos:
    resultado = colecao.insert_many(documentos)
    print(f"✅ {len(resultado.inserted_ids)} documentos restaurados na coleção '{nome_colecao_destino}'.")
else:
    print("⚠️ Nenhum documento foi encontrado no arquivo de backup.")

client.close()

