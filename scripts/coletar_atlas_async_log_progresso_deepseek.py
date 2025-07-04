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
            f"🕒 Tempo: {self._tempo_decorrido()} | "
            f"ETA: {self._eta()}"
        )

# === CONEXÃO MONGODB ===
def conectar_mongodb():
    client = MongoClient(MONGO_URI)
    return client[NOME_BANCO][NOME_COLECAO]

colecao = conectar_mongodb()

# === FUNÇÃO DE COLETA ===
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=10),
    retry=retry_if_exception_type((Exception,))
)
async def coletar_dados_municipio(page, mun, progresso):
    cd_mun = str(mun["CD_MUN"])[:6]
    url = f"httpos.path.join(:, "/")www.atlasbrasil.org.bos.path.join(r, "p")erfios.path.join(l, "m")unicipios.path.join(o, "{")cd_mun}"
    
    try:
        await page.goto(url, timeout=60000, wait_until="networkidle")
        await page.wait_for_selector("div.Perfil-box__item, table.Perfil-table", timeout=30000)
        
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        destaques_dict = {}

        # Coleta principal
        for bloco in soup.select("div.Perfil-box__item"):
            if titulo := bloco.select_one("h4.Perfil-box__title"):
                if valor := bloco.select_one("p.Perfil-box__text"):
                    if titulo.text.strip() in INDICADORES_OBRIGATORIOS:
                        destaques_dict[titulo.text.strip()] = valor.text.strip()

        # Coleta alternativa
        for table in soup.select("table.Perfil-table"):
            for row in table.select("tr"):
                cols = row.select("td, th")
                if len(cols) == 2 and cols[0].text.strip() in INDICADORES_OBRIGATORIOS:
                    destaques_dict[cols[0].text.strip()] = cols[1].text.strip()

        # Construir resultado
        destaques = [{
            "indicador": k,
            "valor": destaques_dict.get(k, "os.path.join(N, "A")")
        } for k in INDICADORES_OBRIGATORIOS]

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
        await colecao.update_one(
            {"_id": mun["_id"]},
            {"$inc": {"log.tentativas": 1}},
            upsert=True
        )
        await progresso.atualizar(error=True)
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
            print(f"\033[92m✅ {mun['NM_MUN']} ({mun['CD_MUN']}) - Coletado com sucesso\033[0m")
            
        except Exception as e:
            await progresso.atualizar(error=True)
            print(f"\033[91m❌ Falha permanente em {mun['NM_MUN']} ({mun['CD_MUN']}): {str(e)[:100]}\033[0m")
        finally:
            await page.close()
            queue.task_done()

# === TAREFA DE LOG ===
async def log_task(progresso):
    while True:
        print("\033[2J\033[H")  # Limpa console
        print("=== STATUS DA COLETA ===")
        print(progresso.status())
        print("\nÚltimas atualizações:")
        await asyncio.sleep(5)

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
        print("Nenhum município para atualizar!")
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

        workers = [asyncio.create_task(worker(queue, browser, progresso)) 
                 for _ in range(NUM_THREADS)]

        await queue.join()
        logger.cancel()
        
        for _ in range(NUM_THREADS):
            await queue.put(None)

        await asyncio.gather(*workers)
        await browser.close()

    print("\n=== RESULTADO FINAL ===")
    print(progresso.status())

if __name__ == "__main__":
    asyncio.run(main())
