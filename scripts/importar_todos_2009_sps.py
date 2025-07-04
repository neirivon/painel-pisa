import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# Configurações
PASTA_SPS = "backup_dados_pesados/PISA_novo/DADOS/2009/SPS.TXT"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "pisa"
MODO_CLOUD = False  # True para Streamlit Cloud (não salva CSV/JSON local)

ARQUIVOS = {
    "PISA2009_SPSS_cognitive_item.txt": "pisa_2009_cognitive_item",
    "PISA2009_SPSS_score_cognitive_item.txt": "pisa_2009_score_cognitive_item",
    "PISA2009_SPSS_school.txt": "pisa_2009_school",
    "PISA2009_SPSS_student.txt": "pisa_2009_student",
    "PISA2009_SPSS_parent.txt": "pisa_2009_parent"
}

def extrair_mascara_sps(sps_path):
    col_specs = []
    col_names = []
    lendo = False
    with open(sps_path, encoding="latin1") as f:
        for linha in f:
            linha = linha.strip()
            if linha.upper().startswith("/VARIABLES="):
                lendo = True
                continue
            if lendo:
                if not linha or linha.startswith('"') or linha.startswith("*") or "VALUE LABELS" in linha:
                    break
                partes = linha.split()
                if len(partes) >= 2 and '-' in partes[1]:
                    nome = partes[0]
                    try:
                        ini, fim = partes[1].split('-')
                        col_names.append(nome)
                        col_specs.append((int(ini) - 1, int(fim)))
                    except ValueError:
                        continue
    return col_names, col_specs

def importar_arquivo(txt_path, sps_path, nome_colecao, client):
    try:
        col_names, col_specs = extrair_mascara_sps(sps_path)
        df = pd.read_fwf(txt_path, names=col_names, colspecs=col_specs, encoding="latin1")
        df = df.dropna(how="all")
        if df.empty:
            print(f"⚠️  Arquivo vazio: {txt_path}")
            return

        if not MODO_CLOUD:
            base = os.path.splitext(os.path.basename(txt_path))[0]
            os.makedirs("dados_processados/pisa_2009", exist_ok=True)
            df.to_csv(f"dados_processados/pisa_2009/{base}.csv", index=False)
            df.to_json(f"dados_processados/pisa_2009/{base}.json", orient="records", force_ascii=False)

        db = client[DB_NAME]
        db[nome_colecao].delete_many({})
        db[nome_colecao].insert_many(df.to_dict(orient="records"))
        print(f"✅ Importado com sucesso: {txt_path} → coleção '{nome_colecao}' ({len(df)} registros)")
    except Exception as e:
        print(f"❌ Erro ao importar '{txt_path}': {e}")

def main():
    client = MongoClient(MONGO_URI)
    for nome_arquivo, nome_colecao in ARQUIVOS.items():
        txt_path = os.path.join(PASTA_SPS, nome_arquivo)
        sps_path = txt_path.replace(".txt", ".sps")
        print(f"\n📂 Importando: {nome_arquivo} → coleção '{nome_colecao}'")
        importar_arquivo(txt_path, sps_path, nome_colecao, client)
    client.close()
    print("\n🔒 Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    main()

