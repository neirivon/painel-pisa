import streamlit as st
st.set_page_config(page_title="Dados e Representação do PISA no Brasil", layout="wide")

from utils.componentes import estilo
estilo()

modo = st.secrets["modo"] if "modo" in st.secrets else "local"

st.title("🗃️ Onde ficam armazenados os dados e relatórios do PISA relacionados a cada edição e quem representa o Brasil?")

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

# 👇 Novo bloco inserido abaixo
st.markdown("---")
st.markdown("### 📊 Comparativo de Estruturas: OCDE x INEP")

st.markdown("""
Esta tabela resume como os dados do PISA são apresentados pelas duas entidades:

| Aspecto                     | OCDE (Internacional)                                            | INEP (Brasil)                                                  |
|----------------------------|------------------------------------------------------------------|----------------------------------------------------------------|
| **Formato dos dados**      | `.csv`, `.sav`, `.sas7bdat`                                     | `.pdf`, `.xlsx`                                                |
| **Microdados**             | Sim, completos por estudante (com códigos de país, escola etc.) | Parcialmente agregados ou recortes específicos                 |
| **Relatórios**             | Técnicos e analíticos, com foco global e rankings               | Relatórios descritivos focados no desempenho brasileiro        |
| **Ferramentas de análise** | SPSS, R, Python, Stata                                          | Principalmente PDF e gráficos fixos em relatórios              |
| **Campos educacionais**    | ESCS, PV1READ, PV1MATH, PV1SCIE, IDSTUD, etc.                   | Médias por região, escola pública/privada, gênero              |
| **Foco analítico**         | Comparação entre países, tendências globais                     | Situação do Brasil ao longo do tempo                           |
| **Periodicidade**          | Trienal                                                         | Trienal (com eventual atraso na publicação)                    |

Essa comparação ajuda a entender como unir forças: usar a robustez dos microdados da OCDE com a contextualização nacional feita pelo INEP.
""")

