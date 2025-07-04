import json
import os
import pandas as pd
import warnings
import tempfile
from sentence_transformers import SentenceTransformer, util

# Silenciar warnings de limpeza automática de diretórios temporários
warnings.filterwarnings("ignore", category=ResourceWarning, module=tempfile.__name__)

# Caminho local do JSON da rubrica
CAMINHO_RUBRICA = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapase_ia_v4.json"
CAMINHO_SAIDA = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/analise_formatividade_somatividade.json"

# Embeddings leves compatíveis com Streamlit Cloud
modelo = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Vetores de referência
base_formatividade = "Aprendizagem contínua, feedback, reflexão, desenvolvimento pessoal, acompanhamento do progresso, autoavaliação"
base_somatividade = "Resultado final, nota, certificação, desempenho, exame padronizado, avaliação externa, produto final"

emb_form = modelo.encode(base_formatividade, convert_to_tensor=True)
emb_soma = modelo.encode(base_somatividade, convert_to_tensor=True)

# Função de classificação
def classificar_descritor(texto):
    emb = modelo.encode(texto, convert_to_tensor=True)
    sim_form = float(util.cos_sim(emb, emb_form))
    sim_soma = float(util.cos_sim(emb, emb_soma))
    tipo = "formativo" if sim_form > sim_soma else "somativo"
    if abs(sim_form - sim_soma) < 0.08:
        tipo = "híbrido"
    return tipo, round(sim_form, 3), round(sim_soma, 3)

# Processamento da rubrica
with open(CAMINHO_RUBRICA, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

resultados = []

for dim in rubrica["dimensoes"]:
    for nivel in dim.get("niveis", []):
        classificacao, score_form, score_soma = classificar_descritor(nivel["descricao"])
        resultados.append({
            "dimensao": dim["dimensao"],
            "nivel": nivel["nome"],
            "descricao": nivel["descricao"],
            "classificacao": classificacao,
            "similaridade_formatividade": score_form,
            "similaridade_somatividade": score_soma
        })

# Salvar resultado JSON
with open(CAMINHO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print(f"✅ Análise concluída! Resultado salvo em: {CAMINHO_SAIDA}")

