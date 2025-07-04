import os
import re

# Caminhos de entrada e saída
ARQUIVO_SAS = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SAS/PISA2009_SAS_school.sas")
ARQUIVO_SAIDA = os.path.expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SAS/mascara_school_2009.txt")

def extrair_mascara(arquivo_entrada, arquivo_saida):
    padrao = re.compile(r'^\s*([A-Z0-9_]+)\s+(\d+)\s*-\s*(\d+)', re.IGNORECASE)
    linhas_utilizadas = []

    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        for linha in f:
            match = padrao.search(linha)
            if match:
                nome = match.group(1).upper()
                inicio = match.group(2)
                fim = match.group(3)
                linhas_utilizadas.append(f"{nome} {inicio} {fim}")

    with open(arquivo_saida, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(linhas_utilizadas))

    print(f"✅ Máscara extraída com {len(linhas_utilizadas)} variáveis.")
    print(f"📄 Arquivo gerado: {arquivo_saida}")

if __name__ == "__main__":
    extrair_mascara(ARQUIVO_SAS, ARQUIVO_SAIDA)

