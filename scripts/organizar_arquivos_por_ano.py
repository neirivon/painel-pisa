import os
import shutil

# Caminho onde estão todos os arquivos OCDE
PASTA_ORIGEM = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cde"

# Prefixos para detectar o ano correto
prefixos_para_ano = {
    "CY0": "2000",
    "CY3": "2003",
    "CY6": "2006",
    "CY09": "2009",
    "CY1MD9": "2009",
    "CY12": "2012",
    "CY1MD12": "2012",
    "CY15": "2015",
    "CY1MD15": "2015",
    "CY1MDAI": "2018",
    "CY2": "2022"
}

# Garante que a pasta existe
def garantir_pasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

# Detecta o ano com base no nome do arquivo
def detectar_ano(nome_arquivo):
    for prefixo, ano in prefixos_para_ano.items():
        if nome_arquivo.startswith(prefixo):
            return ano
    return "desconhecido"

# Move os arquivos para suas respectivas pastas
for arquivo in os.listdir(PASTA_ORIGEM):
    caminho_arquivo = os.path.join(PASTA_ORIGEM, arquivo)
    
    if not os.path.isfile(caminho_arquivo):
        continue  # Ignorar se não for arquivo
    
    ano = detectar_ano(arquivo)
    destino = os.path.join(PASTA_ORIGEM, ano)
    garantir_pasta(destino)

    try:
        shutil.move(caminho_arquivo, os.path.join(destino, arquivo))
        print(f"📦 {arquivo} → {destino}")
    except Exception as e:
        print(f"❌ Erro ao mover {arquivo}: {e}")

