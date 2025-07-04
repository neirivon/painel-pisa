from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
import os
import json
import re
import pandas as pd
from pymongo import MongoClient

# Conexão com o MongoDB Dockerizado
client = conectar_mongo(nome_banco="saeb")[1]
db = client["pisa"]
colecao = db["relatorios_inep"]

# Pasta dos JSONs extraídos
pasta = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "i")neos.path.join(p, "e")xtraido/"))
arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".json")])

print(f"🔍 Encontrados {len(arquivos)} arquivos para análise.")

resultados = []

# Tópicos buscados
padroes = {
    "desempenho": r"\b(desempenho|resultados)\b",
    "competencias": r"\b(competências?|habilidades?)\b",
    "equidade": r"\b(equidade|desigualdade|diferença entre grupos)\b",
    "comparações": r"\b(comparações?|países|internacional)\b",
    "politicas_publicas": r"\b(políticas públicas|recomendações|sugestões)\b",
    "brasil": r"\bbrasil\b"
}

for nome_arquivo in arquivos:
    ano = re.search(r"\d{4}", nome_arquivo).group()
    caminho = os.path.join(pasta, nome_arquivo)

    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.read().lower()

    doc = {
        "ano": int(ano),
        "arquivo": nome_arquivo
    }

    for topico, padrao in padroes.items():
        doc[topico] = bool(re.search(padrao, texto))

    colecao.insert_one(doc)
    resultados.append(doc)
    print(f"📄 Analisado: {nome_arquivo}")

# Exporta para CSV
df_resultado = pd.DataFrame(resultados)
df_resultado.to_csv("relatorios_inep_resumo.csv", index=False)

print("\n✅ Resumo gerado com sucesso:")
print(df_resultado.head(10))  # Visualização inicial
print("📁 Arquivo salvo: relatorios_inep_resumo.csv")

client.close()

