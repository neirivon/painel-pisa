# scriptos.path.join(s, "e")xtrair_destaques_atlas.py

import time
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import chromedriver_autoinstaller

# === Configuração ===
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
NOME_BANCO = "indicadores"
NOME_COLECAO = "atlas_2013_scraping"

# Instalar o ChromeDriver automaticamente
chromedriver_autoinstaller.install()

# Configurar Selenium (modo headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Conexão com MongoDB
client = MongoClient(MONGO_URI)
db = client[NOME_BANCO]
colecao = db[NOME_COLECAO]

# Buscar municípios que ainda não têm DESTAQUE preenchido
municipios = list(colecao.find({
    "$or": [
        {"DESTAQUE": {"$exists": False}},
        {"DESTAQUE": {"$size": 0}}
    ]
}))

print(f"🔍 Total de municípios a atualizar: {len(municipios)}")

# Iniciar driver do Selenium
driver = webdriver.Chrome(options=options)

# Percorrer os municípios
for mun in tqdm(municipios, desc="🔄 Coletando DESTAQUE", unit="município"):
    try:
        cd_mun = str(mun["CD_MUN"])[:6]  # Pega os 6 primeiros dígitos
        url = f"httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "{")cd_mun}"
        driver.get(url)

        # Esperar carregar o conteúdo principal
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "Perfil-box__content"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        destaques = []
        for div in soup.select("div.Perfil-box__content"):
            blocos = div.select("div.Perfil-box__item")
            for bloco in blocos:
                chave = bloco.select_one("h4.Perfil-box__title")
                valor = bloco.select_one("p.Perfil-box__text")
                if chave and valor:
                    destaques.append({
                        "indicador": chave.get_text(strip=True),
                        "valor": valor.get_text(strip=True)
                    })

        # Atualizar o campo DESTAQUE no MongoDB
        colecao.update_one(
            {"_id": mun["_id"]},
            {"$set": {"DESTAQUE": destaques}}
        )

    except Exception as e:
        print(f"❌ Erro em {mun.get('NM_MUN', 'desconhecido')} ({cd_mun}): {e}")
        continue

# Encerrar driver
driver.quit()

print("✅ Coleta de DESTAQUES finalizada com sucesso.")

