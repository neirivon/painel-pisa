# scripts/exportar_rubrica_saeb_v2_csv.py

import os
import json
import csv

# Caminho base do projeto
BASE_DIR = "/home/neirivon/SINAPSE2.0/PISA"

# Caminhos do arquivo JSON de entrada e CSV de saída
JSON_PATH = os.path.join(BASE_DIR, "dados_processados", "rubricas", "rubrica_saeb_v2.json")
CSV_PATH = os.path.join(BASE_DIR, "dados_processados", "rubricas", "rubrica_saeb_v2.csv")

# Carregar o arquivo JSON
with open(JSON_PATH, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# Criar o arquivo CSV
with open(CSV_PATH, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Dimensão", "Nível", "Título", "Descrição", "Exemplos"])

    for dim in rubrica.get("dimensoes", []):
        nome_dimensao = dim.get("dimensao", "")
        for nivel in dim.get("niveis", []):
            writer.writerow([
                nome_dimensao,
                nivel.get("nivel", ""),
                nivel.get("titulo", ""),
                nivel.get("descricao", ""),
                " | ".join(nivel.get("exemplos", []))
            ])

print(f"✅ CSV exportado com sucesso para: {CSV_PATH}")

