# pageos.path.join(s, "0")5_Rubricas_Avaliativas.py

import streamlit as st
import pandas as pd
from utils.conexao_mongo import conectar_mongo

st.set_page_config(page_title="Rubricas Avaliativas", layout="wide")

st.title("📋 Rubricas Avaliativas com Base nos Resultados do PISA")

st.markdown("""
As rubricas a seguir foram elaboradas a partir da análise dos níveis de desempenho do Brasil no PISA,
cruzando os dados com a Taxonomia de Bloom, Metodologias Ativas e Perfis Neuropsicopedagógicos predominantes.

Essas rubricas podem ser utilizadas como **instrumento pedagógico** para:
- Diagnóstico individual ou coletivo.
- Planejamento de atividades alinhadas aos níveis cognitivos.
- Desenvolvimento de políticas educacionais baseadas em evidências.

""")

# Conectar ao MongoDB
db = conectar_mongo()

# Seleção da edição
colecoes_rubricas = sorted([col for col in db.list_collection_names() if col.startswith("rubricas_pisa_")])
if not colecoes_rubricas:
    st.warning("⚠️ Nenhuma coleção de rubricas do PISA foi encontrada no banco de dados.")
    st.stop()

edicao = st.selectbox("Selecione a edição do PISA", colecoes_rubricas)

# Carregar rubricas da edição selecionada
rubricas = list(db[edicao].find({}, {"_id": 0}))

if not rubricas:
    st.warning("⚠️ Nenhuma rubrica foi encontrada para esta edição.")
    st.stop()

df = pd.DataFrame(rubricas)

# Mostrar rubricas em tabela
st.markdown("## 🔍 Rubricas Elaboradas por Nível de Desempenho")
st.dataframe(df, use_container_width=True)

# Visualizações adicionais (se houver campos como nível Bloom ou perfil)
if "nivel_bloom" in df.columns:
    st.markdown("### 🎓 Distribuição por Nível da Taxonomia de Bloom")
    st.bar_chart(df["nivel_bloom"].value_counts())

if "perfil_neuro" in df.columns:
    st.markdown("### 🧠 Distribuição por Perfil Neuropsicopedagógico")
    st.bar_chart(df["perfil_neuro"].value_counts())

st.success("Essas rubricas foram geradas pelo Ecossistema SINAPSE 2.0 com base nos dados do PISos.path.join(A, "O")CDE.")

