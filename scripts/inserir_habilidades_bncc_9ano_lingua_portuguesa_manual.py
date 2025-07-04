#os.path.join(!, "u")sos.path.join(r, "b")ios.path.join(n, "e")nv python3
# scriptos.path.join(s, "i")nserir_habilidades_bncc_9ano_lingua_portuguesa_manual.py

import os
import json
import csv
from datetime import datetime
from pymongo import MongoClient

# — CONFIGURAÇÕES — #
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "rubricas"
COLLECTION = "sinapse_9ano_lingua_portuguesa"

OUTPUT_JSON = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_lingua_portuguesa.json"
OUTPUT_CSV  = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "h")abilidades_bncc_9ano_lingua_portuguesa.csv"

# — LISTA DE HABILIDADES (24 itens) — #
habilidades_lp = [
    {"codigo": "EF09LP01", "habilidade": "Analisar o fenômeno da desinformação em diferentes mídias."},
    {"codigo": "EF09LP02", "habilidade": "Analisar e comentar a cobertura jornalística em diferentes mídias."},
    {"codigo": "EF09LP03", "habilidade": "Produzir artigos de opinião com base em argumentos consistentes."},
    {"codigo": "EF09LP04", "habilidade": "Escrever textos respeitando normas gramaticais e de pontuação."},
    {"codigo": "EF09LP05", "habilidade": "Identificar complementos e modificadores em frases e textos."},
    {"codigo": "EF09LP06", "habilidade": "Diferenciar e aplicar regência verbal corretamente."},
    {"codigo": "EF09LP07", "habilidade": "Comparar usos de voz ativa e passiva em diferentes contextos."},
    {"codigo": "EF09LP08", "habilidade": "Identificar e empregar conectores em produções textuais."},
    {"codigo": "EF09LP09", "habilidade": "Analisar elementos linguísticos e notacionais da escrita."},
    {"codigo": "EF09LP10", "habilidade": "Comparar regras de colocação pronominal e seus efeitos."},
    {"codigo": "EF09LP11", "habilidade": "Inferir efeitos de sentido a partir de recursos linguísticos."},
    {"codigo": "EF09LP12", "habilidade": "Reconhecer e refletir sobre a variação linguística e estrangeirismos."},
    {"codigo": "EF09LP13", "habilidade": "Interpretar metáforas, ironias e outras figuras de linguagem."},
    {"codigo": "EF09LP14", "habilidade": "Planejar e revisar textos com base em critérios discursivos."},
    {"codigo": "EF09LP15", "habilidade": "Identificar o ponto de vista em diferentes gêneros opinativos."},
    {"codigo": "EF09LP16", "habilidade": "Analisar intertextualidade em gêneros literários e não literários."},
    {"codigo": "EF09LP17", "habilidade": "Reescrever textos de forma coesa e coerente."},
    {"codigo": "EF09LP18", "habilidade": "Ler criticamente campanhas publicitárias e propagandas."},
    {"codigo": "EF09LP19", "habilidade": "Avaliar o uso de imagens e textos em gêneros multimodais."},
    {"codigo": "EF09LP20", "habilidade": "Analisar textos narrativos considerando enredo e narrador."},
    {"codigo": "EF09LP21", "habilidade": "Interpretar poemas e identificar recursos poéticos."},
    {"codigo": "EF09LP22", "habilidade": "Identificar relações lógicas em textos dissertativo-argumentativos."},
    {"codigo": "EF09LP23", "habilidade": "Compreender o papel da linguagem na construção da realidade social."},
    {"codigo": "EF09LP24", "habilidade": "Elaborar textos autorais a partir de temas da realidade social."},
]

# adiciona campos fixos a cada documento
for doc in habilidades_lp:
    doc.update({
        "area": "Linguagens",
        "componente": "Língua Portuguesa",
        "timestamp_extracao": datetime.utcnow()
    })

# — GARANTE QUE A PASTA EXISTA — #
os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

# — SALVA JSON — #
with open(OUTPUT_JSON, "w", encoding="utf-8") as jf:
    # converter datetime para ISO string
    for d in habilidades_lp:
        d["timestamp_extracao"] = d["timestamp_extracao"].isoformat() + "Z"
    json.dump(habilidades_lp, jf, ensure_ascii=False, indent=2)

# — SALVA CSV — #
with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as cf:
    writer = csv.DictWriter(cf, fieldnames=list(habilidades_lp[0].keys()))
    writer.writeheader()
    writer.writerows(habilidades_lp)

# — INSERE NO MONGO — #
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
col = db[COLLECTION]
# limpa antes de inserir
col.delete_many({})
res = col.insert_many(habilidades_lp)
print(f"🌐 Inseridos {len(res.inserted_ids)} documentos em '{DB_NAME}.{COLLECTION}'.")
client.close()

