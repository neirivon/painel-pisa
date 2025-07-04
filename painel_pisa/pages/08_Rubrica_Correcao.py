import streamlit as st
st.set_page_config(page_title="Rubrica de Correção - PISA OCDE", layout="wide")

from utils.componentes import estilo
estilo()

modo = st.secrets["modo"] if "modo" in st.secrets else "local"

st.title("🧮 Como funciona a correção das provas do PISA?")

st.markdown("""
### 📋 Existe uma **rubrica internacional padronizada**

As respostas dissertativas do PISA (principalmente em **Leitura** e **Ciências**) são avaliadas com base em **rubricas detalhadas**, que definem:

- **Níveis de desempenho**
- **Critérios objetivos**
- **Descritores esperados**

---

### 📚 Dimensões avaliadas

Cada área tem suas **dimensões cognitivas**:

#### 📖 Leitura
- Localizar e recuperar informações
- Compreender e integrar
- Avaliar e refletir

#### 🧪 Ciências
- Explicar fenômenos cientificamente
- Avaliar e projetar investigação científica
- Interpretar dados e evidências cientificamente

#### ➗ Matemática
- Formular situações matemáticas
- Empregar conceitos e procedimentos
- Interpretar e comunicar resultados

---

### 🎯 Níveis de proficiência

As respostas são classificadas em **níveis numerados** (ex: de 1 a 6 ou 1 a 4), conforme:

- Correção conceitual
- Clareza e organização
- Aplicação contextual
- Uso apropriado de estratégias

---

### ✨ Exemplo simplificado de rubrica:

| Nível | Descrição resumida                                |
|-------|---------------------------------------------------|
| 0     | Resposta em branco ou totalmente incorreta        |
| 1     | Resposta parcial ou incompleta                    |
| 2     | Resposta correta, mas com explicação limitada     |
| 3     | Resposta bem estruturada, clara e contextualizada |

---

As rubricas completas são disponibilizadas pela OCDE em manuais técnicos e documentos de aplicação restrita a avaliadores.
""")

