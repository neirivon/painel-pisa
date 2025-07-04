# diagnosticar_colecoes.py

from pymongo import MongoClient
import re

# Conexão MongoDB
client = MongoClient('mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin')
db = client['pisa']

print("📂 Diagnóstico das Coleções no Banco 'pisa':\n")

colecoes = db.list_collection_names()

# Expressões para identificar padrão
padrao_ocde = re.compile(r'(ocde|cy1mda|pfd|cy\d+)', re.IGNORECASE)
padrao_inep = re.compile(r'(inep)', re.IGNORECASE)
padrao_ano = re.compile(r'(2000|2003|2006|2009|2012|2015|2018|2022)')

# Diagnóstico
for colecao in sorted(colecoes):
    origem = "🔍 Desconhecida"
    ano = "❓"
    
    if padrao_ocde.search(colecao):
        origem = "🌍 OCDE"
    elif padrao_inep.search(colecao):
        origem = "🇧🇷 INEP"
    
    match_ano = padrao_ano.search(colecao)
    if match_ano:
        ano = match_ano.group(1)
    
    print(f"📌 Coleção: {colecao}")
    print(f"   ➡️ Origem: {origem}")
    print(f"   📅 Ano detectado: {ano}\n")

client.close()

