
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.conexao_mongo import conectar_mongo

st.set_page_config(page_title="Painel Real - PISos.path.join(A, "S")AEB", layout="wide")
st.title("📊 Painel Comparativo com Dados Reais: PISA 2022, INEP, SAEB 2021 e 2023")

# Conectar ao MongoDB
db, client = conectar_mongo()

# Buscar dados das coleções relevantes
pisa_ocde = db["pisa_ocde_2022_medias"].find_one({"local": "Brasil"}) or {}
inep = db["inep_pisa_2022_resultados"].find_one({"local": "Brasil"}) or {}
saeb_2021_br = db["saeb_2021_estados"].find_one({"local": "Brasil"}) or {}
saeb_2021_mg = db["saeb_2021_estados"].find_one({"local": "Minas Gerais"}) or {}
saeb_2021_tri = db["saeb_2021_mesorregioes"].find_one({"local": "Triângulo Mineiro e Alto Paranaíba"}) or {}
saeb_2023_br = db["saeb_2023_estados"].find_one({"local": "Brasil"}) or {}
saeb_2023_tri = db["saeb_2023_mesorregioes"].find_one({"local": "Triângulo Mineiro e Alto Paranaíba"}) or {}

# Construir DataFrame de comparação
dados = [
    {"Região": "PISA OCDE 2022 - Brasil", "Leitura": pisa_ocde.get("leitura"), "Matemática": pisa_ocde.get("matematica"), "Ciências": pisa_ocde.get("ciencias")},
    {"Região": "INEP - PISA 2022", "Leitura": inep.get("leitura"), "Matemática": inep.get("matematica"), "Ciências": inep.get("ciencias")},
    {"Região": "Brasil (SAEB 2021)", "Leitura": saeb_2021_br.get("leitura"), "Matemática": saeb_2021_br.get("matematica")},
    {"Região": "Minas Gerais (SAEB 2021)", "Leitura": saeb_2021_mg.get("leitura"), "Matemática": saeb_2021_mg.get("matematica")},
    {"Região": "Triângulo M. e Alto P. (2021)", "Leitura": saeb_2021_tri.get("leitura"), "Matemática": saeb_2021_tri.get("matematica")},
    {"Região": "Brasil (SAEB 2023)", "Leitura": saeb_2023_br.get("leitura"), "Matemática": saeb_2023_br.get("matematica")},
    {"Região": "Triângulo M. e Alto P. (2023)", "Leitura": saeb_2023_tri.get("leitura"), "Matemática": saeb_2023_tri.get("matematica")},
]

df = pd.DataFrame(dados)

# Mostrar gráficos
st.markdown("### Desempenho em Leitura e Matemática")

col1, col2 = st.columns(2)

with col1:
    fig_leitura = px.bar(df, x="Região", y="Leitura", title="Desempenho em Leitura", text_auto=True)
    st.plotly_chart(fig_leitura, use_container_width=True)

with col2:
    fig_mate = px.bar(df, x="Região", y="Matemática", title="Desempenho em Matemática", text_auto=True)
    st.plotly_chart(fig_mate, use_container_width=True)

# Mostrar tabela
st.markdown("### Tabela de Dados Reais")
st.dataframe(df.set_index("Região"))

st.success("Os dados são extraídos em tempo real do MongoDB dockerizado.")
