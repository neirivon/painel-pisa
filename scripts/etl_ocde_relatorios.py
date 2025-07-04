import os
import json
import fitz  # PyMuPDF
from pymongo import MongoClient

# Caminho base atualizado com base em sua estrutura real
PASTA_BASE = "/home/neirivon/backup_dados_pesados/PISA_novo/RELATORIOS"
PASTA_TXT = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/ocde_txt"
PASTA_JSON = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/ocde_json"

# Conexão com MongoDB dockerizado
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

# Cria pastas de saída se não existirem
os.makedirs(PASTA_TXT, exist_ok=True)
os.makedirs(PASTA_JSON, exist_ok=True)

# Percorre os anos (pastas dentro do diretório base)
for ano in sorted(os.listdir(PASTA_BASE)):
    pasta_ano = os.path.join(PASTA_BASE, ano)
    if not os.path.isdir(pasta_ano):
        continue

    for arquivo in os.listdir(pasta_ano):
        if not arquivo.lower().endswith(".pdf"):
            continue

        caminho_pdf = os.path.join(pasta_ano, arquivo)
        nome_base = os.path.splitext(arquivo)[0].replace(" ", "_").replace("-", "_").lower()
        nome_colecao = f"relatorio_ocde_pisa_{ano}_{nome_base}"
        nome_txt = os.path.join(PASTA_TXT, f"{ano}_{nome_base}.txt")
        nome_json = os.path.join(PASTA_JSON, f"{ano}_{nome_base}.json")

        # 1. Extrai texto do PDF
        try:
            doc = fitz.open(caminho_pdf)
            texto = "\n\n".join([page.get_text() for page in doc])
            doc.close()
        except Exception as e:
            print(f"❌ Erro ao processar PDF: {caminho_pdf}\n{e}")
            continue

        # 2. Salva como TXT
        with open(nome_txt, "w", encoding="utf-8") as f:
            f.write(texto)

        # 3. Estrutura em JSON
        documento_json = {
            "ano": int(ano),
            "arquivo": arquivo,
            "caminho_pdf": caminho_pdf,
            "texto": texto.strip(),
            "fonte": "OCDE",
            "versao_extraida": "v1.0",
            "referencia": f"PISA {ano} - OCDE"
        }

        with open(nome_json, "w", encoding="utf-8") as f:
            json.dump(documento_json, f, ensure_ascii=False, indent=2)

        # 4. Insere no MongoDB
        try:
            db[nome_colecao].delete_many({})  # limpa versão anterior se existir
            db[nome_colecao].insert_one(documento_json)
            print(f"✔ Inserido: {nome_colecao}")
        except Exception as e:
            print(f"❌ Erro ao inserir no MongoDB: {nome_colecao}\n{e}")

# 5. Fecha a conexão com MongoDB
client.close()
print("🔒 Conexão com MongoDB encerrada com sucesso.")

