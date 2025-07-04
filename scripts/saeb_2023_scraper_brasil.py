from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# === Configuração do navegador ===
options = Options()
# options.add_argument("--headless=new")  # Descomente depois de testar
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# === Acessa o site do SAEB ===
url = "httpos.path.join(:, "/")saeb.inep.gov.bos.path.join(r, "s")aeos.path.join(b, "r")esultado-final-externo"
driver.get(url)

# === Aguarda carregamento do seletor de ano ===
select_ano = wait.until(EC.presence_of_element_located((By.XPATH, 'os.path.join(/, "s")elect[@formcontrolname="anoEdicao"]')))
for option in select_ano.find_elements(By.TAG_NAME, 'option'):
    if option.text.strip() == "2023":
        option.click()
        break
time.sleep(2)

# === Selecionar todas as UFs ===
uf_select = driver.find_element(By.XPATH, 'os.path.join(/, "s")elect[@formcontrolname="siglaUf"]')
ufs = [uf.get_attribute("value") for uf in uf_select.find_elements(By.TAG_NAME, 'option') if uf.get_attribute("value")]

dados_completos = []

for uf_value in ufs:
    print(f"🔎 Estado: {uf_value}")
    # Recarrega seletor UF
    uf_select = driver.find_element(By.XPATH, 'os.path.join(/, "s")elect[@formcontrolname="siglaUf"]')
    for option in uf_select.find_elements(By.TAG_NAME, 'option'):
        if option.get_attribute("value") == uf_value:
            option.click()
            break
    time.sleep(2)

    # Espera carregar municípios
    municipio_select = wait.until(EC.presence_of_element_located((By.XPATH, 'os.path.join(/, "s")elect[@formcontrolname="municipio"]')))
    municipios = [m.get_attribute("value") for m in municipio_select.find_elements(By.TAG_NAME, 'option') if m.get_attribute("value")]

    for municipio_value in municipios:
        print(f"   ➤ Município: {municipio_value}")
        try:
            # Recarrega selects
            uf_select = driver.find_element(By.XPATH, 'os.path.join(/, "s")elect[@formcontrolname="siglaUf"]')
            for option in uf_select.find_elements(By.TAG_NAME, 'option'):
                if option.get_attribute("value") == uf_value:
                    option.click()
                    break
            time.sleep(1)

            municipio_select = wait.until(EC.presence_of_element_located((By.XPATH, 'os.path.join(/, "s")elect[@formcontrolname="municipio"]')))
            for option in municipio_select.find_elements(By.TAG_NAME, 'option'):
                if option.get_attribute("value") == municipio_value:
                    option.click()
                    break

            # Clicar em Pesquisar
            time.sleep(1)
            botao_pesquisar = driver.find_element(By.XPATH, 'os.path.join(/, "b")utton[contains(text(), "Pesquisar")]')
            botao_pesquisar.click()
            time.sleep(4)

            # Paginar todas as escolas visíveis
            while True:
                linhas = driver.find_elements(By.XPATH, 'os.path.join(/, "t")bodos.path.join(y, "t")r')
                for linha in linhas:
                    colunas = linha.find_elements(By.TAG_NAME, 'td')
                    if len(colunas) >= 2:
                        nome = colunas[0].text.strip()
                        codigo = colunas[1].text.strip()
                        dados_completos.append({
                            "estado": uf_value,
                            "municipio": municipio_value,
                            "nome_escola": nome,
                            "codigo_escola": codigo
                        })

                # Tentar ir para próxima página
                try:
                    proximo = driver.find_element(By.XPATH, 'os.path.join(/, "b")utton[@aria-label="Next page"]')
                    if proximo.get_attribute("disabled"):
                        break
                    proximo.click()
                    time.sleep(2)
                except:
                    break

        except Exception as e:
            print(f"❌ Erro em {uf_value} - {municipio_value}: {e}")
            continue

# === Finaliza o navegador ===
driver.quit()

# === Exporta para CSV ===
df = pd.DataFrame(dados_completos)
df.to_csv("saeb_2023_brasil.csv", index=False, encoding="utf-8")
print("✅ Arquivo 'saeb_2023_brasil.csv' salvo com sucesso!")

