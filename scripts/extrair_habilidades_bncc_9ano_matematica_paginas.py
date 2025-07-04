import os
import json
import csv
from datetime import datetime
from pymongo import MongoClient
from PyPDF2 import PdfReader

# === CONFIGURAÇÕES ===
CAMINHO_PDF = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "B")NCos.path.join(C, "B")NCC_EI_EF_110518_versaofinal_site.pdf"))
CAMINHO_SAIDA_JSON = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_matematica.json"
CAMINHO_SAIDA_CSV = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_matematica.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"

# === PÁGINAS RELEVANTES (0-index) ===
PAGINAS_RELEVANTES = [317, 318, 319, 320]  # PDF usa base 0

# === EXTRAÇÃO DE TEXTO ===
def extrair_habilidades(caminho_pdf, paginas):
    reader = PdfReader(caminho_pdf)
    habilidades = []

    for i in paginas:
        texto = reader.pages[i].extract_text()
        if not texto:
            continue

        linhas = texto.split("\n")
        for linha in linhas:
            if linha.strip().startswith("EF09MA"):
                partes = linha.strip().split(" ", 1)
                if len(partes) == 2:
                    codigo, habilidade = partes
                    habilidades.append({
                        "etapa": "EF - Anos Finais",
                        "ano": "9º ano",
                        "area": "Matemática",
                        "componente": "Matemática",
                        "codigo": codigo,
                        "habilidade": habilidade.strip(),
                        "timestamp_extracao": datetime.utcnow()
                    })
    return habilidades

# === EXECUÇÃO ===
print("📥 Extraindo habilidades da BNCC para o 9º ano de Matemática...")

habilidades_extraidas = extrair_habilidades(CAMINHO_PDF, PAGINAS_RELEVANTES)
print(f"✅ Total de habilidades extraídas: {len(habilidades_extraidas)}")

# === SALVAR JSON ===
os.makedirs(os.path.dirname(CAMINHO_SAIDA_JSON), exist_ok=True)
with open(CAMINHO_SAIDA_JSON, "w", encoding="utf-8") as jf:
    json.dump(habilidades_extraidas, jf, ensure_ascii=False, indent=2, default=str)
print(f"💾 JSON salvo em: {CAMINHO_SAIDA_JSON}")

# === SALVAR CSV ===
with open(CAMINHO_SAIDA_CSV, "w", newline='', encoding="utf-8") as cf:
    writer = csv.DictWriter(cf, fieldnames=["etapa", "ano", "area", "componente", "codigo", "habilidade"])
    writer.writeheader()
    for h in habilidades_extraidas:
        writer.writerow({k: h[k] for k in writer.fieldnames})
print(f"💾 CSV salvo em: {CAMINHO_SAIDA_CSV}")

# === INSERIR NO MONGODB ===
client = MongoClient(MONGO_URI)
db = client["rubricas"]
colecao = db["bncc_9ano"]

if habilidades_extraidas:
    colecao.delete_many({ "ano": "9º ano", "componente": "Matemática" })  # evitar duplicatas
    colecao.insert_many(habilidades_extraidas)
    print(f"🌐 {len(habilidades_extraidas)} documentos inseridos em 'rubricas.bncc_9ano'.")

client.close()
print("🏁 Fim da execução.")

