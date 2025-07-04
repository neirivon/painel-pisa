from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar navegador VISUAL
options = Options()
# NÃO usar headless: queremos ver o que está acontecendo

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Abrir o site
url = "httpos.path.join(:, "/")saeb.inep.gov.bos.path.join(r, "s")aeos.path.join(b, "r")esultado-final-externo"
driver.get(url)

# Aguardar tempo suficiente para carregamento (você pode ajustar se necessário)
time.sleep(15)

# Capturar screenshot
driver.save_screenshot("saeb_teste.png")

# Salvar HTML renderizado
with open("saeb_teste.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

# Encerrar navegador
driver.quit()

print("✅ Teste concluído. Arquivos gerados: saeb_teste.png e saeb_teste.html")

