import os
import argparse
import re
from PyPDF2 import PdfReader

def listar_paginas_com_codigo(caminho_pdf, codigo_busca):
    try:
        reader = PdfReader(caminho_pdf)
    except Exception as e:
        print(f"❌ Erro ao abrir o PDF: {e}")
        return

    print(f"🔍 Buscando por '{codigo_busca}' em {len(reader.pages)} páginas...")
    paginas_encontradas = []

    for i, page in enumerate(reader.pages):
        texto = page.extract_text()
        if texto and re.search(rf"\b{codigo_busca}", texto):
            print(f"✅ Padrão '{codigo_busca}' encontrado na página {i + 1}")
            paginas_encontradas.append(i + 1)

    if not paginas_encontradas:
        print("⚠️ Nenhuma ocorrência encontrada.")
    else:
        print(f"\n📄 Total de páginas com o padrão '{codigo_busca}': {len(paginas_encontradas)}")
        print(f"📑 Páginas: {paginas_encontradas}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Listar páginas do PDF que contêm um determinado código da BNCC.")
    parser.add_argument("--codigo", type=str, required=True, help="Código a ser buscado (ex: EF09LP)")
    parser.add_argument(
        "--pdf",
        type=str,
        default=os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "B")NCos.path.join(C, "B")NCC_EI_EF_110518_versaofinal_site.pdf"),
        help="Caminho do arquivo PDF da BNCC"
    )
    args = parser.parse_args()

    caminho_pdf = args.pdf.replace("~", os.path.expanduser("~"))
    listar_paginas_com_codigo(caminho_pdf, args.codigo)

