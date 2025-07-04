# scripts/sas7bdat_parser.py

import re

def parse_sas_script(sas_path):
    """
    Lê um arquivo .sas contendo comandos INPUT e retorna duas listas:
    - colspecs: tuplas (início, fim) de cada coluna
    - colnames: nomes das colunas
    """
    colspecs = []
    colnames = []

    with open(sas_path, 'r', encoding='latin1') as f:
        lines = f.readlines()

    for line in lines:
        # Remove espaços em branco e ignora comentários
        line = line.strip()
        if not line or line.startswith('*') or line.startswith('//'):
            continue

        # Exemplo de linha:
        #   ST001Q01TA        1 -  1
        match = re.match(r'^([A-Z0-9_]+)\s+(\d+)\s*-\s*(\d+)', line)
        if match:
            name = match.group(1)
            start = int(match.group(2)) - 1  # começa do 0 no Python
            end = int(match.group(3))        # exclusivo
            colnames.append(name)
            colspecs.append((start, end))

    return colspecs, colnames

