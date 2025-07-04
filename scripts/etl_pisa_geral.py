import os
import pyreadstat
import pandas as pd
from pymongo import MongoClient

# Configurações
BASE_DIR = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "d")ados_pisa"))
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BD = "pisa"

# Conexão com o MongoDB
client = MongoClient(MONGO_URI)
db = client[BD]

# Mapeamento de tipos por sufixo ou trecho do nome
TIPOS_MAP = {
    "STU_QQQ": "alunos",
    "STU_COG": "cognitivo",
    "SCH_QQQ": "escolas",
    "TCH_QQQ": "professores",
    "QQQ": "questionario",
    "COG": "cognitivo",
    "TIM": "tempos"
}

def detectar_tipo(nome_arquivo):
    for chave, tipo in TIPOS_MAP.items():
        if chave in nome_arquivo.upper():
            return tipo
    return "desconhecido"

def detectar_ano(caminho):
    caminho_lower = caminho.lower()

    # Detecta arquivos do Pisa for Development
    if "pfd" in caminho_lower or "mda" in caminho_lower or "mdc" in caminho_lower:
        return "pfd"

    # Detecta pastas com o ano no nome
    for pedaco in caminho.split(os.sep):
        if pedaco.isdigit() and len(pedaco) == 4:
            return pedaco

    return "desconhecido"

def importar_arquivo(caminho_completo):
    try:
        nome_arquivo = os.path.basename(caminho_completo)
        ano = detectar_ano(caminho_completo)
        tipo = detectar_tipo(nome_arquivo)

        if ano == "desconhecido" or tipo == "desconhecido":
            print(f"⚠️ Pulando arquivo sem metadados confiáveis: {nome_arquivo}")
            return

        print(f"\n📥 Lendo {nome_arquivo} (ano: {ano}, tipo: {tipo})...")
        if caminho_completo.lower().endswith(".sav"):
            df, _ = pyreadstat.read_sav(caminho_completo)
        elif caminho_completo.lower().endswith(".sas7bdat"):
            df, _ = pyreadstat.read_sas7bdat(caminho_completo)
        else:
            print(f"❌ Tipo não suportado: {caminho_completo}")
            return

        df = df.where(pd.notnull(df), None)
        dados = df.to_dict(orient="records")

        colecao = f"pisa_{ano}_{tipo}"
        print(f"📦 Inserindo {len(dados)} documentos em '{colecao}'...")
        db[colecao].insert_many(dados)
        print(f"✅ {nome_arquivo} importado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao importar {caminho_completo}: {e}")

# Varredura dos arquivos no diretório base
for root, dirs, files in os.walk(BASE_DIR):
    for arquivo in files:
        if arquivo.lower().endswith((".sav", ".sas7bdat")):
            caminho = os.path.join(root, arquivo)
            importar_arquivo(caminho)

client.close()
print("\n🏁 ETL finalizado para todos os arquivos.")

