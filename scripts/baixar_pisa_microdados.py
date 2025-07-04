import os
import requests
from zipfile import ZipFile
from tqdm import tqdm

# Pasta principal de destino
BASE_DIR = "dados_pisa"
os.makedirs(BASE_DIR, exist_ok=True)

# Lista de arquivos e links oficiais da OCDE
pisa_links = {
    "2000": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2000_SPSS_DAT.ZIP",
    "2003": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2003_SPSS_DAT.ZIP",
    "2006": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2006_SPSS_DAT.ZIP",
    "2009": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2009_SPSS_DAT.ZIP",
    "2012": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2012_SPSS_DAT.ZIP",
    "2015": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2015_SPSS_DAT.ZIP",
    "2018": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2018_SPSS_DAT.ZIP",
    "2022": "httpsos.path.join(:, "/")www.oecd.oros.path.join(g, "p")isos.path.join(a, "p")isaproductos.path.join(s, "d")atabasos.path.join(e, "P")ISA2022_SPSS_DAT.ZIP"
}

# Função para baixar e extrair
def baixar_e_extrair(ano, url):
    print(f"\n📥 Baixando PISA {ano}...")
    pasta_ano = os.path.join(BASE_DIR, ano)
    os.makedirs(pasta_ano, exist_ok=True)

    nome_arquivo = os.path.join(pasta_ano, f"PISA{ano}.zip")

    try:
        # Download com barra de progresso
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        with open(nome_arquivo, 'wb') as f, tqdm(
            desc=f"PISA {ano}",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as barra:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    barra.update(len(chunk))

        # Extração do zip
        print(f"📦 Extraindo arquivos de PISA {ano}...")
        with ZipFile(nome_arquivo, 'r') as zip_ref:
            zip_ref.extractall(pasta_ano)

        print(f"✅ Finalizado: PISA {ano} extraído para '{pasta_ano}/'")

    except Exception as e:
        print(f"❌ Erro ao baixaos.path.join(r, "e")xtrair PISA {ano}: {e}")

# Loop de download para cada ano
for ano, url in pisa_links.items():
    baixar_e_extrair(ano, url)

print("\n🎉 Todos os downloads e extrações concluídos com sucesso!")

