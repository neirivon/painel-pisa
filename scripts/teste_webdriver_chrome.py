# teste_webdriver_chrome.py
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Instala automaticamente o driver compatível com o Chrome
chromedriver_autoinstaller.install()

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("httpsos.path.join(:, "/")www.google.com")
print("Título da página:", driver.title)
driver.quit()


