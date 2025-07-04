# painel_pisa/utils/config.py

import os

# ⚙️ Modo de execução: 'local' ou 'cloud'
MODO_EXECUCAO = os.getenv("PISA_MODO", "local").lower()

# Caminho base real do painel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # => painel_pisa/

# Caminhos de dados corrigidos
CAMINHO_DADOS_CLOUD = os.path.join(PAINEL_DIR, "dados_cloud")
CAMINHO_DADOS_LOCAL = os.path.abspath(os.path.join(PAINEL_DIR, "..", "dados_processados"))

# Arquivo geográfico
ARQUIVO_JSON_BRASIL = (
    "pais_2022_detalhado.json" if MODO_EXECUCAO == "local" else "pais_2022_simplificado.json"
)

CONFIG = {
    "MODO": MODO_EXECUCAO,
    "USAR_MONGODB": MODO_EXECUCAO == "local",
    "USAR_FAISS": MODO_EXECUCAO == "local",
    "CAMINHO_DADOS": CAMINHO_DADOS_LOCAL if MODO_EXECUCAO == "local" else CAMINHO_DADOS_CLOUD,
    "ARQUIVO_BRASIL": os.path.join(
        CAMINHO_DADOS_LOCAL if MODO_EXECUCAO == "local" else CAMINHO_DADOS_CLOUD,
        ARQUIVO_JSON_BRASIL,
    ),
    "MONGO_URI": f"mongodb://{os.getenv('MONGO_USER', 'admin')}:{os.getenv('MONGO_PASS', 'admin123')}@{os.getenv('MONGO_HOST', 'localhost')}:{os.getenv('MONGO_PORTA', '27017')}/?authSource=admin"
    if MODO_EXECUCAO == "local" else None,
    "MONGO_BANCO": os.getenv("MONGO_BANCO", "pisa"),
    "FAISS_INDEX_PATH": "/home/neirivon/pisa_faiss/pisa.index" if MODO_EXECUCAO == "local" else None,
}

