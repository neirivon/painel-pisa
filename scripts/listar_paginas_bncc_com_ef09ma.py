from PyPDF2 import PdfReader
import os

CAMINHO_PDF = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "B")NCos.path.join(C, "B")NCC_EI_EF_110518_versaofinal_site.pdf"))

reader = PdfReader(CAMINHO_PDF)
total_paginas = len(reader.pages)

print(f"🔍 Buscando por 'EF09MA' em {total_paginas} páginas...")

for i, page in enumerate(reader.pages):
    texto = page.extract_text()
    if texto and "EF09MA" in texto:
        print(f"✅ Padrão 'EF09MA' encontrado na página {i + 1}")

