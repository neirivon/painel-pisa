from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient
import numpy as np

def etl_pisa2003_student_final_sav():
    # Conectar ao MongoDB
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    collection = db["pisa2003_student"]

    # Apagar documentos antigos
    collection.delete_many({})
    print("✅ Coleção limpa.")

    # Caminho completo do arquivo SAV
    caminho_sav = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "C")Y1MDAI_STU_QQQ.sav"

    print("⏳ Lendo arquivo SAV oficial...")
    df = pd.read_spss(caminho_sav)

    print("✅ Dados carregados.")

    # Selecionar apenas colunas necessárias
    df_extracao = df[["CNT", "PV1READ", "PV1MATH", "PV1SCIE", "W_FSTUWT"]].copy()

    # Tratar pesos ausentes (9997 vira NaN)
    df_extracao["W_FSTUWT"] = df_extracao["W_FSTUWT"].replace(9997, np.nan)

    # Mostrar exemplo
    print("✅ Dados extraídos corretamente, exemplo:")
    print(df_extracao.head())

    # Inserir no MongoDB
    registros = df_extracao.to_dict(orient="records")
    collection.insert_many(registros)
    print(f"✅ {len(registros)} documentos inseridos.")
    
    client.close()
    print("✅ Conexão encerrada.")

if __name__ == "__main__":
    etl_pisa2003_student_final_sav()

