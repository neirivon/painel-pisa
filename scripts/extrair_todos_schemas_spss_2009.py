import os
import re
import json
import csv

PASTA = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT"
ARQUIVOS = [
    "PISA2009_SPSS_cognitive_item.txt",
    "PISA2009_SPSS_student.txt",
    "PISA2009_SPSS_school.txt",
    "PISA2009_SPSS_parent.txt",
    "PISA2009_SPSS_score_cognitive_item.txt"
]

def extrair_schema_spss(linhas):
    padrao = re.compile(r"^\s*([A-Z0-9_]+)\s+(\d+)\s*-\s*(\d+)\s+\(([^)]+)\)")
    schema = []
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("*") or linha.upper().startswith(("SET", "DATA LIST", "EXECUTE", ".")):
            continue
        match = padrao.match(linha)
        if match:
            nome, ini, fim, tipo = match.groups()
            schema.append({
                "campo": nome,
                "posicao_inicial": int(ini),
                "posicao_final": int(fim),
                "tipo": tipo
            })
    return schema

def salvar_schema_json_csv(schema, nome_base):
    caminho_json = os.path.join(PASTA, f"schema_{nome_base}.json")
    caminho_csv = os.path.join(PASTA, f"schema_{nome_base}.csv")

    with open(caminho_json, "w", encoding="utf-8") as jf:
        json.dump(schema, jf, indent=2, ensure_ascii=False)

    with open(caminho_csv, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=["campo", "posicao_inicial", "posicao_final", "tipo"])
        writer.writeheader()
        writer.writerows(schema)

    print(f"✅ JSON gerado: {caminho_json}")
    print(f"✅ CSV gerado:  {caminho_csv}")

for arquivo in ARQUIVOS:
    caminho = os.path.join(PASTA, arquivo)
    nome_base = arquivo.replace("PISA2009_SPSS_", "").replace(".txt", "").lower()
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            linhas = f.readlines()
        schema = extrair_schema_spss(linhas)
        if schema:
            salvar_schema_json_csv(schema, nome_base)
        else:
            print(f"⚠️ Nenhum campo encontrado no arquivo: {arquivo}")
    except Exception as e:
        print(f"❌ Erro ao processar {arquivo}: {e}")

print("🏁 Lote concluído.")

