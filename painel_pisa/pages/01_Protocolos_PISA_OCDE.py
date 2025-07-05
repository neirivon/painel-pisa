import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuração inicial
st.set_page_config(layout="wide", page_title="Protocolos PISA OCDE")

# Caminho robusto para imagens
CAMINHO_IMAGENS = Path(__file__).parent.parent / "assets" / "imagens"

# Título
st.markdown("<h1 style='font-size: 3em;'>📘 Protocolos PISA OCDE</h1>", unsafe_allow_html=True)
st.markdown("### 🔍 Como são definidos os processos, instrumentos e critérios na avaliação internacional do PISA/OCDE?")

# ===============================
# 📊 1. Gráfico de documentos
# ===============================
st.markdown("## 📊 Distribuição dos Protocolos por Coleção")

st.image(CAMINHO_IMAGENS / "grafico_protocolo_pisa_2022.png",
         caption="Documentos Armazenados por Tipo de Protocolo",
         use_container_width=True)

st.info("""
🔍 Este gráfico mostra a **quantidade de documentos disponíveis** por tipo de protocolo do PISA/OCDE (edição 2022).

O **Volume 1** se destaca por ser o documento técnico central, onde estão definidos os critérios avaliativos, a TRI e as estratégias metodológicas globais.
""")

# ===============================
# ☁️ 2. Nuvem de palavras
# ===============================
st.markdown("## ☁️ Nuvem de Palavras dos Protocolos do PISA OCDE")

st.image(CAMINHO_IMAGENS / "nuvem_palavras_protocolo.png",
         caption="Principais termos dos protocolos do PISA 2022",
         use_container_width=True)

# ===============================
# 🧠 3. Painel Interativo: Protocolo mais denso
# ===============================
st.markdown("---")
st.markdown("<h2 style='font-size: 2em;'>🔬 Destaques dos Protocolos PISA OCDE</h2>", unsafe_allow_html=True)
st.markdown("### 💡 Explore os protocolos mais densos, impactantes e invisíveis do PISA/OCDE")

vol1_info = {
    "Título": "📘 Volume 1 – Technical Report (protocolo_pisa_2022_res_vol1)",
    "Documentos": 12,
    "Função": "Cérebro técnico do PISA 2022",
    "Conteúdos-Chave": [
        "✔️ Teoria de Resposta ao Item (TRI)",
        "✔️ Escalas de Proficiência por Área",
        "✔️ Amostragem e Estrutura de Dados",
        "✔️ Design dos Instrumentos Avaliativos",
        "✔️ Estratégias de Validação Estatística"
    ],
    "Impacto": "Define o que é 'saber' em 2022 para a OCDE. É a base metodológica que assegura confiabilidade e comparabilidade global.",
    "Mensagem": "Se você deseja compreender o DNA da avaliação internacional, comece por este protocolo."
}

st.metric(label="📂 Nº de Documentos", value=vol1_info["Documentos"])
st.success(vol1_info["Função"])
st.markdown(f"### {vol1_info['Título']}")
st.markdown(f"<p style='font-size:1.2em'>{vol1_info['Impacto']}</p>", unsafe_allow_html=True)
st.markdown("#### 🔍 Conteúdos Principais:")
for item in vol1_info["Conteúdos-Chave"]:
    st.markdown(f"- {item}")
st.info(f"🧠 {vol1_info['Mensagem']}")

# ===============================
# 📈 4. Gráfico Longitudinal
# ===============================
st.markdown("## 📈 Linha do Tempo: Participação do Brasil no PISA (2000–2022)")

dados_long = {
    "Ano": [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022],
    "Leitura": [396, 403, 393, 412, 410, 407, 413, 410],
    "Matemática": [334, 356, 370, 386, 391, 377, 384, 379],
    "Ciências": [None, None, 390, 405, 405, 401, 404, 403]
}

df_long = pd.DataFrame(dados_long)
df_long = df_long.melt(id_vars="Ano", var_name="Área", value_name="Pontuação")

fig_long = px.line(df_long, x="Ano", y="Pontuação", color="Área",
                   markers=True, line_shape="spline",
                   title="Desempenho do Brasil no PISA por Área (2000–2022)",
                   labels={"Pontuação": "Pontuação Média", "Ano": "Ano"},
                   hover_name="Área")

fig_long.update_layout(hovermode="x unified", height=500)
st.plotly_chart(fig_long, use_container_width=True)

# ===============================
# 🏁 5. Conclusão
# ===============================
st.markdown("## 🏁 Conclusão Estratégica")

st.success("""
📌 Os protocolos do PISA OCDE são mais do que diretrizes técnicas. Eles:

- Garantem **justiça internacional**, mesmo entre países desiguais.
- Promovem **confiabilidade estatística**, graças à TRI.
- Exigem **transparência** e rigor metodológico.

✅ **Quem compreende os protocolos, compreende o PISA.**
""")

