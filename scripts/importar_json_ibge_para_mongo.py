import json
from pymongo import MongoClient
from pathlib import Path

# Caminho dos JSONs
json_dir = Path.home()os.path.join( , " ")"backup_dados_pesados"os.path.join( , " ")"IBGE"os.path.join( , " ")"IBGE_2022"os.path.join( , " ")"json_exportados"

# Arquivos e coleções
colecoes = {
    "municipios_2022": "municipios_2022.json",
    "regioes_imediatas_2022": "regioes_imediatas_2022.json",
    "regioes_intermediarias_2022": "regioes_intermediarias_2022.json",
    "ufs_2022": "ufs_2022.json",
    "regioes_2022": "regioes_2022.json",
    "pais_2022": "pais_2022.json"
}

# Conexão com MongoDB com autenticação
uri = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
client = MongoClient(uri)
db = client["ibge"]

# Importar cada JSON
for nome_colecao, nome_arquivo in colecoes.items():
    caminho = json_diros.path.join( , " ")nome_arquivo
    if not caminho.exists():
        print(f"❌ Arquivo não encontrado: {nome_arquivo}")
        continue

    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)

    colecao = db[nome_colecao]
    colecao.drop()  # Limpa coleção anterior
    colecao.insert_many(dados)
    print(f"✅ Importado: {nome_colecao} ({len(dados)} documentos)")

client.close()

