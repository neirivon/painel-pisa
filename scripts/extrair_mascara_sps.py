import os
import re

ARQUIVO_SPS = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/PISA2009_SPSS_cognitive_item.txt")
ARQUIVO_MASCARA_SAIDA = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT/mascara_extraida_2009.txt")

def extrair_mascara_sps(arquivo_entrada, arquivo_saida):
    padrao = re.compile(r"^\s*/?([A-Z0-9_]+)\s+(\d+)-(\d+)")
    linhas_utilizadas = []

    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            match = padrao.match(linha)
            if match:
                nome = match.group(1)
                inicio = match.group(2)
                fim = match.group(3)
                linhas_utilizadas.append(f"{nome} {inicio} {fim}")

    with open(arquivo_saida, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(linhas_utilizadas))

    print(f"✅ Máscara extraída com {len(linhas_utilizadas)} variáveis.")
    print(f"📄 Arquivo gerado: {arquivo_saida}")

if __name__ == "__main__":
    extrair_mascara_sps(ARQUIVO_SPS, ARQUIVO_MASCARA_SAIDA)

