import os
import json
from pymongo import MongoClient
import pandas as pd

# 🚀 Conexão com MongoDB local
print("🔗 Conectando ao MongoDB local...")
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# 🔎 Localizando coleções de alunos (exceto PfD)
colecoes = [c for c in db.list_collection_names() if "stu" in c and "pfd" not in c]

dados_resultado = []

for col in sorted(colecoes):
    print(f"📥 Processando coleção: {col}")

    dados = list(db[col].find({
        "CNT": {"$exists": True},
        "PV1READ": {"$exists": True},
        "PV1MATH": {"$exists": True},
        "PV1SCIE": {"$exists": True}
    }, {"CNT": 1, "PV1READ": 1, "PV1MATH": 1, "PV1SCIE": 1}))

    if not dados:
        print(f"⚠️ Nenhum dado válido encontrado para {col}. Pulando...")
        continue

    df = pd.DataFrame(dados)
    df["PV1READ"] = pd.to_numeric(df["PV1READ"], errors="coerce")
    df["PV1MATH"] = pd.to_numeric(df["PV1MATH"], errors="coerce")
    df["PV1SCIE"] = pd.to_numeric(df["PV1SCIE"], errors="coerce")

    df_media = df.groupby("CNT")[["PV1READ", "PV1MATH", "PV1SCIE"]].mean().dropna()
    df_media = df_media.sort_values(by="PV1READ", ascending=False)

    ano = col.split("_")[1] if "_" in col else "desconhecido"
    top5 = df_media.head(5)

    if "Brazil" in df_media.index:
        brasil = df_media.loc[["Brazil"]]
    else:
        print(f"❌ Dados do Brasil não encontrados em {col}")
        brasil = pd.DataFrame(columns=df_media.columns)

    df_final = pd.concat([top5, brasil])
    df_final["País"] = df_final.index
    df_final = df_final.reset_index(drop=True)
    df_final["Ano"] = int(ano)

    dados_resultado.extend(df_final.to_dict(orient="records"))
    print(f"✅ Edição {ano}: {len(df_final)} registros adicionados.")

# 💾 Salvando JSON final
os.makedirs("painel_pisa/dados_cloud", exist_ok=True)
caminho_saida = "painel_pisa/dados_cloud/comparativo_brasil_top5_pisa.json"

with open(caminho_saida, "w", encoding="utf-8") as f:
    json.dump(dados_resultado, f, ensure_ascii=False, indent=2)

# 🔒 Encerrando conexão
client.close()
print("🔌 Conexão com MongoDB encerrada.")
print(f"📁 Arquivo salvo em: {caminho_saida}")
print("✅ Processo concluído com sucesso.")

