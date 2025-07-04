from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import pandas as pd
from pymongo import MongoClient

# Conectar ao MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]  # Banco de dados "pisa"
colecao = db["pisa_ocde_2018_completo"]  # Coleção onde salvaremos tudo

# Pasta onde estão os arquivos .xlsx
pasta_arquivos = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")018"))

# Função para limpar nomes de colunas
def limpar_nome_coluna(nome):
    if not isinstance(nome, str):
        return nome
    nome = nome.strip().replace(" ", "_").replace("/", "_ou_").replace("%", "percentual")
    return nome.lower()

# Começar o processamento
for arquivo in os.listdir(pasta_arquivos):
    if arquivo.endswith(".xlsx"):
        caminho_arquivo = os.path.join(pasta_arquivos, arquivo)
        print(f"📂 Processando {arquivo}...")
        try:
            # Carrega TODAS as abas
            xls = pd.read_excel(caminho_arquivo, sheet_name=None, engine="openpyxl")
            for nome_aba, df in xls.items():
                if df.empty:
                    continue
                df = df.rename(columns=lambda x: limpar_nome_coluna(x))
                documentos = df.to_dict(orient="records")
                # Inserir cada linha como um documento
                for doc in documentos:
                    doc["ano"] = 2018
                    doc["arquivo_origem"] = arquivo
                    doc["aba_origem"] = nome_aba
                if documentos:
                    colecao.insert_many(documentos)
                print(f"✅ Inserido aba: {nome_aba} com {len(documentos)} registros.")
        except Exception as e:
            print(f"❌ Erro no arquivo {arquivo}: {e}")

client.close()
print("\n🏁 Processo finalizado!")

