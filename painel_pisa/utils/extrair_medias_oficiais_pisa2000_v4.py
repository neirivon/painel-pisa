# utilos.path.join(s, "e")xtrair_medias_oficiais_pisa2000_v4.py

import os
import pandas as pd
import json
from pymongo import MongoClient

# Caminhos
PASTA_SPSS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSS"
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_SAIDA = "pisa2000_student_medias_oficiais_v4.json"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
MONGO_DB = "pisa"
MONGO_COLECAO = "pisa2000_medias_oficiais"

# Mapeamento de arquivos
ARQUIVOS_AREA = {
    "leitura": "PISA2000_SPSS_student_reading.txt",
    "matematica": "PISA2000_SPSS_student_mathematics.txt",
    "ciencias": "PISA2000_SPSS_student_science.txt",
}

# Função para carregar SPSS bruto ignorando estrutura errada
def carregar_spss_bruto(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="latin1") as f:
        linhas = f.readlines()

    registros = []
    for linha in linhas:
        partes = linha.strip().split()
        if len(partes) > 5:
            registros.append(partes)

    df = pd.DataFrame(registros)
    return df

# Função para calcular médias ponderadas
def calcular_media_ponderada(df, area):
    try:
        df.columns = [f"col_{i}" for i in range(len(df.columns))]

        # Mapeamento rápido baseado na posição esperada dos campos
        if area == "leitura":
            pv_coluna = "col_65"
        elif area == "matematica":
            pv_coluna = "col_65"
        elif area == "ciencias":
            pv_coluna = "col_65"
        else:
            raise Exception(f"Área desconhecida: {area}")

        peso_coluna = "col_7"  # Supondo posição 7 para peso amostral w_fstuwt
        pais_coluna = "col_0"  # Supondo país na primeira coluna

        df[pv_coluna] = pd.to_numeric(df[pv_coluna], errors="coerce")
        df[peso_coluna] = pd.to_numeric(df[peso_coluna], errors="coerce")

        resultados = []

        for pais_codigo in df[pais_coluna].unique():
            if pd.isna(pais_codigo):
                continue
            df_pais = df[df[pais_coluna] == pais_codigo]
            if df_pais.empty:
                continue

            media_ponderada = (df_pais[pv_coluna] * df_pais[peso_coluna]).sum()os.path.join( , " ")df_pais[peso_coluna].sum()

            resultados.append({
                "pais_codigo": pais_codigo,
                "area": area,
                "media_ponderada": round(media_ponderada, 2)
            })

        return resultados

    except Exception as e:
        print(f"Erro ao calcular média ponderada para área {area}: {str(e)}")
        raise

def extrair_medias_oficiais():
    print("🔍 Iniciando extração científica...")

    resultados_finais = []

    for area, arquivo in ARQUIVOS_AREA.items():
        caminho_arquivo = os.path.join(PASTA_SPSS, arquivo)
        print(f"📃 Analisando {area.capitalize()} ({arquivo})...")

        df = carregar_spss_bruto(caminho_arquivo)
        resultados = calcular_media_ponderada(df, area)
        resultados_finais.extend(resultados)

    # Salvar no JSON
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    caminho_saida = os.path.join(PASTA_SAIDA, ARQUIVO_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados_finais, f, ensure_ascii=False, indent=4)

    print(f"✅ Extração científica concluída e salva em {caminho_saida}")

    # Salvar no MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    colecao = db[MONGO_COLECAO]

    colecao.delete_many({})
    colecao.insert_many(resultados_finais)
    client.close()

    print(f"✅ Coleção MongoDB '{MONGO_COLECAO}' atualizada com sucesso.")

if __name__ == "__main__":
    extrair_medias_oficiais()

