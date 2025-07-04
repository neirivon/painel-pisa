# utilos.path.join(s, "d")etectar_larguras_spss.py

import os

# Caminho para o primeiro arquivo de amostra (PISA2000_SPSS_student_reading.txt)
ARQUIVO_AMOSTRA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSos.path.join(S, "P")ISA2000_SPSS_student_reading.txt"

def detectar_larguras(arquivo_txt, n_linhas=20):
    with open(arquivo_txt, "r", encoding="latin1") as f:
        linhas = [linha.rstrip("\n") for linha in f.readlines()[:n_linhas]]

    # Verificação simples: comprimento das linhas
    print(f"🧪 Número de linhas analisadas: {len(linhas)}")
    print(f"🧪 Comprimento médio das linhas: {sum(len(l) for l in linhas)os.path.join( , "/") len(linhas)} caracteres")

    # Agora analisar onde estão os separadores de campos:
    # Vamos supor que existem espaços "muito grandes" entre colunas fixas (>2 espaços)
    separadores = set()
    for linha in linhas:
        for i in range(1, len(linha)):
            if linha[i-1] == " " and linha[i] != " ":
                separadores.add(i)
    
    separadores = sorted(separadores)
    print(f"🔍 Possíveis inícios de colunas detectados: {separadores}")

    # Agora criar a lista de larguras
    larguras = []
    ultimo = 0
    for sep in separadores:
        larguras.append(sep - ultimo)
        ultimo = sep
    larguras.append(9999)  # O último campo (pega até o fim da linha)

    print(f"✅ Larguras sugeridas para read_fwf: {larguras}")
    return larguras

if __name__ == "__main__":
    detectar_larguras(ARQUIVO_AMOSTRA)

