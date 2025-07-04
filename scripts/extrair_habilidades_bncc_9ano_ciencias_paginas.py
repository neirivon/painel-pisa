# scriptos.path.join(s, "e")xtrair_habilidades_bncc_9ano_ciencias_paginas.py

import os
import json
import csv
from datetime import datetime
from pymongo import MongoClient
from PyPDF2 import PdfReader

CAMINHO_PDF = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "B")NCos.path.join(C, "B")NCC_EI_EF_110518_versaofinal_site.pdf"))
PAGINAS = [352, 353]

CAMINHO_JSON = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_ciencias.json"
CAMINHO_CSV = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_ciencias.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "sinapse"
COLECAO = "bncc_9ano_ciencias"

def extrair_habilidades():
    reader = PdfReader(CAMINHO_PDF)
    habilidades = []
    for pagina_num in PAGINAS:
        texto = reader.pages[pagina_num].extract_text()
        for linha in texto.split("\n"):
            if linha.strip().startswith("(EF09CI"):
                codigo = linha.split(")")[0].strip("()")
                habilidade = ")".join(linha.split(")")[1:]).strip()
                habilidades.append({
                    "etapa": "EF - Anos Finais",
                    "ano": "9º ano",
                    "area": "Ciências da Natureza",
                    "componente": "Ciências",
                    "codigo": codigo,
                    "habilidade": habilidade,
                    "timestamp_extracao": datetime.utcnow()
                })
    return habilidades

def salvar_json(habilidades):
    os.makedirs(os.path.dirname(CAMINHO_JSON), exist_ok=True)
    with open(CAMINHO_JSON, "w", encoding="utf-8") as jf:
        json.dump(
            [
                {**h, "timestamp_extracao": h["timestamp_extracao"].isoformat()}
                for h in habilidades
            ],
            jf,
            ensure_ascii=False,
            indent=2
        )
    print(f"💾 JSON salvo em: {CAMINHO_JSON}")

def salvar_csv(habilidades):
    with open(CAMINHO_CSV, "w", newline="", encoding="utf-8") as cf:
        writer = csv.DictWriter(cf, fieldnames=["etapa", "ano", "area", "componente", "codigo", "habilidade", "timestamp_extracao"])
        writer.writeheader()
        for h in habilidades:
            h["timestamp_extracao"] = h["timestamp_extracao"].isoformat()
            writer.writerow(h)
    print(f"💾 CSV salvo em: {CAMINHO_CSV}")

def inserir_mongodb(habilidades):
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[COLECAO]
    for h in habilidades:
        h["timestamp_extracao"] = datetime.utcnow()
    colecao.insert_many(habilidades)
    client.close()
    print(f"🌐 Inseridos {len(habilidades)} documentos no MongoDB.")

if __name__ == "__main__":
    print("📥 Extraindo habilidades da BNCC para o 9º ano de Ciências...")
    habilidades_extraidas = extrair_habilidades()
    print(f"✅ Total de habilidades extraídas: {len(habilidades_extraidas)}")
    salvar_json(habilidades_extraidas)
    salvar_csv(habilidades_extraidas)
    inserir_mongodb(habilidades_extraidas)
    print("🏁 Fim da execução.")

