import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Define o modo e caminho
modo = st.secrets["modo"] if "modo" in st.secrets else "local"
CAMINHO = "painel_pisa/dados_cloud" if modo == "cloud" else "painel_pisa/dados_cloud"

# Estilo global se existir
try:
    from utils.estilo import stilo
    stilo()
except:
    pass

st.set_page_config(layout="wide", page_title="📈 Análise Longitudinal – PISA Brasil")
st.title("📈 Análise Longitudinal do Brasil no PISA (2000–2022)")
st.markdown("### Evolução da pontuação média nas áreas de Leitura, Matemática e Ciências")

# Leitura do JSON com os dados
caminho_json = os.path.join(CAMINHO, "analise_longitudinal_brasil.json")
with open(caminho_json, "r", encoding="utf-8") as f:
    dados = json.load(f)

# Processamento
df = pd.DataFrame(dados)
df_long = df.melt(id_vars="Ano", var_name="Área", value_name="Pontuação")

# Gráfico interativo
fig = px.line(df_long, x="Ano", y="Pontuação", color="Área",
              markers=True, line_shape="spline",
              title="Desempenho do Brasil no PISA por Área (2000–2022)",
              labels={"Pontuação": "Pontuação Média", "Ano": "Ano"},
              hover_name="Área")

fig.update_layout(hovermode="x unified", height=500)
st.plotly_chart(fig, use_container_width=True)

# Análise crítica
st.markdown("### 🔍 Interpretação Crítica dos Dados")
st.info("""
O desempenho do Brasil no PISA evoluiu gradualmente entre 2000 e 2012, mas estagnou ou regrediu em alguns anos recentes, especialmente em Matemática.

Alguns fatores possíveis:

- Mudanças políticas e cortes em educação (2015–2022)
- Crescimento desigual de políticas de leitura e formação docente
- Pressão por resultados sem transformação estrutural

**Importante:** A leitura isolada desses dados é limitada. O cruzamento com ESCS e os protocolos técnicos permite interpretações mais precisas e contextualizadas.
""")

