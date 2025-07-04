# extrair_schemas_student_2000.py

import re
import os
import json

ARQUIVOS_SAS = {
    "math": {
        "sas": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SAS/PISA2000_SAS_student_mathematics.sas",
        "saida": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_student_math_2000.json"
    },
    "read": {
        "sas": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SAS/PISA2000_SAS_student_reading.sas",
        "saida": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_student_read_2000.json"
    },
    "scie": {
        "sas": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SAS/PISA2000_SAS_student_science.sas",
        "saida": "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/schema_student_scie_2000.json"
    }
}

def extrair_schema(sas_path):
    with open(sas_path, "r", encoding="latin1") as f:
        conteudo = f.read()

    match = re.search(r"input\s+(.*?);", conteudo, re.DOTALL | re.IGNORECASE)
    if not match:
        return []

    bloco = match.group(1)
    linhas = [linha.strip() for linha in bloco.splitlines() if linha.strip()]
    schema = []

    for linha in linhas:
        partes = re.split(r"\s+", linha)
        if len(partes) != 2:
            continue
        nome, pos = partes
        tipo = "str" if "$" in pos else "int"
        pos = pos.replace("$", "")
        if "-" in pos:
            ini, fim = pos.split("-")
            schema.append({
                "nome": nome,
                "inicio": int(ini),
                "fim": int(fim),
                "tipo": tipo
            })

    return schema

def main():
    os.makedirs("/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS/", exist_ok=True)

    for chave, info in ARQUIVOS_SAS.items():
        schema = extrair_schema(info["sas"])
        if not schema:
            print(f"❌ Não foi possível extrair o schema para: {info['sas']}")
        else:
            with open(info["saida"], "w", encoding="utf-8") as f:
                json.dump(schema, f, ensure_ascii=False, indent=2)
            print(f"✅ Schema salvo em: {info['saida']}")

if __name__ == "__main__":
    main()

