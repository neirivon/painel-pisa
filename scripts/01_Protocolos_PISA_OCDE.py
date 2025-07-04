import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="📘 Protocolos do PISA OCDE", layout="wide")

st.title("📘 Protocolos Utilizados no PISA OCDE 2022")
st.markdown("Visualize abaixo os principais documentos utilizados como base metodológica e operacional no ciclo de 2022 do PISA OCDE.")

# 🔌 Conexão com MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# Filtra apenas as coleções com prefixo correto
colecoes = sorted([c for c in db.list_collection_names() if c.startswith("protocolo_pisa_2022")])

# Cria uma aba para cada coleção
abas = st.tabs([c.replace("protocolo_pisa_2022_", "").replace("_", " ").title() for c in colecoes])

for aba, nome_colecao in zip(abas, colecoes):
    with aba:
        st.subheader(f"📂 Coleção: {nome_colecao}")
        documentos = db[nome_colecao].find({}, {"_id": 0, "arquivo_original": 1, "pagina_inicio": 1, "pagina_fim": 1, "conteudo": 1})

        for doc in documentos:
            nome = doc.get("arquivo_original", "Arquivo sem nome")
            inicio = doc.get("pagina_inicio", "?")
            fim = doc.get("pagina_fim", "?")
            conteudo = doc.get("conteudo", "⚠️ Conteúdo não disponível.")

            st.markdown(f"### 📄 {nome}")
            st.markdown(f"🗂️ Páginas: **{inicio} a {fim}**")
            st.markdown(f"📝 Trecho:")
            st.info(conteudo[:3000] if isinstance(conteudo, str) else str(conteudo))

client.close()

