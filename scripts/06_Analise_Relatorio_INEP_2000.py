from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# pageos.path.join(s, "0")6_Analise_Relatorio_INEP_2000.py

import streamlit as st
import pandas as pd
from pymongo import MongoClient
from utils.estilo_global import aplicar_estilo

st.set_page_config(page_title="Análise - Relatório INEP 2000", layout="wide")
aplicar_estilo()

st.title("📑 Análise do Relatório INEP 2000 com IA")
st.markdown("Este painel apresenta os parágrafos analisados da edição brasileira do **Relatório Nacional do PISA 2000**, com classificações automáticas baseadas na **Taxonomia de Bloom**.")

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
collection = db["relatorio_inep_pisa_2000_analise_v2"]

# Carregar documentos
docs = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(docs)

if df.empty:
    st.warning("⚠️ Nenhum dado encontrado na coleção.")
else:
    secoes = df["secao"].unique().tolist()
    secao_escolhida = st.selectbox("📂 Selecione a seção", secoes)

    filtrado = df[df["secao"] == secao_escolhida].sort_values(by="indice")

    for _, row in filtrado.iterrows():
        st.markdown(f"**📄 Parágrafo {row['indice']+1}** — *Seção: {row['secao']}*")
        st.markdown(f"> {row['texto_original'][:400]}{'...' if len(row['texto_original']) > 400 else ''}")
        st.markdown(f"🔎 **Classificação IA:** `{row['nivel_bloom']}`")
        st.markdown("---")

