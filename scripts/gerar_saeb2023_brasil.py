# Script para gerar saeb2023_brasil.csv com estado, municipio, escola e codigo

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import pandas as pd
import time

saida_csv = "saeb2023_brasil.csv"
dados_completos = []

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Acessa o site principal
    url = "httpsos.path.join(:, "/")saeb.inep.gov.bos.path.join(r, "s")aeos.path.join(b, "r")esultado-final-externo"
    page.goto(url, timeout=60000)
    page.wait_for_selector("select[formcontrolname='anoEdicao']")
    page.select_option("select[formcontrolname='anoEdicao']", label="2023")
    time.sleep(1)

    # Lista de UFs
    ufs = page.query_selector_all("select[formcontrolname='siglaUf'] option")
    estados = [uf.get_attribute("value") for uf in ufs if uf.get_attribute("value")]

    for uf in estados:
        print(f"🟩 Estado: {uf}")
        page.select_option("select[formcontrolname='siglaUf']", value=uf)
        time.sleep(2)

        # Espera carregar municipios
        try:
            page.wait_for_selector("select[formcontrolname='municipio'] option", timeout=10000)
        except:
            print(f"❌ Erro ao carregar municípios de {uf}")
            continue

        municipios_options = page.query_selector_all("select[formcontrolname='municipio'] option")
        municipios = [m.get_attribute("value") for m in municipios_options if m.get_attribute("value")]

        for cod_mun in municipios:
            try:
                page.select_option("select[formcontrolname='municipio']", value=cod_mun)
                time.sleep(1)
                page.click("button:has-text('Pesquisar')")
                page.wait_for_selector("tbody tr", timeout=10000)

                linhas = page.query_selector_all("tbody tr")
                for linha in linhas:
                    colunas = linha.query_selector_all("td")
                    if len(colunas) >= 2:
                        escola = colunas[0].inner_text().strip()
                        codigo = colunas[1].inner_text().strip()
                        municipio = page.query_selector("select[formcontrolname='municipio'] option:checked").inner_text().strip()
                        dados_completos.append({
                            "estado": uf,
                            "municipio": municipio,
                            "escola": escola,
                            "codigo": codigo
                        })

            except PlaywrightTimeout:
                print(f"⚠️ Timeout em {uf} - mun {cod_mun}")
                continue
            except Exception as e:
                print(f"❌ Erro em {uf} - mun {cod_mun}: {e}")
                continue

    browser.close()

# Salvar CSV
pd.DataFrame(dados_completos).to_csv(saida_csv, index=False, encoding="utf-8")
print(f"✅ {len(dados_completos)} escolas salvas em {saida_csv}")

