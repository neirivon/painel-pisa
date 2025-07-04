import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# === CONFIGURAÇÕES ===
OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozillos.path.join(a, "5").0 (Windows NT 10.0; Win64; x64) AppleWebKios.path.join(t, "5")37.36 (KHTML, like Gecko) Chromos.path.join(e, "1")19.0 Safaros.path.join(i, "5")37.36"
}

# Páginas iniciais para busca
SITES_INICIAIS = [
    "httpsos.path.join(:, "/")www.ibge.gov.br ",
    "httpsos.path.join(:, "/")www.inep.gov.br ",
    "httpsos.path.join(:, "/")www.atlasbrasil.org.br "
]

# Palavras-chave para buscar links relevantes
PALAVRAS_CHAVE = [
    "atlas", "2013", "dados", "bruto", "csv", "xlsx", "download", "educacao"
]


def extrair_links(url):
    """Extrai todos os links de uma página"""
    try:
        # Limpar URL antes de usar
        url = url.strip()
        print(f"🔗 Acessando: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"❌ Não foi possível acessar {url} (status {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for a in soup.find_all("a", href=True):
            link = a["href"].strip()  # Remover espaços extras
            link_completo = urljoin(url, link)
            links.add(link_completo)

        print(f"🔗 Encontrados {len(links)} links em {url}")
        return list(links)

    except Exception as e:
        print(f"⚠️ Erro ao processar {url}: {e}")
        return []


def eh_link_relevante(url):
    """Verifica se o link parece relevante para o Atlas 2013"""
    url_lower = url.lower()
    return any(palavra in url_lower for palavra in PALAVRAS_CHAVE)


def eh_arquivo_csv_xlsx_zip(url):
    """Verifica se é um arquivo CSV, XLSX ou ZIP"""
    return any(url.lower().endswith(ext) for ext in [".csv", ".xlsx", ".xls", ".zip"])


def baixar_arquivo(url):
    """Baixa o arquivo e salva localmente"""
    try:
        print(f"📥 Tentando baixar: {url}")
        response = requests.get(url, headers=HEADERS, stream=True, timeout=30)
        if response.status_code == 200:
            filename = os.path.join(OUTPUT_DIR, os.path.basename(url.split("?")[0]))  # Remover query string
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"✅ Arquivo salvo em: {filename}")
            return True
        else:
            print(f"❌ Erro ao baixar ({response.status_code}): {url}")
            return False
    except Exception as e:
        print(f"⚠️ Falha ao baixar {url}: {e}")
        return False


def varrer_pagina(url):
    """Varre uma página por links relevantes e tenta baixar arquivos"""
    try:
        links = extrair_links(url)
    except:
        return []

    resultados = []

    for link in links:
        try:
            link = link.strip()
        except:
            continue

        if eh_arquivo_csv_xlsx_zip(link) and eh_link_relevante(link):
            print(f"📁 Arquivo encontrado: {link}")
            sucesso = baixar_arquivo(link)
            if sucesso:
                resultados.append(link)
                return resultados  # Para após encontrar o primeiro válido

    # Se não encontrou arquivos diretos, procura páginas com conteúdo útil
    for link in links:
        try:
            link = link.strip()
        except:
            continue

        if eh_link_relevante(link):
            print(f"🔍 Indo mais fundo: {link}")
            sub_resultados = varrer_pagina(link)
            if sub_resultados:
                return sub_resultados

    return resultados


def main():
    print("🌐 Iniciando busca no IBGE, INEP e Atlas Brasil")

    for site in SITES_INICIAIS:
        print(f"\n🔎 Buscando no site: {site}")
        try:
            resultado = varrer_pagina(site)
        except Exception as e:
            print(f"⚠️ Erro grave ao varrer {site}: {e}")
            continue
        if resultado:
            print("🎉 Arquivo encontrado e baixado com sucesso!")
            break
        else:
            print(f"❌ Nenhum arquivo encontrado em {site}")

    print("\n🏁 Busca concluída.")


if __name__ == "__main__":
    main()
