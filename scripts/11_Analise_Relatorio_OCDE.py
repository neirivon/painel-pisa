# painel_pisos.path.join(a, "p")ageos.path.join(s, "1")3_Analise_Relatorio_OCDE.py

import streamlit as st
from utils.conexao_mongo import conectar_mongo
import pandas as pd
import plotly.express as px

# === Configuração da Página ===
st.set_page_config(page_title="Análise Relatório OCDE - PISA 2000", layout="wide")

# === CSS Global para consistência visual ===
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        font-size: 17px;
    }
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
    }
    .metric-container {
        text-align: center;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
os.path.join(<, "s")tyle>
""", unsafe_allow_html=True)

# === Título ===
st.title("📊 Análise Crítica do Relatório OCDE - PISA 2000")

# === Conectar ao MongoDB e carregar dados ===
db = conectar_mongo()
colecao = db["pisa_ocde_2000_relatorio"]
docs = list(colecao.find({}, {"_id": 0, "pagina": 1, "texto": 1}))
df = pd.DataFrame(docs).sort_values(by="pagina")

# === Métricas ===
st.markdown("### Estatísticas Iniciais do Relatório")
col1, col2 = st.columns(2)
col1.metric("Total de Páginas", df.shape[0])
col2.metric("Idioma", "Inglês (Original OCDE)")

# === Pré-análise textual (contagem de palavras por página) ===
df["tokens"] = df["texto"].apply(lambda x: len(x.split()))
st.markdown("### Distribuição de Palavras por Página")
fig = px.histogram(df, x="pagina", y="tokens", nbins=50, labels={"tokens": "Nº de Palavras", "pagina": "Página"})
st.plotly_chart(fig, use_container_width=True)

# === Visão Geral do Conteúdo ===
st.markdown("---")
st.subheader("📘 Interpretação Preliminar (com base estrutural)")
st.markdown("""
Este painel apresenta uma leitura exploratória do **Relatório Técnico da OCDE (PISA 2000)**. O conteúdo está armazenado no MongoDB, mantendo o idioma original (inglês), enquanto a análise interpretativa é feita em português.

Com base em futuras análises semânticas e classificações por Taxonomia de Bloom e rubricas avaliativas, o painel será atualizado com:

- Níveis cognitivos identificados por IA (ex: Aplicar, Analisar, Criar)
- Áreas temáticas (Leitura, Matemática, Ciências)
- Sugestões de políticas públicas com base nos achados

📌 A próxima etapa envolverá **classificação de trechos por nível de complexidade**, perfil educacional, e **visualizações comparativas entre países** — alinhado aos princípios de **avaliação formativa** (Bloom, 1956; OCDE, 2001).
""")

# === Exibição opcional das primeiras páginas (apenas exploratório, não o foco) ===
with st.expander("🔍 Ver Primeiras Páginas do Relatório (Inglês)", expanded=False):
    for _, row in df.head(5).iterrows():
        st.markdown(f"**Página {row['pagina']}**")
        st.text_area(label="", value=row["texto"], height=200, key=row['pagina'])

# === Rodapé ===
st.markdown("---")
st.caption("OCDE (2001). PISA 2000 Technical Report | Relatório estruturado via SINAPSE 2.0 – Análise Crítica com Foco Educacional.")

