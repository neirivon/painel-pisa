import os
import fitz  # PyMuPDF
import json

# Caminho da pasta com os PDFs
pasta_pdfs = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "i")neos.path.join(p, "p")df"))
pasta_saida = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "i")neos.path.join(p, "e")xtraido"))
os.makedirs(pasta_saida, exist_ok=True)

def extrair_texto_pdf(arquivo_pdf):
    try:
        with fitz.open(arquivo_pdf) as doc:
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
        return texto
    except Exception as e:
        print(f"❌ Erro ao processar {arquivo_pdf}: {e}")
        return None

def salvar_texto_json(nome_pdf, texto):
    nome_base = os.path.splitext(nome_pdf)[0]
    caminho_json = os.path.join(pasta_saida, f"{nome_base}.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump({"arquivo": nome_pdf, "texto": texto}, f, ensure_ascii=False, indent=2)
    print(f"✅ Texto salvo: {caminho_json}")

def processar_todos_pdfs():
    arquivos = sorted(os.listdir(pasta_pdfs))
    pdfs = [a for a in arquivos if a.lower().endswith(".pdf")]

    if not pdfs:
        print("⚠️ Nenhum PDF encontrado na pasta.")
        return

    print(f"🔍 Encontrados {len(pdfs)} PDFs na pasta.")
    for pdf in pdfs:
        caminho = os.path.join(pasta_pdfs, pdf)
        print(f"📄 Processando: {pdf}")
        texto = extrair_texto_pdf(caminho)
        if texto:
            salvar_texto_json(pdf, texto)

if __name__ == "__main__":
    processar_todos_pdfs()

