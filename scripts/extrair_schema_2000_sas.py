import os
import json
import re
import csv

PASTA_SAS = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SAS"
PASTA_SAIDA = PASTA_SAS  # mesmo local dos .sas

arquivos_sas = {
    "schema_student_math_2000": "PISA2000_SAS_student_mathematics.sas",
    "schema_student_read_2000": "PISA2000_SAS_student_reading.sas",
    "schema_student_scie_2000": "PISA2000_SAS_student_science.sas",
    "schema_school_2000": "PISA2000_SAS_school_questionnaire.sas",
    "schema_cognitive_2000": "PISA-2000-SAS-control-file-for-the-cognitive-item-data-file.sas"
}

regex_input = re.compile(r"@(\d+)\s+([A-Z0-9_]+)\s+(\$)?(\d+)", re.IGNORECASE)

def extrair_schema(arquivo_path):
    schema = []
    with open(arquivo_path, "r", encoding="latin1") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or not linha.startswith("@"):
                continue
            match = regex_input.search(linha)
            if match:
                inicio = int(match.group(1))
                nome = match.group(2)
                tipo = "str" if match.group(3) == "$" else "int"
                tamanho = int(match.group(4))
                fim = inicio + tamanho - 1
                schema.append({
                    "nome": nome,
                    "inicio": inicio,
                    "fim": fim,
                    "tipo": tipo
                })
    return schema

for nome_saida, nome_arquivo in arquivos_sas.items():
    caminho_sas = os.path.join(PASTA_SAS, nome_arquivo)
    schema = extrair_schema(caminho_sas)

    # Exportar para JSON
    caminho_json = os.path.join(PASTA_SAIDA, f"{nome_saida}.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)

    # Exportar para CSV
    caminho_csv = os.path.join(PASTA_SAIDA, f"{nome_saida}.csv")
    with open(caminho_csv, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "inicio", "fim", "tipo"])
        writer.writeheader()
        writer.writerows(schema)

    print(f"✅ JSON gerado: {caminho_json}")
    print(f"✅ CSV gerado:  {caminho_csv}")

print("🏁 Extração de schemas SAS 2000 concluída.")

