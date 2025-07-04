import os
import json
import re

def extrair_schema_sas(caminho_sas):
    variaveis = []
    with open(caminho_sas, "r", encoding="utf-8", errors="ignore") as f:
        linhas = f.readlines()

    inicio_input = False
    for linha in linhas:
        linha = linha.strip()
        if not inicio_input:
            if linha.lower().startswith("input"):
                inicio_input = True
            continue
        if linha == ";" or linha.lower().startswith("cards"):
            break
        # Expressão para capturar variáveis e posições
        match = re.match(r"(\w+)\s+\$?(\d+)-(\d+)", linha)
        if match:
            nome, ini, fim = match.groups()
            variaveis.append({
                "name": nome,
                "start": int(ini),
                "end": int(fim)
            })

    return variaveis

# Diretórios base
BASE_DIR = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2003"
SAS_DIR = os.path.join(BASE_DIR, "SAS")
SCHEMA_DIR = os.path.join(BASE_DIR, "SCHEMAS")

# Garante que a pasta de saída existe
os.makedirs(SCHEMA_DIR, exist_ok=True)

arquivos = {
    "student": "PISA2003_SAS_student.sas",
    "school": "PISA2003_SAS_school.sas",
    "cognitive_item": "PISA2003_SAS_cognitive_item.sas"
}

for tipo, nome_arquivo in arquivos.items():
    caminho = os.path.join(SAS_DIR, nome_arquivo)
    try:
        schema = extrair_schema_sas(caminho)
        caminho_saida = os.path.join(SCHEMA_DIR, f"schema_{tipo}_2003.json")
        with open(caminho_saida, "w", encoding="utf-8") as f:
            json.dump(schema, f, ensure_ascii=False, indent=2)
        print(f"✅ Schema salvo em: {caminho_saida}")
    except Exception as e:
        print(f"❌ Erro ao processar {nome_arquivo}: {e}")

