from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "u")nificar_camadas_geograficas.py

import os
import json
from pathlib import Path
from pymongo import MongoClient

# Caminho local onde estão os arquivos .json das camadas
PASTA_BASE = Path.home()os.path.join( , " ")"backup_dados_pesados"os.path.join( , " ")"IBGE"os.path.join( , " ")"IBGE_2022"os.path.join( , " ")"json_exportados"

# Lista das coleções geográficas em ordem hierárquica
ARQUIVOS = {
    "pais": "pais_2022_detalhado.json",
    "regiao": "regioes_2022.json",
    "uf": "ufs_2022.json",
    "intermediaria": "regioes_intermediarias_2022.json",
    "imediata": "regioes_imediatas_2022.json",
    "municipio": "municipios_2022.json"
}

# Conectar ao MongoDB local
client = conectar_mongo(nome_banco="saeb")[1]
db = client["ibge"]
colecao = db["camadas_unificadas_2022"]
colecao.drop()  # Limpar coleção anterior se existir

# Função para carregar JSON de cada camada
def carregar_json(nome_arquivo):
    caminho = PASTA_BASEos.path.join( , " ")nome_arquivo
    if not caminho.exists():
        raise FileNotFoundError(f"❌ Arquivo não encontrado: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

# Inserir todos os documentos em uma coleção unificada
total_inseridos = 0
for camada, nome_arquivo in ARQUIVOS.items():
    dados = carregar_json(nome_arquivo)

    for doc in dados:
        doc["camada"] = camada
        doc["codigo"] = (
            doc.get("CD_MUNICIPIO") or
            doc.get("CD_RGIMEDIAT") or
            doc.get("CD_RGINTER") or
            doc.get("CD_UF") or
            doc.get("CD_RG") or
            doc.get("CD_PAIS") or
            None
        )
        colecao.insert_one(doc)
        total_inseridos += 1

print(f"✅ Total de documentos unificados inseridos: {total_inseridos}")
client.close()

