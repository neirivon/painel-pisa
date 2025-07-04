from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import pandas as pd
from pymongo import MongoClient

# Caminho onde estão os arquivos
caminho_pasta = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")018"))

# Conecta ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["pisa_ocde_2018_paises_temp"]

colecao.delete_many({})  # Limpa antes de importar

# Colunas que podem indicar país
colunas_possiveis = {"PAIS", "Pais", "País", "COUNTRY", "Country", "CNT", "CNTISO", "NOME", "Nation"}

paises_encontrados = set()

for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith(".xlsx"):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        try:
            xls = pd.read_excel(caminho_arquivo, sheet_name=None, engine="openpyxl")
            for nome_aba, df in xls.items():
                if not df.empty:
                    for coluna in df.columns:
                        if any(c.lower() in coluna.lower() for c in colunas_possiveis):
                            valores = df[coluna].dropna().unique()
                            for pais in valores:
                                if isinstance(pais, str) and len(pais.strip()) > 0:
                                    paises_encontrados.add(pais.strip())
                # Salva para futura análise se quiser
                colecao.insert_one({
                    "arquivo": arquivo,
                    "aba": nome_aba,
                    "colunas": list(df.columns)
                })
        except Exception as e:
            print(f"❌ Erro ao ler {arquivo}: {e}")

print(f"\n🌍 Número total de países encontrados: {len(paises_encontrados)}")
print("📋 Lista de países encontrados:")
print(sorted(paises_encontrados))

client.close()

