# scriptos.path.join(s, "g")erar_rubrica_sinapse_9ano_matematica_v1.py

import json
import csv
from datetime import datetime
from pymongo import MongoClient

# === CONFIGURAÇÕES ===
CAMINHO_JSON_ORIGEM = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_matematica.json"
CAMINHO_JSON_DESTINO = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_matematica_v1.json"
CAMINHO_CSV_DESTINO = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_matematica_v1.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "rubricas"
COLLECTION_NAME = "sinapse_9ano_matematica"

# === HEURÍSTICAS PEDAGÓGICAS ===
def inferir_taxonomia_bloom(texto):
    if any(v in texto.lower() for v in ["compreender", "reconhecer", "identificar"]):
        return "Compreensão"
    elif any(v in texto.lower() for v in ["resolver", "aplicar", "usar", "utilizar", "elaborar"]):
        return "Aplicação"
    elif any(v in texto.lower() for v in ["analisar", "relacionar", "comparar", "diferenciar"]):
        return "Análise"
    else:
        return "Conhecimento"

def inferir_metodologia(texto):
    if "problema" in texto.lower():
        return "Problematização"
    elif any(k in texto.lower() for k in ["tecnologia", "software", "plano cartesiano", "fluxograma"]):
        return "Gamificação e projetos"
    else:
        return "Aprendizagem baseada em competências"

def inferir_perfil_neuro(texto):
    if "visual" in texto.lower() or "representação" in texto.lower():
        return "Visual e espacial"
    elif "raciocínio" in texto.lower() or "lógico" in texto.lower():
        return "Raciocínio lógico"
    elif "texto" in texto.lower():
        return "Verbal linguístico"
    else:
        return "Misto com suporte instrucional"

def inferir_taxonomia_solo(texto):
    if texto.count(" e ") >= 2 and "relaç" in texto.lower():
        return "Relacional"
    elif texto.count(" e ") >= 1:
        return "Multiestrutural"
    else:
        return "Uniestrutural"

def inferir_dua(texto):
    if any(k in texto.lower() for k in ["representação", "acessível", "inclusivo"]):
        return "Engajamento e Representação Múltipla"
    elif any(k in texto.lower() for k in ["autonomia", "planejar", "ajustar"]):
        return "Ação e Expressão"
    else:
        return "Percepção e Compreensão"

# === PROCESSAMENTO ===
with open(CAMINHO_JSON_ORIGEM, "r", encoding="utf-8") as f:
    habilidades = json.load(f)

rubrica_sinapse = []
agora = datetime.utcnow().isoformat()

for item in habilidades:
    habilidade_texto = item["habilidade"]

    rubrica = {
        "codigo": item["codigo"],
        "habilidade": habilidade_texto,
        "taxonomia_bloom": inferir_taxonomia_bloom(habilidade_texto),
        "metodologia_sugerida": inferir_metodologia(habilidade_texto),
        "perfil_neuropsicopedagogico": inferir_perfil_neuro(habilidade_texto),
        "taxonomia_solo": inferir_taxonomia_solo(habilidade_texto),
        "dua": inferir_dua(habilidade_texto),
        "versao": "v1",
        "etapa": item["etapa"],
        "ano": item["ano"],
        "area": item["area"],
        "componente": item["componente"],
        "timestamp_geracao": agora
    }

    rubrica_sinapse.append(rubrica)

# === SALVAR JSON ===
with open(CAMINHO_JSON_DESTINO, "w", encoding="utf-8") as jf:
    json.dump(rubrica_sinapse, jf, ensure_ascii=False, indent=2)

# === SALVAR CSV ===
with open(CAMINHO_CSV_DESTINO, "w", newline="", encoding="utf-8") as cf:
    writer = csv.DictWriter(cf, fieldnames=rubrica_sinapse[0].keys())
    writer.writeheader()
    writer.writerows(rubrica_sinapse)

# === INSERIR NO MONGODB ===
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]
collection.insert_many(rubrica_sinapse)
client.close()

print("✅ Rubrica SINAPSE enriquecida gerada e armazenada com sucesso.")
print(f"📄 JSON: {CAMINHO_JSON_DESTINO}")
print(f"📄 CSV:  {CAMINHO_CSV_DESTINO}")
print(f"🌐 MongoDB: {DB_NAME}.{COLLECTION_NAME}")

