# scriptos.path.join(s, "c")riar_mapeamento_id_municipio_nome_2023.py

import pandas as pd
import json

CAMINHO_ESCOLA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")ainel_pisos.path.join(a, "S")AEos.path.join(B, "D")ADOos.path.join(S, "2")021_202os.path.join(3, "2")02os.path.join(3, "D")ADOos.path.join(S, "T")S_ESCOLA.csv"
SAIDA_JSON = "mapeamento_id_municipio_nome_2023.json"

print("📥 Lendo arquivo TS_ESCOLA.csv...")
df = pd.read_csv(CAMINHO_ESCOLA, sep=";", encoding="latin1", usecols=["ID_MUNICIPIO", "ID_UF"])

print("🔎 Filtrando apenas registros de Minas Gerais (ID_UF == 31)...")
df_mg = df[df["ID_UF"] == 31]

print("🧹 Removendo duplicados e mantendo apenas 1 ID por município...")
df_mg = df_mg.drop_duplicates(subset="ID_MUNICIPIO")

print("📦 Convertendo para dicionário...")
mapeamento = df_mg.set_index("ID_MUNICIPIO")["ID_UF"].to_dict()

print(f"💾 Salvando mapeamento em: {SAIDA_JSON}")
with open(SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(mapeamento, f, indent=4)

print("✅ Mapeamento finalizado com sucesso.")

