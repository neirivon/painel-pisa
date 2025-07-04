from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# parser_pisa_2000.py
import re
from pymongo import MongoClient

# Conexão MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_2000_raw"]

# Nova coleção para dados extraídos
colecao_parser = db["pisa_2000_parser"]

# Padrões básicos para localizar informações (podemos expandir depois)
padrao_pais = re.compile(r'Country:\s*(.+)', re.IGNORECASE)
padrao_area = re.compile(r'Subject:\s*(Mathematics|Reading|Science)', re.IGNORECASE)
padrao_nome_variavel = re.compile(r'Variable:\s*(.+)', re.IGNORECASE)
padrao_valor = re.compile(r'Value:\s*(.+)', re.IGNORECASE)

# Processamento dos documentos
for doc in colecao.find():
    texto = doc.get("texto", "")

    pais = None
    area = None
    variaveis = []

    for linha in texto.splitlines():
        linha = linha.strip()

        match_pais = padrao_pais.search(linha)
        match_area = padrao_area.search(linha)
        match_variavel = padrao_nome_variavel.search(linha)
        match_valor = padrao_valor.search(linha)

        if match_pais:
            pais = match_pais.group(1)
        elif match_area:
            area = match_area.group(1)
        elif match_variavel:
            nome_var = match_variavel.group(1)
        elif match_valor:
            valor_var = match_valor.group(1)
            if pais and area and nome_var and valor_var:
                variaveis.append({
                    "pais": pais,
                    "area": area,
                    "variavel": nome_var,
                    "valor": valor_var
                })

    if variaveis:
        colecao_parser.insert_many(variaveis)

print("✅ Parsing e inserção no MongoDB concluídos!")
client.close()

