# scripts/gerar_schema_json_mascara_2009.py

import re
import json
from pathlib import Path

ARQUIVO_MASCARA = Path.home() / "backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/mascara_extraida_2009.txt"
ARQUIVO_SAIDA = Path.home() / "backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/schema_cognitive_item_2009.json"

def linha_para_dict(linha):
    # Exemplo: M033Q01       25	-	25    (A)
    match = re.match(r'^(\w+)\s+(\d+)\s*-\s*(\d+)\s+\(([^)]+)\)', linha)
    if not match:
        return None
    campo, ini, fim, tipo_raw = match.groups()
    tipo = tipo_raw.strip().upper()
    if tipo.startswith("A"):
        tipo_final = "str"
    elif tipo.startswith("F"):
        tipo_final = "float"
    elif tipo.startswith("N"):
        tipo_final = "int"
    else:
        tipo_final = "str"
    return {
        "campo": campo,
        "inicio": int(ini) - 1,
        "fim": int(fim),
        "tipo": tipo_final
    }

def main():
    if not ARQUIVO_MASCARA.exists():
        print(f"❌ Arquivo de máscara não encontrado: {ARQUIVO_MASCARA}")
        return

    with open(ARQUIVO_MASCARA, "r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

    schema = []
    for linha in linhas:
        d = linha_para_dict(linha)
        if d:
            schema.append(d)
        else:
            print(f"⚠️ Ignorando linha inválida: {linha}")

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    print(f"✅ Schema gerado com sucesso: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()

