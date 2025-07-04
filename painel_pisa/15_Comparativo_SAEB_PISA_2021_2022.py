from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

st.set_page_config(page_title="Comparativo SAEB × PISA", layout="wide")

# === Carregar dados do MongoDB (SAEB 2021 – 9º ano) ===
@st.cache_data
def carregar_dados_saeb():
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["saeb"]
    collection = db["saeb_2021_municipios_9ano"]
    df = pd.DataFrame(list(collection.find({}, {"_id": 0, "NO_UF": 1, "MEDIA_9_LP": 1, "MEDIA_9_MT": 1})))
    client.close()
    return df

# === Carregar dados do PISA (2022) – pré-processado ===
@st.cache_data
def carregar_dados_pisa():
    return pd.DataFrame({
        "UF": ["MG", "SP", "BA", "CE", "RS", "PA", "MA", "RJ", "PE", "PR"],
        "ESTADO": ["Minas Gerais", "São Paulo", "Bahia", "Ceará", "Rio Grande do Sul", "Pará", "Maranhão", "Rio de Janeiro", "Pernambuco", "Paraná"],
        "PISA_MT": [388, 395, 342, 375, 402, 345, 336, 392, 348, 405],
        "PISA_LP": [410, 420, 360, 400, 430, 362, 355, 415, 365, 432]
    })

# === Normalizar valores em escala percentual ===
def normalizar_escala(series, minimo, maximo):
    return ((series - minimo)os.path.join( , " ")(maximo - minimo)) * 100

# === Preparar dados ===
df_saeb = carregar_dados_saeb()
df_saeb_grouped = df_saeb.groupby("NO_UF").agg({
    "MEDIA_9_MT": "mean",
    "MEDIA_9_LP": "mean"
}).reset_index().rename(columns={"NO_UF": "ESTADO"})

df_pisa = carregar_dados_pisa()

# Escalas:
# SAEB: média 250, mínimo teórico ~0, máximo ~500
# PISA: média 500, mínimo ~200, máximo ~800
df_saeb_grouped["MT_SAEB_%"] = normalizar_escala(df_saeb_grouped["MEDIA_9_MT"], 200, 400)
df_saeb_grouped["LP_SAEB_%"] = normalizar_escala(df_saeb_grouped["MEDIA_9_LP"], 200, 400)
df_pisa["MT_PISA_%"] = normalizar_escala(df_pisa["PISA_MT"], 200, 600)
df_pisa["LP_PISA_%"] = normalizar_escala(df_pisa["PISA_LP"], 200, 600)

# === Unir DataFrames ===
comparativo = pd.merge(df_saeb_grouped, df_pisa, on="ESTADO", how="inner")

# === Gráficos ===
st.title("📊 Comparativo: SAEB 2021 (9º Ano) × PISA 2022")
st.markdown("Comparação de desempenho em **escala percentual normalizada** entre avaliações nacionais e internacionais.")

col1, col2 = st.columns(2)

with col1:
    fig_mt = px.bar(
        comparativo.sort_values("MT_PISA_%", ascending=False),
        x="ESTADO",
        y=["MT_SAEB_%", "MT_PISA_%"],
        barmode="group",
        color_discrete_sequence=["#636EFA", "#EF553B"],
        labels={"value": "Proficiência (%)", "ESTADO": "Estado", "variable": "Fonte"},
        title="📐 Matemática – SAEB vs PISA"
    )
    st.plotly_chart(fig_mt, use_container_width=True)

with col2:
    fig_lp = px.bar(
        comparativo.sort_values("LP_PISA_%", ascending=False),
        x="ESTADO",
        y=["LP_SAEB_%", "LP_PISA_%"],
        barmode="group",
        color_discrete_sequence=["#00CC96", "#AB63FA"],
        labels={"value": "Proficiência (%)", "ESTADO": "Estado", "variable": "Fonte"},
        title="📘 Leitura – SAEB vs PISA"
    )
    st.plotly_chart(fig_lp, use_container_width=True)

# === Explicações ===
st.markdown("---")
st.markdown("### ℹ️ Notas sobre a Normalização e Comparação")
st.markdown("""
- As escalas do SAEB e do PISA são **diferentes** em origem e construção. Para viabilizar a comparação, foi aplicada uma **normalização percentual linear**.
- Esta comparação tem caráter **pedagógico e exploratório**, e não pretende substituir análises técnicas mais aprofundadas.
- Estados com melhores resultados em ambos os exames indicam **coerência entre as avaliações** e políticas educacionais eficazes.
""")

