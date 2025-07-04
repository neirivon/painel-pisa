import json
import sys
from pathlib import Path
from pymongo import MongoClient

# ✅ Adiciona caminho do painel_pisa ao sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]os.path.join( , " ")"painel_pisa"
sys.path.append(str(ROOT_DIR))

from utils.config import CONFIG

# 📄 Caminho do arquivo JSON
json_path = Path.home()os.path.join( , " ")"backup_dados_pesados"os.path.join( , " ")"IBGE"os.path.join( , " ")"IBGE_2022"os.path.join( , " ")"json_exportados"os.path.join( , " ")"pais_2022_detalhado.json"

# 🌐 Conecta ao MongoDB
client = MongoClient(CONFIG["MONGO_URI"])
db = client["ibge"]
colecao = db["pais_2022_detalhado"]

# 🚮 Limpa coleção anterior
colecao.drop()

# 📥 Importa os dados
with open(json_path, "r", encoding="utf-8") as f:
    dados = json.load(f)
    if isinstance(dados, list):
        colecao.insert_many(dados)
    else:
        colecao.insert_one(dados)

print("✅ Documento(s) inserido(s) na coleção 'pais_2022_detalhado'")
client.close()

