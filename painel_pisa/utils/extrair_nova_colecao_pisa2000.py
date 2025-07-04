# utilos.path.join(s, "e")xtrair_nova_colecao_pisa2000.py

from pymongo import MongoClient
import re

def conectar_mongo():
    uri = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
    client = MongoClient(uri)
    db = client["pisa"]
    return client, db

def extrair_e_inserir_medias():
    client, db = conectar_mongo()
    colecao_origem = db["pisa_ocde_2000_organizado"]
    colecao_destino = db["pisa2000_medias_extracao"]

    documentos = list(colecao_origem.find())
    padrao_linha = re.compile(r"^(BRA|OECD Avg|OECD Total)\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)")

    registros = []

    for doc in documentos:
        texto = doc.get("texto_extraido", "")
        linhas = texto.split("\n")
        for linha in linhas:
            linha = linha.strip()
            match = padrao_linha.match(linha)
            if match:
                pais = match.group(1)
                leitura = float(match.group(2))
                matematica = float(match.group(4))
                ciencias = float(match.group(6))
                registro = {
                    "pais": pais,
                    "leitura": leitura,
                    "matematica": matematica,
                    "ciencias": ciencias,
                    "ano": 2000
                }
                registros.append(registro)

    if registros:
        colecao_destino.delete_many({})  # Limpa antes de inserir
        colecao_destino.insert_many(registros)
        print(f"✅ Inseridos {len(registros)} documentos na coleção 'pisa2000_medias_extracao'.")
    else:
        print("⚠️ Nenhum registro extraído. Verifique o padrao ou os documentos.")

    client.close()

if __name__ == "__main__":
    extrair_e_inserir_medias()

