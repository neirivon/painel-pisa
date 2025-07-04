import streamlit as st

try:
    PISA_MODO = st.secrets["PISA_MODO"]
    MONGO_USER = st.secrets["MONGO_USER"]
    MONGO_PASS = st.secrets["MONGO_PASS"]
    MONGO_HOST = st.secrets["MONGO_HOST"]
    MONGO_PORTA = st.secrets["MONGO_PORTA"]
    MONGO_BANCO = st.secrets["MONGO_BANCO"]
    RUBRICA_VERSAO = st.secrets["RUBRICA_VERSAO"]
    
    MONGO_URI = (
        f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority"
    )

    CONFIG = {
        "MODO": PISA_MODO,
        "MONGO_USER": MONGO_USER,
        "MONGO_PASS": MONGO_PASS,
        "MONGO_HOST": MONGO_HOST,
        "MONGO_PORTA": MONGO_PORTA,
        "MONGO_URI": MONGO_URI,
        "MONGO_BANCO": MONGO_BANCO,
        "RUBRICA_VERSAO": RUBRICA_VERSAO,
        "CAMINHO_DADOS": "painel_pisa/dados_cloud"
    }

except KeyError as e:
    st.error(f"🔒 Variável secreta ausente: {e}")
    st.stop()

