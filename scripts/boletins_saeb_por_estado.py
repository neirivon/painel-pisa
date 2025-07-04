# Coletor Playwright para boletins SAEB 2023 por estado (coEscola)

import pandas as pd
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time
import os

# === Configurações ===
csv_entrada = "saeb2023_brasil.csv"  # Arquivo com colunas: estado, municipio, escola, codigo
saida_dir = Path("boletins_por_estado")
saida_dir.mkdir(exist_ok=True)

# === Carregar dados ===
df = pd.read_csv(csv_entrada, dtype=str)
ufs = df['estado'].unique()

# === Função para processar um estado ===
def processar_estado(uf):
    print(f"\n🟩 Coletando boletins para UF: {uf}")
    df_uf = df[df['estado'] == uf].copy()
    boletins = []

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for idx, row in df_uf.iterrows():
            co_escola = row['codigo']
            url = f"httpos.path.join(:, "/")saeb.inep.gov.bos.path.join(r, "s")aeos.path.join(b, "r")esultado-final-externos.path.join(o, "b")oletim?anoProjeto=2023&coEscola={co_escola}"

            try:
                page.goto(url, timeout=30000)
                page.wait_for_selector(".titulo-escola", timeout=10000)

                escola = page.query_selector(".titulo-escola").inner_text().strip()
                rede = page.query_selector(".mat-card-subtitle span").inner_text().strip()

                # Notas podem estar em .valor-indicador
                notas = page.query_selector_all(".valor-indicador")
                nota_lp = notas[0].inner_text().strip() if len(notas) > 0 else ""
                nota_mat = notas[1].inner_text().strip() if len(notas) > 1 else ""

                boletins.append({
                    "co_escola": co_escola,
                    "escola": escola,
                    "municipio": row['municipio'],
                    "estado": uf,
                    "rede": rede,
                    "nota_lp": nota_lp,
                    "nota_mat": nota_mat
                })

            except PlaywrightTimeout:
                print(f"⚠️ Timeout para escola {co_escola}")
                continue
            except Exception as e:
                print(f"❌ Erro em {co_escola}: {e}")
                continue

            time.sleep(1.5)  # Respeito ao servidor

        browser.close()

    # Salvar CSV
    df_saida = pd.DataFrame(boletins)
    out_path = saida_diros.path.join( , " ")f"boletins_{uf.lower()}.csv"
    df_saida.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ Salvo: {out_path} ({len(df_saida)} registros)")

# === Loop por estado ===
for uf in sorted(ufs):
    processar_estado(uf)
