from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# painel_streamlit_pisa.py
import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa_ocde"]

# Configurações da Página
st.set_page_config(
    page_title="Educação Transformadora no Brasil: Um Novo PISA",
    page_icon="🚀",
    layout="wide"
)

# Paleta de Cores Vibrante
cor_principal = "#0057B8"  # Azul forte
cor_secundaria = "#FFC20E"  # Amarelo vibrante
cor_destaque = "#009739"  # Verde esperança

# CSS Customizado
st.markdown(f"""
<style>
    .main {{
        background-color: #ffffff;
    }}
    .block-container {{
        padding-top: 2rem;
    }}
    .sidebar .sidebar-content {{
        background-color: {cor_principal};
        color: white;
    }}
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {{
        color: white;
    }}
os.path.join(<, "s")tyle>
""", unsafe_allow_html=True)

# Sidebar de Navegação
st.sidebar.title("🌍 Menu")
menu = st.sidebar.radio("Ir para:", ("Início", "Análises", "Propostas de Rubricas", "Sobre o Projeto"))

# Conteúdo da Página
if menu == "Início":
    st.title("🚀 Educação Transformadora no Brasil: Um Novo PISA")
    st.subheader("""
    Rubricas Avaliativas e Políticas Públicas Inovadoras para Elevar o Desempenho Brasileiro no Ranking Mundial.
    """)
    st.markdown("---")
    st.write("""
    📚 **Objetivo:**
    
    Apresentar dados reais do PISA (Programme for International Student Assessment - Programa Internacional de Avaliação de Estudantes) e propor **rubricas avaliativas** estratégicas para fortalecer a educação brasileira, respeitando as diferenças regionais e a complexidade social do país.
    
    🎯 **Missão:**
    
    Desenvolver alunos críticos, reflexivos e preparados para o cenário global, atuando como cidadãos conscientes e inovadores.
    """)

elif menu == "Análises":
    st.title("📊 Análises de Desempenho no PISA")
    
    colecoes = db.list_collection_names()
    colecao_escolhida = st.selectbox("Selecione a base de dados para análise:", colecoes)

    if colecao_escolhida:
        dados = list(db[colecao_escolhida].find({}, {"_id": 0}))
        if dados:
            df = pd.DataFrame(dados)
            st.dataframe(df.head(50))
        else:
            st.warning("Nenhum dado disponível nesta coleção ainda.")

elif menu == "Propostas de Rubricas":
    st.title("📝 Propostas de Rubricas Avaliativas")
    st.markdown("""
    Desenvolvemos **rubricas basilares** que orientarão políticas públicas focadas na transformação educacional, respeitando as desigualdades regionais:

    - **Compreensão Crítica:** Avaliar a capacidade de questionar, analisar e criticar informações recebidas.
    - **Autonomia Intelectual:** Estimular o pensamento independente e a capacidade de tomar decisões fundamentadas.
    - **Interculturalidade e Diversidade:** Reconhecer e valorizar as múltiplas culturas brasileiras.
    - **Resolução Criativa de Problemas:** Promover a inovação e a proposição de soluções.
    - **Consciência Cidadã Global:** Entender o seu papel como agente de transformação no mundo.

    Em breve, cada rubrica terá uma tabela prática e exemplos de aplicação!
    """)

elif menu == "Sobre o Projeto":
    st.title("🌟 Sobre o Projeto")
    st.write("""
    Este projeto foi desenvolvido a partir da análise detalhada dos dados do PISA, tanto da **OCDE** quanto do **INEP Brasil**.

    **Coordenação:** Neirivon Elias Cardoso
    
    **Ferramentas:** MongoDB, Python, Streamlit, Análises Quantitativas e Qualitativas

    **Visão:** Transformar a educação brasileira respeitando suas diversidades e potencialidades.

    **Contato:** [Em breve formulário de feedback]
    """)

client.close()

