import os
import fitz  # PyMuPDF
from pymongo import MongoClient
from datetime import datetime
from hashlib import sha256

# Caminho dos arquivos PDF
PASTA_PDFS = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/"

# Conectar ao MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# Filtrar coleções do tipo protocolo
colecoes = [c for c in db.list_collection_names() if c.startswith("protocolo_pisa_2022_")]

print(f"📦 Total de coleções encontradas: {len(colecoes)}\n")
total_docs = 0

try:
    for nome_colecao in colecoes:
        print(f"🔍 Verificando coleção: {nome_colecao}")
        colecao = db[nome_colecao]

        documentos = colecao.find({ "conteudo": None })

        for doc in documentos:
            arquivo = doc.get("arquivo_original")
            caminho_pdf = doc.get("fonte")
            pagina_inicio = doc.get("pagina_inicio")
            pagina_fim = doc.get("pagina_fim")

            if not caminho_pdf or not os.path.exists(caminho_pdf):
                print(f"  ⚠️ Arquivo não encontrado: {caminho_pdf}")
                continue

            if not isinstance(pagina_inicio, int) or not isinstance(pagina_fim, int):
                print(f"  ⚠️ Páginas inválidas: {pagina_inicio} a {pagina_fim} — {arquivo}")
                continue

            if caminho_pdf.endswith(".xlsx"):
                print(f"  ⏭️ Ignorando planilha: {arquivo}")
                continue

            try:
                with fitz.open(caminho_pdf) as pdf:
                    texto = ""
                    for i in range(pagina_inicio - 1, pagina_fim):
                        if i < len(pdf):
                            texto += pdf[i].get_text()

                texto_limpo = texto.strip().replace("\n", " ").replace("  ", " ")

                hash_valor = sha256(texto_limpo.encode("utf-8")).hexdigest()

                colecao.update_one(
                    { "_id": doc["_id"] },
                    {
                        "$set": {
                            "conteudo": texto_limpo,
                            "hash_conteudo": hash_valor,
                            "data_extracao": datetime.now().isoformat()
                        },
                        "$unset": { "trecho_do_conteudo": "" }
                    }
                )

                print(f"  ✅ Conteúdo preenchido: {arquivo}")
                total_docs += 1

            except Exception as e:
                print(f"  ❌ Erro ao processar {arquivo}: {e}")

except Exception as geral:
    print(f"🔥 Erro geral: {geral}")

finally:
    print(f"\n📊 Total de documentos atualizados: {total_docs}")
    client.close()
    print("🔒 Conexão MongoDB fechada com sucesso.")

