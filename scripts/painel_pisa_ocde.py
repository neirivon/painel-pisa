from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

# Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]

st.set_page_config(layout="wide")
st.title("🌍 Painel Interativo - Microdados PISA PfD (OCDE)")
st.markdown("**Fonte:** OCDE · PISA for Development · Alunos · Perfil socioeconômico e desempenho educacional")

# Coleta os dados da coleção correta
dados = pd.DataFrame(list(db["pisa_pfd_alunos"].find({}, {
    "CNT": 1,
    "CNTSCHID": 1,
    "ST004D01T": 1,
    "ESCS15": 1,
    "PV1MATH": 1,
    "PV1READ": 1,
    "PV1SCIE": 1,
    "_id": 0
})))

# Conversão segura para numérico
for col in ["ESCS15", "PV1MATH", "PV1READ", "PV1SCIE"]:
    dados[col] = pd.to_numeric(dados[col], errors="coerce")

dados = dados.dropna(subset=["ESCS15", "PV1MATH", "PV1READ", "PV1SCIE"])

# Tradução de nomes
dados = dados.rename(columns={
    "ESCS15": "Nível Socioeconômico",
    "PV1MATH": "Nota em Matemática",
    "PV1READ": "Nota em Leitura",
    "PV1SCIE": "Nota em Ciências",
    "CNT": "País",
    "ST004D01T": "Gênero",
    "CNTSCHID": "Escola"
})

# Filtros interativos
st.sidebar.header("Filtros")
paises = sorted(dados["País"].dropna().unique())
generos = sorted(dados["Gênero"].dropna().unique())

filtro_paises = st.sidebar.multiselect("País(es)", paises, default=paises)
filtro_generos = st.sidebar.multiselect("Gênero(s)", generos, default=generos)

dados = dados[(dados["País"].isin(filtro_paises)) & (dados["Gênero"].isin(filtro_generos))]

# Criar faixas do nível socioeconômico
dados["Faixa Socioeconômica"] = pd.cut(dados["Nível Socioeconômico"], bins=[-999, -2, -1, 0, 1, 999],
                                       labels=["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"])

# Gráfico de barras: médias por faixa
st.subheader("📊 Desempenho médio por Faixa Socioeconômica")
medias = dados.groupby("Faixa Socioeconômica")[["Nota em Matemática", "Nota em Leitura", "Nota em Ciências"]].mean().reset_index()

fig_barras = px.bar(medias, x="Faixa Socioeconômica",
                    y=["Nota em Matemática", "Nota em Leitura", "Nota em Ciências"],
                    barmode="group",
                    labels={"value": "Nota Média", "variable": "Disciplina"},
                    title="Médias de Notas por Faixa Socioeconômica")
st.plotly_chart(fig_barras, use_container_width=True)

# Mapa de calor das correlações
st.subheader("🔥 Correlação entre Nível Socioeconômico e Notas")

corr = dados[["Nível Socioeconômico", "Nota em Matemática", "Nota em Leitura", "Nota em Ciências"]].corr().round(2)

fig_corr = px.imshow(corr.loc[["Nível Socioeconômico"]],
                     text_auto=True,
                     aspect="auto",
                     color_continuous_scale="Blues",
                     title="Correlação com Nível Socioeconômico")
st.plotly_chart(fig_corr, use_container_width=True)

# Boxplot por gênero
st.subheader("📈 Distribuição de Notas por Gênero")
for materia in ["Nota em Matemática", "Nota em Leitura", "Nota em Ciências"]:
    st.markdown(f"**{materia}**")
    fig = px.box(dados, x="Gênero", y=materia, points="all", color="Gênero")
    st.plotly_chart(fig, use_container_width=True)

# Médias por escola (bônus)
st.subheader("🏫 Médias por Escola")
agrupado = dados.groupby(["País", "Escola"]).agg({
    "Nível Socioeconômico": "mean",
    "Nota em Matemática": "mean",
    "Nota em Leitura": "mean",
    "Nota em Ciências": "mean"
}).reset_index()

fig_escolas = px.scatter(agrupado, x="Nível Socioeconômico", y="Nota em Matemática",
                         color="País", hover_data=["Escola"],
                         title="Desempenho médio em Matemática por Escola")
st.plotly_chart(fig_escolas, use_container_width=True)

