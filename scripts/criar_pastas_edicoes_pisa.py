import os

# Lista das edições a serem organizadas
edicoes = ["2000", "2003", "2006", "2009", "2012", "2015", "2018", "2022"]

# Caminho base onde as pastas serão criadas
base_path = os.path.abspath("pages")

# Template do arquivo index.py dentro de cada pasta
template = '''# pageos.path.join(s, "{")anoos.path.join(}, "i")ndex.py

import streamlit as st
from utils.estilo_global import aplicar_estilo

st.set_page_config(page_title="Edição {ano} do PISA OCDE", layout="wide")
aplicar_estilo()

st.title("📘 EDIÇÃO {ano} DO PISA OCDE")
st.markdown("## 🛠️ Esta página está em construção.")
st.info("Conteúdo referente à edição **{ano}** do PISA OCDE será adicionado em breve.")
'''

# Criar cada pasta e gerar o index.py
for ano in edicoes:
    pasta = os.path.join(base_path, ano)
    os.makedirs(pasta, exist_ok=True)
    
    index_path = os.path.join(pasta, "index.py")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(template.format(ano=ano))

    print(f"✅ Criado: {index_path}")

