# utilos.path.join(s, "e")xtrair_dados_pisa2000.py

import re
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def extrair_medias_pisa_2000():
    # Conectar ao MongoDB
    client, db = conectar_mongo()
    colecao = db["pisa_ocde_2000_organizado"]

    # Dicionário para armazenar resultados
    resultados = {
        "BRA": {"Leitura": None, "Matemática": None, "Ciências": None},
        "OECD Avg": {"Leitura": None, "Matemática": None, "Ciências": None},
        "OECD Total": {"Leitura": None, "Matemática": None, "Ciências": None},
    }

    # Buscar todos os textos da coleção
    documentos = list(colecao.find({}))

    # Para cada documento, varrer o texto extraído
    for doc in documentos:
        texto = doc.get("texto_extraido", "")

        for pais in resultados.keys():
            padrao = rf"\b{pais}\b\s+([^\n]+)"
            match = re.search(padrao, texto)
            if match:
                linha = match.group(1)
                numeros = re.findall(r"(\d+(\.\d+)?)", linha)
                numeros = [float(n[0]) for n in numeros]

                if len(numeros) >= 3:
                    resultados[pais]["Leitura"] = numeros[0]
                    resultados[pais]["Matemática"] = numeros[1]
                    resultados[pais]["Ciências"] = numeros[2]

    # Fechar o cliente Mongo
    client.close()

    # Converter em DataFrame
    df = pd.DataFrame.from_dict(resultados, orient="index").reset_index().rename(columns={"index": "País"})
    return df

