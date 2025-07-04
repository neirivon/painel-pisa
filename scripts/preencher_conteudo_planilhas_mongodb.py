import os
import openpyxl
from pymongo import MongoClient
from hashlib import sha256
from datetime import datetime

# Caminho onde estão os arquivos .xlsx
PASTA_PLANILHAS = "/home/neirivon/backup_dados_pesados/PISA_novo/PROTOCOLOS/2022/"

# Conexão com MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

colecoes = [c for c in db.list_collection_names() if c.startswith("protocolo_pisa_2022_")]

print(f"📊 Iniciando preenchimento de planilhas...")
total_atualizados = 0

try:
    for nome_colecao in colecoes:
        colecao = db[nome_colecao]

        documentos = colecao.find({ "pagina_inicio": "planilha", "conteudo": None })

        for doc in documentos:
            arquivo = doc["arquivo_original"]
            caminho = doc["fonte"]

            if not os.path.exists(caminho):
                print(f"  ⚠️ Arquivo não encontrado: {caminho}")
                continue

            try:
                wb = openpyxl.load_workbook(caminho, data_only=True)
                texto = ""
                for sheet in wb.worksheets:
                    for row in sheet.iter_rows(values_only=True):
                        linha = [str(cell) for cell in row if cell is not None]
                        texto += " | ".join(linha) + "\n"

                texto_limpo = texto.strip().replace("  ", " ").replace("\n\n", "\n")
                hash_valor = sha256(texto_limpo.encode("utf-8")).hexdigest()

                colecao.update_one(
                    { "_id": doc["_id"] },
                    {
                        "$set": {
                            "conteudo": texto_limpo,
                            "hash_conteudo": hash_valor,
                            "data_extracao": datetime.now().isoformat()
                        },
                        "$unset": { "trecho_do_conteudo": "" }
                    }
                )

                print(f"  ✅ Planilha preenchida: {arquivo}")
                total_atualizados += 1

            except Exception as e:
                print(f"  ❌ Erro ao processar planilha {arquivo}: {e}")

except Exception as geral:
    print(f"🔥 Erro geral: {geral}")

finally:
    print(f"\n📁 Total de planilhas atualizadas: {total_atualizados}")
    client.close()
    print("🔒 Conexão MongoDB fechada com sucesso.")

