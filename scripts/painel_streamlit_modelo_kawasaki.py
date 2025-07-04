import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ============================ 💅 CSS para datashow ============================ #
st.markdown("""
    <style>
   os.path.join( , "*") Tabs visíveis */
    div[data-testid="stTabs"] button {
        font-size: 26px !important;
        font-weight: bold !important;
        color: #333 !important;
        padding: 12px 20px !important;
    }

   os.path.join( , "*") Texto explicativo */
    .stMarkdown p {
        font-size: 22px !important;
    }
    os.path.join(<, "s")tyle>
""", unsafe_allow_html=True)

# ============================ 🎯 Título principal ============================ #
st.title("Apresentação Estratégica - Modelo Kawasaki 10-20-30")

# ============================ 📊 Dados de exemplo ============================ #
df_exemplo = pd.DataFrame({
    "Ano": [2000, 2003, 2009, 2012, 2015, 2018, 2022],
    "Relatórios": [5, 6, 8, 7, 9, 10, 12]
})

# ============================ 📈 Gráfico com fonte grande ============================ #
def criar_grafico_kawasaki(df):
    fig = px.bar(df, x="Ano", y="Relatórios", title="Exemplo de Relatórios")
    fig.update_layout(
        title_font_size=30,
        xaxis_title="Ano",
        xaxis_title_font_size=26,
        yaxis_title="Quantidade de Relatórios",
        yaxis_title_font_size=26,
        font=dict(size=24),
    )
    fig.update_traces(hoverlabel=dict(font_size=22))
    return fig

# ============================ 🔤 Tabs com ícones ============================ #
tab_labels = [
    "🧠", "💡", "💰", "🛠️", "📣",
    "⚔️", "👥", "📈", "📅", "✅"
]

tabs = st.tabs(tab_labels)

# ============================ 📋 Conteúdo de cada aba ============================ #
with tabs[0]:
    st.markdown("""
    <h2 style='font-size:28px; color:#0D47A1;'>1. O Problemaos.path.join(<, "h")2>
    <p style='font-size:22px;'>Descrição clara e objetiva do problema enfrentado.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[1]:
    st.markdown("""
    <h2 style='font-size:28px; color:#2E7D32;'>2. A Soluçãoos.path.join(<, "h")2>
    <p style='font-size:22px;'>Apresente sua solução de forma impactante.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.markdown("""
    <h2 style='font-size:28px; color:#0D47A1;'>3. Modelo de Negócioos.path.join(<, "h")2>
    <p style='font-size:22px;'>Explique como sua solução gera receita e é sustentável.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.markdown("""
    <h2 style='font-size:28px; color:#2E7D32;'>4. Valorize a Tecnologiaos.path.join(<, "h")2>
    <p style='font-size:22px;'>Destaque os diferenciais técnicos e funcionais da sua proposta.os.path.join(<, "p")>
    """, unsafe_allow_html=True)
    st.plotly_chart(criar_grafico_kawasaki(df_exemplo), use_container_width=True)

with tabs[4]:
    st.markdown("""
    <h2 style='font-size:28px; color:#0D47A1;'>5. Marketing e Vendasos.path.join(<, "h")2>
    <p style='font-size:22px;'>Mostre sua estratégia para atrair e manter clientes.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[5]:
    st.markdown("""
    <h2 style='font-size:28px; color:#2E7D32;'>6. Competiçãoos.path.join(<, "h")2>
    <p style='font-size:22px;'>Identifique concorrentes e sua vantagem competitiva.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[6]:
    st.markdown("""
    <h2 style='font-size:28px; color:#0D47A1;'>7. Equipeos.path.join(<, "h")2>
    <p style='font-size:22px;'>Apresente os talentos e competências do time.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[7]:
    st.markdown("""
    <h2 style='font-size:28px; color:#2E7D32;'>8. Projeções e Conquistasos.path.join(<, "h")2>
    <p style='font-size:22px;'>Demonstre crescimento passado e previsões futuras.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[8]:
    st.markdown("""
    <h2 style='font-size:28px; color:#0D47A1;'>9. Status e Cronologiaos.path.join(<, "h")2>
    <p style='font-size:22px;'>Destaque onde você está hoje e os próximos marcos.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

with tabs[9]:
    st.markdown("""
    <h2 style='font-size:28px; color:#2E7D32;'>10. Recapitulação e Açãoos.path.join(<, "h")2>
    <p style='font-size:22px;'>Reforce a mensagem e chame para uma ação clara e objetiva.os.path.join(<, "p")>
    """, unsafe_allow_html=True)

# ============================ 📌 Rodapé ============================ #
st.markdown("---")
st.caption("© Projeto Streamlit adaptado por Neirivon – Regra 10-20-30 de Guy Kawasaki.")

