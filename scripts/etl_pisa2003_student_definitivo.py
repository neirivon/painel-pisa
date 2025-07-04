from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
from pymongo import MongoClient

def etl_pisa2003_student_corrigido_final():
    # Conectar ao MongoDB
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    collection = db["pisa2003_student"]

    # Apagar documentos antigos
    collection.delete_many({})
    print("✅ Coleção limpa.")

    # Arquivo correto
    ARQUIVO_STUDENT = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(3, "I")Nos.path.join(T, "I")NT_stui_2003_v2.txt"

    # Ler o arquivo usando separador inteligente
    print("⏳ Lendo o arquivo corrigido final...")
    df = pd.read_csv(
        ARQUIVO_STUDENT,
        sep=r"\s+",
        engine="python",
        header=None,
        encoding="latin1",
        on_bad_lines='skip'
    )

    # Extração das variáveis principais corretas
    df_extracao = pd.DataFrame()
    df_extracao["CNT"] = df[0].str.slice(3, 6)  # extrai país (posição 4–6 do campo 0)
    df_extracao["PV1READ"] = pd.to_numeric(df[179], errors='coerce')
    df_extracao["PV1MATH"] = pd.to_numeric(df[180], errors='coerce')
    df_extracao["PV1SCIE"] = pd.to_numeric(df[181], errors='coerce')
    df_extracao["W_FSTUWT"] = pd.to_numeric(df[182], errors='coerce')

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
    etl_pisa2003_student_corrigido_final()

