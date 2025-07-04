# painel_pisa/utils/validador_caminhos.py

import os
import streamlit as st

def validar_caminho(caminho, tipo="arquivo", descricao="Recurso"):
    """
    Valida se o caminho existe e é do tipo esperado (arquivo ou pasta).
    Exibe alerta no Streamlit se houver erro.

    Parâmetros:
    - caminho (str): caminho completo a ser validado
    - tipo (str): "arquivo" ou "pasta"
    - descricao (str): texto que será exibido no alerta, ex: "Base de dados", "Rubrica JSON"

    Retorna:
    - True se válido
    - False se inválido
    """
    if tipo == "arquivo":
        if not os.path.isfile(caminho):
            st.warning(f"⚠️ {descricao} não encontrado: `{caminho}`")
            return False
    elif tipo == "pasta":
        if not os.path.isdir(caminho):
            st.warning(f"⚠️ Pasta não encontrada: `{caminho}`")
            return False
    else:
        st.error("❌ Tipo inválido no validador_caminhos.py (esperado: 'arquivo' ou 'pasta')")
        return False

    return True

