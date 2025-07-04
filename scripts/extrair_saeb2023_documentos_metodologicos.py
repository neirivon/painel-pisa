# scripts/extrair_saeb2023_documentos_metodologicos.py

import os
import json
from PyPDF2 import PdfReader
from datetime import datetime
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo

# ========================
# CONFIGURAÇÃO
# ========================
DOCUMENTOS = [
    {
        "caminho": "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2021_2023/2023/LEIA-ME E DOCUMENTOS TÉCNICOS/Nota Técnica - Detalhamento da população e resultados do SAEB 2023.pdf",
        "titulo": "Nota Técnica - Detalhamento da população e resultados do SAEB 2023"
    },
    {
        "caminho": "/home/neirivon/backup_dados_pesados/SAEB_novo/DADOS/2021_2023/2023/LEIA-ME E DOCUMENTOS TÉCNICOS/Relatorio_de_Amostragem_SAEB_2023.pdf",
        "titulo": "Relatório de Amostragem SAEB 2023"
    }
]

ANO = 2023
FONTE = "INEP"
TIPO = "documento metodológico"
NOME_BANCO = "saeb"
NOME_COLECAO = "documentos_metodologicos_2023"
JSON_OUT = "dados_processados/saeb/documentos_metodologicos_2023.json"

# ========================
# EXTRAÇÃO DOS DOCUMENTOS
# ========================
registros = []
print("📄 Extraindo texto dos documentos metodológicos do SAEB 2023...")

for doc in DOCUMENTOS:
    texto = ""
    reader = PdfReader(doc["caminho"])
    for page in reader.pages:
        texto += page.extract_text() + "\n\n"

    registros.append({
        "ano": ANO,
        "tipo": TIPO,
        "fonte": FONTE,
        "titulo": doc["titulo"],
        "texto": texto.strip(),
        "timestamp": datetime.utcnow().isoformat()
    })

# ========================
# SALVAMENTO EM JSON
# ========================
os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(registros, f, ensure_ascii=False, indent=2)
print(f"✅ JSON salvo em: {JSON_OUT}")

# ========================
# INSERÇÃO NO MONGODB
# ========================
print("📡 Conectando ao MongoDB dockerizado com autenticação...")
db, client = conectar_mongo(nome_banco=NOME_BANCO)
colecao = db[NOME_COLECAO]

# Remover duplicatas com mesmo título antes de inserir
for reg in registros:
    colecao.replace_one(
        {"ano": ANO, "titulo": reg["titulo"]},
        reg,
        upsert=True
    )

print(f"✅ Documentos inseridos/atualizados em MongoDB: {NOME_BANCO}.{NOME_COLECAO}")
client.close()
print("🔒 Conexão com MongoDB encerrada com sucesso.")

