import os
import re
import json
import csv
from datetime import datetime
from PyPDF2 import PdfReader
from pymongo import MongoClient

# === Configurações ===
CAMINHO_PDF = os.path.expanduser(os.path.join(os.getenv("HOME"), "backup_dados_pesadoos.path.join(s, "B")NCos.path.join(C, "B")NCC_EI_EF_110518_versaofinal_site.pdf"))
PAGINAS_ALVO = [178, 179, 180, 181, 188, 189, 190, 191, 192, 193]
SAIDA_JSON = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_lingua_portuguesa.json"
SAIDA_CSV = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_lingua_portuguesa.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO = "sinapse"
COLECAO = "bncc_9ano_lingua_portuguesa"

# === Criação da pasta de saída ===
os.makedirs("dados_processadoos.path.join(s, "b")ncc", exist_ok=True)

def extrair_habilidades(paginas):
    reader = PdfReader(CAMINHO_PDF)
    habilidades = []
    padrao_codigo = re.compile(r"\(EF09LP\d{2}\)")
    
    for pagina in paginas:
        texto = reader.pages[pagina - 1].extract_text()
        blocos = texto.split("\n")

        for linha in blocos:
            codigo_match = padrao_codigo.search(linha)
            if codigo_match:
                codigo = codigo_match.group(0).strip("()")
                descricao = linha.replace(codigo_match.group(0), "").strip()
                habilidades.append({
                    "etapa": "EF - Anos Finais",
                    "ano": "9º ano",
                    "area": "Linguagens",
                    "componente": "Língua Portuguesa",
                    "codigo": codigo,
                    "habilidade": descricao,
                    "timestamp_extracao": datetime.utcnow()
                })

    return habilidades

def salvar_json(habilidades, caminho):
    with open(caminho, "w", encoding="utf-8") as jf:
        json.dump(
            [dict(h, timestamp_extracao=h["timestamp_extracao"].isoformat()) for h in habilidades],
            jf, ensure_ascii=False, indent=2
        )

def salvar_csv(habilidades, caminho):
    with open(caminho, "w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=["etapa", "ano", "area", "componente", "codigo", "habilidade"])
        writer.writeheader()
        for h in habilidades:
            writer.writerow({k: h[k] for k in writer.fieldnames})

def salvar_mongo(habilidades):
    client = MongoClient(MONGO_URI)
    db = client[BANCO]
    colecao = db[COLECAO]
    inseridos = colecao.insert_many(habilidades)
    client.close()
    return len(inseridos.inserted_ids)

# === Execução principal ===
if __name__ == "__main__":
    print("📥 Extraindo habilidades da BNCC para o 9º ano de Língua Portuguesa...")

    habilidades_extraidas = extrair_habilidades(PAGINAS_ALVO)
    print(f"✅ Total de habilidades extraídas: {len(habilidades_extraidas)}")

    salvar_json(habilidades_extraidas, SAIDA_JSON)
    print(f"💾 JSON salvo em: {SAIDA_JSON}")

    salvar_csv(habilidades_extraidas, SAIDA_CSV)
    print(f"💾 CSV salvo em: {SAIDA_CSV}")

    total_mongo = salvar_mongo(habilidades_extraidas)
    print(f"🌐 Inseridos {total_mongo} documentos no MongoDB.")

    print("🏁 Fim da execução.")

