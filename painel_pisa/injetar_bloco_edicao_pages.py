import os

# Caminho da pasta pages (ajuste conforme necessário)
pages_dir = "os.path.join(., "p")ages"

# Arquivos a ignorar
arquivos_ignorar = {
    "01_Resumo_Edicao.py",
    "98_Exportar_PDF_Completo.py",
    "99_Referencias_Bibliograficas.py"
}

# Bloco que será injetado após "import streamlit as st"
bloco_edicao = '''
# === Edições disponíveis ===
edicoes_disponiveis = ["2000", "2003", "2006", "2009", "2012", "2015", "2018", "2022"]

# === Seleção persistente da edição ===
if "edicao_selecionada" not in st.session_state:
    st.session_state.edicao_selecionada = "2000"

# Mostrar combobox
edicao = st.selectbox("Selecione a edição do PISA:", edicoes_disponiveis, index=edicoes_disponiveis.index(st.session_state.edicao_selecionada), key="edicao_pisa")

# Atualiza ao mudar seleção
if edicao != st.session_state.edicao_selecionada:
    st.session_state.edicao_selecionada = edicao
    st.rerun()

# Confirma edição ativa
edicao = st.session_state.edicao_selecionada
st.markdown(f"### ✏️ Edição selecionada: {edicao}")

# === Execução dinâmica do index.py da edição ===
if edicao != "2000":
    caminho_index = os.path.join(os.path.dirname(__file__), edicao, "index.py")
    if os.path.exists(caminho_index):
        with open(caminho_index, "r", encoding="utf-8") as f:
            codigo = f.read()
            exec(codigo, globals())
        st.stop()
'''

# Aplicar a lógica
for nome in os.listdir(pages_dir):
    caminho = os.path.join(pages_dir, nome)
    if (
        os.path.isfile(caminho)
        and nome.endswith(".py")
        and nome not in arquivos_ignorar
        and "index.py" not in nome
    ):
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()

        if "edicao_selecionada" not in conteudo:
            novo_conteudo = conteudo.replace(
                "import streamlit as st",
                "import streamlit as st\n" + bloco_edicao.strip()
            )
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(novo_conteudo)
            print(f"✅ Bloco de edição injetado: {nome}")
        else:
            print(f"⏭️ Já possui lógica de edição: {nome}")

