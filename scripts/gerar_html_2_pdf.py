import asyncio
from playwright.async_api import async_playwright

async def gerar_pdf_html_para_arquivo():
    caminho_html = "/home/neirivon/Downloads/tcle_com_pdf_hash.html"  # Substitua se necessário
    caminho_saida = "/home/neirivon/Downloads/TCLE_assinado_Leonor_Teixeira.pdf"

    async with async_playwright() as p:
        navegador = await p.chromium.launch()
        pagina = await navegador.new_page()

        # Abrir o arquivo HTML local
        await pagina.goto(f"file://{caminho_html}")

        # Marcar as opções e clicar no botão para gerar o HASH
        await pagina.check("#autorizacao")
        await pagina.check("#aceite")
        await pagina.click("text=🔐 Gerar HASH e iniciar avaliação")

        # Espera o hash ser preenchido (ID = assinatura_hash)
        await pagina.wait_for_selector("#assinatura_hash")

        # Clica no botão de gerar PDF
        await pagina.click("text=📄 Baixar TCLE assinado em PDF")

        # Alternativamente, gerar um PDF diretamente da página renderizada:
        await pagina.pdf(path=caminho_saida, format="A4")

        print(f"✅ PDF gerado com sucesso: {caminho_saida}")
        await navegador.close()

# Executar
asyncio.run(gerar_pdf_html_para_arquivo())

