import json
import csv
import os
from datetime import datetime
from pymongo import MongoClient

CAMINHO_JSON_ENTRADA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_lingua_portuguesa.json"
CAMINHO_JSON_SAIDA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_lingua_portuguesa_v1.json"
CAMINHO_CSV_SAIDA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_lingua_portuguesa_v1.csv"
COLECAO_MONGO = "rubricas.sinapse_9ano_lingua_portuguesa"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"

# Heurísticas pedagógicas
def inferir_taxonomia_bloom(texto):
    texto = texto.lower()
    if any(v in texto for v in ["reconhecer", "compreender", "identificar"]):
        return "Compreensão"
    if any(v in texto for v in ["usar", "resolver", "aplicar", "produzir", "organizar"]):
        return "Aplicação"
    if any(v in texto for v in ["analisar", "distinguir", "comparar", "avaliar"]):
        return "Análise"
    return "Outro"

def inferir_metodologia(texto):
    if "problema" in texto or "resolver" in texto:
        return "Problematização"
    if "produzir" in texto or "criar" in texto:
        return "Aprendizagem baseada em projetos"
    if "jogo" in texto or "lúdico" in texto:
        return "Gamificação"
    return "Leitura Orientada"

def inferir_perfil_neuropsicopedagogico(texto):
    if "texto" in texto and "opinião" in texto:
        return "Expressividade verbal e argumentativa"
    if "visual" in texto or "imagem" in texto:
        return "Apoio visual no processo cognitivo"
    if "refletir" in texto or "interpretação" in texto:
        return "Leitor crítico e inferencial"
    return "Compreensão leitora com suporte metacognitivo"

def inferir_taxonomia_solo(texto):
    if texto.count(".") <= 1:
        return "Uniestrutural"
    elif texto.count(".") == 2:
        return "Multiestrutural"
    else:
        return "Relacional"

# Carregando as habilidades
with open(CAMINHO_JSON_ENTRADA, "r", encoding="utf-8") as f:
    habilidades = json.load(f)

rubricas_sinapse = []
for item in habilidades:
    habilidade = item["habilidade"]
    rubrica = {
        "codigo": item.get("codigo"),
        "habilidade": habilidade,
        "taxonomia_bloom": inferir_taxonomia_bloom(habilidade),
        "metodologia_sugerida": inferir_metodologia(habilidade),
        "perfil_neuropsicopedagogico": inferir_perfil_neuropsicopedagogico(habilidade),
        "taxonomia_solo": inferir_taxonomia_solo(habilidade),
        "timestamp_versao": datetime.utcnow().isoformat(),
        "versao": "v1"
    }
    rubricas_sinapse.append(rubrica)

# Salvando como JSON
os.makedirs(os.path.dirname(CAMINHO_JSON_SAIDA), exist_ok=True)
with open(CAMINHO_JSON_SAIDA, "w", encoding="utf-8") as jf:
    json.dump(rubricas_sinapse, jf, ensure_ascii=False, indent=2)

# Salvando como CSV
with open(CAMINHO_CSV_SAIDA, "w", encoding="utf-8", newline="") as cf:
    writer = csv.DictWriter(cf, fieldnames=rubricas_sinapse[0].keys())
    writer.writeheader()
    writer.writerows(rubricas_sinapse)

# Inserindo no MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database("rubricas")
colecao = db.get_collection("sinapse_9ano_lingua_portuguesa")
colecao.delete_many({})
colecao.insert_many(rubricas_sinapse)
client.close()

print("✅ Rubrica SINAPSE enriquecida gerada e armazenada com sucesso.")
print(f"📄 JSON: {CAMINHO_JSON_SAIDA}")
print(f"📄 CSV:  {CAMINHO_CSV_SAIDA}")
print(f"🌐 MongoDB: {COLECAO_MONGO}")

