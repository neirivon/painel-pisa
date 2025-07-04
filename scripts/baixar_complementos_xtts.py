# baixar_complementos_xtts.py

import os
import requests
from tqdm import tqdm

# Caminho onde os arquivos devem ser salvos
DESTINO = os.path.expanduser("~/SINAPSE2.0/PISA/modelos_coqui/xtts_v2")
os.makedirs(DESTINO, exist_ok=True)

# Arquivos faltantes com seus nomes e URLs
ARQUIVOS = {
    "speakers.pth": "https://huggingface.co/coqui/XTTS-v2/resolve/main/speakers.pth",
    "language_ids.json": "https://huggingface.co/coqui/XTTS-v2/resolve/main/language_ids.json"
}

def baixar_arquivo(nome, url):
    caminho_arquivo = os.path.join(DESTINO, nome)
    if os.path.exists(caminho_arquivo) and os.path.getsize(caminho_arquivo) > 0:
        print(f"✅ {nome} já existe, ignorado.")
        return

    print(f"⬇️ Baixando: {nome} ...")
    try:
        resposta = requests.get(url, stream=True)
        resposta.raise_for_status()

        total = int(resposta.headers.get('content-length', 0))
        with open(caminho_arquivo, 'wb') as f, tqdm(
            desc=nome,
            total=total,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as barra:
            for dado in resposta.iter_content(chunk_size=1024):
                f.write(dado)
                barra.update(len(dado))

        print(f"✅ {nome} salvo em: {caminho_arquivo}")

    except requests.exceptions.HTTPError as errh:
        print(f"❌ Erro HTTP ao baixar {nome}: {errh}")
    except Exception as e:
        print(f"❌ Erro ao baixar {nome}: {e}")

# Baixa os arquivos
for nome_arquivo, url_arquivo in ARQUIVOS.items():
    baixar_arquivo(nome_arquivo, url_arquivo)

