# utils/paths.py

import os

# Caminho raiz do projeto (painel_pisa/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Diretórios de ativos
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOGOS_DIR = os.path.join(ASSETS_DIR, "logos")
IMAGENS_DIR = os.path.join(ASSETS_DIR, "imagens")

# Diretórios de dados
DADOS_CLOUD = os.path.join(BASE_DIR, "dados_cloud")
DADOS_LOCAL = os.path.abspath(os.path.join(BASE_DIR, "..", "dados_processados"))

