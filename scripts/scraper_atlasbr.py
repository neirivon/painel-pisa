# scraper_atlasbr.py

import time
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ==== Configurações do Selenium (modo headless) ====
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# ==== Lista de códigos IBGE dos municípios (exemplo com 10 primeiros para testar) ====
codigos_ibge = [
    1100015, 1100023, 1100031, 1100049, 1100056,
    1100064, 1100072, 1100080, 1100098, 1100106
    # ... continue com todos os municípios do Brasil
]

# ==== Função de extração de dados de um município ====
def extrair_dados_municipio(codigo):
    url = f"httpsos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "{")codigo}"
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        bloco = soup.find("div", class_="perfil-municipio__content")
        nome_mun = soup.find("h1").get_text(strip=True).split(",")[0]
        uf = soup.find("h1").get_text(strip=True).split(",")[1].strip()

        campos = bloco.find_all("div", class_="indicador__valor")
        rotulos = bloco.find_all("div", class_="indicador__titulo")

        dados = {
            "COD_MUNICIPIO": codigo,
            "MUNICIPIO": nome_mun,
            "UF": uf,
        }

        for rotulo, valor in zip(rotulos, campos):
            chave = rotulo.get_text(strip=True).upper()
            val = valor.get_text(strip=True).replace("\xa0", " ")
            dados[chave] = val

        return dados
    except Exception as e:
        print(f"❌ Erro no código {codigo}: {e}")
        return None

# ==== Coleta de todos os dados ====
registros = []
for codigo in tqdm(codigos_ibge, desc="Extraindo municípios"):
    info = extrair_dados_municipio(codigo)
    if info:
        registros.append(info)

driver.quit()

# ==== Salvar em CSV ====
df = pd.DataFrame(registros)
df.to_csv("atlasbr_municipios_scraped.csv", index=False, encoding="utf-8-sig")
print("✅ Extração finalizada: atlasbr_municipios_scraped.csv")

