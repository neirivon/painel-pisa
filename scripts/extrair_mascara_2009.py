# scripts/extrair_mascara_2009.py

import re
from pathlib import Path

# Caminho do arquivo SPSS com a máscara
ARQUIVO_SPSS = Path.home() / "backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/PISA2009_SPSS_cognitive_item.txt"
ARQUIVO_SAIDA = Path.home() / "backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/mascara_extraida_2009.txt"

def extrair_mascara_spss(conteudo):
    linhas_mascara = []
    lendo = False
    for linha in conteudo.splitlines():
        linha = linha.strip()
        if linha.startswith("DATA LIST FILE"):
            lendo = True
            continue
        if lendo:
            if linha.startswith("*") or linha.upper().startswith("VARIABLE LABELS") or not linha:
                break
            linhas_mascara.append(linha)
    return linhas_mascara

def main():
    if not ARQUIVO_SPSS.exists():
        print(f"❌ Arquivo SPSS não encontrado: {ARQUIVO_SPSS}")
        return

    with open(ARQUIVO_SPSS, "r", encoding="utf-8") as f:
        conteudo = f.read()

    mascara = extrair_mascara_spss(conteudo)
    if not mascara:
        print("❌ Nenhuma máscara foi extraída.")
        return

    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(mascara))

    print(f"✅ Máscara extraída com sucesso: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()

