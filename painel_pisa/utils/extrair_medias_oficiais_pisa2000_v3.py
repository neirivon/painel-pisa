# utilos.path.join(s, "e")xtrair_medias_oficiais_pisa2000_v3.py

import pandas as pd
import json
import os
from pymongo import MongoClient

# Configurações principais
PASTA_SPSS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSS"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_SAIDA = "pisa2000_student_medias_oficiais_v3.json"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
BANCO_MONGO = "pisa"
COLECAO_MONGO = "pisa2000_medias_oficiais"

# Mapeamento dos arquivos e colunas relevantes (baseado nos manuais)
ARQUIVOS_SPSS = {
    "leitura": {
        "arquivo": "PISA2000_SPSS_student_reading.txt",
        "variavel_pv": "PV1READ",
        "larguras": [(0, 3), (3, 13), (13, 23)]  # Exemplo fictício, ajustaremos real abaixo
    },
    "matematica": {
        "arquivo": "PISA2000_SPSS_student_mathematics.txt",
        "variavel_pv": "PV1MATH",
        "larguras": [(0, 3), (3, 13), (13, 23)]
    },
    "ciencias": {
        "arquivo": "PISA2000_SPSS_student_science.txt",
        "variavel_pv": "PV1SCIE",
        "larguras": [(0, 3), (3, 13), (13, 23)]
    }
}

# Códigos de países da OCDE em 2000
Paises_OCDE = [
    "036", "040", "056", "124", "203", "208", "246", "250",
    "276", "300", "348", "352", "372", "380", "392", "410",
    "428", "438", "442", "484", "528", "554", "578", "616",
    "620", "643", "724", "752", "756", "826", "840"
]

def carregar_spss_fixed_width(caminho_arquivo, larguras):
    colspecs = [(inicio, fim) for inicio, fim in larguras]
    nomes_colunas = ["country", "w_fstuwt", "pv1"]
    df = pd.read_fwf(caminho_arquivo, colspecs=colspecs, names=nomes_colunas)
    return df

def calcular_media_ponderada(df):
    df = df.dropna(subset=["w_fstuwt", "pv1"])
    df["w_fstuwt"] = pd.to_numeric(df["w_fstuwt"], errors="coerce")
    df["pv1"] = pd.to_numeric(df["pv1"], errors="coerce")
    return (df["pv1"] * df["w_fstuwt"]).sum()os.path.join( , " ")df["w_fstuwt"].sum()

def extrair_medias_oficiais():
    print("🔍 Iniciando extração científica...")

    resultados = []

    for area, info in ARQUIVOS_SPSS.items():
        arquivo = info["arquivo"]
        caminho_arquivo = os.path.join(PASTA_SPSS, arquivo)

        print(f"📃 Analisando {area.title()} ({arquivo})...")

        df = carregar_spss_fixed_width(caminho_arquivo, info["larguras"])

        # Separar países OCDE
        df_ocde = df[df["country"].isin(Paises_OCDE)]

        # Cálculo por país
        medias_por_pais = []
        for pais in df_ocde["country"].unique():
            dados_pais = df_ocde[df_ocde["country"] == pais]
            media_pais = calcular_media_ponderada(dados_pais)
            medias_por_pais.append({
                "pais_codigo": pais,
                "area": area,
                "media": round(media_pais, 2)
            })

        # Cálculo OECD Avg
        media_ocde_avg = calcular_media_ponderada(df_ocde)

        resultados.append({
            "area": area,
            "media_oecd_avg": round(media_ocde_avg, 2),
            "medias_paises": medias_por_pais,
            "origem": "extraído_fixed_width"
        })

    # Salvar JSON
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    caminho_saida = os.path.join(PASTA_SAIDA, ARQUIVO_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)

    print(f"✅ Extração científica concluída e salva em {caminho_saida}")

    # Salvar no MongoDB
    client = MongoClient(MONGO_URI)
    db = client[BANCO_MONGO]
    colecao = db[COLECAO_MONGO]
    colecao.delete_many({})  # Limpar antes
    colecao.insert_many(resultados)
    client.close()

    print(f"✅ Coleção MongoDB '{COLECAO_MONGO}' atualizada com sucesso.")

if __name__ == "__main__":
    extrair_medias_oficiais()

