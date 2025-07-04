from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# extrair_texto_docx.py
from docx import Document
from pymongo import MongoClient
import os

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_2000_raw"]
colecao.delete_many({})  # Limpa a coleção antes de importar de novo

# Caminho onde estão os .docx
pasta_docx = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")000"))

# Processar todos os .docx da pasta
for arquivo in os.listdir(pasta_docx):
    if arquivo.endswith(".docx"):
        caminho_arquivo = os.path.join(pasta_docx, arquivo)
        print(f"📂 Lendo {arquivo}...")
        doc = Document(caminho_arquivo)
        texto = []
        for paragrafo in doc.paragraphs:
            texto.append(paragrafo.text)
        texto_completo = "\n".join(texto)

        colecao.insert_one({
            "arquivo": arquivo,
            "texto": texto_completo
        })

print("✅ Textos extraídos e inseridos no MongoDB!")
client.close()

