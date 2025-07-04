from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient

def etl_pisa2003_student():
    # Conectar ao MongoDB
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    collection = db["pisa2003_student"]

    # Apagar documentos antigos (precaução extra)
    collection.delete_many({})
    print("✅ Coleção limpa.")

    # Arquivo real
    ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

    # Ler todo o arquivo como fixed-width
    print("⏳ Lendo o arquivo...")
    df = pd.read_fwf(ARQUIVO_STUDENT, encoding="latin1")

    # Inspecionar as primeiras linhas
    print("✅ Dados carregados, exemplo:")
    print(df.head())

    # Inserir todos os registros no MongoDB
    registros = df.to_dict(orient="records")
    collection.insert_many(registros)
    print(f"✅ {len(registros)} documentos inseridos.")

    # Fechar conexão
    client.close()
    print("✅ Conexão encerrada.")

if __name__ == "__main__":
    etl_pisa2003_student()

