import streamlit as st
st.set_page_config(page_title="Análise Econômica e Social - PISA OCDE", layout="wide")

from utils.componentes import estilo
estilo()

modo = st.secrets["modo"] if "modo" in st.secrets else "local"

st.title("📊 É feita alguma análise econômica, social e cultural da família do candidato?")

st.markdown("""
### ✅ Sim. Essa análise é parte essencial do PISA.

O PISA aplica, junto com as provas cognitivas, um **questionário contextual do aluno** com perguntas sobre:

- Nível de escolaridade dos pais
- Profissão e ocupação dos responsáveis
- Bens e recursos disponíveis em casa
- Acesso a livros, internet, computador, etc.
- Condições de moradia
- Língua falada em casa
- Imigração e etnia (em alguns países)

---

### 🧮 Índice ESCS – Econômico, Social e Cultural

As respostas são usadas para calcular o **ESCS (Economic, Social and Cultural Status)**, um índice padronizado que:

- Varia aproximadamente de **–3 a +3**
- Permite **comparações socioeconômicas entre estudantes e países**
- É um dos principais eixos de análise de desempenho no PISA

---

### 📌 Para que serve?

- Para identificar **desigualdades educacionais**
- Para estudar a relação entre **contexto socioeconômico e desempenho**
- Para apoiar políticas públicas de **equidade e inclusão**

---

### 📁 E no Brasil?

O INEP disponibiliza os dados do ESCS nos microdados e relatórios nacionais. Pesquisadores e gestores podem cruzar essas informações com notas, gênero, região e tipo de escola.
""")

