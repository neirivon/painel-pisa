import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from pymongo import MongoClient
from bs4 import BeautifulSoup
from tqdm import tqdm

# ===== Configurações ====
URL_BASE = "httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipio/"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCOS_ORIGEM = "ibge"
COLECAO_MUNICIPIOS = "municipios_2022"
BANCO_DESTINO = "indicadores"
COLECAO_SAIDA = "atlas_2013_scraping"

# ===== Configurar WebDriver (sem abrir navegador) =====
chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options)

# ===== Conectar ao MongoDB ====
client = MongoClient(MONGO_URI)
db_ibge = client[BANCOS_ORIGEM]
db_indicadores = client[BANCO_DESTINO]
municipios = list(db_ibge[COLECAO_MUNICIPIOS].find({}, {"CD_MUN": 1, "NM_MUN": 1, "SIGLA_UF": 1, "_id": 0}))

# Limpar coleção de destino (opcional)
db_indicadores[COLECAO_SAIDA].drop()

# ===== Coletar dados do site ====
print(f"🔍 Total de municípios encontrados: {len(municipios)}")

for mun in tqdm(municipios, desc="🧪 Coletando dados"):
    cd_mun = mun["CD_MUN"]
    cd_atlas = cd_mun[:-1]  # Remove o último dígito
    url = f"{URL_BASE}{cd_atlas}"

    try:
        driver.get(url)
        time.sleep(1.5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extrair o bloco de destaque (dados textuais)
        destaque = soup.find("div", class_="destaque")
        paragrafos = destaque.find_all("p") if destaque else []

        dados_textuais = [p.text.strip() for p in paragrafos if p.text.strip()]

        doc_saida = {
            "CD_MUN": cd_mun,
            "NM_MUN": mun.get("NM_MUN"),
            "SIGLA_UF": mun.get("SIGLA_UF"),
            "URL": url,
            "DESTAQUE": dados_textuais
        }

        db_indicadores[COLECAO_SAIDA].insert_one(doc_saida)

    except Exception as e:
        print(f"❌ Erro em {cd_mun} ({mun.get('NM_MUN')}): {e}")

driver.quit()
client.close()
print("✅ Coleta finalizada e dados armazenados no MongoDB.")

