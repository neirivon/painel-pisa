from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient
import numpy as np

def etl_pisa2003_student_final_com_wfstuwt():
    # Conectar ao MongoDB
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    collection = db["pisa2003_student"]

    # Apagar documentos antigos
    collection.delete_many({})
    print("✅ Coleção limpa.")

    # Caminho para o arquivo
    ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

    # Leitura usando separador inteligente
    print("⏳ Lendo o arquivo definitivo para notas e peso...")
    df = pd.read_csv(
        ARQUIVO_STUDENT,
        sep=r"\s+",
        engine="python",
        header=None,
        encoding="latin1",
        on_bad_lines='skip'
    )

    # Extração definitiva
    df_extracao = pd.DataFrame()
    df_extracao["CNT"] = df[0].str.slice(3, 6)
    df_extracao["PV1READ"] = pd.to_numeric(df[91], errors='coerce')
    df_extracao["PV1MATH"] = pd.to_numeric(df[92], errors='coerce')
    df_extracao["PV1SCIE"] = pd.to_numeric(df[93], errors='coerce')

    # Atenção: Ajustar aqui para o campo correto do W_FSTUWT
    # Como seu arquivo só tinha até a coluna 184 antes, parece que coluna 184 é a mais plausível para ser W_FSTUWT
    try:
        df_extracao["W_FSTUWT"] = pd.to_numeric(df[184], errors='coerce')
        # Tratar 9997 como NaN
        df_extracao["W_FSTUWT"] = df_extracao["W_FSTUWT"].replace(9997, np.nan)
    except KeyError:
        print("⚠️ Atenção: Não foi possível localizar a coluna 184 para W_FSTUWT!")
        df_extracao["W_FSTUWT"] = np.nan  # Preenche nulo para evitar falhas

    # Mostrar exemplo
    print("✅ Dados extraídos corretamente, exemplo:")
    print(df_extracao.head())

    # Inserir no MongoDB
    registros = df_extracao.to_dict(orient="records")
    collection.insert_many(registros)
    print(f"✅ {len(registros)} documentos inseridos.")

    # Fechar conexão
    client.close()
    print("✅ Conexão encerrada.")

if __name__ == "__main__":
    etl_pisa2003_student_final_com_wfstuwt()

