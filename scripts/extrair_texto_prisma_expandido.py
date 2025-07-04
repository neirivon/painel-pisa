import fitz  # PyMuPDF

# Caminho para o PDF expandido local
pdf_path = "/home/neirivon/backup_dados_pesados/PRISMA/PRISMA_2020_expanded_checklist.pdf"

# Caminho de saída do texto bruto extraído
txt_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/PRISMA_2020_expandido_texto_bruto.txt"

# Abre o documento
doc = fitz.open(pdf_path)
full_text = ""

# Concatena texto de todas as páginas
for page in doc:
    full_text += page.get_text() + "\n\n"

# Salva o texto extraído em um arquivo .txt
with open(txt_output_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"✔ Texto extraído para: {txt_output_path}")

