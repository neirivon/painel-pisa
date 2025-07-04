# utilos.path.join(s, "e")xtrair_medias_oficiais_pisa2000_v2.py

import os
import pandas as pd
import json
from pymongo import MongoClient

# Diretórios dos arquivos
PASTA_SPSS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSS"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"

# Arquivos SPSS TXT
ARQUIVOS = {
    "leitura": "PISA2000_SPSS_student_reading.txt",
    "matematica": "PISA2000_SPSS_student_mathematics.txt",
    "ciencias": "PISA2000_SPSS_student_science.txt"
}

# Configuração MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
MONGO_DB = "pisa"

# Códigos dos países da OCDE em 2000
OCDE_2000_CODIGOS = {"036","040","056","124","203","208","246","250","276","300",
                     "348","352","372","380","392","410","428","438","442","484",
                     "528","554","578","616","620","643","724","752","756","826","840"}

# Função para ler cada arquivo SPSS TXT
def ler_spss_txt(caminho):
    df = pd.read_csv(caminho, delimiter="\t", encoding="latin1", dtype=str)
    return df

# Função para calcular as médias ponderadas por país
def calcular_media_ponderada(df, area):
    resultados = []

    # Detectar campos corretos
    col_country = None
    col_weight = None
    pv_fields = []

    for coluna in df.columns:
        if coluna.lower() == "country":
            col_country = coluna
        elif coluna.lower() == "cnt":
            col_country = coluna
        elif coluna.lower() == "w_fstuwt":
            col_weight = coluna
        elif coluna.lower().startswith("pv1") or coluna.lower().startswith("pv2") or coluna.lower().startswith("pv3") or coluna.lower().startswith("pv4") or coluna.lower().startswith("pv5"):
            pv_fields.append(coluna)

    if not col_country or not col_weight or len(pv_fields) < 5:
        raise Exception(f"Erro: Arquivo {area} não contém campos esperados.")

    # Converter plausível values e pesos para float
    for col in pv_fields:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col_weight] = pd.to_numeric(df[col_weight], errors="coerce")

    # Grupo por país
    for pais, dados in df.groupby(col_country):
        medias_pv = []
        for pv in pv_fields:
            soma_peso = dados[col_weight].sum()
            if soma_peso > 0:
                media = (dados[pv] * dados[col_weight]).sum()os.path.join( , " ")soma_peso
                medias_pv.append(media)

        if medias_pv:
            media_final = sum(medias_pv)os.path.join( , " ")len(medias_pv)
            resultados.append({
                "pais": pais,
                "media": round(media_final, 2),
                "area": area,
                "origem": "SPSS PISA 2000"
            })

    return resultados

# Função principal de extração
def extrair_medias_oficiais():
    print("\U0001F50D Iniciando extração científica...")

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    # Para cada área (leitura, matemática, ciências)
    for area, arquivo in ARQUIVOS.items():
        print(f"\U0001F4C3 Analisando {area.title()} ({arquivo})...")

        caminho = os.path.join(PASTA_SPSS, arquivo)
        df = ler_spss_txt(caminho)
        resultados = calcular_media_ponderada(df, area)

        # Separar OCDE e Total
        resultados_ocde = [r for r in resultados if r["pais"] in OCDE_2000_CODIGOS]
        resultados_total = resultados

        # Inserir no MongoDB
        colecao_ocde = f"pisa2000_medias_{area}_ocde"
        colecao_total = f"pisa2000_medias_{area}_total"

        db[colecao_ocde].drop()
        db[colecao_total].drop()

        db[colecao_ocde].insert_many(resultados_ocde)
        db[colecao_total].insert_many(resultados_total)

        # Salvar como JSON
        pasta_saida_area = os.path.join(PASTA_SAIDA)
        if not os.path.exists(pasta_saida_area):
            os.makedirs(pasta_saida_area)

        with open(os.path.join(pasta_saida_area, f"pisa2000_medias_{area}_ocde.json"), "w", encoding="utf-8") as f:
            json.dump(resultados_ocde, f, ensure_ascii=False, indent=4)

        with open(os.path.join(pasta_saida_area, f"pisa2000_medias_{area}_total.json"), "w", encoding="utf-8") as f:
            json.dump(resultados_total, f, ensure_ascii=False, indent=4)

        print(f"\U0001F3C6 Extração concluída para {area.title()}. {len(resultados)} registros.")

    client.close()
    print("\U0001F389 Todas áreas processadas com sucesso!")

if __name__ == "__main__":
    extrair_medias_oficiais()

