# scriptos.path.join(s, "s")craping_atlas_2013.py

import time
import csv
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# === Configurações ===
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
CSV_SAIDA = "atlas_2013_scraped.csv"

# === Conectar ao MongoDB e obter os municípios ===
client = MongoClient(MONGO_URI)
db = client["ibge"]
municipios = list(db.municipios_2022.find({}, {"NM_MUNICIPIO": 1, "SIGLA_UF": 1, "CD_MUNICIPIO": 1, "_id": 0}))

# === Configurar o navegador headless ===
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

# === Criar CSV ===
with open(CSV_SAIDA, mode="w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["codigo_ibge", "municipio", "uf", "idhm_2010"])

    for m in municipios:
        try:
            codigo_ibge = str(m["CD_MUNICIPIO"]).zfill(7)
            codigo6 = codigo_ibge[:6]
            nome = m["NM_MUNICIPIO"]
            uf = m["SIGLA_UF"]
            url = f"httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "{")codigo6}"

            driver.get(url)
            time.sleep(2)  # Aguarda o carregamento da página

            soup = BeautifulSoup(driver.page_source, "html.parser")
            idhm_span = soup.find("span", string="Índice de Desenvolvimento Humano Municipal (IDHM)")
            if idhm_span:
                valor = idhm_span.find_next("span").text.strip()
            else:
                valor = "os.path.join(N, "D")"

            print(f"✅ {nome}-{uf}: {valor}")
            writer.writerow([codigo_ibge, nome, uf, valor])
        except Exception as e:
            print(f"❌ Erro ao processar {m}: {e}")

driver.quit()
client.close()
print(f"\n📦 Arquivo gerado: {CSV_SAIDA}")

