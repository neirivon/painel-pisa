# utilos.path.join(s, "l")oader_dados.py

import os
import json
from pymongo import MongoClient
from utils.config import CONFIG

# === Conexão MongoDB (apenas se permitido) ===
if CONFIG["USAR_MONGODB"]:
    client = MongoClient(CONFIG["MONGO_URI"])
    mongo = client["pisa"]
else:
    mongo = None

def _listar_edicoes_em(diretorio_base):
    base_path = os.path.join(os.path.dirname(__file__), "..", diretorio_base)
    if not os.path.exists(base_path):
        return []
    edicoes = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    edicoes.sort()
    return edicoes

def _carregar_dados_em(diretorio_base, edicao, nome_arquivo="dados.json"):
    caminho = os.path.join(os.path.dirname(__file__), "..", diretorio_base, str(edicao), nome_arquivo)
    if not os.path.exists(caminho):
        return None
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

# === PISA OCDE ===
def carregar_edicoes_pisa():
    if CONFIG["USAR_MONGODB"] and mongo:
        edicoes = []
        for nome in mongo.list_collection_names():
            if nome.startswith("pisa_ocde_") and nome.endswith("_alunos"):
                try:
                    edicao = nome.replace("pisa_ocde_", "").replace("_alunos", "")
                    int(edicao)
                    edicoes.append(edicao)
                except ValueError:
                    pass
        return sorted(edicoes)
    else:
        return _listar_edicoes_em(CONFIG["CAMINHO_DADOS"])

def carregar_dados_pisa(edicao):
    if CONFIG["USAR_MONGODB"] and mongo:
        nome_colecao = f"pisa_ocde_{edicao}_alunos"
        if nome_colecao in mongo.list_collection_names():
            return list(mongo[nome_colecao].find({}, {"_id": 0}))
    return _carregar_dados_em(CONFIG["CAMINHO_DADOS"], edicao, "dados.json")

# === SAEB INEP ===
def carregar_edicoes_saeb():
    return _listar_edicoes_em("dados_saeb_inep")

def carregar_dados_saeb(edicao):
    return _carregar_dados_em("dados_saeb_inep", edicao)

# === Relatórios INEP ===
def carregar_edicoes_relatorios_inep():
    return _listar_edicoes_em("relatorios_inep_pisa")

def carregar_dados_relatorio_inep(edicao):
    return _carregar_dados_em("relatorios_inep_pisa", edicao, "relatorio.json")

