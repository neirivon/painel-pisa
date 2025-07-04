import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel INEP – PISA", layout="wide")

st.title("📘 Painel Analítico dos Relatórios INEP – PISA Brasil")
st.markdown("Análise dos principais tópicos abordados nos relatórios do INEP entre 2000 e 2022.")

# Carregar dados
df = pd.read_csv("relatorios_inep_resumo.csv")

# Filtros
col1, col2 = st.columns(2)
anos = col1.multiselect("📅 Selecione os anos", options=df["ano"].unique(), default=list(df["ano"].unique()))
topicos = col2.multiselect(
    "🧩 Tópicos analisados",
    options=["desempenho", "competencias", "equidade", "comparações", "politicas_publicas"],
    default=["desempenho", "competencias", "equidade", "comparações", "politicas_publicas"]
)

df_filtrado = df[df["ano"].isin(anos)]

# Mostrar tabela
st.subheader("📊 Tabela de Relatórios INEP")
st.dataframe(df_filtrado[["ano", "arquivo"] + topicos])

# Gráfico de presença por tópico
st.subheader("📈 Presença dos Tópicos nos Relatórios")
df_melt = df_filtrado.melt(id_vars=["ano"], value_vars=topicos, var_name="Tópico", value_name="Presente")
df_melt["Presente"] = df_melt["Presente"].map({True: "Sim", False: "Não"})

fig = px.histogram(
    df_melt,
    x="ano",
    color="Presente",
    facet_col="Tópico",
    category_orders={"Presente": ["Sim", "Não"]},
    barmode="group",
    text_auto=True
)

fig.update_layout(height=500, title="Ocorrência de Tópicos por Ano")
st.plotly_chart(fig, use_container_width=True)

