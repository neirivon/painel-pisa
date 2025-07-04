# scriptos.path.join(s, "c")onverter_csv_para_json_blindado.py

import pandas as pd
import numpy as np
import json
import math
import os

from jsonschema import validate, ValidationError

CAMINHO_CSV = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_por_pais_por_item_pisa2022.csv"
CAMINHO_JSON = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "m")edias_pais_item_escs_2022.json"

def limpar_valor(v):
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    if isinstance(v, (np.float64, np.float32, np.float16)):
        return round(float(v), 6)
    return v

print("📥 Lendo CSV com pandas...")
df = pd.read_csv(CAMINHO_CSV, dtype=str).applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.replace(["nan", "NaN", "NAN", "inf", "-inf", "None", "NULL"], None, inplace=True)

print("🔍 Convertendo colunas numéricas...")
for col in df.columns:
    if col != "pais":
        df[col] = pd.to_numeric(df[col], errors="coerce")

print("🧹 Limpeza linha a linha...")
registros = []
for idx, row in df.iterrows():
    item = {}
    for col, val in row.items():
        item[col] = limpar_valor(val)
    registros.append(item)

print("✅ Total de registros limpos:", len(registros))

# Validação mínima com JSON Schema (opcional, mas radicalmente seguro)
print("🛡️ Validando estrutura básica dos dados...")

esquema_basico = {
    "type": "object",
    "properties": {
        "pais": {"type": "string"},
    },
    "required": ["pais"]
}

try:
    for doc in registros[:5]:  # valida apenas os primeiros
        validate(instance=doc, schema=esquema_basico)
except ValidationError as e:
    print("❌ Erro de estrutura:", e.message)
    exit(1)

print(f"💾 Exportando para: {CAMINHO_JSON}")
with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=2, allow_nan=False)

print("🏁 Exportação finalizada com sucesso. JSON 100% compatível.")

