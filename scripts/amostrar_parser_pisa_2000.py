from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from pymongo import MongoClient

client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]

colecao = db["pisa_2000_parser"]
arquivos = colecao.distinct("arquivo_origem")

for arquivo in arquivos:
    print(f"\n📄 Arquivo: {arquivo}")
    docs = colecao.find({"arquivo_origem": arquivo}).limit(5)
    for doc in docs:
        print("—", doc.get("linha", "").strip())

client.close()

