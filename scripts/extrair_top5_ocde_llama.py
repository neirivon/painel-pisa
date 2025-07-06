import json
import requests
import os
from pymongo import MongoClient

colecoes = [
    "relatorio_ocde_pisa_2000_pisa_2000_en",
    "relatorio_ocde_pisa_2003_pisa_2003_en",
    "relatorio_ocde_pisa_2006_pisa_2006_v1_en",
    "relatorio_ocde_pisa_2009_pisa_2009_v1",
    "relatorio_ocde_pisa_2012_pisa_2012_results_snapshot_volume_i_eng",
    "relatorio_ocde_pisa_2015_pisa_2015_v1_en",
    "relatorio_ocde_pisa_2018_pisa_2018_v1_en",
    "relatorio_ocde_pisa_2022_pisa_2022_v1_en"
]

def perguntar_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"❌ Erro ao consultar Ollama: {e}"

# Conectar ao MongoDB com autenticação
print("🔌 Conectando ao MongoDB autenticado...")
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["pisa"]

resultados = []

for colecao in colecoes:
    print(f"📘 Edição {colecao[-11:-3]}: buscando textos...")
    col = db[colecao]
    docs = col.find({}, {"texto": 1}).limit(10)

    textos = [doc.get("texto", "") for doc in docs if "texto" in doc]
    if not textos:
        print(f"⚠️ Edição {colecao[-11:-3]}: nenhum conteúdo textual encontrado.")
        continue

    texto_base = "\n".join(textos[:3])[:2000]

    prompt = (
        f"Avalie o texto abaixo extraído do relatório da OCDE (edição {colecao[-11:-3]} do PISA). "
        "Retorne os 5 países com maiores pontuações em Leitura, Matemática e Ciências, e informe a posição do Brasil. "
        "Use este formato JSON com 3 colunas: Leitura, Matemática, Ciências. Cada coluna deve conter um dicionário com países e suas posições e notas.\n\n"
        f"TEXTO:\n{texto_base}"
    )

    resposta = perguntar_ollama(prompt)
    resultados.append({
        "edicao": colecao[-11:-3],
        "resposta_ia": resposta.strip()
    })

# Salvar em JSON
saida = "painel_pisa/dados_cloud/comparativo_brasil_top5_ocde_llama.json"
os.makedirs(os.path.dirname(saida), exist_ok=True)

with open(saida, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"✅ Finalizado. JSON salvo em: {saida}")

# Fechar conexão com MongoDB
client.close()

