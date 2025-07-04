import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# === CONFIGURAÇÕES ===
OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozillos.path.join(a, "5").0 (Windows NT 10.0; Win64; x64) AppleWebKios.path.join(t, "5")37.36 (KHTML, like Gecko) Chromos.path.join(e, "1")19.0 Safaros.path.join(i, "5")37.36"
}

# Links extraídos do JSON retornado pela API Google Custom Search
LINKS_BUSCA = [
    "httpsos.path.join(:, "/")portalantigo.ipea.gov.bos.path.join(r, "p")ortaos.path.join(l, "i")ndex.php?option=com_content&view=article&id=19152 :atlas-2013-apresenta-o-novo-indice-de-desenvolvimento-humano-municipal&catid=4:presidencia&directory=1",
    "httpsos.path.join(:, "/")www.ipardes.gov.bos.path.join(r, "i")mos.path.join(p, "i")mp.php?page=varinf&var=678 ",
    "httpsos.path.join(:, "/")zenodo.oros.path.join(g, "r")ecordos.path.join(s, "3")943700 ",
    "httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "1")100015"
]

# Lista de possíveis nomes do arquivo CSV
ARQUIVOS_ALVO = [
    "atlas_2013_dados_bruto_pt_BR.csv",
    "atlas2013_dadosbrutos.csv",
    "indicadores_municipais_2013.csv",
    "base_municipios_idhm_2013.csv",
    "tabela_municipios_atlas_2013.csv",
    "dados_municipais_2013_ptbr.csv",
    "base_final_municipios_2013.csv",
    "dados_idhm_municipios.csv",
    "idhm_municipios_2013_ipea.csv",
    "pnud_atlas2013_municipios.csv"
]


def extrair_links(url):
    """Extrai todos os links de uma página"""
    try:
        print(f"🔗 Acessando: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"❌ Não foi possível acessar {url} (status {response.status_code})")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = set()

        for a in soup.find_all("a", href=True):
            link_completo = urljoin(url, a["href"].strip())
            links.add(link_completo)

        print(f"🔗 Encontrados {len(links)} links em {url}")
        return list(links)

    except Exception as e:
        print(f"⚠️ Erro ao processar {url}: {e}")
        return []


def eh_arquivo_alvo(url):
    """Verifica se o link contém algum dos nomes de arquivo alvo"""
    url_lower = url.lower()
    return any(nome.lower() in url_lower for nome in ARQUIVOS_ALVO)


def baixar_arquivo(url):
    """Baixa o arquivo e salva localmente"""
    try:
        print(f"📥 Tentando baixar: {url}")
        response = requests.get(url, headers=HEADERS, stream=True, timeout=30)
        if response.status_code == 200:
            # Identifica qual nome foi encontrado
            for nome in ARQUIVOS_ALVO:
                if nome.lower() in url.lower():
                    filename = os.path.join(OUTPUT_DIR, nome)
                    break
            else:
                # Caso nenhum nome específico esteja na URL
                filename = os.path.join(OUTPUT_DIR, os.path.basename(url.split("?")[0])

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
    """Varre uma página por links relevantes e tenta baixar o CSV"""
    links = extrair_links(url)

    # Primeiro, verifica se algum link tem um dos nomes alvo
    for link in links:
        if eh_arquivo_alvo(link):
            sucesso = baixar_arquivo(link)
            if sucesso:
                return True

    # Se não encontrar diretamente, procura dentro da página
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            conteudo = response.text.lower()
            for nome in ARQUIVOS_ALVO:
                if nome.lower() in conteudo:
                    print(f"📄 Palavra-chave '{nome}' encontrada na página.")
    except:
        pass

    print("❌ Nenhum arquivo compatível encontrado nesta página.")
    return False


def main():
    print("🔍 Iniciando busca por arquivos CSV relacionados ao Atlas 2013")

    for site in LINKS_BUSCA:
        print(f"\n🔎 Analisando site: {site}")
        encontrado = varrer_pagina(site)
        if encontrado:
            print("🎉 Arquivo encontrado e baixado com sucesso!")
            break
        else:
            print(f"❌ Nada encontrado em {site}")

    print("\n🏁 Busca concluída.")


if __name__ == "__main__":
    main()
