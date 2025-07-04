# scriptos.path.join(s, "c")onverter_csv_para_json_2022.py

import pandas as pd
import json
import numpy as np
import math

CAMINHO_CSV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_por_pais_por_item_pisa2022.csv"
CAMINHO_JSON = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_pais_item_escs_2022.json"

def limpar_valor(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v

print("📥 Lendo arquivo CSV...")
df = pd.read_csv(CAMINHO_CSV)

print("🧹 Limpando profundamente NaNs e valores fora do JSON...")
registros = []
linhas_afetadas = 0

for _, linha in df.iterrows():
    registro_limpo = {}
    for coluna, valor in linha.items():
        novo_valor = limpar_valor(valor)
        if novo_valor is None and pd.notnull(valor):
            linhas_afetadas += 1
        registro_limpo[coluna] = novo_valor
    registros.append(registro_limpo)

print(f"🧼 Linhas com valores substituídos por None: {linhas_afetadas}")

print(f"💾 Salvando JSON final em: {CAMINHO_JSON}")
with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=2, allow_nan=False)

print("✅ Conversão finalizada com sucesso. JSON 100% validado.")

