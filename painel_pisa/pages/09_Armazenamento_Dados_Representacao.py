import streamlit as st
st.set_page_config(page_title="Dados e Representação do PISA no Brasil", layout="wide")

from utils.componentes import estilo
estilo()

modo = st.secrets["modo"] if "modo" in st.secrets else "local"

st.title("🗃️ Onde ficam armazenados os dados do PISA e quem representa o Brasil?")

st.markdown("""
### 🌐 Dados internacionais: OCDE

Os microdados, relatórios técnicos e análises comparativas do PISA são armazenados e disponibilizados pela **OCDE** em:

- [https://www.oecd.org/pisa/](https://www.oecd.org/pisa/)
- Downloads de **bases de dados internacionais** (em `.sav`, `.csv` e `.sas7bdat`)
- Manuais de aplicação, códigos dos itens, guias técnicos, escalas e rubricas

---

### 🇧🇷 Dados nacionais: INEP

No Brasil, o órgão responsável é o **INEP** – Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira, ligado ao MEC.

Ele:
- Coordena a aplicação do PISA no território brasileiro
- Publica **relatórios específicos do Brasil** por edição
- Disponibiliza os microdados nacionais e materiais de apoio

Acesse: [https://www.gov.br/inep](https://www.gov.br/inep)

---

### 🗂️ Armazenamento no projeto PISA Streamlit

Neste projeto, os dados do PISA estão:

- **No MongoDB** (modo local): banco `pisa`, com coleções por edição
- **Em arquivos CSV/JSON** (modo cloud): disponíveis para análises, dashboards e inferência

Isso permite comparações longitudinais e análises educacionais com base em rubricas adaptadas.
""")

st.code("""
{
  "colecao": "pisa_2022",
  "campos": ["ESCS15", "PV1READ", "PV1MATH", "PV1SCIE", "AGE", "CNT"],
  "relatorio_inep": "relatorios_ocde_2022",
  "analise_taxonomia": true
}
""", language="json")

