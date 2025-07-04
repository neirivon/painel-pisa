from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# utilos.path.join(s, "e")xtrair_medias_oficiais_pisa2000.py

import os
import pandas as pd
import json
from pymongo import MongoClient

# Pasta dos arquivos SPSS convertidos
PASTA_SPSS = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "S")PSS"

# Arquivos
ARQUIVOS_SPSS = {
    "matematica": "PISA2000_SPSS_student_mathematics.txt",
    "leitura": "PISA2000_SPSS_student_reading.txt",
    "ciencias": "PISA2000_SPSS_student_science.txt"
}

# Pasta de saída JSON
PASTA_SAIDA = "/homos.path.join(e, "n")eirivoos.path.join(n, "S")INAPSE2.os.path.join(0, "P")ISos.path.join(A, "o")cdos.path.join(e, "2")00os.path.join(0, "e")xtracoes"
ARQUIVO_SAIDA = "pisa2000_medias_oficiais.json"

# Países OCDE 2000 (códigos numéricos SPSS)
Paises_OCDE_CODIGOS = [
    36, 40, 56, 124, 203, 208, 246, 250, 276, 300, 348, 352,
    372, 380, 392, 410, 428, 438, 442, 484, 528, 554, 578,
    616, 620, 643, 724, 752, 756, 826, 840
]

# Mapeamento código numérico → sigla
codigo_to_sigla = {
    36: "AUS", 40: "AUT", 56: "BEL", 76: "BRA", 124: "CAN",
    203: "CZE", 208: "DNK", 246: "FIN", 250: "FRA", 276: "DEU",
    300: "GRC", 348: "HUN", 352: "ISL", 372: "IRL", 380: "ITA",
    392: "JPN", 410: "KOR", 428: "LVA", 438: "LIE", 442: "LUX",
    484: "MEX", 528: "NLD", 554: "NZL", 578: "NOR", 616: "POL",
    620: "PRT", 643: "RUS", 724: "ESP", 752: "SWE", 756: "CHE",
    826: "GBR", 840: "USA"
}

def conectar_mongo():
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["pisa"]
    return client, db

def carregar_dados(caminho):
    # Detecta separador (tabulação)
    return pd.read_csv(caminho, sep="\t", low_memory=False)

def extrair_medias_oficiais():
    print("🔎 Iniciando extração científica...")
    
    # Carregar dados
    df_mate = carregar_dados(os.path.join(PASTA_SPSS, ARQUIVOS_SPSS["matematica"]))
    df_read = carregar_dados(os.path.join(PASTA_SPSS, ARQUIVOS_SPSS["leitura"]))
    df_scie = carregar_dados(os.path.join(PASTA_SPSS, ARQUIVOS_SPSS["ciencias"]))

    # Confirmar variáveis
    if "country" not in df_mate.columns or "pv1math" not in df_mate.columns:
        raise Exception("Erro: Campos esperados não encontrados em Matemática.")
    if "country" not in df_read.columns or "pv1read" not in df_read.columns:
        raise Exception("Erro: Campos esperados não encontrados em Leitura.")
    if "country" not in df_scie.columns or "pv1scie" not in df_scie.columns:
        raise Exception("Erro: Campos esperados não encontrados em Ciências.")

    resultados = []

    # Lista de todos países encontrados
    codigos_presentes = sorted(set(df_mate["country"].dropna().astype(int)))

    for codigo in codigos_presentes:
        sigla = codigo_to_sigla.get(codigo, None)
        if sigla is None:
            continue  # Ignorar países fora da lista
        
        alunos_mate = df_mate[df_mate["country"] == codigo]
        alunos_read = df_read[df_read["country"] == codigo]
        alunos_scie = df_scie[df_scie["country"] == codigo]

        media_mate = alunos_mate[[f"pv{i}math" for i in range(1, 6)]].mean(axis=1).mean()
        media_read = alunos_read[[f"pv{i}read" for i in range(1, 6)]].mean(axis=1).mean()
        media_scie = alunos_scie[[f"pv{i}scie" for i in range(1, 6)]].mean(axis=1).mean()

        resultado = {
            "pais": sigla,
            "leitura": round(media_read, 1),
            "matematica": round(media_mate, 1),
            "ciencias": round(media_scie, 1),
            "ano": 2000,
            "origem": "extração_spss"
        }
        resultados.append(resultado)
        print(f"✅ {sigla} extraído: L={resultado['leitura']}, M={resultado['matematica']}, C={resultado['ciencias']}")

    # Cálculo OECD Avg (média dos 28 países OCDE)
    df_ocde = pd.DataFrame([r for r in resultados if r["pais"] in codigo_to_sigla.values()])
    oecd_avg = {
        "pais": "OECD Avg",
        "leitura": round(df_ocde["leitura"].mean(), 1),
        "matematica": round(df_ocde["matematica"].mean(), 1),
        "ciencias": round(df_ocde["ciencias"].mean(), 1),
        "ano": 2000,
        "origem": "extração_spss"
    }
    resultados.append(oecd_avg)
    print(f"🏁 OECD Avg calculado: {oecd_avg}")

    # Salvar JSON
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)

    caminho_saida = os.path.join(PASTA_SAIDA, ARQUIVO_SAIDA)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=4)
    
    print(f"💾 JSON salvo em {caminho_saida}")

    # Salvar no MongoDB
    client, db = conectar_mongo()
    db["pisa2000_medias_oficiais"].drop()
    db["pisa2000_medias_oficiais"].insert_many(resultados)
    client.close()

    print(f"✅ Todos os dados salvos na coleção pisa2000_medias_oficiais.")

if __name__ == "__main__":
    extrair_medias_oficiais()

