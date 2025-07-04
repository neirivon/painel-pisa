# ~/SINAPSE2.0/PISA/scripts/debug_json_erro.py

import json

json_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_2_completa.json"

try:
    with open(json_path, "r", encoding="utf-8") as f:
        content = f.read()
        data = json.loads(content)
        print("✅ JSON carregado com sucesso!")

except json.decoder.JSONDecodeError as e:
    erro_linha = e.lineno
    erro_coluna = e.colno
    erro_msg = e.msg

    print(f"❌ Erro de sintaxe JSON: {erro_msg}")
    print(f"📍 Linha: {erro_linha}, Coluna: {erro_coluna}\n")

    linhas = content.splitlines()
    if erro_linha <= len(linhas):
        print("📄 Contexto com erro:")
        print("-" * 60)
        print(f"{erro_linha:>4}: {linhas[erro_linha - 2] if erro_linha >= 2 else ''}")
        print(f"{erro_linha:>4}: {linhas[erro_linha - 1]}")
        print(" " * (erro_coluna + 4) + "🔻")
        print(f"{erro_linha+1:>4}: {linhas[erro_linha] if erro_linha < len(linhas) else ''}")
        print("-" * 60)

    else:
        print("⚠️ Linha de erro fora do intervalo do arquivo.")

