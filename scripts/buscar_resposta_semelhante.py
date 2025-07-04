# scriptos.path.join(s, "b")uscar_resposta_semelhante.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_PATH = os.path.join(BASE_DIR, ".os.path.join(., "d")ados_processadoos.path.join(s, "r")espostas")
index_path = os.path.join(DADOS_PATH, "faiss_index_pisa_sinapse.index")
metadata_path = os.path.join(DADOS_PATH, "faiss_metadata_pisa_sinapse.json")

# Carregar modelo e FAISS
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(index_path)

with open(metadata_path, "r", encoding="utf-8") as f:
    metadados = json.load(f)

# ========= 🧠 Função de busca semântica =========
def buscar_mais_proxima(resposta_aluno, top_k=1):
    emb = model.encode([resposta_aluno])
    D, I = index.search(np.array(emb).astype("float32"), top_k)

    resultados = []
    for idx in I[0]:
        resultados.append(metadados[idx])
    return resultados

# ========= 🧪 Teste =========
if __name__ == "__main__":
    resposta_aluno = input("Digite sua resposta: ").strip()

    similares = buscar_mais_proxima(resposta_aluno, top_k=3)
    print("\n🔍 Respostas mais semelhantes:\n")
    for i, r in enumerate(similares, 1):
        print(f"{i}. [{r['area']}] Pergunta {r['numero']}")
        print(f"   Pergunta: {r['pergunta']}")
        print(f"   Resposta Correta: {r['resposta_correta']}\n")

