import streamlit as st
import json
import pandas as pd
import os
from painel_pisa.utils.estilo_global import aplicar_estilo
import matplotlib.pyplot as plt

aplicar_estilo()
st.title("\U0001F4CA Comparativo do Brasil com os 5 primeiros colocados no PISA")
st.markdown("Dados de 2000 a 2022 | Fonte: OCDE (PISA)")

# 🔁 Modo local ou cloud
modo = st.sidebar.radio("Modo", ["local", "cloud"])
CAMINHO_JSON = ("/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/comparativo_brasil_top5_pisa_2000_2022.json"
    if modo == "cloud"
    else "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/comparativo_brasil_top5_pisa_2000_2022.json"
)

# 📂 Carregar dados
with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
    dados = json.load(f)

# 🌟 Área selecionada
area = st.selectbox("Selecione a área", ["Leitura", "Matemática", "Ciências"])

# 🔢 Preparar DataFrame
linhas = []
for edicao in dados:
    ano = edicao["edicao"]
    ranking = edicao["resposta_ia"].get(area, {})
    for pais, info in ranking.items():
        posicao = info.get("Posição")
        nota = info.get("Nota")
        if nota is not None:
            linhas.append({
                "Ano": ano,
                "País": pais,
                "Nota": nota,
                "Brasil": "Brasil" if pais == "Brasil" else "Top 5"
            })

df = pd.DataFrame(linhas)

# 🎨 Gráfico por ano
st.subheader(f"\U0001F4C9 Comparação de notas em **{area}** ao longo dos anos")
anos = sorted(df["Ano"].unique())

for ano in anos:
    df_ano = df[df["Ano"] == ano].sort_values("Nota", ascending=False)
    fig, ax = plt.subplots()
    cores = ["#FF5733" if p == "Brasil" else "#3498DB" for p in df_ano["País"]]
    ax.barh(df_ano["País"], df_ano["Nota"], color=cores)
    ax.invert_yaxis()
    ax.set_title(f"PISA {ano} - {area}")
    ax.set_xlabel("Nota")
    st.pyplot(fig)

# 📈 Linha do tempo da posição do Brasil
st.subheader("\U0001F4CC Evolução da posição do Brasil")
anos_pos = []
posicoes = []

for edicao in dados:
    ano = edicao["edicao"]
    info_brasil = edicao["resposta_ia"][area].get("Brasil", {})
    if info_brasil.get("Posição"):
        anos_pos.append(ano)
        posicoes.append(info_brasil["Posição"])

if anos_pos:
    df_pos = pd.DataFrame({"Ano": anos_pos, "Posição": posicoes})
    fig2, ax2 = plt.subplots()
    ax2.plot(df_pos["Ano"], df_pos["Posição"], marker="o", color="#FF5733", linewidth=2)
    ax2.set_ylim(ax2.get_ylim()[::-1])  # Inverter eixo para posição menor em cima
    ax2.set_title(f"Evolução da posição do Brasil em {area}")
    ax2.set_ylabel("Posição")
    ax2.set_xlabel("Ano")
    st.pyplot(fig2)
else:
    st.info("📬 Brasil não participou ou não teve posição definida em algumas edições.")

