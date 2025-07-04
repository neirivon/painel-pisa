# scripts/gerar_rubrica_sinapse_ia_v1_2_ollama_local.py

import requests
import json
from datetime import datetime
from tqdm import tqdm

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3"

dimensoes = [
    {
        "nome": "Progressão Cognitiva Educacional",
        "prompt": """
Gere uma dimensão para rubrica pedagógica chamada "Progressão Cognitiva Educacional", com 4 níveis (nota 1 a 4), cada um contendo:

- nome
- descrição
- três exemplos práticos com título e descrição

Os exemplos devem ser contextualizados com base no SAEB 2017.
Formato de saída: JSON com lista "niveis".
        """.strip()
    },
    {
        "nome": "Perfil Socioeconômico e Contextual",
        "prompt": """
Gere uma dimensão chamada "Perfil Socioeconômico e Contextual" para uma rubrica avaliativa baseada no SAEB 2017.

Cada um dos 4 níveis deve conter:
- nome
- descrição
- 3 exemplos práticos que reflitam realidades sociais do Brasil

Formato de saída: JSON com lista "niveis".
        """.strip()
    }
]

rubrica = {
    "nome": "rubrica_sinapse_ia",
    "versao": "v1.2",
    "base": "SAEB 2017",
    "modelo": "LLaMA3 8B (Ollama)",
    "timestamp": datetime.now().isoformat(),
    "dimensoes": []
}

headers = {"Content-Type": "application/json"}

for dim in tqdm(dimensoes, desc="Gerando dimensões com LLaMA3"):
    payload = {
        "model": MODELO,
        "prompt": dim["prompt"],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, headers=headers, json=payload)
        response.raise_for_status()
        resultado_bruto = response.json()["response"]

        # Tentativa de conversão da parte relevante em JSON
        niveis_json = json.loads(resultado_bruto)
        rubrica["dimensoes"].append({
            "dimensao": dim["nome"],
            "origem": "SAEB 2017",
            "finalidade": "Construção de descritores pedagógicos contextualizados via IA",
            "niveis": niveis_json
        })

    except Exception as e:
        print(f"❌ Erro ao gerar {dim['nome']}: {e}")
        rubrica["dimensoes"].append({
            "dimensao": dim["nome"],
            "origem": "SAEB 2017",
            "finalidade": "Construção de descritores pedagógicos contextualizados via IA",
            "niveis": []
        })

# Salvar JSON final
caminho_saida = "dados_processados/bncc/rubrica_sinapse_ia_v1_2.json"
with open(caminho_saida, "w", encoding="utf-8") as f:
    json.dump(rubrica, f, ensure_ascii=False, indent=2)

print(f"\n✅ Rubrica salva com sucesso em: {caminho_saida}")

