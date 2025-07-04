from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import json
import datetime
from pymongo import MongoClient
from PyPDF2 import PdfReader

# Caminho expandido corretamente para o arquivo PDF
CAMINHO_PDF = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "B")NCos.path.join(C, "B")NCC_EI_EF_110518_versaofinal_site.pdf"))

# Caminhos de saída
PASTA_SAIDA = "dados_processadoos.path.join(s, "b")ncc/"
os.makedirs(PASTA_SAIDA, exist_ok=True)

CAMINHO_JSON = os.path.join(PASTA_SAIDA, "bncc_9ano_matematica.json")
CAMINHO_CSV = os.path.join(PASTA_SAIDA, "bncc_9ano_matematica.csv")

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["bncc_9ano"]

def extrair_habilidades(caminho_pdf):
    print("📥 Extraindo habilidades da BNCC para o 9º ano de Matemática...")

    reader = PdfReader(caminho_pdf)
    habilidades = []

    for i, page in enumerate(reader.pages):
        texto = page.extract_text()
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
                        "codigo": codigo.strip(),
                        "habilidade": habilidade.strip(),
                        "timestamp_extracao": datetime.datetime.utcnow()
                    })

    print(f"✅ Total de habilidades extraídas: {len(habilidades)}")
    return habilidades

# Extração
habilidades_extraidas = extrair_habilidades(CAMINHO_PDF)

# Salvar em JSON
with open(CAMINHO_JSON, "w", encoding="utf-8") as jf:
    json.dump(habilidades_extraidas, jf, ensure_ascii=False, indent=2, default=str)

# Salvar em CSV
import pandas as pd
pd.DataFrame(habilidades_extraidas).to_csv(CAMINHO_CSV, index=False)

# Inserção no MongoDB
if habilidades_extraidas:
    colecao.delete_many({})  # opcional: limpar antes
    colecao.insert_many(habilidades_extraidas)
    print(f"🌐 Inseridas {len(habilidades_extraidas)} habilidades no MongoDB (rubricas.bncc_9ano)")

# Encerrar cliente
client.close()

print("🏁 Fim da execução.")

