import streamlit as st
import json
import os

# Define o caminho de dados baseado no modo
modo = st.secrets["modo"] if "modo" in st.secrets else "local"
CAMINHO = "painel_pisa/dados_cloud" if modo == "cloud" else "painel_pisa/dados_cloud"

# Página
st.set_page_config(layout="wide", page_title="Entidade que Organiza o PISA")

# Estilo opcional (caso tenha stilo() definido em outro arquivo utilitário)
try:
    from utils.estilo import stilo
    stilo()
except:
    pass

st.title("🌍 Quem organiza o PISA?")
st.markdown("### Entenda qual é a entidade internacional responsável e como o programa é financiado.")

# Carregando os dados do JSON
caminho_json = os.path.join(CAMINHO, "entidade_pisa.json")
with open(caminho_json, "r", encoding="utf-8") as f:
    entidade = json.load(f)

# Apresentação dos dados
st.subheader(f"📘 {entidade['nome_completo']} ({entidade['sigla']})")
st.markdown(f"**Sede:** {entidade['sede']}")
st.markdown(f"**Fundação:** {entidade['fundacao']}")
st.markdown(f"**Participantes:** {entidade['participantes']}")
st.markdown(f"**Objetivo:** {entidade['objetivo']}")
st.markdown(f"**Financiamento:** {entidade['financiamento']}")
st.markdown(f"[🔗 Site oficial da OCDE - PISA]({entidade['referencia']})")



