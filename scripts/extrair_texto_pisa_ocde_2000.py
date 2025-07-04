import fitz  # PyMuPDF
import json
import os

# === Caminho do PDF ===
caminho_pdf = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "R")ELATORIos.path.join(O, "P")ISA-OCDE-2000-en.pdf"

# === Verificação do caminho ===
if not os.path.exists(caminho_pdf):
    raise FileNotFoundError(f"Arquivo não encontrado: {caminho_pdf}")

# === Abrir e extrair o conteúdo ===
doc = fitz.open(caminho_pdf)
print(f"📄 Total de páginas no relatório: {len(doc)}")

documentos = []

for i, page in enumerate(doc):
    texto = page.get_text().strip()
    if texto:  # Ignora páginas em branco
        documentos.append({
            "origem": "ocde_2000",
            "arquivo": os.path.basename(caminho_pdf),
            "pagina": i + 1,
            "texto": texto
        })

# === Caminho de saída do JSON ===
caminho_saida = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoeos.path.join(s, "p")isa_2000_ocde_paginas.json"
os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

# === Salvar em JSON ===
with open(caminho_saida, "w", encoding="utf-8") as f:
    json.dump(documentos, f, ensure_ascii=False, indent=2)

print(f"✅ Extração concluída! {len(documentos)} páginas com texto foram salvas em: {caminho_saida}")

