from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# pageos.path.join(s, "1")3_Dashboard_SAEB_2021_5Ano.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient

# ✅ Deve ser o primeiro comando do Streamlit
st.set_page_config(page_title="Dashboard SAEB 2021 – 5º Ano", layout="wide")

# 🔄 Conexão MongoDB e cache
@st.cache_data
def carregar_dados_mongo():
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["saeb"]
    collection = db["saeb_2021_municipios_5ano"]
    df = pd.DataFrame(list(collection.find({}, {"_id": 0})))
    client.close()
    return df

# 🚀 Carregar dados
df = carregar_dados_mongo()
df_validos = df.dropna(subset=["PROFICIENCIA_LP_SAEB", "PROFICIENCIA_MT_SAEB"])

# 🏅 Top e 🚨 Bottom 10 - Língua Portuguesa
top10_lp = df_validos.sort_values("PROFICIENCIA_LP_SAEB", ascending=False).head(10)
bottom10_lp = df_validos.sort_values("PROFICIENCIA_LP_SAEB", ascending=True).head(10)

# 🧠 Top e 🚨 Bottom 10 - Matemática
top10_mt = df_validos.sort_values("PROFICIENCIA_MT_SAEB", ascending=False).head(10)
bottom10_mt = df_validos.sort_values("PROFICIENCIA_MT_SAEB", ascending=True).head(10)

# 🖥️ Título
st.title("📊 Dashboard SAEB 2021 – 5º Ano (Municípios)")

# 📘 Língua Portuguesa
col1, col2 = st.columns(2)
with col1:
    st.subheader("🏅 Top 10 – Língua Portuguesa")
    fig, ax = plt.subplots()
    sns.barplot(data=top10_lp, y="ID_MUNICIPIO", x="PROFICIENCIA_LP_SAEB", palette="Blues", ax=ax)
    ax.set_title("Top 10 Municípios – LP")
    ax.set_xlabel("Proficiência")
    ax.set_ylabel("Município (ID)")
    st.pyplot(fig)

with col2:
    st.subheader("🚨 Piores 10 – Língua Portuguesa")
    fig, ax = plt.subplots()
    sns.barplot(data=bottom10_lp, y="ID_MUNICIPIO", x="PROFICIENCIA_LP_SAEB", palette="Reds", ax=ax)
    ax.set_title("Bottom 10 Municípios – LP")
    ax.set_xlabel("Proficiência")
    ax.set_ylabel("Município (ID)")
    st.pyplot(fig)

# 🧮 Matemática
col3, col4 = st.columns(2)
with col3:
    st.subheader("🏅 Top 10 – Matemática")
    fig, ax = plt.subplots()
    sns.barplot(data=top10_mt, y="ID_MUNICIPIO", x="PROFICIENCIA_MT_SAEB", palette="Greens", ax=ax)
    ax.set_title("Top 10 Municípios – Matemática")
    ax.set_xlabel("Proficiência")
    ax.set_ylabel("Município (ID)")
    st.pyplot(fig)

with col4:
    st.subheader("🚨 Piores 10 – Matemática")
    fig, ax = plt.subplots()
    sns.barplot(data=bottom10_mt, y="ID_MUNICIPIO", x="PROFICIENCIA_MT_SAEB", palette="Oranges", ax=ax)
    ax.set_title("Bottom 10 Municípios – Matemática")
    ax.set_xlabel("Proficiência")
    ax.set_ylabel("Município (ID)")
    st.pyplot(fig)

# 🧠 Fonte
st.markdown("---")
st.markdown("📌 Fonte: Microdados SAEB 2021 (INEos.path.join(P, "M")EC) – 5º Ano do Ensino Fundamental.")

