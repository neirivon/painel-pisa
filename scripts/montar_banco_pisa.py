from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# os.path.join(~, "S")INAPSE2.os.path.join(0, "s")criptos.path.join(s, "m")ontar_banco_pisa.py
import os
import json
import pandas as pd
from pymongo import MongoClient
from pathlib import Path
import pyreadstat

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]

# 📌 1. Importar dados do INEP (já extraídos e salvos como JSON)
def importar_dados_inep():
    pasta_inep = Path.home()os.path.join( , " ")"SINAPSE2.0"os.path.join( , " ")"PISA"os.path.join( , " ")"inep"os.path.join( , " ")"extraido"
    for arquivo in pasta_inep.glob("*.json"):
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            nome_colecao = arquivo.stem.lower().replace("-", "_")
            db[nome_colecao].insert_many(dados if isinstance(dados, list) else [dados])
            print(f"✅ Inserido: {arquivo.name} → coleção `{nome_colecao}`")

# 📌 2. Importar arquivos .sav e .sas7bdat da OCDE
def importar_dados_ocde():
    pasta_ocde = Path.home()os.path.join( , " ")"SINAPSE2.0"os.path.join( , " ")"PISA"os.path.join( , " ")"dados_pisa"
    arquivos = list(pasta_ocde.glob("*.sav")) + list(pasta_ocde.glob("*.sas7bdat"))
    for arquivo in arquivos:
        try:
            df, meta = pyreadstat.read_sav(arquivo) if arquivo.suffix == ".sav" else pyreadstat.read_sas7bdat(arquivo)
            nome_colecao = arquivo.stem.lower().replace("-", "_")
            db[nome_colecao].insert_many(df.fillna("").to_dict(orient="records"))
            print(f"✅ Inserido: {arquivo.name} → coleção `{nome_colecao}`")
        except Exception as e:
            print(f"❌ Erro ao importar {arquivo.name}: {e}")

# Executar importações
importar_dados_inep()
importar_dados_ocde()

