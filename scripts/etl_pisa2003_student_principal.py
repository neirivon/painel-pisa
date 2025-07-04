from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient

def etl_pisa2003_student_principal():
    # Conectar ao MongoDB
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    collection = db["pisa2003_student"]

    # Apagar documentos antigos
    collection.delete_many({})
    print("✅ Coleção limpa.")

    # Arquivo correto
    ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

    # Definição manual das colunas principais
    colspecs = [
        (3, 6),      # CNT (país) - 4-6 (começa em 0)
        (345, 348),  # AGE - 346-348
        (507, 515),  # ESCS - 508-515
        (816, 824),  # PV1READ - 817-824
        (843, 851),  # PV1MATH - 844-851
        (870, 878),  # PV1SCIE - 871-878
        (1382, 1390) # W_FSTUWT - 1383-1390
    ]
    nomes_colunas = ["CNT", "AGE", "ESCS", "PV1READ", "PV1MATH", "PV1SCIE", "W_FSTUWT"]

    # Leitura dos dados
    print("⏳ Lendo o arquivo...")
    df = pd.read_fwf(
        ARQUIVO_STUDENT,
        colspecs=colspecs,
        names=nomes_colunas,
        encoding="latin1"
    )

    # Limpeza básica
    df = df.dropna(subset=["CNT", "AGE"])

    # Mostrar exemplo dos dados lidos
    print("✅ Dados carregados, exemplo:")
    print(df.head())

    # Inserir no MongoDB
    registros = df.to_dict(orient="records")
    collection.insert_many(registros)
    print(f"✅ {len(registros)} documentos inseridos.")

    # Fechar conexão
    client.close()
    print("✅ Conexão encerrada.")

if __name__ == "__main__":
    etl_pisa2003_student_principal()

