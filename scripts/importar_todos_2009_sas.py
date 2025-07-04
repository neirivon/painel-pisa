import os
import pandas as pd
from pymongo import MongoClient
from os.path import expanduser

# === Configurações de caminhos ===
TXT_DIR = expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT")
SAS_DIR = expanduser("~/backup_dados_pesados/PISA_novo/DADOS/2009/SAS")

# === Mapeamento entre arquivos SAS/TXT e nomes de coleção ===
ARQUIVOS = [
    {
        "sas": "PISA2009_SAS_cognitive_item.sas",
        "txt": "PISA2009_SPSS_cognitive_item.txt",
        "colecao": "pisa_2009_cognitive_item"
    },
    {
        "sas": "PISA2009_SAS_scored_cognitive_item.sas",
        "txt": "PISA2009_SPSS_score_cognitive_item.txt",
        "colecao": "pisa_2009_score_cognitive_item"
    },
    {
        "sas": "PISA2009_SAS_school.sas",
        "txt": "PISA2009_SPSS_school.txt",
        "colecao": "pisa_2009_school"
    },
    {
        "sas": "PISA2009_SAS_student.sas",
        "txt": "PISA2009_SPSS_student.txt",
        "colecao": "pisa_2009_student"
    },
    {
        "sas": "PISA2009_SAS_parent.sas",
        "txt": "PISA2009_SPSS_parent.txt",
        "colecao": "pisa_2009_parent"
    }
]

# === Função para converter arquivo SAS para especificações de leitura ===
def parse_sas(file_path):
    colspecs = []
    names = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "@" in line and "$" in line:
                parts = line.strip().split()
                try:
                    pos = int(parts[1].replace("@", ""))
                    nome = parts[2]
                    tam = int(parts[3].replace("$", ""))
                    colspecs.append((pos - 1, pos - 1 + tam))
                    names.append(nome)
                except:
                    continue
    return colspecs, names

# === Conexão com MongoDB ===
cliente = MongoClient("mongodb://localhost:27017/")
db = cliente["pisa"]

# === Importação de cada arquivo ===
for item in ARQUIVOS:
    txt_path = os.path.join(TXT_DIR, item["txt"])
    sas_path = os.path.join(SAS_DIR, item["sas"])
    colecao = item["colecao"]

    print(f"\n📂 Importando: {item['txt']} → coleção '{colecao}'")

    try:
        colspecs, names = parse_sas(sas_path)
        if not colspecs or not names:
            raise ValueError("❌ SAS inválido: nenhum campo lido")

        df = pd.read_fwf(txt_path, colspecs=colspecs, names=names, encoding="latin1")
        registros = df.to_dict(orient="records")
        db[colecao].delete_many({})
        if registros:
            db[colecao].insert_many(registros)
            print(f"✅ Importado com sucesso! Total: {len(registros)} documentos.")
        else:
            print("⚠️ Arquivo vazio ou mal estruturado.")
    except Exception as e:
        print(f"❌ Erro ao importar '{txt_path}': {e}")

# === Fechamento da conexão ===
cliente.close()
print("\n🔒 Conexão com MongoDB encerrada.")

