# scriptos.path.join(s, "g")erar_rubrica_sinapse_9ano_ciencias_v1.py

import json
import csv
from datetime import datetime
from pymongo import MongoClient
import os

CAMINHO_JSON_ENTRADA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_ciencias.json"
CAMINHO_JSON_SAIDA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_ciencias_v1.json"
CAMINHO_CSV_SAIDA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_ciencias_v1.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "rubricas"
COLLECTION_NAME = "sinapse_9ano_ciencias"

def heuristicas_enriquecimento(habilidade):
    texto = habilidade["habilidade"].lower()
    verbos_bloom = {
        "compreender": "Compreensão",
        "reconhecer": "Compreensão",
        "identificar": "Compreensão",
        "relacionar": "Análise",
        "analisar": "Análise",
        "resolver": "Aplicação",
        "usar": "Aplicação",
        "aplicar": "Aplicação",
        "comparar": "Análise",
        "formular": "Síntese",
        "avaliar": "Avaliação",
        "demonstrar": "Aplicação"
    }

    metodologias = []
    if "problema" in texto or "resolver" in texto:
        metodologias.append("Problematização")
    if "experimento" in texto or "prática" in texto:
        metodologias.append("Aprendizagem baseada em projetos")
    if "jogo" in texto or "simulação" in texto:
        metodologias.append("Gamificação")

    if not metodologias:
        metodologias.append("Aula expositiva dialógica")

    perfil = "Raciocínio lógico e inferência científica"
    if "experimento" in texto:
        perfil = "Investigação empírica com mediação visual"
    elif "texto" in texto:
        perfil = "Leitura interpretativa com ênfase em linguagem científica"

    tax_bloom = next((v for k, v in verbos_bloom.items() if k in texto), "Conhecimento")

    if any(w in texto for w in ["relacionar", "comparar", "articular"]):
        tax_solo = "Relacional"
    elif any(w in texto for w in ["dois", "vários", "diversos"]):
        tax_solo = "Multiestrutural"
    else:
        tax_solo = "Uniestrutural"

    return {
        "taxonomia_bloom": tax_bloom,
        "metodologia_sugerida": metodologias[0],
        "perfil_neuropsicopedagogico": perfil,
        "taxonomia_solo": tax_solo
    }

def main():
    with open(CAMINHO_JSON_ENTRADA, "r", encoding="utf-8") as f:
        habilidades = json.load(f)

    enriquecidas = []
    for hab in habilidades:
        enriquecida = {**hab, **heuristicas_enriquecimento(hab)}
        enriquecida["fonte"] = "BNCC"
        enriquecida["disciplina"] = "Ciências"
        enriquecida["ano"] = "9º ano"
        enriquecida["timestamp_versao"] = datetime.utcnow().isoformat()
        enriquecidas.append(enriquecida)

    os.makedirs(os.path.dirname(CAMINHO_JSON_SAIDA), exist_ok=True)

    with open(CAMINHO_JSON_SAIDA, "w", encoding="utf-8") as jf:
        json.dump(enriquecidas, jf, ensure_ascii=False, indent=2)

    with open(CAMINHO_CSV_SAIDA, "w", encoding="utf-8", newline="") as cf:
        writer = csv.DictWriter(cf, fieldnames=enriquecidas[0].keys())
        writer.writeheader()
        writer.writerows(enriquecidas)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    collection.delete_many({})
    collection.insert_many(enriquecidas)
    client.close()

    print("✅ Rubrica SINAPSE enriquecida gerada e armazenada com sucesso.")
    print(f"📄 JSON: {CAMINHO_JSON_SAIDA}")
    print(f"📄 CSV:  {CAMINHO_CSV_SAIDA}")
    print(f"🌐 MongoDB: {DB_NAME}.{COLLECTION_NAME}")

if __name__ == "__main__":
    main()

