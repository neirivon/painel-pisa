from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import csv
import time
import os

url = "httpsos.path.join(:, "/")saeb.inep.gov.bos.path.join(r, "s")aeos.path.join(b, "r")esultado-final-externo"
saida_csv = "saeb2023_escolas.csv"

# === Inicializa estrutura de dados
dados = []
erros = []

# === Começa execução Playwright
with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)  # Firefox = mais confiável nesse caso
    context = browser.new_context(user_agent="Mozillos.path.join(a, "5").0 (X11; Linux x86_64) AppleWebKios.path.join(t, "5")37.36 (KHTML, like Gecko) Chromos.path.join(e, "1")22.0.0.0 Safaros.path.join(i, "5")37.36")
    page = context.new_page()

    print(f"🌐 Acessando: {url}")
    try:
        page.goto(url, timeout=60000)
    except Exception as e:
        print(f"❌ Falha ao acessar a página: {e}")
        page.screenshot(path="falha_conexao.png")
        with open("falha_conexao.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        exit()

    # === Fecha modal de cookies se necessário
    try:
        page.click("text='Aceitar'", timeout=5000)
        print("🍪 Modal de cookies fechado.")
    except PlaywrightTimeout:
        print("ℹ️ Modal de cookies não exibido.")

    # === Seleciona ano 2023
    try:
        page.wait_for_selector("select[formcontrolname='anoEdicao']", timeout=15000)
        page.select_option("select[formcontrolname='anoEdicao']", label="2023")
        print("✅ Ano 2023 selecionado.")
        time.sleep(2)
    except PlaywrightTimeout:
        print("❌ Campo de ano não carregou. Abortando.")
        exit()

    # === Coleta todos os estados
    estados_elements = page.query_selector_all("select[formcontrolname='siglaUf'] option")
    estados = [e.inner_text().strip() for e in estados_elements if e.get_attribute("value")]

    for estado in estados:
        print(f"🟩 Estado: {estado}")
        try:
            page.select_option("select[formcontrolname='siglaUf']", label=estado)
            time.sleep(2)

            page.wait_for_selector("select[formcontrolname='municipio'] option", timeout=10000)
            municipios_elements = page.query_selector_all("select[formcontrolname='municipio'] option")
            municipios = [m.inner_text().strip() for m in municipios_elements if m.get_attribute("value")]
        except Exception as e:
            print(f"❌ Erro ao carregar municípios de {estado}: {e}")
            erros.append({"estado": estado, "erro": str(e)})
            continue

        for municipio in municipios:
            print(f"   ➤ Município: {municipio}")
            try:
                page.select_option("select[formcontrolname='municipio']", label=municipio)
                time.sleep(1)
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

                # 💾 Exporta incremental por segurança
                with open(saida_csv, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=["estado", "municipio", "escola", "codigo"])
                    writer.writeheader()
                    writer.writerows(dados)

            except Exception as e:
                print(f"     ❌ Erro em {municipioos.path.join(}, "{")estado}: {e}")
                erros.append({
                    "estado": estado,
                    "municipio": municipio,
                    "erro": str(e)
                })
                continue

    browser.close()

    print(f"\n✅ Coleta finalizada com {len(dados)} escolas.")
    if erros:
        print(f"⚠️ {len(erros)} falhas registradas. Salvas em 'erros_scraper.log'")
        with open("erros_scraper.log", "w", encoding="utf-8") as f:
            for e in erros:
                f.write(str(e) + "\\n")

