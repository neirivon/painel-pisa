# utilos.path.join(s, "l")ogger_padronizado.py

import os
from datetime import datetime

def configurar_log(nome_base_script: str):
    # Caminho absoluto da pasta onde está o script atual
    base_dir = os.path.dirname(os.path.abspath(__file__))  # utils/
    raiz_projeto = os.path.abspath(os.path.join(base_dir, ".."))  # volta para a raiz do projeto (PISA)

    # Caminho completo da pasta de logs
    pasta_logs = os.path.join(raiz_projeto, "logs")
    os.makedirs(pasta_logs, exist_ok=True)

    # Nome do arquivo com data e hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo_log = os.path.join(pasta_logs, f"{nome_base_script}_{timestamp}.log")

    return open(nome_arquivo_log, "w", encoding="utf-8")

