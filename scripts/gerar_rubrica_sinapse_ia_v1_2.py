import os
import json
import torch
from pymongo import MongoClient
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM

# === CONFIGURAÇÃO DE HARDWARE (Limites) ===
torch.set_default_dtype(torch.float16)
torch.cuda.set_per_process_memory_fraction(0.25, device=0)  # 25% da GPU (6GB total ≈ 1.5GB)
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# === CONEXÃO MONGODB ===
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["saeb"]
colecao = db["saeb_2017_escolas"]

# === PARÂMETROS DE FILTRAGEM (REGIÃO) ===
micro_codigos_validos = [
    "5304", "5306", "5308", "5310", "5312", "5314", "5316", "5318", "5320",
    "5322", "5324", "5326", "5330", "5332", "5334", "5336", "5338", "5340"
]

# === MODELO DE IA ===
modelo_id = "meta-llama/Meta-Llama-3-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(modelo_id)
modelo = AutoModelForCausalLM.from_pretrained(modelo_id, torch_dtype=torch.float16, device_map="auto")

# === PROMPT BASE ===
prompt_template = """
Você é um especialista em avaliação educacional. A partir dos dados abaixo, gere um descritor pedagógico e 3 exemplos contextualizados para o Triângulo Mineiro e Alto Paranaíba. Use linguagem clara e educacional.

📊 Dados da escola (SAEB 2017):
{dados}

🔍 Saída esperada:
{{
  "nivel": "Nome do Nível (nota)",
  "descricao": "...",
  "exemplos": [
    "...",
    "...",
    "..."
  ]
}}
"""

# === CONSULTA E PROCESSAMENTO ===
def gerar_descritor_e_exemplos(dado_saeb):
    dados_formatados = json.dumps(dado_saeb, indent=2, ensure_ascii=False)
    prompt = prompt_template.format(dados=dados_formatados)

    entradas = tokenizer(prompt, return_tensors="pt").to("cuda")
    saida = modelo.generate(**entradas, max_new_tokens=500, do_sample=True, top_p=0.9, temperature=0.7)
    resposta = tokenizer.decode(saida[0], skip_special_tokens=True)

    return resposta.split("Saída esperada:")[-1].strip()

# === LOOP DE AMOSTRAS ===
resultados = []
amostras = colecao.find({"CO_MICRORREGIAO": {"$in": micro_codigos_validos}}).limit(30)

for i, doc in enumerate(amostras):
    print(f"🔍 Processando exemplo {i+1}...")
    try:
        resultado = gerar_descritor_e_exemplos(doc)
        resultados.append(json.loads(resultado))
    except Exception as e:
        print(f"⚠️ Erro ao gerar resultado para exemplo {i+1}: {e}")

# === DOCUMENTO FINAL ===
rubrica = {
    "nome": "rubrica_sinapse_ia",
    "versao": "1.2",
    "timestamp": datetime.utcnow().isoformat(),
    "base_dados": "SAEB 2017",
    "observacao": "Exemplos contextualizados para o Triângulo Mineiro e Alto Paranaíba",
    "dimensoes": resultados
}

# === SALVAMENTO EM JSON ===
with open("dados_processados/bncc/rubrica_sinapse_ia_v1_2.json", "w", encoding="utf-8") as f:
    json.dump(rubrica, f, ensure_ascii=False, indent=2)

print("✅ Rubrica SINAPSE IA v1.2 gerada com sucesso!")
client.close()

