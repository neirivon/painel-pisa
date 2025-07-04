
# painel_pisa/utils/avaliador_ia.py — Versão final (sem FAISS), compatível com rubrica SINAPSE v6a corrigida

import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# === Caminho para a rubrica corrigida ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RUBRICA_PATH = os.path.join(BASE_DIR, "PISA", "dados_processados", "rubricas", "rubrica_sinapse_v6a_corrigida.json")

# === Carrega rubrica corrigida ===
with open(RUBRICA_PATH, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# Organiza por dimensão
rubricas_por_dimensao = {}
for item in rubrica:
    dim = item["dimensao"]
    rubricas_por_dimensao.setdefault(dim, []).append(item)

# Modelo de Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# === Função principal ===
def avaliar_resposta_sinapse(resposta_usuario: str, rubrica=rubricas_por_dimensao, modo="local", area_fornecida=None):
    resposta = resposta_usuario.strip()
    if not resposta:
        return {}, 0.0, {
            "classificacao": "Incompleto",
            "sugestao": "Tente escrever pelo menos um parágrafo com sua ideia inicial.",
            "feedback_por_dimensao": {}
        }

    emb_resposta = model.encode([resposta])[0]

    avaliacao = {}
    total = 0

    for dimensao, niveis in rubrica.items():
        melhor_nivel = None
        melhor_sim = -1
        for nivel in niveis:
            emb_descritor = model.encode([nivel["descricao"]])[0]
            sim = cosine_similarity([emb_resposta], [emb_descritor])[0][0]
            if sim > melhor_sim:
                melhor_sim = sim
                melhor_nivel = {
                    "nivel": nivel["nivel"],
                    "titulo": nivel["titulo"],
                    "descricao": nivel["descricao"],
                    "similaridade": round(float(sim), 3)
                }
        avaliacao[dimensao] = melhor_nivel
        total += melhor_nivel["nivel"]

    media = round(total / len(rubrica), 2)

    if media < 2:
        classificacao = "Inicial"
        sugestao = "Explore mais ideias e organize melhor sua resposta."
    elif media < 3.5:
        classificacao = "Intermediário"
        sugestao = "Você pode aprofundar com argumentos, exemplos e conexões."
    else:
        classificacao = "Avançado"
        sugestao = "Resposta bem desenvolvida. Continue nesse ritmo!"

    return avaliacao, media, {
        "classificacao": classificacao,
        "sugestao": sugestao,
        "feedback_por_dimensao": avaliacao
    }
