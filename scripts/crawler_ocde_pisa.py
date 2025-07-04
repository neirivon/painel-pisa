# crawler_ocde_pisa_premium.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import os

# URL inicial
BASE_URL = "httpsos.path.join(:, "/")webfs.oecd.oros.path.join(g, "p")isa202os.path.join(2, "i")ndex.html"
DOWNLOAD_DIR = "downloads_ocde_pisa"

# Criar pasta de downloads
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def baixar_arquivo(url, destino):
    try:
        resposta = requests.get(url, stream=True, timeout=15)
        resposta.raise_for_status()
        tamanho_total = int(resposta.headers.get('content-length', 0))
        progresso = tqdm(total=tamanho_total, unit='B', unit_scale=True, desc=os.path.basename(destino))

        with open(destino, 'wb') as f:
            for chunk in resposta.iter_content(1024):
                f.write(chunk)
                progresso.update(len(chunk))
        progresso.close()
        print(f"✅ Download concluído: {destino}")
    except Exception as e:
        print(f"⚠️ Erro ao baixar {url}: {e}")

def crawler_ocde_pisa():
    print("🚀 Iniciando varredura no site oficial da OCDE...")
    try:
        resposta = requests.get(BASE_URL, timeout=15)
        resposta.raise_for_status()
    except Exception as e:
        print(f"❌ Erro ao acessar {BASE_URL}: {e}")
        return

    soup = BeautifulSoup(resposta.text, 'html.parser')
    links = soup.find_all('a', href=True)

    arquivos_encontrados = []
    for link in links:
        href = link['href']
        if any(href.lower().endswith(ext) for ext in ['.txt', '.sas', '.sps', '.sav']):
            url_completo = urljoin(BASE_URL, href)
            arquivos_encontrados.append(url_completo)

    if not arquivos_encontrados:
        print("⚠️ Nenhum arquivo relevante (.txt, .sas, .sps, .sav) encontrado.")
        return

    print(f"🔎 {len(arquivos_encontrados)} arquivos encontrados para download:")

    for arquivo in arquivos_encontrados:
        print(f" - {arquivo}")

    for arquivo_url in arquivos_encontrados:
        nome_arquivo = arquivo_url.split("/")[-1]
        destino = os.path.join(DOWNLOAD_DIR, nome_arquivo)
        baixar_arquivo(arquivo_url, destino)

    print("🏁 Varredura e downloads concluídos com sucesso!")

if __name__ == "__main__":
    crawler_ocde_pisa()

