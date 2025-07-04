import fitz  # PyMuPDF
import json

# Caminho do PDF expandido
pdf_path = "/home/neirivon/backup_dados_pesados/PRISMA/PRISMA_2020_expanded_checklist.pdf"

# Caminho do JSON de saída
json_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/prisma_checklist_expandido_populado.json"

# Abre o PDF
doc = fitz.open(pdf_path)

itens = []
coletando = False
item_atual = {}

for page in doc:
    text = page.get_text()
    lines = text.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("Item") and any(str(n) in line for n in range(1, 28)):
            if item_atual:
                itens.append(item_atual)
                item_atual = {}
            partes = line.split()
            try:
                numero = int(partes[1])
                titulo = " ".join(partes[2:])
                item_atual = {"numero": numero, "titulo": titulo, "descricao": ""}
                coletando = True
            except:
                continue
        elif coletando:
            if line == "":
                coletando = False
            elif "©" in line or "PRISMA" in line:
                continue
            else:
                item_atual["descricao"] += (" " + line if item_atual["descricao"] else line)

if item_atual:
    itens.append(item_atual)

# Verificação
print(f"✔ Total de itens extraídos: {len(itens)}")
for i, item in enumerate(itens[:3], 1):
    print(f"Prévia do item {i}:")
    print(f"  Número: {item['numero']}")
    print(f"  Título: {item['titulo']}")
    print(f"  Descrição: {item['descricao'][:80]}...")
    print("---")

# Monta estrutura final
output = {
    "versao": "PRISMA 2020",
    "tipo": "expandido",
    "fonte": "Página oficial do PRISMA",
    "referencia_abnt": "PAGE, M. J. et al. PRISMA 2020 expanded checklist. PRISMA, 2021. Disponível em: <https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-w7ra.pdf>. Acesso em: 06 jun. 2025.",
    "url": "https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-w7ra.pdf",
    "itens": itens
}

# Salva JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✔ Checklist PRISMA 2020 expandido salvo em: {json_output_path}")

