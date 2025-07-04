# scripts/gerar_conclusao_pisa_ocde.py

import os
import json
import requests
import warnings
import pandas as pd
from pathlib import Path
from pymongo import MongoClient

# Suprimir warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

# Configurações MongoDB
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO_DADOS = "rubricas"
COLECAO_HISTORICO = "historico_pisa_brasil"
COLECAO_RUBRICA = "rubrica_sinapse_ia"

# Caminhos de saída
CAMINHO_CONCLUSAO = "painel_pisa/dados_cloud/conclusao_pisa_ocde.json"
CAMINHO_LOG_IGNORADOS = "painel_pisa/dados_cloud/log_anos_ignorados.csv"

# Endpoint da API do Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

def conectar_mongo():
    print("🔌 Conectando ao MongoDB...")
    return MongoClient(MONGO_URI)

def carregar_dados_mongo(cliente):
    db = cliente["pisa"]
    col = db[COLECAO_HISTORICO]
    dados = list(col.find({"Ano": 2022, "Pais": {"$in": ["Brazil", "BR", "Brasil"]}}, {"_id": 0}))
    return pd.DataFrame(dados)

def carregar_rubrica(cliente):
    print("📚 Buscando rubrica SINAPSE IA v1.4 do MongoDB...")
    col = cliente[BANCO_DADOS][COLECAO_RUBRICA]
    rubrica = col.find_one({"versao": "v1.4"}, {"_id": 0})
    if not rubrica:
        raise ValueError("❌ Rubrica SINAPSE IA v1.4 não encontrada.")
    return rubrica

def preparar_prompt(dados, rubrica):
    try:
        math = dados.loc[dados["Variavel"] == "PV1MATH", "Valor"].values[0]
        read = dados.loc[dados["Variavel"] == "PV1READ", "Valor"].values[0]
        escs = dados.loc[dados["Variavel"] == "ESCS", "Valor"].values[0]
    except IndexError:
        return None

    prompt = f"O Brasil obteve as seguintes pontuações médias no PISA 2022:\n"
    prompt += f"- Leitura: {read}\n- Matemática: {math}\n- ESCS: {escs}\n"
    prompt += "Com base nesses dados, gere uma conclusão pedagógica considerando as dimensões da seguinte rubrica:\n\n"

    for dim in rubrica["dimensoes"]:
        prompt += f"📘 {dim['dimensao']}:\n"
        for nivel in dim["niveis"]:
            prompt += f"- ({nivel['nota']}) {nivel['nome']}: {nivel['descricao']}\n"
        prompt += "\n"

    prompt += "Gere um parágrafo interpretativo sobre a situação educacional do Brasil no PISA 2022 com base nessa rubrica."
    return prompt

def gerar_conclusao_ollama(prompt):
    print("💬 Enviando prompt para o modelo LLaMA3 via Ollama...")
    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        raise RuntimeError(f"Erro na API Ollama: {response.text}")

    return response.json().get("response", "").strip()

def salvar_resultados(conclusoes, ignorados):
    Path(CAMINHO_CONCLUSAO).write_text(json.dumps(conclusoes, ensure_ascii=False, indent=2), encoding="utf-8")
    pd.DataFrame(ignorados).to_csv(CAMINHO_LOG_IGNORADOS, index=False)
    print(f"💾 Conclusões salvas em: {CAMINHO_CONCLUSAO}")
    print(f"🗒️ Log de anos ignorados salvo em: {CAMINHO_LOG_IGNORADOS}")

def main():
    cliente = conectar_mongo()
    try:
        dados_df = carregar_dados_mongo(cliente)
        if dados_df.empty:
            print("⚠️ Nenhum dado encontrado para 2022.")
            return

        rubrica = carregar_rubrica(cliente)
    finally:
        cliente.close()
        print("🔒 Conexão com MongoDB encerrada.")

    print("📊 Dados encontrados. Processando...")
    prompt = preparar_prompt(dados_df, rubrica)

    if not prompt:
        print("⚠️ Dados incompletos. Ignorando 2022.")
        salvar_resultados([], [{"Ano": 2022, "Motivo": "Dados incompletos"}])
        return

    try:
        resposta = gerar_conclusao_ollama(prompt)
        salvar_resultados([{"Ano": 2022, "Conclusao": resposta}], [])
        print("✅ Conclusão gerada com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao gerar conclusão: {e}")
        salvar_resultados([], [{"Ano": 2022, "Motivo": str(e)}])

if __name__ == "__main__":
    main()

