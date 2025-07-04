import os

# Caminho da pasta onde estão os arquivos .py (ajuste se necessário)
pages_dir = "os.path.join(., "p")ages"

# Arquivos que NÃO devem ser alterados
arquivos_ignorar = {
    "01_Resumo_Edicao.py",
    "98_Exportar_PDF_Completo.py",
    "99_Referencias_Bibliograficas.py"
}

# Percorrer todos os .py da pasta base
for nome in os.listdir(pages_dir):
    caminho = os.path.join(pages_dir, nome)

    if (
        os.path.isfile(caminho)
        and nome.endswith(".py")
        and nome not in arquivos_ignorar
        and "index.py" not in nome
    ):
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        import_idx = None
        config_idx = None

        for i, linha in enumerate(linhas):
            if "import streamlit as st" in linha:
                import_idx = i
            if "st.set_page_config" in linha and config_idx is None:
                config_idx = i

        # Corrigir se set_page_config está antes do import ou import está faltando
        if config_idx is not None and (import_idx is None or config_idx < import_idx):
            print(f"🔧 Corrigindo: {nome}")
            linha_config = linhas.pop(config_idx)
            if import_idx is not None:
                linhas.pop(import_idx)
            else:
                import_idx = 0  # forçar topo

            # Inserir no topo
            linhas.insert(0, "import streamlit as st\n")
            linhas.insert(1, linha_config)

            with open(caminho, "w", encoding="utf-8") as f:
                f.writelines(linhas)
        else:
            print(f"✅ OK: {nome}")

