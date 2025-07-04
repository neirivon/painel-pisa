from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
import numpy as np
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
df_clean = df[np.isfinite(df["ESCS15"])]
df_clean = df_clean[np.isfinite(df_clean["PV1MATH"])]
df_clean = df_clean[np.isfinite(df_clean["PV1READ"])]
df_clean = df_clean[np.isfinite(df_clean["PV1SCIE"])]
print(f"✅ Registros após limpeza: {len(df_clean)}")

# Exportar JSON
print("💾 Exportando para JSON...")
df_clean.to_json("pisa_pfd_alunos_limpo.json", orient="records", lines=True)
print("📁 Arquivo gerado: pisa_pfd_alunos_limpo.json")

# Agrupamentos
print("📊 Calculando média de ESCS15 por gênero...")
print(df_clean.groupby("ST004D01T")["ESCS15"].mean())

print("\n🏫 Média de ESCS15 por escola (5 primeiras):")
print(df_clean.groupby("CNTSCHID")["ESCS15"].mean().head())

print("\n🌍 Média de ESCS15 por país:")
print(df_clean.groupby("CNT")["ESCS15"].mean())

# Correlações
print("\n📈 Correlações entre ESCS15 e PVs:")
print(df_clean[["ESCS15", "PV1MATH", "PV1READ", "PV1SCIE"]].corr()["ESCS15"])

# Gráficos
print("📊 Gerando histograma de ESCS15...")
sns.histplot(df_clean["ESCS15"], bins=50, kde=True)
plt.title("Distribuição do ESCS15 (PISA PfD)")
plt.xlabel("ESCS15")
plt.ylabel("Frequência")
plt.grid(True)
plt.savefig("escs15_histograma.png")
plt.close()
print("📁 Arquivo gerado: escs15_histograma.png")

print("📊 Gerando gráfico de dispersão ESCS15 vs PV1MATH...")
sns.scatterplot(data=df_clean, x="ESCS15", y="PV1MATH", alpha=0.3)
plt.title("Dispersão: ESCS15 vs PV1MATH")
plt.xlabel("ESCS15")
plt.ylabel("PV1MATH")
plt.grid(True)
plt.savefig("escs15_vs_pv1math.png")
plt.close()
print("📁 Arquivo gerado: escs15_vs_pv1math.png")

client.close()
print("\n✅ JSON, gráficos e análises geradas com sucesso.")

