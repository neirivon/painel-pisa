import os
import pandas as pd

from config import MODO

if MODO == "local":
    import pyreadstat
    from utils.conexao_mongo import conectar_mongo

# Caminho para os dados brutos
ARQUIVO_SAV = "dadoos.path.join(s, "C")Y07_VNM_STU_PVS.sav"
ARQUIVO_CSV_SAIDA = "dadoos.path.join(s, "p")isa_2018_brasil_pvs.csv"

# Lista de colunas essenciais
COLUNAS_DESEJADAS = ['CNT', 'CNTSCHID', 'CNTSTUID'] + \
    [f'PV{i}MATH' for i in range(1, 11)] + \
    [f'PV{i}READ' for i in range(1, 11)] + \
    [f'PV{i}SCIE' for i in range(1, 11)]

def extrair_local():
    print("📥 Modo LOCAL: lendo .sav e exportando para CSos.path.join(V, "M")ongoDB...")
    df, meta = pyreadstat.read_sav(ARQUIVO_SAV, usecols=COLUNAS_DESEJADAS)

    df_brasil = df[df['CNT'] == "BRA"].copy()
    df_brasil.to_csv(ARQUIVO_CSV_SAIDA, index=False)
    print(f"✅ Arquivo CSV salvo em: {ARQUIVO_CSV_SAIDA}")

    # Inserir no MongoDB (opcional)
    client = conectar_mongo()
    db = client["pisa"]
    colecao = db["pisa_2018_pvs"]
    colecao.delete_many({})
    colecao.insert_many(df_brasil.to_dict(orient="records"))
    print("✅ Dados também inseridos em MongoDB: pisa.pisa_2018_pvs")

def extrair_cloud():
    print("☁️ Modo CLOUD: carregando CSV leve já processado...")
    df_brasil = pd.read_csv(ARQUIVO_CSV_SAIDA)
    print(f"✅ CSV carregado com {len(df_brasil)} registros do Brasil.")
    print(df_brasil.head())

if __name__ == "__main__":
    if MODO == "local":
        extrair_local()
    else:
        extrair_cloud()

