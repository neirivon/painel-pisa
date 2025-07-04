# scripts/extrair_escalas_saeb2023_tradicional.py

import os
import json
from PyPDF2 import PdfReader
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo
from pymongo.errors import OperationFailure

# =====================
# CONFIGURAÇÃO
# =====================
PDF_PATH = "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2021_2023/2023/ESCALAS DE PROFICIÊNCIA/Escalas de Proficiência do Saeb.pdf"
ANO = 2023
TIPO = "tradicional"
NOME_BANCO = "saeb"
NOME_COLECAO = "saeb_escalas_2023"

JSON_OUT = "dados_processados/saeb/escalas_saeb2023_tradicional.json"

# =====================
# EXTRAÇÃO DO PDF
# =====================
print("📄 Extraindo texto da escala tradicional (SAEB 2023)...")
reader = PdfReader(PDF_PATH)
texto_completo = ""

for page in reader.pages:
    texto = page.extract_text()
    if texto:
        texto_completo += texto + "\n\n"

registro = {
    "ano": ANO,
    "tipo": TIPO,
    "fonte": "INEP",
    "documento": "Escalas de Proficiência do Saeb (versão tradicional)",
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
try:
    db, client = conectar_mongo(nome_banco=NOME_BANCO)
    colecao = db[NOME_COLECAO]

    colecao.replace_one(
        {"ano": ANO, "tipo": TIPO},
        registro,
        upsert=True
    )
    print(f"✅ Documento inserido/atualizado em MongoDB: {NOME_BANCO}.{NOME_COLECAO}")
except OperationFailure as e:
    print(f"❌ Falha na operação MongoDB: {e}")
finally:
    client.close()
    print("🔒 Conexão com MongoDB encerrada com sucesso.")

