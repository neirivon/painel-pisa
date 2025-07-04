# scriptos.path.join(s, "s")craping_atlas_2013_municipios.py

import asyncio
import random
from datetime import timedelta
from pymongo import MongoClient
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from playwright.async_api import async_playwright
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from tqdm.asyncio import tqdm


# === CONFIGURAÇÕES ===
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
NOME_BANCO = "indicadores"
NOME_COLECAO = "atlas_2013_scraping"
NUM_THREADS = 8
DELAY_SEGUNDOS = [3, 4, 5]

INDICADORES_OBRIGATORIOS = {
    "IDHM",
    "Esperança de vida ao nascer",
    "Renda per capita",
    "População",
    "Gini",
    "Taxa de frequência líquida ao ensino médio"
}

ua = UserAgent(browsers=["chrome", "firefox"])


# === CONEXÃO COM MONGODB ===
def conectar_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[NOME_BANCO]
    return db[NOME_COLECAO]


colecao = conectar_mongodb()


# === FUNÇÃO DE COLETA DE UM MUNICÍPIO ===
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, max=15),
    retry=retry_if_exception_type((Exception,))
)
async def coletar_dados_municipio(page, mun):
    cd_mun = str(mun["CD_MUN"])[:6]
    url = f"httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "{")cd_mun}"

    await page.set_extra_http_headers({"User-Agent": ua.random})
    await page.goto(url, timeout=40000, wait_until="domcontentloaded")
    await page.wait_for_timeout(random.choice(DELAY_SEGUNDOS) * 1000)

    html = await page.content()
    soup = BeautifulSoup(html, "html.parser")

    destaques = []

    for bloco in soup.select("div.Perfil-box__item"):
        titulo_tag = bloco.select_one("h4.Perfil-box__title")
        valor_tag = bloco.select_one("p.Perfil-box__text")
        if titulo_tag and valor_tag:
            nome = titulo_tag.get_text(strip=True)
            valor = valor_tag.get_text(strip=True)
            if nome in INDICADORES_OBRIGATORIOS:
                destaques.append({
                    "indicador": nome,
                    "valor": valor
                })

    nomes_coletados = [d['indicador'] for d in destaques]
    for nome in INDICADORES_OBRIGATORIOS:
        if nome not in nomes_coletados:
            destaques.append({"indicador": nome, "valor": ""})

    doc_final = {
        "CD_MUN": mun.get("CD_MUN"),
        "NM_MUN": mun.get("NM_MUN"),
        "SIGLA_UF": mun.get("SIGLA_UF"),
        "URL": url,
        "DESTAQUE": destaques
    }

    colecao.update_one(
        {"_id": mun["_id"]},
        {"$set": doc_final}
    )

    return True


# === WORKER COM LOG DE PROGRESSO ===
async def worker(queue, browser, pbar, status):
    while True:
        mun = await queue.get()
        if mun is None:
            break

        try:
            page = await browser.new_page()
            resultado = await coletar_dados_municipio(page, mun)
            if resultado:
                status["sucesso"] += 1
        except Exception as e:
            status["falha"] += 1
            print(f"❌ Falha em {mun['NM_MUN']} ({mun['CD_MUN']}): {e}")
        finally:
            await page.close()
            pbar.update(1)
            queue.task_done()


# === MAIN ===
async def main():
    municipios = list(colecao.find({
        "$or": [
            {"DESTAQUE": {"$exists": False}},
            {"DESTAQUE": {"$size": 0}}
        ]
    }))

    total = len(municipios)
    print(f"🔍 Total de municípios a atualizar: {total}")

    status = {"sucesso": 0, "falha": 0}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        queue = asyncio.Queue()

        for mun in municipios:
            queue.put_nowait(mun)
        for _ in range(NUM_THREADS):
            queue.put_nowait(None)

        with tqdm(total=total, desc="📊 Coletando municípios") as pbar:
            tasks = [
                asyncio.create_task(worker(queue, browser, pbar, status))
                for _ in range(NUM_THREADS)
            ]

            await queue.join()

            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

        await browser.close()

    print("\n✅ Coleta finalizada.")
    print(f"🟢 Sucessos: {status['sucesso']}")
    print(f"🔴 Falhas: {status['falha']}")


if __name__ == "__main__":
    asyncio.run(main())

