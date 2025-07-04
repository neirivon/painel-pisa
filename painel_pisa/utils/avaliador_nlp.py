# painel_pisos.path.join(a, "u")tilos.path.join(s, "a")valiador_nlp.py

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import os

# =============================
# Inicialização (modo lazy)
# =============================
_model = None
_tokenizer = None

# Rubrica com níveis (exemplo pedagógico adaptado)
RUBRICA_SINAPSE_NIVEIS = {
    0: "Resposta ausente ou irrelevante.",
    1: "Resposta superficial, sem conexão clara com o tema.",
    2: "Resposta básica, mas demonstra compreensão inicial.",
    3: "Resposta desenvolvida com análise e contextualização.",
    4: "Resposta excelente com pensamento crítico e profundidade."
}

# =============================
# Carregar modelo apenas uma vez
# =============================
def carregar_modelo():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        modelo_id = "distilbert-base-uncased"
        _tokenizer = AutoTokenizer.from_pretrained(modelo_id)
        _model = AutoModelForSequenceClassification.from_pretrained(modelo_id, num_labels=5)
        _model.eval()

# =============================
# Avaliar resposta com DistilBERT (simulado por logits)
# =============================
def avaliar_resposta_nlp(resposta: str):
    carregar_modelo()

    if not resposta.strip():
        return 0, RUBRICA_SINAPSE_NIVEIS[0]

    inputs = _tokenizer(resposta, return_tensors="pt", truncation=True, padding=True, max_length=256)

    with torch.no_grad():
        outputs = _model(**inputs)
        logits = outputs.logits
        probas = torch.nn.functional.softmax(logits, dim=1).numpy()
        nota = int(np.argmax(probas))

    feedback = RUBRICA_SINAPSE_NIVEIS.get(nota, "Erro ao gerar feedback.")
    return nota, feedback

