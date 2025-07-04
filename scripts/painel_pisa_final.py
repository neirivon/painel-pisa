from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient

st.set_page_config(page_title="Painel PISA Brasil", layout="wide")

st.title("📊 Painel PISA Brasil - OCDE + INEP")
st.markdown("**Análise Integrada dos Dados do PISA para o Brasil (2000 a 2022)**")

# --- Carregar dados do MongoDB com mapeamento de ano ---
@st.cache_data
def carregar_dados_mongo():
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    colecao = db["cy1mdai_stu_qqq"]
    registros = list(colecao.find({}, {
        "CYC": 1,
        "PV1MATH": 1,
        "PV1READ": 1,
        "PV1SCIE": 1,
        "ESCS15": 1
    }))

    df = pd.DataFrame(registros)

    # Mapear CYC → Ano
    mapa_cyc = {
        "1MDA": 2000,
        "2MDA": 2003,
        "3MDA": 2006,
        "4MDA": 2009,
        "5MDA": 2012,
        "6MDA": 2015,
        "7MDA": 2018,
        "8MDA": 2022
    }
    df["Ano"] = df["CYC"].map(mapa_cyc)

    # Renomear campos para exibição
    df.rename(columns={
        "PV1MATH": "Nota em Matemática",
        "PV1READ": "Nota em Leitura",
        "PV1SCIE": "Nota em Ciências",
        "ESCS15": "ESCS (Índice Socioeconômico, Cultural e Escolar)"
    }, inplace=True)

    return df.dropna(subset=["Ano"])

df = carregar_dados_mongo()

# --- Filtros ---
st.sidebar.header("🎛️ Filtros")
anos_disponiveis = sorted(df["Ano"].unique())
anos = st.sidebar.multiselect("Selecione o(s) ano(s):", anos_disponiveis, default=anos_disponiveis)
df_filtrado = df[df["Ano"].isin(anos)]

# --- Dimensão a visualizar ---
dimensao = st.selectbox("📈 Dimensão a visualizar:", [
    "Nota em Matemática", "Nota em Leitura", "Nota em Ciências", "ESCS (Índice Socioeconômico, Cultural e Escolar)"
])

# --- Gráfico interativo ---
fig = px.box(df_filtrado, x="Ano", y=dimensao, points="all", template="plotly_white",
             title=f"Evolução de {dimensao} no Brasil - PISA")
st.plotly_chart(fig, use_container_width=True)

# --- Glossário ---
with st.expander("📘 Glossário"):
    st.markdown("""
- **PISA**: Avaliação internacional trienal de estudantes de 15 anos promovida pela OCDE.
- **ESCS (Índice Socioeconômico, Cultural e Escolar)**: Indicador que combina variáveis econômicas, sociais e educacionais da família do aluno.
- **Notas PISA**: Escala de 0 a 800 em Leitura, Matemática e Ciências.
""")

# --- Rubricas Avaliativas ---
with st.expander("🧩 Rubricas Avaliativas com Base Teórica"):
    st.markdown("""
### 🧠 Interpretação do ESCS (Índice Socioeconômico, Cultural e Escolar)
| Faixa de ESCS | Interpretação |
|---------------|---------------|
| < -1.0        | Vulnerabilidade extrema |
| -1.0 a 0.0    | Vulnerabilidade moderada |
| 0.0 a 1.0     | Condição socioeconômica média |
| > 1.0         | Alta condição socioeconômica |

### 📊 Interpretação das Notas PISA
| Nota          | Nível Cognitivo |
|---------------|------------------|
| < 400         | Baixo desempenho |
| 400 a 499     | Básico |
| 500 a 599     | Adequado |
| ≥ 600         | Avançado |

### 🧭 Interpretações Baseadas em Dados
- A média da OCDE gira em torno de **500 pontos**.  
- Brasil frequentemente apresenta médias **abaixo da OCDE** → Necessidade de ações educativas robustas.
- Desaceleração no crescimento das notas → Reforçar inovação pedagógica.
- Desigualdades regionais → Priorizar políticas de equidade social e educacional.
""")

# --- Fundamentação Teórica ---
with st.expander("📚 Fundamentação Teórica e Proposta Didática"):
    st.markdown("""
O PISA evidencia desafios educacionais brasileiros ligados a desigualdades sociais e práticas pedagógicas desatualizadas.

---

### 🎯 Proposta Educacional Integrada

**📖 Taxonomia de Bloom para Avaliação Cognitiva**  
_Aplicação prática:_  
Implementar avaliações em sala que não apenas cobrem memorização, mas desenvolvam análise crítica, síntese e criação de novos conhecimentos.

**🎮 Metodologias Ativas**  
_Aplicação prática:_  
Utilizar estratégias como Gamificação e Sala de Aula Invertida para aumentar o engajamento dos estudantes e personalizar o aprendizado.

**🧠 Perfil Neuropsicopedagógico**  
_Aplicação prática:_  
Diagnosticar estilos cognitivos e emocionais dos alunos para adaptar métodos de ensino às necessidades individuais, promovendo inclusão e equidade.

---

### 🏛️ Políticas Públicas Propostas

**📊 Rubricas Avaliativas Personalizadas**  
_Aplicação prática:_  
Construir indicadores regionais e escolares baseados em ESCS e notas PISA, propondo metas pedagógicas customizadas.

**📚 Uso contínuo dos dados do PISA**  
_Aplicação prática:_  
Transformar análises do PISA em políticas educacionais dinâmicas, monitoradas ano a ano nas redes públicas.

**🔧 Ferramentas Educacionais Interativas**  
_Aplicação prática:_  
Desenvolver dashboards, aplicativos e simuladores de melhoria de aprendizagem com dados abertos — como este painel PISA Brasil.

---
""")

# --- Créditos ---
st.markdown("---")
st.markdown("👨‍🏫 Desenvolvido por Neirivon Elias Cardoso | ECOSSISTEMA SINAPSE 2.0 | Dados reais extraídos da **OCDE + INEP**, organizados em banco MongoDB 🚀")

