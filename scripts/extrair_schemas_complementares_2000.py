# scripts/extrair_schemas_complementares_2000.py

import os
import re
import json

CAMINHO_SAS = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SAS"
ARQUIVOS = {
    "schema_cognitive_item_2000.json": "PISA-2000-SAS-control-file-for-the-cognitive-item-data-file.sas",
    "schema_school_2000.json": "PISA2000_SAS_school_questionnaire.sas",
}
PASTA_SAIDA = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2000/SCHEMAS"
os.makedirs(PASTA_SAIDA, exist_ok=True)

def extrair_schema_sas(caminho_sas):
    with open(caminho_sas, "r", encoding="utf-8", errors="ignore") as f:
        conteudo = f.read()

    match = re.search(r"\binput\b(.+?);", conteudo, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        print(f"❌ Nenhuma seção 'input' encontrada em: {caminho_sas}")
        return []

    blocos = match.group(1).strip().split("\n")
    schema = []

    for linha in blocos:
        linha = linha.strip().rstrip(";").replace("\t", " ")
        if not linha:
            continue
        partes = re.split(r"\s+", linha)
        if len(partes) >= 2:
            nome = partes[0]
            posicao = partes[1]
            tipo = "str" if "$" in posicao else "int"
            posicao = posicao.replace("$", "")
            if "-" in posicao:
                start, end = posicao.split("-")
                schema.append({
                    "name": nome,
                    "type": tipo,
                    "start": int(start),
                    "end": int(end)
                })
            else:
                schema.append({
                    "name": nome,
                    "type": tipo,
                    "start": int(posicao),
                    "end": int(posicao)
                })

    return schema

for nome_arquivo_saida, nome_sas in ARQUIVOS.items():
    caminho_completo = os.path.join(CAMINHO_SAS, nome_sas)
    schema = extrair_schema_sas(caminho_completo)
    caminho_saida = os.path.join(PASTA_SAIDA, nome_arquivo_saida)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    print(f"✅ Schema salvo em: {caminho_saida}")

