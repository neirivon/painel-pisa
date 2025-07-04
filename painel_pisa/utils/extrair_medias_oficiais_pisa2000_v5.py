# utilos.path.join(s, "e")xtrair_medias_oficiais_pisa2000_v5.py

import pandas as pd
import os
import json
from pymongo import MongoClient

# Caminhos
PASTA_SPS_FILES = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSS"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_SAIDA = "pisa2000_student_medias_oficiais_v5.json"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
MONGO_DB = "pisa"
MONGO_COLLECTION = "pisa2000_medias_oficiais"

# Arquivos de entrada
ARQUIVOS = {
    "leitura": "PISA2000_SPSS_student_reading.txt",
    "matematica": "PISA2000_SPSS_student_mathematics.txt",
    "ciencias": "PISA2000_SPSS_student_science.txt"
}

# Mapeamento de países OCDE (códigos numéricos)
CODIGOS_OCDE = {
    "036", "040", "056", "124", "203", "208", "246", "250", "276", "300",
    "348", "352", "372", "380", "392", "410", "428", "438", "442", "484",
    "528", "554", "578", "616", "620", "643", "724", "752", "756", "826", "840"
}

# Função auxiliar para calcular média ponderada usando WLE
def calcular_media_wle(df, coluna_wle, coluna_peso, coluna_pais):
    medias = {}
    for pais in df[coluna_pais].unique():
        if pd.isna(pais):
            continue
        subset = df[df[coluna_pais] == pais]
        if subset.empty:
            continue
        try:
            media = (subset[coluna_wle] * subset[coluna_peso]).sum()os.path.join( , " ")subset[coluna_peso].sum()
            medias[str(pais)] = media
        except ZeroDivisionError:
            medias[str(pais)] = None
    return medias

# Função principal
def extrair_medias_oficiais():
    resultados = []
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    colecao = db[MONGO_COLLECTION]
    colecao.drop()  # Limpamos antes

    for area, arquivo in ARQUIVOS.items():
        caminho = os.path.join(PASTA_SPS_FILES, arquivo)
        print(f"📃 Analisando {area.capitalize()} ({arquivo})...")

        try:
            df = pd.read_fwf(caminho, widths=[10]*30, header=None)
        except Exception as e:
            print(f"❌ Erro ao abrir {arquivo}: {e}")
            continue

        # Tentamos detectar as colunas que importam
        df.columns = [f"col_{i}" for i in range(len(df.columns))]

        # Mapeamento inicial bruto (vamos melhorar depois)
        df["country"] = df["col_0"]
        df["w_fstuwt"] = pd.to_numeric(df["col_1"], errors="coerce")  # peso amostral aproximado
        df["wle"] = pd.to_numeric(df["col_2"], errors="coerce")  # nota aproximada

        # Filtra apenas OCDE
        df_ocde = df[df["country"].astype(str).str.zfill(3).isin(CODIGOS_OCDE)]

        if df_ocde.empty:
            print(f"⚠️ Nenhum país OCDE encontrado no arquivo {arquivo}.")
            continue

        medias_paises = calcular_media_wle(df_ocde, "wle", "w_fstuwt", "country")

        # Calcula OECD Avg e OECD Total
        wle_geral = (df_ocde["wle"] * df_ocde["w_fstuwt"]).sum()os.path.join( , " ")df_ocde["w_fstuwt"].sum()

        resultados.append({
            "area": area,
            "medias_paises": medias_paises,
            "media_ocde_avg": wle_geral,
            "origem": "WLE_PISA2000"
        })

    # Salva no JSON
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    caminho_saida = os.path.join(PASTA_SAIDA, ARQUIVO_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print(f"✅ Extração científica concluída e salva em {caminho_saida}")

    # Insere no MongoDB
    colecao.insert_many(resultados)
    print(f"✅ Coleção MongoDB '{MONGO_COLLECTION}' atualizada com sucesso.")

    client.close()

if __name__ == "__main__":
    extrair_medias_oficiais()

