import fitz  # PyMuPDF
import pymongo

# Configuração do MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = "relatorios_inep_pisa"

# Caminho do PDF
PDF_PATH = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "i")neos.path.join(p, "2")00os.path.join(0, "p")isa_2000_relatorio_nacional.pdf"

def extrair_texto_e_imagens(pdf_path):
    doc = fitz.open(pdf_path)
    elementos = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        texto = page.get_text("text")
        imagens = page.get_images(full=True)

        if texto.strip():
            elementos.append({
                "tipo": "texto",
                "conteudo": texto.strip()
            })

        if imagens:
            elementos.append({
                "tipo": "imagem",
                "descricao": f"Imagem detectada na página {page_num + 1}.",
                "pagina": page_num + 1
            })

    return elementos

def inserir_mongodb(documento):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Remove documento anterior se existir (opcional)
    collection.delete_many({"ano": documento["ano"], "tipo": "relatorio_inep"})

    collection.insert_one(documento)
    client.close()

if __name__ == "__main__":
    print("📚 Extraindo texto e imagens do Relatório INEP 2000...")
    elementos = extrair_texto_e_imagens(PDF_PATH)

    documento = {
        "ano": 2000,
        "tipo": "relatorio_inep",
        "titulo": "Relatório Nacional do PISA 2000 - Brasil",
        "texto_geral": "Texto extraído do relatório completo.",
        "elementos": elementos
    }

    print(f"📥 Inserindo no MongoDB: {len(elementos)} elementos extraídos...")
    inserir_mongodb(documento)
    print("✅ Relatório INEP 2000 armazenado no MongoDB com sucesso!")

