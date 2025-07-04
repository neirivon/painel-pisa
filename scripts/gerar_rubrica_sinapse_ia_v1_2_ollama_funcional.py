import requests
import json
from datetime import datetime
from tqdm import tqdm
import os
import time

# Configurações do modelo e da API local
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
MAX_TENTATIVAS = 3
DELAY_SEGUNDOS = 2

# Lista de dimensões a serem geradas
dimensoes = [
    "Progressão Cognitiva Educacional",
    "Perfil Socioeconômico e Contextual"
]

# Prompt base ajustado para maior clareza com LLAMA3
def montar_prompt(dimensao):
    return f"""
Você é um especialista pedagógico e deve criar uma rubrica detalhada com base nos dados do SAEB 2017.

Gere uma estrutura JSON contendo exatamente 4 níveis para a dimensão "{dimensao}".
Cada nível deve ter os seguintes campos:

- nota (número inteiro de 1 a 4)
- nome (título curto e descritivo)
- descricao (explicação detalhada, em até 2 linhas)
- exemplos (lista com exatamente 3 objetos, cada um com "titulo" e "descricao")

⚠️ Regras importantes:
- Retorne apenas o JSON válido, sem explicações ou textos adicionais
- Não use markdown
- Garanta que todas as chaves sejam strings válidas
- Evite caracteres especiais que possam corromper o JSON
"""

# Função para enviar prompt e obter resposta do modelo
def gerar_resposta_ia(dimensao):
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            payload = {
                "model": MODEL_NAME,
                "prompt": montar_prompt(dimensao),
                "stream": False,
                "temperature": 0.4,   # Menos aleatório para respostas mais previsíveis
                "max_tokens": 8192,   # Limite alto para garantir saída completa
                "stop": ["Observação:", "Nota:"],  # Palavras que param a geração
            }

            resposta = requests.post(OLLAMA_URL, json=payload, timeout=120)

            if resposta.status_code == 200:
                try:
                    conteudo = resposta.json().get("response", "")
                    if not conteudo.strip():
                        raise ValueError("Resposta vazia recebida")
                    return json.loads(conteudo)
                except json.JSONDecodeError as je:
                    print(f"❌ Erro ao decodificar JSON na tentativa {tentativa}: {je}")
                    time.sleep(DELAY_SEGUNDOS)
            else:
                print(f"❌ Código HTTP {resposta.status_code} na tentativa {tentativa}")
                print(resposta.text)
                time.sleep(DELAY_SEGUNDOS)

        except Exception as e:
            print(f"⚠️ Exceção na tentativa {tentativa}: {e}")
            time.sleep(DELAY_SEGUNDOS)

    print(f"🔴 Falha após {MAX_TENTATIVAS} tentativas para '{dimensao}'")
    return None

# Estrutura principal da rubrica
rubrica = {
    "nome": "rubrica_sinapse_ia",
    "versao": "v1.2",
    "base": "SAEB 2017",
    "modelo": "LLaMA3 8B (Ollama)",
    "timestamp": datetime.now().isoformat(),
    "dimensoes": []
}

# Loop de geração das dimensões
print("🧠 Gerando rubrica pedagógica com LLaMA3:")
for dimensao in tqdm(dimensoes, desc="Processando dimensões"):
    try:
        resposta_json = gerar_resposta_ia(dimensao)
        if isinstance(resposta_json, dict):
            niveis = list(resposta_json.values())[0] if len(resposta_json) == 1 else resposta_json.get("niveis", [])
        elif isinstance(resposta_json, list):
            niveis = resposta_json
        else:
            niveis = []

        if niveis and len(niveis) >= 4:
            rubrica["dimensoes"].append({
                "dimensao": dimensao,
                "origem": "SAEB 2017",
                "finalidade": "Construção de descritores pedagógicos contextualizados via IA",
                "niveis": niveis[:4]  # Garante exatamente 4 níveis
            })
        else:
            print(f"⚠️ Níveis insuficientes ou inválidos para '{dimensao}'")
    except Exception as e:
        print(f"❌ Erro ao processar '{dimensao}': {e}")

# Salvar resultado em arquivo
output_path = "dados_processados/bncc/rubrica_sinapse_ia_v1_2.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(rubrica, f, ensure_ascii=False, indent=2)

print(f"\n✅ Rubrica salva com sucesso em: {output_path}")
