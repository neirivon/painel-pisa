import os

# ⚙️ Modo de execução: 'local' ou 'cloud'
MODO_EXECUCAO = os.getenv("PISA_MODO", "local").lower()

# Caminho base do painel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))  # => painel_pisa/

# Caminhos para dados
CAMINHO_DADOS_CLOUD = os.path.join(PAINEL_DIR, "dados_cloud")
CAMINHO_DADOS_LOCAL = os.path.abspath(os.path.join(PAINEL_DIR, "..", "dados_processados"))

# Arquivo geo simplificado na nuvem, detalhado localmente
ARQUIVO_JSON_BRASIL = (
    "pais_2022_detalhado.json" if MODO_EXECUCAO == "local" else "pais_2022_simplificado.json"
)

# Construção da URI do MongoDB
if MODO_EXECUCAO == "cloud":
    MONGO_URI = (
        f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}"
        f"@{os.getenv('MONGO_HOST')}/?retryWrites=true&w=majority"
    )
else:
    MONGO_URI = (
        f"mongodb://{os.getenv('MONGO_USER', 'admin')}:{os.getenv('MONGO_PASS', 'admin123')}"
        f"@{os.getenv('MONGO_HOST', 'localhost')}:{os.getenv('MONGO_PORTA', '27017')}/?authSource=admin"
    )

# Configurações unificadas
CONFIG = {
    "MODO": MODO_EXECUCAO,
    "USAR_MONGODB": True,
    "USAR_FAISS": MODO_EXECUCAO == "local",  # FAISS apenas local
    "CAMINHO_DADOS": CAMINHO_DADOS_LOCAL if MODO_EXECUCAO == "local" else CAMINHO_DADOS_CLOUD,
    "ARQUIVO_BRASIL": os.path.join(
        CAMINHO_DADOS_LOCAL if MODO_EXECUCAO == "local" else CAMINHO_DADOS_CLOUD,
        ARQUIVO_JSON_BRASIL,
    ),
    "MONGO_URI": MONGO_URI,
    "MONGO_BANCO": os.getenv("MONGO_BANCO", "pisa"),
    "FAISS_INDEX_PATH": "/home/neirivon/pisa_faiss/pisa.index" if MODO_EXECUCAO == "local" else None,
    "RUBRICA_VERSAO": os.getenv("RUBRICA_VERSAO", "v1.7"),
}

