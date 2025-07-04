# pageos.path.join(s, "1")5_Explicacao_ESCS_SAEB.py

import streamlit as st
import pandas as pd
from utils.estilo_global import aplicar_estilo

# Configuração da página
st.set_page_config(page_title="📉 ESCS no SAEB – Foco no Nível 0", layout="wide")
aplicar_estilo()

st.title("📉 Por que o SAEB relaciona o ESCS apenas ao Nível 0?")

st.markdown("""
O **SAEB** exibe a relação entre o **ESCS (Status Econômico, Social e Cultural)** e o desempenho dos alunos **apenas para o Nível 0 (abaixo do mínimo esperado)**.

Essa decisão é **técnica e pedagógica**, como mostra a tabela abaixo:
""")

# Criar DataFrame com os dados da tabela
dados = {
    "Critério": [
        "1. Foco em vulnerabilidade extrema",
        "2. Direcionamento de políticas públicas",
        "3. Robustez estatística no nível 0",
        "4. Comunicação clara à sociedade",
        "5. Evita estigmatização em outros níveis"
    ],
    "Explicação": [
        "O nível 0 representa os estudantes com maior risco de exclusão educacional. A maioria tem ESCS muito baixo.",
        "Permite ações como reforço escolar, distribuição de recursos e programas como o 'Alfabetiza Brasil'.",
        "A correlação negativa entre ESCS e desempenho é mais forte no nível 0. Nos níveis superiores, há outros fatores envolvidos.",
        "Facilita mostrar que o problema não é do aluno, mas do contexto socioeconômico.",
        "Mostrar ESCS nos níveis altos poderia reforçar preconceitos, como 'pobres não aprendem', o que é falso e perigoso."
    ]
}

df = pd.DataFrame(dados)

# Exibir tabela
st.dataframe(df, use_container_width=True)

# Rodapé explicativo
st.markdown("""
---
🔍 **Observação importante:**  
O objetivo não é rotular, mas sim **identificar onde a desigualdade mais impacta** o aprendizado.  
**Todos os estudantes podem alcançar altos níveis**, independentemente do ESCS — desde que as **condições pedagógicas e estruturais sejam garantidas**.
""")

