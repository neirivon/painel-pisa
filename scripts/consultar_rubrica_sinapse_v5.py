from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "c")onsultar_rubrica_sinapse_v5.py

import argparse
import re
from pymongo import MongoClient

# === Conexão MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
collection = db["sinapse_todas_v5"]

# === Parser de argumentos ===
parser = argparse.ArgumentParser(description="Consulta a Rubrica SINAPSE v5 no MongoDB.")
parser.add_argument("--dimensao", type=str, help="Filtra por nome completo da dimensão")
parser.add_argument("--nivel", type=int, help="Filtra por nível (1 a 5)")
parser.add_argument("--titulo", type=str, help="Filtra por título exato do nível (ex: Criador de Conexões)")
parser.add_argument("--regex", type=str, help="Busca por palavra-chave na descrição (regex, sem aspas)")

args = parser.parse_args()

# === Construção dinâmica do filtro ===
filtro = {}
if args.dimensao:
    filtro["dimensao"] = args.dimensao
if args.nivel:
    filtro["nivel"] = args.nivel
if args.titulo:
    filtro["titulo"] = args.titulo
if args.regex:
    filtro["descricao"] = { "$regex": args.regex, "$options": "i" }

# === Execução da consulta ===
resultados = collection.find(filtro)

print("=== Resultados ===")
for doc in resultados:
    print(f"[{doc['dimensao']}] Nível {doc['nivel']} — {doc['titulo']}\n→ {doc['descricao']}\n")

client.close()

