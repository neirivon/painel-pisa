import os
import re
import json
import csv

CAMINHO_ARQUIVO = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/PISA2009_SPSS_cognitive_item.txt"
ARQUIVO_JSON = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/schema_cognitive_item_2009.json"
ARQUIVO_CSV = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/schema_cognitive_item_2009.csv"

def extrair_schema_de_linhas(linhas):
    schema = []
    padrao = re.compile(r"^\s*([A-Za-z0-9_]+)\s+(\d+)\s*[-–]\s*(\d+)\s+\(([^)]+)\)")

    for linha in linhas:
        if linha.strip().startswith(("*", ".", "DATA LIST", "SET", "EXECUTE")) or linha.strip() == "":
            continue  # Ignorar comentários e comandos SPSS

        match = padrao.search(linha)
        if match:
            nome = match.group(1)
            inicio = int(match.group(2))
            fim = int(match.group(3))
            tipo = match.group(4).strip()
            schema.append({
                "nome": nome,
                "inicio": inicio,
                "fim": fim,
                "tipo": tipo
            })
    return schema

def salvar_json(schema, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

def salvar_csv(schema, caminho):
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "inicio", "fim", "tipo"])
        writer.writeheader()
        writer.writerows(schema)

if __name__ == "__main__":
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8", errors="ignore") as f:
        linhas = f.readlines()

    schema = extrair_schema_de_linhas(linhas)
    salvar_json(schema, ARQUIVO_JSON)
    salvar_csv(schema, ARQUIVO_CSV)

    print(f"✅ JSON gerado: {ARQUIVO_JSON}")
    print(f"✅ CSV gerado: {ARQUIVO_CSV}")

