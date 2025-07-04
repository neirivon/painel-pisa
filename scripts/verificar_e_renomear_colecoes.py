# verificar_renomear_pisa_ocde.py
from pymongo import MongoClient
from collections import Counter
import re

def conectar_mongo():
    uri = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
    client = MongoClient(uri)
    db = client["pisa"]
    return client, db

def inferir_tipo(colecao, docs):
    campos = Counter()
    exemplo = {}

    for doc in docs:
        campos.update(doc.keys())
        exemplo.update(doc)

    chaves = set(campos.keys())

    if {"CNT", "ESCS15", "PV1MATH", "PV1READ", "PV1SCIE"} & chaves:
        return "alunos"
    if {"media", "leitura", "matematica", "ciencias"} & chaves:
        return "medias_oficiais"
    if {"VARID", "IDCNTRY"} & chaves:
        return "tabelas"
    if {"rubricas", "nivel", "percentual"} <= chaves:
        if "microrregiao" in chaves:
            return "rubricas_micro"
        return "rubricas_brasil"
    if {"secao", "nivel_bloom", "descricao"} <= chaves:
        return "relatorio_inep_bloom"
    if {"arquivo", "texto"} <= chaves:
        if "ocde" in colecao.lower():
            return "relatorio_ocde"
        return "relatorio_inep"
    if "lmc" in colecao.lower():
        return "comparativo_lmc"
    return "tipo_desconhecido"

def nome_padronizado(nome_antigo, tipo):
    match_ano = re.search(r"(\d{4})", nome_antigo)
    ano = match_ano.group(1) if match_ano else "xxxx"

    if tipo == "alunos":
        return f"pisa{ano}_alunos"
    elif tipo == "medias_oficiais":
        return f"pisa{ano}_medias_oficiais"
    elif tipo == "tabelas":
        return f"pisa{ano}_tabelas"
    elif tipo == "relatorio_ocde":
        return f"relatorio_ocde_{ano}"
    elif tipo == "relatorio_inep":
        return f"relatorio_inep_{ano}"
    elif tipo == "relatorio_inep_bloom":
        return f"relatorio_inep_bloom_{ano}"
    elif tipo == "rubricas_brasil":
        return f"rubricas_{ano}_brasil"
    elif tipo == "rubricas_micro":
        return f"rubricas_{ano}_micro"
    elif tipo == "comparativo_lmc":
        return f"pisa{ano}_comparativo_lmc"
    else:
        return f"{nome_antigo}_tipo_desconhecido"

def main():
    client, db = conectar_mongo()
    colecoes = db.list_collection_names()
    print("📦 Verificando coleções...\n")

    for nome in sorted(colecoes):
        docs = list(db[nome].find().limit(10))
        if not docs:
            print(f"⚠️  '{nome}': coleção vazia.")
            continue

        tipo = inferir_tipo(nome, docs)
        novo_nome = nome_padronizado(nome, tipo)

        if nome != novo_nome:
            print(f"🔄 '{nome}' → '{novo_nome}'")
            # db[nome].rename(novo_nome)  # Descomente para renomear no banco
        else:
            print(f"✅ '{nome}': nome já está padronizado.")

    client.close()
    print("\n🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    main()

