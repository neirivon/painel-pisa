import streamlit as st
st.set_page_config(page_title="Tipos de Prova - PISA OCDE", layout="wide")

from utils.componentes import estilo
estilo()

modo = st.secrets["modo"] if "modo" in st.secrets else "local"

st.title("📝 Quais tipos de prova são aplicadas no PISA?")

st.markdown("""
### 📚 Áreas avaliadas

O PISA aplica provas padronizadas para medir **competências de estudantes de 15 anos** em três grandes áreas:

- **Leitura** (Reading)
- **Matemática** (Mathematics)
- **Ciências** (Science)

---

### 🧪 Tipos de itens

Os testes incluem diferentes tipos de questões, como:

- Questões de **múltipla escolha**
- Itens de **resposta construída** (como perguntas abertas)
- Itens baseados em **situações-problema contextualizadas**
- Simulações baseadas em computador (em edições recentes)

---

### 💡 Foco variável por edição

A cada edição do PISA, uma das áreas recebe **maior peso** (chamada de área principal), enquanto as outras são áreas secundárias.

Por exemplo:
- **2018** → foco em Leitura
- **2022** → foco em Matemática

---

### 🖥️ Provas em papel ou computador?

- Desde 2015, o padrão é a **aplicação computadorizada**
- O Brasil optou por prova em **computador em 2015 e 2018**
- Em 2022, a aplicação foi **totalmente digital**
""")

