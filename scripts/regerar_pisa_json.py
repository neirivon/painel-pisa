from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
import numpy as np
from pymongo import MongoClient

print("🔌 Conectando ao MongoDB...")
client = conectar_mongo(nome_banco="saeb")[1]
col = client.pisa.pisa_pfd_alunos

print("📦 Carregando dados da coleção...")
campos = {
    "ESCS15": 1, "ST004D01T": 1, "CNTSCHID": 1, "CNT": 1,
    "PV1MATH": 1, "PV1READ": 1, "PV1SCIE": 1, "_id": 0
}
df = pd.DataFrame(list(col.find({}, campos)))
print(f"📊 Registros carregados: {len(df)}")

print("🧹 Limpando NaNs e registros inválidos...")
df_clean = df[
    np.isfinite(df["ESCS15"]) &
    np.isfinite(df["PV1MATH"]) &
    np.isfinite(df["PV1READ"]) &
    np.isfinite(df["PV1SCIE"])
]
print(f"✅ Registros após limpeza: {len(df_clean)}")

print("💾 Exportando JSON...")
df_clean.to_json("pisa_pfd_alunos_limpo.json", orient="records", lines=True)
print("📁 Arquivo gerado: pisa_pfd_alunos_limpo.json")

client.close()

