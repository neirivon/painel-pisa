from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient
from docx import Document
import os
import re

# Caminho base
caminho_base = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "c")onvertidos"

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_2000_tabelas_textuais"]
colecao.delete_many({})  # limpeza anterior para testes

# Função para identificar se a linha é de cabeçalho
def extrair_colunas(linha):
    return re.split(r'\s{2,}', linha.strip())

# Processar cada arquivo DOCX
for nome_arquivo in sorted(os.listdir(caminho_base)):
    if nome_arquivo.endswith(".docx"):
        caminho_completo = os.path.join(caminho_base, nome_arquivo)
        doc = Document(caminho_completo)

        print(f"📂 Processando {nome_arquivo}...")

        paragrafos = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        bloco_tabela = []
        cabecalho = []
        topico = ""
        inseridos = 0

        for linha in paragrafos:
            if re.match(r'.*(Question|Table|Percentage).*', linha, re.IGNORECASE):
                topico = linha.strip()
                continue

            colunas = extrair_colunas(linha)
            if len(colunas) >= 3 and all(len(c) < 60 for c in colunas):
                if not cabecalho:
                    cabecalho = colunas
                    continue
                else:
                    entrada = dict(zip(cabecalho, colunas))
                    entrada["arquivo_origem"] = nome_arquivo
                    entrada["topico"] = topico
                    colecao.insert_one(entrada)
                    inseridos += 1
            else:
                cabecalho = []

        print(f"✅ Inseridos {inseridos} documentos no MongoDB.\n")

client.close()

