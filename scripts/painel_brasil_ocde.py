from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# painel_brasil_ocde.py
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.graph_objects as go

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa_ocde"]

# Mapear as coleções dos anos disponíveis
anos_colecoes = {
    "2000": "pisa_2000_texto",
    "2003": "pisa_2003",
    "2009": "pisa_2009",
    "2012": "pisa_2012",
    "2015": "pisa_2015",
    "2018": "pisa_2018_completo",
    "2022": "pisa_2022"
}

# Nome bonito para as disciplinas
disciplinas_nomes = {
    "reading": "Leitura",
    "mathematics": "Matemática",
    "science": "Ciências"
}

# Função para puxar dados
def buscar_dados(ano):
    colecao_nome = anos_colecoes.get(ano)
    if not colecao_nome:
        return None

    colecao = db[colecao_nome]
    dados = []

    for disciplina, nome_bonito in disciplinas_nomes.items():
        # Buscar Brasil
        brasil = colecao.find_one({"pais": {"$regex": "Brasil", "$options": "i"}, "disciplina": {"$regex": disciplina, "$options": "i"}})
        # Buscar OCDE Média
        ocde = colecao.find_one({"pais": {"$regex": "OECD", "$options": "i"}, "disciplina": {"$regex": disciplina, "$options": "i"}})

        if brasil and ocde:
            dados.append({
                "Disciplina": nome_bonito,
                "Nota_Brasil": float(brasil.get("nota", 0)),
                "Nota_OCDE": float(ocde.get("nota", 0))
            })

    return pd.DataFrame(dados)

# Streamlit Interface
st.set_page_config(page_title="PISA Brasil vs OCDE", layout="centered")

st.title("📚 Comparativo Brasil vs Média OCDE no PISA")
st.caption("Fonte: Banco de Dados OCDE + MongoDB")

ano_escolhido = st.selectbox("Selecione o ano da edição do PISA:", list(anos_colecoes.keys()))

df = buscar_dados(ano_escolhido)

if df is not None and not df.empty:
    st.subheader(f"Notas Médias - {ano_escolhido}")

    fig = go.Figure(data=[
        go.Bar(name='Brasil 🇧🇷', x=df["Disciplina"], y=df["Nota_Brasil"]),
        go.Bar(name='Média OCDE 🌍', x=df["Disciplina"], y=df["Nota_OCDE"])
    ])
    fig.update_layout(barmode='group', xaxis_title="Área Avaliada", yaxis_title="Nota Média")

    st.plotly_chart(fig)

    # Mostrar resumo numérico
    st.subheader("📈 Resumo Numérico:")
    for idx, row in df.iterrows():
        diferenca = row["Nota_Brasil"] - row["Nota_OCDE"]
        status = "acima" if diferenca > 0 else "abaixo"
        st.write(f"**{row['Disciplina']}**: Brasil obteve **{row['Nota_Brasil']}** pontos, enquanto a média OCDE foi **{row['Nota_OCDE']}** pontos. Resultado: **{abs(diferenca):.1f} pontos {status} da média mundial**.")

else:
    st.warning("❌ Dados ainda não disponíveis para este ano selecionado.")

# Encerrar conexão
client.close()

