# scripts/extrair_matriz_ciencias_natureza_saeb2023.py

import os, json
from PyPDF2 import PdfReader
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo
from pymongo.errors import OperationFailure

PDF_PATH = "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2021_2023/2023/MATRIZES DE REFERÊNCIA/Matriz de Referência de Ciências da Natureza.pdf"
ANO = 2023
AREA = "ciencias_natureza"
NOME_BANCO = "saeb"
NOME_COLECAO = "saeb_matrizes_2023"
JSON_OUT = "dados_processados/saeb/matriz_ciencias_natureza_2023.json"

print("📄 Extraindo texto da matriz de Ciências da Natureza...")
reader = PdfReader(PDF_PATH)
texto = "\n\n".join([p.extract_text() for p in reader.pages])

registro = {
    "ano": ANO,
    "area": AREA,
    "fonte": "INEP",
    "documento": "Matriz de Referência de Ciências da Natureza do Saeb (2023)",
    "texto": texto.strip()
}

os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(registro, f, ensure_ascii=False, indent=2)
print(f"✅ JSON salvo em: {JSON_OUT}")

print("📡 Conectando ao MongoDB dockerizado com autenticação...")
db, client = conectar_mongo(nome_banco=NOME_BANCO)
colecao = db[NOME_COLECAO]

try:
    colecao.replace_one({"ano": ANO, "area": AREA}, registro, upsert=True)
    print(f"✅ Documento inserido/atualizado em MongoDB: {NOME_BANCO}.{NOME_COLECAO}")
except OperationFailure as e:
    print(f"❌ Erro MongoDB: {e}")
finally:
    client.close()
    print("🔒 Conexão com MongoDB encerrada com sucesso.")

