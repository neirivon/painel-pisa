import streamlit as st
st.set_page_config(page_title="O que e o pisa - PISA OCDE", layout="wide")
from utils.componentes import estilo
import sys
import os

# Aplica o estilo padronizado
estilo()

# Define modo local/cloud
modo = st.secrets["modo"] if "modo" in st.secrets else "local"

# Título da página
st.title("📖 O que é o PISA?")

st.markdown("""
### ✳️ Definição

O **PISA** (Programme for International Student Assessment), ou **Programa Internacional de Avaliação de Estudantes**, é uma avaliação internacional aplicada a cada três anos, coordenada pela **OCDE** – Organização para a Cooperação e Desenvolvimento Econômico.

Seu principal objetivo é **avaliar a capacidade dos estudantes de 15 anos de idade** em aplicar conhecimentos de **leitura, matemática e ciências** em situações do cotidiano. Mais do que medir conteúdo escolar, o PISA avalia **competências essenciais para a vida adulta**.

---

### 🔠 Significado do Acrônimo

| Letra | Termo em Inglês | Tradução |
|-------|------------------|----------|
| P     | Programme        | Programa |
| I     | for International| para Internacional |
| S     | Student          | Estudantes |
| A     | Assessment       | Avaliação |

---

### 🌐 Quem organiza o PISA?

A avaliação é organizada pela **OCDE (OECD - Organisation for Economic Co-operation and Development)**, uma entidade internacional composta por mais de 30 países-membros, cujo foco é promover políticas públicas que melhorem o bem-estar econômico e social da população mundial.

No Brasil, a aplicação do PISA é coordenada pelo **INEP (Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira)**, vinculado ao Ministério da Educação (MEC).

---

### 💰 Quem financia o PISA?

O financiamento do PISA ocorre de forma **compartilhada entre os países participantes**. Cada país arca com os custos operacionais da aplicação local (como impressão das provas, logística e treinamento), enquanto a OCDE coordena o projeto global, sendo custeada por contribuições dos países-membros.

No caso do Brasil, os recursos para a aplicação do PISA são oriundos do **orçamento público federal**, repassado ao INEP/MEC.
""")

