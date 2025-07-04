# scriptos.path.join(s, "g")erar_questoes_pisa_ordenadas.py

import pandas as pd
import json
import os
from datetime import datetime

try:
    print("🔄 Iniciando geração das questões ordenadas por área...")

    pasta_entrada = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "d")ados_processadoos.path.join(s, "q")uestoes/"))
    pasta_saida = pasta_entrada  # mesma pasta de entrada e saída
    os.makedirs(pasta_saida, exist_ok=True)

    arquivo_origem = os.path.join(pasta_entrada, "questoes_pisa_tri_mineiro_completas.json")
    with open(arquivo_origem, "r", encoding="utf-8") as f:
        questoes = json.load(f)

    # Ordenar manualmente por área
    ordem_area = ["Leitura", "Matemática", "Ciências"]
    questoes_ordenadas = sorted(questoes, key=lambda x: ordem_area.index(x["area"]))

    lista_planificada = []
    for q in questoes_ordenadas:
        lista_planificada.append({
            "Área": q["area"],
            "Questão ID": q["questao_id"],
            "Pergunta": q["pergunta"],
            "Resposta Modelo": q["resposta_modelo"],
            "Resposta Mediana": q["resposta_mediana"],
            "Resposta Inadequada": q["resposta_inadequada"],
            "Dimensões": ", ".join(q["dimensoes_avaliadas"])
        })

    df = pd.DataFrame(lista_planificada)

    nome_base = "questoes_pisa_ordenadas"
    caminho_json = os.path.join(pasta_saida, f"{nome_base}.json")
    caminho_csv = os.path.join(pasta_saida, f"{nome_base}.csv")

    with open(caminho_json, "w", encoding="utf-8") as jf:
        json.dump(lista_planificada, jf, indent=2, ensure_ascii=False)
    df.to_csv(caminho_csv, index=False)

    print("✅ Arquivos gerados com sucesso!")
    print(f"📄 CSV: {caminho_csv}")
    print(f"🧾 JSON: {caminho_json}")

except Exception as e:
    print("❌ Ocorreu um erro ao gerar os arquivos ordenados:")
    print(e)

