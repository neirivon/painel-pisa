import os

# Caminho da pasta onde estão os arquivos .py
pages_dir = "os.path.join(., "p")ages"

# Arquivos que devem ser ignorados
arquivos_ignorar = {
    "01_Resumo_Edicao.py",
    "98_Exportar_PDF_Completo.py",
    "99_Referencias_Bibliograficas.py"
}

# Processa os arquivos .py da pasta base (sem subpastas)
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

        # Se ainda não tiver 'import os', injeta no topo
        if "import os" not in conteudo:
            novo_conteudo = "import os\n" + conteudo
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(novo_conteudo)
            print(f"✅ 'import os' injetado em: {nome}")
        else:
            print(f"⏭️ Já possui 'import os': {nome}")

