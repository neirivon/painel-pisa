from playwright.sync_api import sync_playwright
import csv
import time

url = "httpsos.path.join(:, "/")saeb.inep.gov.bos.path.join(r, "s")aeos.path.join(b, "r")esultado-final-externo"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context(storage_state="cookies_inep.json")
    page = context.new_page()

    print(f"🌐 Acessando {url} com cookies de sessão...")
    page.goto(url, timeout=60000)
    time.sleep(5)

    # Seleciona ano 2023
    page.select_option("select[formcontrolname='anoEdicao']", label="2023")
    time.sleep(2)

    # Seleciona estado MG
    page.select_option("select[formcontrolname='siglaUf']", label="MG")
    time.sleep(2)

    # Seleciona município Uberlândia
    page.select_option("select[formcontrolname='municipio']", label="Uberlândia")
    time.sleep(2)

    # Clica no botão Pesquisar
    page.click("button:has-text('Pesquisar')")
    page.wait_for_selector("tbody tr", timeout=10000)

    # Extrai dados da tabela
    dados = []
    linhas = page.query_selector_all("tbody tr")
    for linha in linhas:
        colunas = linha.query_selector_all("td")
        if len(colunas) >= 2:
            nome_escola = colunas[0].inner_text().strip()
            codigo_escola = colunas[1].inner_text().strip()
            dados.append({
                "municipio": "Uberlândia",
                "estado": "MG",
                "escola": nome_escola,
                "codigo": codigo_escola
            })

    browser.close()

    # Salva CSV
    with open("saeb2023_uberlandia.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["estado", "municipio", "escola", "codigo"])
        writer.writeheader()
        writer.writerows(dados)

    print(f"✅ {len(dados)} escolas salvas em saeb2023_uberlandia.csv")

