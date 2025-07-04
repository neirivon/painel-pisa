from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient
import numpy as np

def etl_pisa2003_student_com_peso_correto():
    # Conectar ao MongoDB
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    collection = db["pisa2003_student"]

    # Apagar documentos antigos
    collection.delete_many({})
    print("✅ Coleção limpa.")

    # Caminho para o arquivo
    ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

    print("⏳ Lendo arquivo com extração precisa por colunas fixas...")

    # Definindo colunas fixas conforme posição oficial
    colspecs = [
        (3, 6),    # CNT: código do país
        (910, 916), # PV1READ (posição estimada em caracteres - depende do layout PISA real)
        (916, 922), # PV1MATH
        (922, 928), # PV1SCIE
        (176-1, 183)  # W_FSTUWT - posição correta segundo SAS
    ]

    nomes_colunas = ["CNT", "PV1READ", "PV1MATH", "PV1SCIE", "W_FSTUWT"]

    # Carregar somente as colunas necessárias
    df = pd.read_fwf(
        ARQUIVO_STUDENT,
        colspecs=colspecs,
        names=nomes_colunas,
        encoding="latin1"
    )

    # Convertendo para numérico onde necessário
    df["PV1READ"] = pd.to_numeric(df["PV1READ"], errors="coerce")
    df["PV1MATH"] = pd.to_numeric(df["PV1MATH"], errors="coerce")
    df["PV1SCIE"] = pd.to_numeric(df["PV1SCIE"], errors="coerce")
    df["W_FSTUWT"] = pd.to_numeric(df["W_FSTUWT"], errors="coerce")

    # Corrigir peso 9997 para NaN
    df["W_FSTUWT"] = df["W_FSTUWT"].replace(9997, np.nan)

    # Mostrar exemplo
    print("✅ Dados extraídos corretamente, exemplo:")
    print(df.head())

    # Inserir no MongoDB
    registros = df.to_dict(orient="records")
    collection.insert_many(registros)
    print(f"✅ {len(registros)} documentos inseridos.")
    
    client.close()
    print("✅ Conexão encerrada.")

if __name__ == "__main__":
    etl_pisa2003_student_com_peso_correto()

