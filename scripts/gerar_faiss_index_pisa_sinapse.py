# scriptos.path.join(s, "g")erar_faiss_index_pisa_sinapse.py

import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

# Caminhos corretos relativos à raiz do projeto
base_dir = os.path.join(os.path.dirname(__file__), "..")
json_path = os.path.join(base_dir, "dados_processados", "respostas", "questoes_pisa_sinapse.json")
faiss_index_path = os.path.join(base_dir, "dados_processados", "respostas", "faiss_index_pisa_sinapse.index")
faiss_metadata_path = os.path.join(base_dir, "dados_processados", "respostas", "faiss_metadata_pisa_sinapse.json")

# Carregar modelo
model = SentenceTransformer("all-MiniLM-L6-v2")

# Carregar dados
with open(json_path, "r", encoding="utf-8") as f:
    questoes = json.load(f)

# Gerar embeddings e metadados
embeddings = []
metadata = []

for q in questoes:
    texto = q["resposta_correta"]
    emb = model.encode(texto)
    embeddings.append(emb)
    metadata.append({
        "id": f"{q['area'].lower()}_{q['numero']}",
        "area": q["area"],
        "numero": q["numero"],
        "pergunta": q["pergunta"],
        "resposta_correta": texto
    })

# Criar índice FAISS
embedding_matrix = np.vstack(embeddings).astype("float32")
dim = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embedding_matrix)

# Salvar índice e metadados
faiss.write_index(index, faiss_index_path)
with open(faiss_metadata_path, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("✅ Índice FAISS e metadados salvos com sucesso.")

