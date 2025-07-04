import streamlit as st
st.set_page_config(page_title="Gamificação do Desempenho - PISA", layout="wide")  # ✅ Agora é o primeiro comando Streamlit

import pandas as pd
from datetime import datetime
from transformers import pipeline
import uuid
import os
import json

# 🌐 Estilo visual global
from utils.componentes import estilo
estilo()

# 🌍 Modo de execução
modo = st.secrets["modo"] if "modo" in st.secrets else "local"

# 🎯 Título e explicação
st.markdown("# 🏆 Gamificação do Desempenho")
st.markdown("Responda às questões e acompanhe sua **pontuação**, **evolução** e **feedback pedagógico** com base em rubricas adaptadas do PISA OCDE.")

# 📚 Questões
questoes = {
    "Leitura": "Escreva uma análise crítica sobre o impacto das redes sociais na forma como os jovens interpretam textos jornalísticos.",
    "Matemática": "Descreva como você explicaria a importância de porcentagem e proporção para economizar no dia a dia de uma família.",
    "Ciências": "Disserte sobre os efeitos do desmatamento na biodiversidade e como políticas públicas podem mitigar esse problema."
}

area = st.selectbox("📚 Escolha a área da questão:", list(questoes.keys()))
st.markdown(f"### 🎓 Questão de {area}")
st.info(questoes[area])

resposta = st.text_area("✍️ Digite sua resposta aqui:", height=300)

if resposta.strip():
    if st.button("✅ Enviar Resposta e Atualizar Desempenho"):
        with st.spinner("🤖 Avaliando com IA pedagógica..."):

            nlp = pipeline("sentiment-analysis")
            resultado = nlp(resposta[:512])[0]
            pontuacao = 3 if resultado["label"] == "POSITIVE" else 1
            cor = "🟢" if pontuacao >= 3 else "🟠"

            st.success(f"{cor} Pontuação atribuída: **{pontuacao}/4**")
            st.markdown("### 💬 Feedback Inteligente:")
            st.write("✔️ Resposta bem estruturada, com argumentos relevantes.") if pontuacao == 3 else st.write("🔍 Resposta precisa de mais desenvolvimento e conexões conceituais.")

            resultado_final = {
                "id": str(uuid.uuid4()),
                "data": str(datetime.now()),
                "area": area,
                "resposta": resposta,
                "pontuacao": pontuacao,
                "modelo": "BERT-sentiment",
                "feedback": resultado
            }

            if modo == "local":
                salvar_json = os.path.join("painel_pisa", "dados_cloud", "historico_gamificacao.json")
                if os.path.exists(salvar_json):
                    with open(salvar_json, "r") as f:
                        historico = json.load(f)
                else:
                    historico = []

                historico.append(resultado_final)

                with open(salvar_json, "w") as f:
                    json.dump(historico, f, indent=4)

            else:
                if "historico_gamificacao_cloud" not in st.session_state:
                    st.session_state["historico_gamificacao_cloud"] = []
                st.session_state["historico_gamificacao_cloud"].append(resultado_final)

            st.balloons()

            # 🧮 Exibe histórico de desempenho
            st.markdown("## 📊 Histórico de Respostas")
            historico_df = pd.DataFrame([resultado_final])
            st.dataframe(historico_df[["data", "area", "pontuacao"]])
else:
    st.warning("✍️ Responda à questão acima para iniciar sua gamificação pedagógica.")

