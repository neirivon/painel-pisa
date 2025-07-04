import os
import pandas as pd
from pymongo import MongoClient

# Caminho da pasta com os arquivos INT
PASTA_INT = "/home/neirivon/backup_dados_pesados/PISA_novo/DADOS/2009/INT"

# Credenciais de autenticação MongoDB dockerizado
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"

# Dicionário com nomes dos arquivos e coleções alvo
arquivos_colecoes = {
    "INT_COG09_S_DEC11.txt": "pisa_2009_cog_s",
    "INT_COG09_TD_DEC11.txt": "pisa_2009_cog_td",
    "INT_PAR09_DEC11.txt": "pisa_2009_parent",
    "INT_SCQ09_Dec11.txt": "pisa_2009_school",
    "INT_STQ09_DEC11.txt": "pisa_2009_student"
}

def importar_microdados():
    # Conectar ao MongoDB autenticado
    client = MongoClient(MONGO_URI)
    db = client["pisa"]

    for arquivo, colecao in arquivos_colecoes.items():
        caminho = os.path.join(PASTA_INT, arquivo)
        print(f"📥 Lendo arquivo: {caminho}")

        try:
            df = pd.read_csv(caminho, sep="\t", encoding="latin1", low_memory=False)
        except Exception as e:
            print(f"❌ Erro ao ler {arquivo}: {e}")
            continue

        registros = df.to_dict(orient="records")
        print(f"📦 Inserindo {len(registros):,} documentos na coleção '{colecao}'...")

        try:
            db[colecao].delete_many({})
            db[colecao].insert_many(registros)
            print(f"✅ Coleção '{colecao}' importada com sucesso!\n")
        except Exception as e:
            print(f"❌ Erro ao inserir na coleção '{colecao}': {e}")

    # Fechar conexão
    client.close()
    print("🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    importar_microdados()

