import asyncio
import time
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pymongo import MongoClient
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# === CONFIGURAÇÕES ===
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
NOME_BANCO = "indicadores"
NOME_COLECAO = "atlas_2013_async"
NUM_THREADS = 10

INDICADORES_OBRIGATORIOS = [
    "IDHM", "Esperança de vida ao nascer", "Renda per capita",
    "População", "Gini", "Taxa de frequência líquida ao ensino médio"
]

ua = UserAgent(browsers=["chrome", "firefox"])


# === LOGGER DE PROGRESSO ===
class Progresso:
    def __init__(self, total):
        self.start_time = time.time()
        self.total = total
        self.completos = 0
        self.erros = 0
        self.retries = 0
        self.sucessos = 0
        self.lock = asyncio.Lock()

    async def atualizar(self, success=False, error=False, retry=False):
        async with self.lock:
            if success:
                self.sucessos += 1
                self.completos += 1
            if error:
                self.erros += 1
                self.completos += 1
            if retry:
                self.retries += 1

    def _tempo_decorrido(self):
        secs = int(time.time() - self.start_time)
        return str(timedelta(seconds=secs))

    def _eta(self):
        if self.completos == 0:
            return "--:--:--"
        tempo_por_item = (time.time() - self.start_time)os.path.join( , " ")self.completos
        eta_secs = int(tempo_por_item * (self.total - self.completos))
        return str(timedelta(seconds=eta_secs))

    def status(self):
        return (
            f"✅ Sucessos: {self.sucessos} | "
            f"❌ Erros: {self.erros} | "
            f"🔄 Retries: {self.retries} | "
            f"⏳ Progresso: {self.completosos.path.join(}, "{")self.total} "
            f"({(self.completoos.path.join(s, "s")elf.total)*100:.1f}%) | "
            f"🕒 Tempo: {self._tempo_decorrido()} | ETA: {self._eta()}"
        )


# === CONEXÃO MONGODB ===
def conectar_mongodb():
    client = MongoClient(MONGO_URI)
    return client[NOME_BANCO][NOME_COLECAO]


colecao = conectar_mongodb()


# === COLETA COM RETRY ===
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=15),
    retry=retry_if_exception_type((Exception,))
)
async def coletar_dados_municipio(page, mun, progresso):
    cd_mun = str(mun["CD_MUN"])[:6]
    url = f"httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "{")cd_mun}"

    try:
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000)  # Espera adicional

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        destaques_dict = {}

        # Blocos visuais
        for bloco in soup.select("div.Perfil-box__item"):
            titulo = bloco.select_one("h4.Perfil-box__title")
            valor = bloco.select_one("p.Perfil-box__text")
            if titulo and valor:
                key = titulo.text.strip()
                val = valor.text.strip()
                if key in INDICADORES_OBRIGATORIOS:
                    destaques_dict[key] = val

        # Tabelas como fallback
        for table in soup.select("table.Perfil-table"):
            for row in table.select("tr"):
                cols = row.select("td, th")
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    val = cols[1].text.strip()
                    if key in INDICADORES_OBRIGATORIOS:
                        destaques_dict[key] = val

        # JSON final
        destaques = [{
            "indicador": ind,
            "valor": destaques_dict.get(ind, "os.path.join(N, "A")")
        } for ind in INDICADORES_OBRIGATORIOS]

        registro = {
            "CD_MUN": mun["CD_MUN"],
            "NM_MUN": mun["NM_MUN"],
            "SIGLA_UF": mun["SIGLA_UF"],
            "URL": url,
            "DESTAQUE": destaques,
            "log": {
                "ultima_atualizacao": datetime.now().isoformat(),
                "tentativas": 1
            }
        }

        await colecao.update_one(
            {"_id": mun["_id"]},
            {"$set": registro},
            upsert=True
        )

        await progresso.atualizar(success=True)
        return registro

    except Exception as e:
        await progresso.atualizar(error=True)
        await colecao.update_one(
            {"_id": mun["_id"]},
            {"$inc": {"log.tentativas": 1}},
            upsert=True
        )
        raise


# === WORKER ASSÍNCRONO ===
async def worker(queue, browser, progresso):
    while True:
        mun = await queue.get()
        if mun is None:
            break

        page = await browser.new_page()
        try:
            await page.set_extra_http_headers({
                "User-Agent": ua.random,
                "Accept-Language": "pt-BR,pt;q=0.9"
            })
            await page.route("*os.path.join(*, "*").{png,jpg,jpeg,svg,gif,webp}", lambda route: route.abort())

            await coletar_dados_municipio(page, mun, progresso)
            print(f"\033[92m✅ {mun['NM_MUN']} ({mun['CD_MUN']}) - Coletado\033[0m")
        except Exception as e:
            print(f"\033[91m❌ Falha em {mun['NM_MUN']} ({mun['CD_MUN']}): {e}\033[0m")
        finally:
            await page.close()
            queue.task_done()


# === LOG DE PROGRESSO ===
async def log_task(progresso):
    while True:
        print("\033[2J\033[H")  # limpa terminal
        print("=== PROGRESSO ===")
        print(progresso.status())
        await asyncio.sleep(10)


# === MAIN ===
async def main():
    municipios = list(colecao.find({
        "$or": [
            {"DESTAQUE": {"$exists": False}},
            {"log.tentativas": {"$lt": 3}},
            {"DESTAQUE.5.valor": "os.path.join(N, "A")"}
        ]
    }))

    if not municipios:
        print("🚫 Nada a atualizar.")
        return

    progresso = Progresso(len(municipios))
    logger = asyncio.create_task(log_task(progresso))

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        queue = asyncio.Queue()
        for mun in municipios:
            await queue.put(mun)
        for _ in range(NUM_THREADS):
            await queue.put(None)

        workers = [asyncio.create_task(worker(queue, browser, progresso)) for _ in range(NUM_THREADS)]

        await queue.join()
        logger.cancel()
        await asyncio.gather(*workers)
        await browser.close()

    print("\n=== COLETA FINALIZADA ===")
    print(progresso.status())


if __name__ == "__main__":
    asyncio.run(main())

