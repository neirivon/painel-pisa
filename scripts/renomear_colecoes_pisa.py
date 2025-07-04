from pymongo import MongoClient
import re

def conectar_mongo():
    uri = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
    client = MongoClient(uri)
    db = client["pisa"]
    return client, db

def extrair_ano(nome_colecao):
    match = re.search(r'(\d{4})', nome_colecao)
    return match.group(1) if match else None

def determinar_tipo(nome_colecao, campos):
    nome_lower = nome_colecao.lower()
    campos_lower = [campo.lower() for campo in campos]

    if "student" in nome_lower or "alunos" in nome_lower or any(campo in campos_lower for campo in ["cnt", "escs15", "pv1math"]):
        return "alunos"
    elif "media" in nome_lower or any(campo in campos_lower for campo in ["media", "leitura", "matematica", "ciencias"]):
        return "medias"
    elif "relatorio" in nome_lower or "texto" in campos_lower:
        return "relatorio"
    elif "rubrica" in nome_lower or "rubricas" in campos_lower:
        return "rubricas"
    elif "comparativo" in nome_lower or "lmc" in nome_lower:
        return "comparativo_lmc"
    else:
        return "tipo_desconhecido"

def main():
    client, db = conectar_mongo()
    colecoes = db.list_collection_names()

    for nome_antigo in colecoes:
        amostra = db[nome_antigo].find_one()
        if not amostra:
            print(f"⚠️  '{nome_antigo}': coleção vazia.")
            continue

        campos = list(amostra.keys())
        ano = extrair_ano(nome_antigo)
        tipo = determinar_tipo(nome_antigo, campos)

        if not ano or tipo == "tipo_desconhecido":
            print(f"⚠️  '{nome_antigo}': não foi possível determinar o novo nome.")
            continue

        novo_nome = f"pisa_ocde_{ano}_{tipo}"
        if nome_antigo != novo_nome:
            print(f"🔄 Renomeando '{nome_antigo}' para '{novo_nome}'")
            db[nome_antigo].rename(novo_nome)
        else:
            print(f"✅ '{nome_antigo}' já está padronizado.")

    client.close()
    print("🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    main()

