import os
import re

# Caminho da pasta 'pages' — ajuste conforme necessário
pages_dir = "os.path.join(., "p")ages"

# Arquivos que não devem ser modificados
arquivos_ignorar = {
    "01_Resumo_Edicao.py",
    "98_Exportar_PDF_Completo.py",
    "99_Referencias_Bibliograficas.py"
}

# Corrigir todos os .py exceto os ignorados
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

        # Localizar set_page_config fora do topo
        match = re.search(r"st\.set_page_config\(.*?\)\n", conteudo)
        if match:
            linha_config = match.group()

            # Só corrigir se não estiver no topo
            if not conteudo.strip().startswith(linha_config.strip()):
                conteudo_sem_config = conteudo.replace(linha_config, "")
                novo_conteudo = linha_config + "\n" + conteudo_sem_config

                with open(caminho, "w", encoding="utf-8") as f:
                    f.write(novo_conteudo)

                print(f"✅ Corrigido: {nome}")
            else:
                print(f"⏭️ Já está correto: {nome}")
        else:
            print(f"⚠️ Nenhum st.set_page_config encontrado: {nome}")

