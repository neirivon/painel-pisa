import streamlit as st
st.set_page_config(page_title="Viagem para Prova - PISA OCDE", layout="wide")

from utils.componentes import estilo
estilo()

modo = st.secrets["modo"] if "modo" in st.secrets else "local"

st.title("✈️ Os alunos precisam viajar para outro país para fazer a prova?")

st.markdown("""
### ❌ Não. A aplicação é sempre feita **no próprio país**.

A prova do PISA é aplicada **no país de origem dos estudantes**, geralmente em suas próprias escolas, seguindo critérios rigorosos de amostragem e aplicação padronizada definidos pela **OCDE**.

---

### 📍 Como a aplicação ocorre?

- O **INEP**, no caso do Brasil, coordena localmente a aplicação com apoio de aplicadores treinados.
- A OCDE fornece as diretrizes, materiais e protocolos.
- A prova pode ser aplicada em **papel ou computador**, dependendo da edição e infraestrutura disponível.
- Toda a aplicação segue um rigoroso **manual de padronização internacional**, garantindo comparabilidade entre países.

---

### 🌐 Por que essa escolha?

Evitar a necessidade de deslocamento internacional garante:
- **Inclusão de estudantes de diferentes contextos socioeconômicos**
- **Redução de custos operacionais**
- **Maior aderência à realidade educacional local**

Essa estratégia reforça o compromisso do PISA com a **equitatividade e validade científica** de seus resultados.
""")

