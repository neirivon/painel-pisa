import os
import re

# Caminho absoluto para sua pasta de páginas
PASTA_PAGINAS = "painel_pisa/pages"

def gerar_titulo(nome_arquivo):
    nome = re.sub(r"^\d+_", "", nome_arquivo).replace(".py", "")
    nome = nome.replace("_", " ").strip().capitalize()
    return nome

def processar_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    ja_tem_config = any("st.set_page_config" in linha for linha in linhas)
    if ja_tem_config:
        print(f"🔁 Já possui set_page_config: {os.path.basename(caminho_arquivo)}")
        return

    nova_linha_config = None
    for i, linha in enumerate(linhas):
        if "import streamlit as st" in linha:
            titulo = gerar_titulo(os.path.basename(caminho_arquivo))
            nova_linha_config = f"st.set_page_config(page_title=\"{titulo} - PISA OCDE\", layout=\"wide\")\n"
            linhas.insert(i + 1, nova_linha_config)
            break

    if not nova_linha_config:
        # Se não tem import, adiciona no topo
        titulo = gerar_titulo(os.path.basename(caminho_arquivo))
        linhas.insert(0, "import streamlit as st\n")
        linhas.insert(1, f"st.set_page_config(page_title=\"{titulo} - PISA OCDE\", layout=\"wide\")\n")

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.writelines(linhas)

    print(f"✅ Atualizado: {os.path.basename(caminho_arquivo)}")

def aplicar_em_todas_as_paginas():
    for nome_arquivo in os.listdir(PASTA_PAGINAS):
        if nome_arquivo.endswith(".py"):
            caminho = os.path.join(PASTA_PAGINAS, nome_arquivo)
            processar_arquivo(caminho)

if __name__ == "__main__":
    aplicar_em_todas_as_paginas()

