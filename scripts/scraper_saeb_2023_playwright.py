from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import csv
import time

url = "httpsos.path.join(:, "/")saeb.inep.gov.bos.path.join(r, "s")aeos.path.join(b, "r")esultado-final-externo"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # use headless=True se quiser rodar invisível
    context = browser.new_context()
    page = context.new_page()

    print(f"Acessando {url}...")
    page.goto(url)

    # 1. Fecha modal de cookies se existir
    try:
        page.click("text='Aceitar'", timeout=5000)
        print("Modal de cookies fechado.")
    except PlaywrightTimeout:
        print("Modal de cookies não encontrado.")

    # 2. Aguarda seletor de estado (UF)
    try:
        page.wait_for_selector("select[formcontrolname='siglaUf']", timeout=15000)
        print("Página carregada com sucesso.")
    except PlaywrightTimeout:
        print("Falha ao carregar os componentes da página.")
        exit()

    # 3. Seleciona ano 2023
    page.select_option("select[formcontrolname='anoEdicao']", label="2023")
    time.sleep(2)

    # 4. Coleta estados disponíveis
    estados_elements = page.query_selector_all("select[formcontrolname='siglaUf'] option")
    estados = [e.inner_text().strip() for e in estados_elements if e.get_attribute("value")]

    dados = []

    for estado in estados:
        print(f"🟩 Estado: {estado}")
        page.select_option("select[formcontrolname='siglaUf']", label=estado)
        time.sleep(2)

        # Aguarda carregamento de municípios
        try:
            page.wait_for_selector("select[formcontrolname='municipio'] option", timeout=10000)
        except PlaywrightTimeout:
            print(f"❌ Municípios não carregaram para {estado}, pulando...")
            continue

        municipios_elements = page.query_selector_all("select[formcontrolname='municipio'] option")
        municipios = [m.inner_text().strip() for m in municipios_elements if m.get_attribute("value")]

        for municipio in municipios:
            print(f"   ➤ Município: {municipio}")
            try:
                page.select_option("select[formcontrolname='municipio']", label=municipio)
                time.sleep(1)

                # Clica no botão Pesquisar
                page.click("button:has-text('Pesquisar')")
                page.wait_for_selector("tbody tr", timeout=10000)

                linhas = page.query_selector_all("tbody tr")
                for linha in linhas:
                    colunas = linha.query_selector_all("td")
                    if len(colunas) >= 2:
                        nome_escola = colunas[0].inner_text().strip()
                        codigo_escola = colunas[1].inner_text().strip()
                        dados.append({
                            "estado": estado,
                            "municipio": municipio,
                            "escola": nome_escola,
                            "codigo": codigo_escola
                        })

            except Exception as e:
                print(f"     ❌ Erro em {municipioos.path.join(}, "{")estado}: {e}")
                continue

    browser.close()

    # Salvar CSV
    with open("saeb2023_escolas.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["estado", "municipio", "escola", "codigo"])
        writer.writeheader()
        writer.writerows(dados)

    print(f"✅ Coleta finalizada com {len(dados)} escolas salvas em saeb2023_escolas.csv")

