# painel_pisa/utils/config.py

import os
import streamlit as st
from dotenv import load_dotenv

# Detecta o modo de execução
PISA_MODO = os.getenv("PISA_MODO", "").lower()

if not PISA_MODO:
    # Se não tiver vindo do .env, tenta pegar do secrets do Streamlit Cloud
    try:
        PISA_MODO = st.secrets["PISA_MODO"].lower()
    except Exception:
        PISA_MODO = "local"  # fallback padrão

# Modo local (.env)
if PISA_MODO == "local":
    load_dotenv()

    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORTA = os.getenv("MONGO_PORTA", "27017")
    MONGO_BANCO = os.getenv("MONGO_BANCO")
    RUBRICA_VERSAO = os.getenv("RUBRICA_VERSAO")

    MONGO_URI = (
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORTA}/?authSource=admin"
    )

# Modo cloud (Streamlit Cloud)
else:
    try:
        MONGO_USER = st.secrets["MONGO_USER"]
        MONGO_PASS = st.secrets["MONGO_PASS"]
        MONGO_HOST = st.secrets["MONGO_HOST"]
        MONGO_PORTA = st.secrets.get("MONGO_PORTA", "27017")
        MONGO_BANCO = st.secrets["MONGO_BANCO"]
        RUBRICA_VERSAO = st.secrets["RUBRICA_VERSAO"]

        MONGO_URI = (
            f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority"
        )
    except KeyError as e:
        st.error("🔒 Variável de segredo ausente no Streamlit Cloud.")
        st.stop()

# Caminhos de diretório
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAINEL_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

CAMINHO_DADOS_LOCAL = os.path.abspath(os.path.join(PAINEL_DIR, "..", "dados_processados"))
CAMINHO_DADOS_CLOUD = os.path.join(PAINEL_DIR, "dados_cloud")

CAMINHO_DADOS = CAMINHO_DADOS_LOCAL if PISA_MODO == "local" else CAMINHO_DADOS_CLOUD
ARQUIVO_JSON_BRASIL = (
    "pais_2022_detalhado.json" if PISA_MODO == "local" else "pais_2022_simplificado.json"
)

# Configuração final (sem valores sensíveis expostos)
CONFIG = {
    "MODO": PISA_MODO,
    "MONGO_URI": MONGO_URI,
    "MONGO_BANCO": MONGO_BANCO,
    "RUBRICA_VERSAO": RUBRICA_VERSAO,
    "CAMINHO_DADOS": CAMINHO_DADOS,
    "ARQUIVO_BRASIL": os.path.join(CAMINHO_DADOS, ARQUIVO_JSON_BRASIL),
    "USAR_MONGODB": PISA_MODO == "local",
    "USAR_FAISS": PISA_MODO == "local",
}

