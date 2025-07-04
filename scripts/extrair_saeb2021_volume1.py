# scripts/extrair_saeb2021_volume1.py

import os
import json
import csv
from PyPDF2 import PdfReader
from painel_pisa.utils.config import CONFIG
from painel_pisa.utils.conexao_mongo import conectar_mongo

# =====================
# CONFIGURAÇÃO
# =====================
PDF_PATH = "/home/neirivon/backup_dados_pesados/SAEB_novo/RELATORIOS/2021_2023/2021/relatorio_de_resultados_do_saeb_2021_volume_1.pdf"
PAG_INICIO = 21
PAG_FIM = 264

ANO = 2021
VOLUME = 1
NOME_BANCO = "saeb"
NOME_COLECAO = "saeb_relatorios_2021"

# Caminhos de saída
JSON_OUT = "dados_processados/saeb/relatorios_2021_volume1.json"
CSV_OUT = "dados_processados/saeb/relatorios_2021_volume1.csv"

# =====================
# EXTRAÇÃO DO PDF
# =====================
print("📄 Extraindo texto do PDF...")
reader = PdfReader(PDF_PATH)
texto_completo = ""

for i in range(PAG_INICIO - 1, PAG_FIM):
    page = reader.pages[i]
    texto_completo += page.extract_text() + "\n\n"

registro = {
    "ano": ANO,
    "volume": VOLUME,
    "paginas": f"{PAG_INICIO}-{PAG_FIM}",
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
# SALVAR EM CSV
# =====================
with open(CSV_OUT, "w", encoding="utf-8", newline="") as f_csv:
    writer = csv.DictWriter(f_csv, fieldnames=["ano", "volume", "paginas", "texto"])
    writer.writeheader()
    writer.writerow(registro)
print(f"✅ CSV salvo em: {CSV_OUT}")

# =====================
# INSERIR NO MONGODB
# =====================
print("📡 Conectando ao MongoDB dockerizado com autenticação...")

try:
    db, client = conectar_mongo(
        nome_banco=NOME_BANCO,
        uri="mongodb://admin:admin123@localhost:27017/?authSource=admin"
    )
    colecao = db[NOME_COLECAO]

    # Prevenção de duplicatas
    colecao.delete_many({
        "ano": ANO,
        "volume": VOLUME,
        "paginas": f"{PAG_INICIO}-{PAG_FIM}"
    })

    colecao.insert_one(registro)
    print(f"✅ Documento inserido em MongoDB: {NOME_BANCO}.{NOME_COLECAO}")

finally:
    client.close()
    print("🔒 Conexão com MongoDB encerrada com sucesso.")

