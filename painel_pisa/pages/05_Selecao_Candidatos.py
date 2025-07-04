import streamlit as st
st.set_page_config(page_title="Seleção de Candidatos - PISA OCDE", layout="wide")

from utils.componentes import estilo
estilo()

modo = st.secrets["modo"] if "modo" in st.secrets else "local"

st.title("🎯 Como é feita a seleção dos candidatos no PISA?")

st.markdown("""
### 🧪 Amostragem científica por país

A seleção dos alunos que participam do PISA segue uma **metodologia de amostragem estatística rigorosa**, coordenada pela **OCDE**, com apoio de institutos nacionais (como o INEP, no Brasil).

---

### 🧑‍🎓 Critério principal:

- **Idade: 15 anos completos até o dia 1º de maio do ano da aplicação**
- Independente da série escolar
- Deve estar **matriculado e frequentando** alguma instituição de ensino formal

---

### 📋 Etapas da seleção:

1. **Amostragem das escolas** com estudantes elegíveis
2. **Seleção aleatória dos alunos** dentro dessas escolas
3. Garantia de que a amostra seja **representativa do país como um todo**

---

### 📈 Representatividade

Esse processo garante que os resultados do PISA reflitam **a realidade nacional dos jovens de 15 anos**, possibilitando comparações válidas entre países.
""")

