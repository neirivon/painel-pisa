from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import pandas as pd
from pymongo import MongoClient

# Caminho da pasta com arquivos XLSX
pasta_xlsx = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")018"))
arquivos_xlsx = [f for f in os.listdir(pasta_xlsx) if f.endswith(".xlsx")]

# Conexão com o MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2018"]

# Função de tradução de nomes de colunas
def traduzir_colunas(colunas):
    traducoes = {
        "CNT": "País",
        "Country": "País",
        "Mean": "Média",
        "Score": "Nota",
        "Average": "Média",
        "Gender": "Gênero",
        "School": "Escola",
        "ESCS": "Índice Socioeconômico",
        "Math": "Matemática",
        "Reading": "Leitura",
        "Science": "Ciências",
        "ESCS15": "Índice Socioeconômico aos 15 anos"
    }
    return [traducoes.get(col.strip(), col.strip()) for col in colunas]

# Limpa a coleção antes de novo carregamento (opcional)
colecao.delete_many({})

# Importar cada arquivo
for arquivo in arquivos_xlsx:
    caminho_arquivo = os.path.join(pasta_xlsx, arquivo)
    print(f"📂 Processando {arquivo}...")
    try:
        df = pd.read_excel(caminho_arquivo, engine="openpyxl")
        df.columns = traduzir_colunas(df.columns)
        df = df.dropna(how="all")  # Remove linhas totalmente vazias
        registros = df.to_dict(orient="records")
        
        # Inserir no MongoDB
        for registro in registros:
            registro["ano"] = 2018
            registro["arquivo_origem"] = arquivo
        if registros:
            colecao.insert_many(registros)
            print(f"✅ {len(registros)} registros inseridos.")
    except Exception as e:
        print(f"❌ Erro no arquivo {arquivo}: {e}")

client.close()
print("\n🚀 Importação concluída com sucesso!")

