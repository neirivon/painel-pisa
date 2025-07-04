import os
import pandas as pd
from pymongo import MongoClient

# Caminho base
CAMINHO_BASE = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2006/INT"

# Arquivos e coleções correspondentes
ARQUIVOS_COLECOES = {
    "INT_Cogn06_S_Dec07.txt": "pisa_2006_cog_s",
    "INT_Cogn06_T_Dec07.txt": "pisa_2006_cog_t",
    "INT_Par06_Dec07.txt": "pisa_2006_parent",
    "INT_Sch06_Dec07.txt": "pisa_2006_school",
    "INT_Stu06_Dec07.txt": "pisa_2006_student",
}

# Conectar ao MongoDB (com autenticação)
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

for nome_arquivo, nome_colecao in ARQUIVOS_COLECOES.items():
    caminho_arquivo = os.path.join(CAMINHO_BASE, nome_arquivo)
    print(f"📥 Lendo arquivo: {caminho_arquivo}")

    try:
        df = pd.read_csv(caminho_arquivo, sep="\t", encoding="latin-1", low_memory=False)
        registros = df.to_dict(orient="records")

        print(f"📦 Inserindo {len(registros):,} documentos na coleção '{nome_colecao}'...")
        db[nome_colecao].delete_many({})  # remove duplicações caso o script seja reexecutado
        db[nome_colecao].insert_many(registros)
        print(f"✅ Coleção '{nome_colecao}' importada com sucesso!\n")

    except Exception as e:
        print(f"❌ Erro ao importar '{nome_arquivo}': {e}\n")

# Fechar conexão
client.close()
print("🔒 Conexão com MongoDB encerrada.")

