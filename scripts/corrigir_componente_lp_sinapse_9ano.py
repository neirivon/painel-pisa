from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "c")orrigir_componente_lp_sinapse_9ano.py

import pandas as pd
from pymongo import MongoClient

# 📥 Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["sinapse_9ano_lingua_portuguesa"]

# 📤 Coleta os dados
dados = list(colecao.find({}, {"_id": 0}))
df = pd.DataFrame(dados)

# ✅ Correção direta da coluna 'componente'
df["componente"] = "Língua Portuguesa"

# 🔄 Sobrescreve a coleção corrigida
colecao.delete_many({})
colecao.insert_many(df.to_dict(orient="records"))

# 💾 Exporta para JSON e CSV
df.to_json("dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_lingua_portuguesa_v1_corrigido.json", orient="records", indent=2, force_ascii=False)
df.to_csv("dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_lingua_portuguesa_v1_corrigido.csv", index=False)

# ✅ Fecha conexão com o MongoDB
client.close()

print("✅ Componente 'Língua Portuguesa' corrigido com sucesso.")

