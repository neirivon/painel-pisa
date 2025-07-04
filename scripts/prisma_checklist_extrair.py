import fitz  # PyMuPDF
import json

# Caminho para o arquivo PDF original
pdf_path = "/home/neirivon/backup_dados_pesados/PRISMA/PRISMA_2020_checklist.pdf"

# Caminho para o arquivo JSON de saída
json_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/prisma_checklist_resumido_populado.json"

# Abre o PDF
doc = fitz.open(pdf_path)

itens = []

# Loop pelas páginas para buscar os itens da checklist (normalmente todos estão na primeira ou segunda página)
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()

    lines = text.split("\n")
    for line in lines:
        if line.strip() and line[0].isdigit() and "." in line:
            # Exemplo de linha: "1. Título: Identifique o relatório como uma revisão sistemática."
            try:
                numero, resto = line.strip().split(".", 1)
                if ":" in resto:
                    titulo, descricao = resto.split(":", 1)
                else:
                    titulo = resto
                    descricao = ""
                itens.append({
                    "numero": int(numero.strip()),
                    "titulo": titulo.strip(),
                    "descricao": descricao.strip()
                })
            except Exception:
                continue

# Monta o objeto final
output = {
    "versao": "PRISMA 2020",
    "tipo": "resumido",
    "fonte": "Página oficial do PRISMA",
    "referencia_abnt": "PAGE, M. J. et al. PRISMA 2020 checklist. PRISMA, 2021. Disponível em: <https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf>. Acesso em: 06 jun. 2025.",
    "url": "https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf",
    "itens": itens
}

# Salva o JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Checklist PRISMA 2020 resumido extraído para: {json_output_path}")

