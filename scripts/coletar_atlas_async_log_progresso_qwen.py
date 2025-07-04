import asyncio
import random
import logging
from datetime import timedelta
from pathlib import Path
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from pymongo import MongoClient
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from collections import deque


# === CONFIGURAÇÕES ===
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
NOME_BANCO = "indicadores"
NOME_COLECAO = "atlas_2013_async"

NUM_THREADS = 10  # Ajuste conforme sua máquina

INDICADORES_OBRIGATORIOS = {
    "IDHM",
    "Esperança de vida ao nascer",
    "Renda per capita",
    "População",
    "Gini",
    "Taxa de frequência líquida ao ensino médio"
}

# Pasta para logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIRos.path.join( , " ")"progresso.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Configurar User-Agent aleatório
ua = UserAgent(browsers=["chrome", "firefox"])

# Variáveis globais de progresso
total_municipios = 0
municipios_concluidos = 0
lock = asyncio.Lock()


# === CONEXÃO COM MONGODB ===
def conectar_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[NOME_BANCO]
    return db[NOME_COLECAO]


colecao = conectar_mongodb()


# Função para atualizar progresso
async def atualizar_progresso(sucesso=True):
    global municipios_concluidos
    async with lock:
        municipios_concluidos += 1
        percentual = (municipios_concluidosos.path.join( , " ")total_municipios) * 100
        logging.info(f"Progresso: {municipios_concluidosos.path.join(}, "{")total_municipios} ({percentual:.1f}%)")


# === FUNÇÃO PRINCIPAL DE COLETA ASSÍNCRONA ===
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=10),
    retry=retry_if_exception_type((Exception,))
)
async def coletar_dados_municipio(page, mun):
    cd_mun = str(mun["CD_MUN"])[:6]
    url = f"httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "{")cd_mun}"

    try:
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")

        # Esperar carregar conteúdo dinâmico
        await page.wait_for_selector("div.Perfil-box__item", timeout=20000)

        html = await page.content()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        destaques = []

        for bloco in soup.select("div.Perfil-box__item"):
            titulo_tag = bloco.select_one("h4.Perfil-box__title")
            valor_tag = bloco.select_one("p.Perfil-box__text")
            if titulo_tag and valor_tag:
                indicador_nome = titulo_tag.get_text(strip=True)
                if indicador_nome in INDICADORES_OBRIGATORIOS:
                    destaques.append({
                        "indicador": indicador_nome,
                        "valor": valor_tag.get_text(strip=True)
                    })

        # Garantir todos os indicadores estejam presentes
        nomes_coletados = [d['indicador'] for d in destaques]
        for nome in INDICADORES_OBRIGATORIOS:
            if nome not in nomes_coletados:
                destaques.append({"indicador": nome, "valor": ""})

        registro_final = {
            "CD_MUN": mun.get("CD_MUN"),
            "NM_MUN": mun.get("NM_MUN"),
            "SIGLA_UF": mun.get("SIGLA_UF"),
            "URL": url,
            "DESTAQUE": destaques
        }

        # Atualizar no MongoDB
        colecao.update_one(
            {"_id": mun["_id"]},
            {"$set": {"DESTAQUE": destaques}}
        )

        await atualizar_progresso(sucesso=True)
        return registro_final

    except Exception as e:
        logging.error(f"❌ Erro ao coletar {mun.get('NM_MUN', 'desconhecido')} ({cd_mun}): {e}")
        await atualizar_progresso(sucesso=False)
        raise


# === FUNÇÃO QUE RODA CADA THREAD ===
async def worker(queue, browser):
    while True:
        mun = await queue.get()
        if mun is None:
            break

        page = await browser.new_page()

        # Definir user-agent aleatório
        await page.set_extra_http_headers({"User-Agent": ua.random})

        try:
            resultado = await coletar_dados_municipio(page, mun)
            if resultado:
                logging.info(f"✅ Dados coletados: {resultado['NM_MUN']} - {resultado['CD_MUN']}")
        finally:
            await page.close()
            queue.task_done()


# === FUNÇÃO PRINCIPAL ===
async def main():
    global total_municipios
    municipios = list(colecao.find({
        "$or": [
            {"DESTAQUE": {"$exists": False}},
            {"DESTAQUE": {"$size": 0}}
        ]
    }))

    total_municipios = len(municipios)
    print(f"🔍 Total de municípios a atualizar: {total_municipios}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        queue = asyncio.Queue()

        # Adicionar municípios na fila
        for mun in municipios:
            queue.put_nowait(mun)

        # Adicionar sentinelas para finalizar workers
        for _ in range(NUM_THREADS):
            queue.put_nowait(None)

        # Criar tarefas
        tasks = []
        for _ in range(NUM_THREADS):
            task = asyncio.create_task(worker(queue, browser))
            tasks.append(task)

        print(f"🚀 Iniciando coleta assíncrona com {NUM_THREADS} threads...")
        await queue.join()

        # Cancelar tarefas
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        await browser.close()

    print("🎉 Coleta concluída com sucesso!")


if __name__ == "__main__":
    asyncio.run(main())
