import os
import json
import pandas as pd
from pymongo import MongoClient
import requests
from pathlib import Path

# Configurações Mongo
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
BANCO_PISA = "pisa"
COL_HISTORICO = "historico_pisa_brasil"
BANCO_RUBRICA = "rubricas"
COL_RUBRICA = "rubrica_sinapse_ia"

# Caminho local para salvar JSON (opcional)
CAMINHO_SAIDA = "painel_pisa/dados_cloud/conclusao_pisa_ocde.json"

def conectar_mongo():
    return MongoClient(MONGO_URI)

def obter_dados_2022():
    cliente = conectar_mongo()
    try:
        col = cliente[BANCO_PISA][COL_HISTORICO]
        dados = list(col.find({
            "Ano": 2022,
            "Pais": {"$in": ["Brazil", "BR", "Brasil"]},
            "Variavel": {"$in": ["PV1MATH", "PV1READ", "ESCS"]}
        }, {"_id": 0}))
        return pd.DataFrame(dados)
    finally:
        cliente.close()

def obter_rubrica():
    cliente = conectar_mongo()
    try:
        col = cliente[BANCO_RUBRICA][COL_RUBRICA]
        doc = col.find_one({"versao": "v1.4"}, {"_id": 0})
        return doc
    finally:
        cliente.close()

def montar_prompt(dados_df, rubrica):
    try:
        math = float(dados_df[dados_df["Variavel"] == "PV1MATH"]["Valor"].values[0])
        read = float(dados_df[dados_df["Variavel"] == "PV1READ"]["Valor"].values[0])
        escs = float(dados_df[dados_df["Variavel"] == "ESCS"]["Valor"].values[0])
    except IndexError:
        raise ValueError("Dados incompletos para PV1MATH, PV1READ ou ESCS.")

    prompt = f"""
O Brasil obteve as seguintes pontuações médias no PISA 2022:
- Leitura: {read:.3f}
- Matemática: {math:.3f}
- ESCS (indicador socioeconômico): {escs:.4f}

Com base nesses dados, gere uma conclusão pedagógica interpretativa utilizando as seguintes dimensões da Rubrica SINAPSE IA v1.4:

"""

    for dim in rubrica["dimensoes"]:
        prompt += f"📘 {dim['dimensao']}:\n"
        for nivel in dim["niveis"]:
            prompt += f"- ({nivel['nota']}) {nivel['nome']}: {nivel['descricao']}\n"
        prompt += "\n"

    prompt += "Explique a situação educacional do Brasil com base nessas evidências.\n"
    return prompt.strip()

def enviar_para_ollama(prompt):
    resposta = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 500
            }
        }
    )
    return resposta.json()["response"]

def main():
    print("🔌 Conectando ao MongoDB...")
    dados = obter_dados_2022()
    rubrica = obter_rubrica()
    print("📚 Rubrica e dados carregados com sucesso.")

    print("✍️ Montando prompt para o modelo...")
    prompt = montar_prompt(dados, rubrica)

    print("💬 Enviando prompt para o modelo LLaMA3 via Ollama...")
    resposta = enviar_para_ollama(prompt)

    texto_final = f"📜 Texto:\n{resposta.strip()}\n\n📊 Dados utilizados:\n- Leitura: {dados[dados['Variavel']=='PV1READ']['Valor'].values[0]}\n- Matemática: {dados[dados['Variavel']=='PV1MATH']['Valor'].values[0]}\n- ESCS: {dados[dados['Variavel']=='ESCS']['Valor'].values[0]}\n\n📘 Rubrica aplicada: SINAPSE IA v1.4"

    print("\n" + "="*80)
    print(texto_final)
    print("="*80)

    # Opcional: salvar localmente
    Path(CAMINHO_SAIDA).write_text(json.dumps({
        "Ano": 2022,
        "Conclusao": resposta.strip(),
        "Prompt": prompt
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n💾 Também salvo em {CAMINHO_SAIDA}")

if __name__ == "__main__":
    main()

