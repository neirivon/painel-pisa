import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Configuração da página
st.set_page_config(layout="wide", page_title="Evolução PISA Brasil")

# Estilo global
st.markdown("""
<style>
    .big-font {
        font-size: 2.3em !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big-font'>📈 Evolução do Desempenho do Brasil no PISA (2000–2022)</div>", unsafe_allow_html=True)

# Carregar dados do JSON
CAMINHO = os.path.join("painel_pisa", "dados_cloud", "dados_longitudinais_brasil.json")
with open(CAMINHO, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Processar dados
df = pd.DataFrame(dados)
df_long = df.melt(id_vars="Ano", var_name="Área", value_name="Pontuação")

# Gráfico interativo
fig = px.line(df_long, x="Ano", y="Pontuação", color="Área",
              markers=True, line_shape="spline",
              title="Pontuação Média do Brasil no PISA por Área",
              labels={"Pontuação": "Pontuação Média", "Ano": "Ano"},
              hover_name="Área")

fig.update_layout(hovermode="x unified", height=500)
st.plotly_chart(fig, use_container_width=True)

# Interpretação
st.info("""
📌 **Interpretação Pedagógica e Política:**

- **2003:** Leve recuperação pós-crise de aprendizagem. Influência de mudanças no ENEM.
- **2009:** Avanço graças ao IDEB e políticas de alfabetização e avaliação externa.
- **2015:** Queda relacionada à crise institucional e cortes em políticas educacionais.
- **2018–2022:** Estagnação, apesar de maior alinhamento técnico ao modelo PISA.

🎯 O gráfico não mostra apenas notas — mostra o reflexo de **escolhas políticas e pedagógicas** feitas ao longo de mais de duas décadas.
""")

