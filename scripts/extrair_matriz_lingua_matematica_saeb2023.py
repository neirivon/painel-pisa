# scripts/extrair_matriz_lingua_matematica_saeb2023.py

import os
import json
from PyPDF2 import PdfReader
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo
from pymongo.errors import OperationFailure

# =====================
# CONFIGURAÇÃO
# =====================
PDF_PATH = "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2021_2023/2023/MATRIZES DE REFERÊNCIA/Matriz de Referência de Língua Portuguesa e Matemática do Saeb.pdf"
ANO = 2023
AREA = "lingua_matematica"
NOME_BANCO = "saeb"
NOME_COLECAO = "saeb_matrizes_2023"
JSON_OUT = "dados_processados/saeb/matriz_lp_matematica_2023.json"

# =====================
# EXTRAÇÃO DO PDF
# =====================
print("📄 Extraindo texto da matriz de referência (Língua Portuguesa e Matemática)...")
reader = PdfReader(PDF_PATH)
texto_completo = ""

for page in reader.pages:
    texto_completo += page.extract_text() + "\n\n"

registro = {
    "ano": ANO,
    "area": AREA,
    "fonte": "INEP",
    "documento": "Matriz de Referência de Língua Portuguesa e Matemática do Saeb (2023)",
    "texto": texto_completo.strip()
}

# =====================
# SALVAR EM JSON
# =====================
os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
with open(JSON_OUT, "w", encoding="utf-8") as f_json:
    json.dump(registro, f_json, ensure_ascii=False, indent=2)
print(f"✅ JSON salvo em: {JSON_OUT}")

# =====================
# INSERIR NO MONGODB
# =====================
print("📡 Conectando ao MongoDB dockerizado com autenticação...")
db, client = conectar_mongo(nome_banco=NOME_BANCO)
colecao = db[NOME_COLECAO]

try:
    colecao.replace_one(
        {"ano": ANO, "area": AREA},
        registro,
        upsert=True
    )
    print(f"✅ Documento inserido/atualizado em MongoDB: {NOME_BANCO}.{NOME_COLECAO}")
except OperationFailure as e:
    print(f"❌ Falha na operação MongoDB: {e}")
finally:
    client.close()
    print("🔒 Conexão com MongoDB encerrada com sucesso.")

