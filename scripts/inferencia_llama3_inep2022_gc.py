import os
import json
import pandas as pd
import gc
from tqdm import tqdm
from pymongo import MongoClient
from painel_pisa.utils.config import CONFIG

import ollama

# Caminhos
JSON_PATH = os.path.join(CONFIG["CAMINHO_DADOS"], "relatorios_inep", "relatorio_inep_2022.json")
OUTPUT_JSON = os.path.join(CONFIG["CAMINHO_DADOS"], "relatorios_inep", "relatorio_inep_2022_enriquecido.json")
OUTPUT_CSV = os.path.join(CONFIG["CAMINHO_DADOS"], "relatorios_inep", "relatorio_inep_2022_enriquecido.csv")

def montar_prompt(paragrafo):
    return (
        "Analise o seguinte parágrafo e identifique:\n"
        "1. O nível da Taxonomia de Bloom mais provável;\n"
        "2. A polaridade do sentimento predominante;\n"
        "3. A dimensão e nível da Rubrica SINAPSE;\n"
        "4. As palavras-chave principais.\n\n"
        f"Texto:\n{json.dumps(paragrafo, ensure_ascii=False)}"
    )

def inferir_campos_llama3(paragrafo):
    prompt = montar_prompt(paragrafo)
    try:
        resposta = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        saida = resposta["message"]["content"]

        json_inicio = saida.find("{")
        json_fim = saida.rfind("}") + 1
        json_bruto = saida[json_inicio:json_fim]
        return json.loads(json_bruto)
    except Exception as e:
        return {"erro": str(e)}

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    enriquecidos = []
    for item in tqdm(dados, desc="Inferindo com LLaMA3"):
        resultado = inferir_campos_llama3(item["paragrafo"])
        enriquecido = {**item, **resultado}
        enriquecidos.append(enriquecido)

    # Salvar no MongoDB
    client = MongoClient(CONFIG["MONGO_URI"])
    db = client["relatorios_inep"]
    colecao = db["inep_2022"]
    colecao.delete_many({})
    colecao.insert_many(enriquecidos)

    # Remover _id para salvar em arquivos
    for doc in enriquecidos:
        doc.pop("_id", None)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(enriquecidos, f, ensure_ascii=False, indent=2)

    pd.DataFrame(enriquecidos).to_csv(OUTPUT_CSV, index=False)

    client.close()
    gc.collect()

    print(f"✅ Inferência concluída. Arquivos salvos em:\n{OUTPUT_JSON}\n{OUTPUT_CSV}")

if __name__ == "__main__":
    main()

