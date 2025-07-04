from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import pandas as pd
import os
from pymongo import MongoClient
from glob import glob

# Caminhos base
base_inep = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "i")nep/"))
base_ocde = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "c")sv/"))
saida_geral = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "p")isa_geral_unificado.csv"))

# Conexão com MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao_geral = db["pisa_geral"]

# Carregar e unificar INEP
def carregar_inep():
    frames = []
    for ano in os.listdir(base_inep):
        ano_path = os.path.join(base_inep, ano)
        arquivos = glob(os.path.join(ano_path, "*.csv"))
        for arquivo in arquivos:
            df = pd.read_csv(arquivo, encoding="utf-8")
            df["origem"] = "INEP"
            df["ano"] = int(ano)
            frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# Carregar e unificar OCDE
def carregar_ocde():
    arquivos = glob(os.path.join(base_ocde, "*.csv"))
    frames = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo)
        df["origem"] = "OCDE"
        for ano in ["2000", "2003", "2006", "2009", "2012", "2015", "2018", "2022"]:
            if ano in arquivo:
                df["ano"] = int(ano)
                break
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# Função principal
def unificar():
    print("🔍 Carregando dados do INEP...")
    df_inep = carregar_inep()
    print(f"✅ INEP: {len(df_inep)} registros")

    print("🔍 Carregando dados da OCDE...")
    df_ocde = carregar_ocde()
    print(f"✅ OCDE: {len(df_ocde)} registros")

    print("🔄 Unificando datasets...")
    df_geral = pd.concat([df_inep, df_ocde], ignore_index=True)

    # Exporta CSV unificado
    df_geral.to_csv(saida_geral, index=False)
    print(f"💾 Exportado para CSV: {saida_geral}")

    # Exporta para MongoDB
    registros = df_geral.to_dict(orient="records")
    if registros:
        colecao_geral.delete_many({})
        colecao_geral.insert_many(registros)
        print(f"📥 Inseridos {len(registros)} registros no MongoDB (coleção 'pisa_geral')")

    print("🏁 Unificação finalizada com sucesso!")

if __name__ == "__main__":
    unificar()

