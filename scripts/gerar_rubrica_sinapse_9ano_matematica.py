import json
import csv
from datetime import datetime
from pymongo import MongoClient
from pathlib import Path

# === Caminhos ===
CAMINHO_JSON_ENTRADA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_matematica.json"
CAMINHO_JSON_SAIDA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_matematica.json"
CAMINHO_CSV_SAIDA = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_matematica.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"

# === Heurísticas simples ===
def inferir_taxonomia_bloom(habilidade):
    habilidade = habilidade.lower()
    if any(v in habilidade for v in ["reconhecer", "compreender", "identificar"]):
        return "Compreensão"
    elif any(v in habilidade for v in ["resolver", "aplicar", "usar", "efetuar", "elaborar", "determinar"]):
        return "Aplicação"
    elif any(v in habilidade for v in ["analisar", "avaliar", "comparar", "diferenciar", "justificar"]):
        return "Análise"
    else:
        return "Conhecimento"

def inferir_metodologia(habilidade):
    if "problema" in habilidade.lower():
        return "Problematização"
    elif any(v in habilidade.lower() for v in ["tecnologia", "software", "algoritmo", "régua", "compasso", "planilha"]):
        return "Gamificação e Aprendizagem baseada em projetos"
    elif "representação gráfica" in habilidade.lower() or "gráfico" in habilidade.lower():
        return "Visualização de dados"
    else:
        return "Método tradicional com reforço digital"

def inferir_perfil_neuro(habilidade):
    if "visual" in habilidade.lower() or "gráfico" in habilidade.lower():
        return "Mediação visual com raciocínio lógico"
    elif "problema" in habilidade.lower():
        return "Pensamento lógico com desafio contextual"
    elif "escrita" in habilidade.lower() or "descrição" in habilidade.lower():
        return "Processamento verbal e linguístico"
    else:
        return "Processamento lógico-matemático"

def inferir_taxonomia_solo(habilidade):
    if habilidade.count(",") >= 2:
        return "Relacional"
    elif habilidade.count(",") == 1:
        return "Multiestrutural"
    else:
        return "Uniestrutural"

def inferir_dua(habilidade):
    if any(v in habilidade.lower() for v in ["visual", "gráfico", "figura", "representação"]):
        return "Múltiplas representações visuais"
    elif any(v in habilidade.lower() for v in ["resolução", "problema", "cotidiano"]):
        return "Engajamento com contexto real"
    elif any(v in habilidade.lower() for v in ["tecnologia", "software", "digital"]):
        return "Recursos digitais acessíveis"
    else:
        return "Flexibilidade na apresentação da informação"

# === Carregar habilidades ===
with open(CAMINHO_JSON_ENTRADA, "r", encoding="utf-8") as f:
    habilidades = json.load(f)

# === Enriquecer ===
rubricas_sinapse = []
for h in habilidades:
    h_enriquecida = {
        **h,
        "taxonomia_bloom": inferir_taxonomia_bloom(h["habilidade"]),
        "metodologia_sugerida": inferir_metodologia(h["habilidade"]),
        "perfil_neuropsicopedagogico": inferir_perfil_neuro(h["habilidade"]),
        "taxonomia_solo": inferir_taxonomia_solo(h["habilidade"]),
        "dua": inferir_dua(h["habilidade"]),
        "timestamp_anotacao": datetime.utcnow().isoformat()
    }
    rubricas_sinapse.append(h_enriquecida)

# === Salvar JSON ===
Path(CAMINHO_JSON_SAIDA).parent.mkdir(parents=True, exist_ok=True)
with open(CAMINHO_JSON_SAIDA, "w", encoding="utf-8") as f:
    json.dump(rubricas_sinapse, f, ensure_ascii=False, indent=2)

# === Salvar CSV ===
with open(CAMINHO_CSV_SAIDA, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rubricas_sinapse[0].keys())
    writer.writeheader()
    writer.writerows(rubricas_sinapse)

# === Inserir no MongoDB ===
client = MongoClient(MONGO_URI)
db = client["rubricas"]
colecao = db["sinapse_9ano_matematica"]
colecao.delete_many({})
colecao.insert_many(rubricas_sinapse)
client.close()

print("✅ Rubrica SINAPSE enriquecida gerada e armazenada com sucesso.")
print(f"📄 JSON: {CAMINHO_JSON_SAIDA}")
print(f"📄 CSV:  {CAMINHO_CSV_SAIDA}")
print(f"🌐 MongoDB: rubricas.sinapse_9ano_matematica")

