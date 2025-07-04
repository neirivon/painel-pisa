import os
import json
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime
import warnings
import requests

warnings.filterwarnings("ignore", category=ResourceWarning)

# MongoDB
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DB_PISA = "pisa"
DB_SAEB = "saeb"
COLECAO_PISA = "historico_pisa_brasil"
COLECAO_RUBRICA = "rubrica_sinapse_ia"
COLECAO_SAEB = "saeb_2021_brasil"

# Arquivo de saída
CAMINHO_SAIDA = "painel_pisa/dados_cloud/conclusao_comparativa_pisa_saeb.json"

def conectar_mongo():
    cliente = MongoClient(MONGO_URI)
    return cliente

def buscar_dados_pisa(cliente):
    col = cliente[DB_PISA][COLECAO_PISA]
    dados = list(col.find({"Ano": 2022, "Pais": {"$in": ["Brazil", "BR", "Brasil"]}}, {"_id": 0}))
    valores = {d["Variavel"]: d["Valor"] for d in dados}
    return valores.get("PV1READ"), valores.get("PV1MATH"), valores.get("ESCS")

def buscar_dados_saeb(cliente):
    col = cliente[DB_SAEB][COLECAO_SAEB]
    doc = col.find_one({"ID": "Brasil"}, {"_id": 0})
    if not doc:
        return None, None
    return doc.get("MEDIA_9_LP"), doc.get("MEDIA_9_MT")

def carregar_rubrica(cliente):
    col = cliente["rubricas"][COLECAO_RUBRICA]
    return col.find_one({"versao": "v1.4"}, {"_id": 0})

def gerar_prompt(read_pisa, math_pisa, escs, lp_saeb, mt_saeb, rubrica):
    prompt = f"""A partir dos dados do PISA 2022 e SAEB 2021, gere uma conclusão pedagógica interpretativa comparando os dois exames. Utilize a Rubrica SINAPSE IA v1.4 para orientar a análise.

📊 Dados PISA:
- Leitura: {read_pisa}
- Matemática: {math_pisa}
- ESCS: {escs}

📊 Dados SAEB:
- Leitura (9º ano): {lp_saeb}
- Matemática (9º ano): {mt_saeb}

📘 Rubrica SINAPSE IA v1.4:
"""
    for dim in rubrica["dimensoes"]:
        prompt += f"\n📘 {dim['dimensao']}:\n"
        for nivel in dim["niveis"]:
            prompt += f"- ({nivel['nota']}) {nivel['nome']}: {nivel['descricao']}\n"
    prompt += "\n✍️ Escreva um parágrafo interpretativo que compare os dados e identifique forças e fragilidades educacionais do Brasil."
    return prompt

def consultar_ollama(prompt):
    print("💬 Enviando prompt para o modelo LLaMA3 via Ollama...")
    resposta = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return resposta.json()["response"].strip()

def salvar_resultado(texto):
    Path(CAMINHO_SAIDA).write_text(json.dumps({
        "texto": texto,
        "timestamp": datetime.now().isoformat()
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"💾 Conclusão salva em: {CAMINHO_SAIDA}")

def main():
    print("📚 Buscando dados do PISA e SAEB...")
    cliente = conectar_mongo()
    try:
        read_pisa, math_pisa, escs = buscar_dados_pisa(cliente)
        lp_saeb, mt_saeb = buscar_dados_saeb(cliente)
        rubrica = carregar_rubrica(cliente)
    finally:
        cliente.close()
        print("🔒 Conexão com MongoDB encerrada.")

    if not all([read_pisa, math_pisa, escs, lp_saeb, mt_saeb]):
        print("⚠️ Dados incompletos. Verifique as coleções.")
        return

    prompt = gerar_prompt(read_pisa, math_pisa, escs, lp_saeb, mt_saeb, rubrica)
    resposta = consultar_ollama(prompt)
    print("\n" + "="*80)
    print("📜 Texto:\n" + resposta)
    print("="*80)
    salvar_resultado(resposta)
    print("✅ Conclusão gerada com sucesso.")

if __name__ == "__main__":
    main()

