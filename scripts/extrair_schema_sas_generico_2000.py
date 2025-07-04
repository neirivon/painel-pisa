import re
import json
import csv
import os
import sys

# === CONFIGURAÇÃO ===
CAMINHO_SAS = sys.argv[1] if len(sys.argv) > 1 else "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SAS/PISA2000_SAS_student_mathematics.sas"
BASENAME = os.path.splitext(os.path.basename(CAMINHO_SAS))[0].lower().replace("pisa2000_sas_", "")
PASTA_OUT = os.path.dirname(CAMINHO_SAS)
JSON_OUT = os.path.join(PASTA_OUT, f"schema_{BASENAME}_2000.json")
CSV_OUT = os.path.join(PASTA_OUT, f"schema_{BASENAME}_2000.csv")

# === EXTRAÇÃO ===
schema = []
with open(CAMINHO_SAS, "r", encoding="latin1") as f:
    lines = f.readlines()

try:
    start_idx = next(i for i, l in enumerate(lines) if l.strip().lower().startswith("input"))
except StopIteration:
    print("❌ Bloco 'input' não encontrado.")
    sys.exit(1)

for line in lines[start_idx + 1:]:
    if not line.strip() or line.lower().startswith("value") or ";" in line:
        break
    match = re.match(r"(\w+)\s+(\$)?(\d+)-(\d+)", line.strip())
    if match:
        nome, tipo, inicio, fim = match.groups()
        schema.append({
            "nome": nome,
            "tipo": "string" if tipo == "$" else "numerico",
            "inicio": int(inicio),
            "fim": int(fim)
        })

if not schema:
    print("❌ Nenhuma variável extraída.")
    sys.exit(1)

# === SALVANDO ===
with open(JSON_OUT, "w", encoding="utf-8") as fjson:
    json.dump(schema, fjson, indent=2, ensure_ascii=False)

with open(CSV_OUT, "w", encoding="utf-8", newline="") as fcsv:
    writer = csv.DictWriter(fcsv, fieldnames=["nome", "tipo", "inicio", "fim"])
    writer.writeheader()
    writer.writerows(schema)

print(f"✅ JSON gerado: {JSON_OUT}")
print(f"✅ CSV gerado:  {CSV_OUT}")

