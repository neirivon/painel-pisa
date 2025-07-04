
import json
import os
from ollama import Client
from pymongo import MongoClient
from painel_pisa.utils.config import CONFIG

client = Client()
mongo_uri = CONFIG.get("MONGO_URI", "mongodb://localhost:27017")
mongo = MongoClient(mongo_uri)
db = mongo["relatorios_inep"]
colecao = db["inep_2018"]

docs = list(colecao.find({}))
resultados = []

for doc in docs:
    texto = doc["paragrafo"].replace('"', '\"')
    prompt = f"""Analise o seguinte parágrafo e identifique:
1. O nível da Taxonomia de Bloom mais provável;
2. A polaridade do sentimento predominante;
3. A dimensão e nível da Rubrica SINAPSE;
4. As palavras-chave principais.

Texto:
\"{texto}\"""    
    resposta = client.chat(model="llama3", messages=[{{"role": "user", "content": prompt}}])
    doc["inferencias_llama3"] = resposta["message"]["content"]
    resultados.append(doc)

# Atualizar MongoDB com inferências
for r in resultados:
    _id = r.pop("_id")
    colecao.update_one({{"_id": _id}}, {{"$set": r}})

print("✅ Inferência concluída para 2018 — Total:", len(resultados))
