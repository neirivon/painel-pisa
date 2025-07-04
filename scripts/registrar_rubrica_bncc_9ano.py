import json
import pandas as pd
import os
from datetime import datetime
from pymongo import MongoClient

# === CONFIGURAÇÃO ===
PASTA_SAIDA = "dados_processadoos.path.join(s, "r")ubricas_edicao_pisa"
ARQUIVO_JSON = f"{PASTA_SAIDAos.path.join(}, "r")ubrica_bncc_9ano.json"
ARQUIVO_CSV = f"{PASTA_SAIDAos.path.join(}, "r")ubrica_bncc_9ano.csv"
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB = "rubricas"
COLLECTION = "rubrica_bncc_9ano"

# === CRIA DIRETÓRIO SE NECESSÁRIO ===
os.makedirs(PASTA_SAIDA, exist_ok=True)

# === RUBRICA PEDAGÓGICA GERAL DO 9º ANO (BNCC) ===
rubrica = {
    "fonte": "BNCC",
    "ano": "9º ano",
    "etapa": "Ensino Fundamental – Anos Finais",
    "descricao_geral": (
        "A BNCC define que no 9º ano do Ensino Fundamental o foco está em consolidar "
        "a aprendizagem matemática com ênfase na resolução de problemas, abstração algébrica, "
        "leitura e interpretação de gráficos, além do aprofundamento das noções estatísticas e probabilísticas."
    ),
    "eixos": ["Números", "Álgebra", "Geometria", "Grandezas e Medidas", "Probabilidade e Estatística"],
    "finalidade_formativa": (
        "Desenvolver competências para utilizar a matemática em contextos cotidianos, acadêmicos e tecnológicos, "
        "estimulando o pensamento crítico e lógico."
    ),
    "abordagens": {
        "taxonomia_bloom": "Aplicação e Análise",
        "metodologia_sugerida": "Gamificação e Resolução de Problemas",
        "perfil_neuropsicopedagogico": "Raciocínio lógico com mediação visual",
        "taxonomia_solo": "Multiestrutural"
    },
    "documento_referencia": "BNCC_EI_EF_110518_versaofinal_site.pdf",
    "timestamp_extracao": datetime.utcnow()
}

# === SALVAR JSON ===
with open(ARQUIVO_JSON, "w", encoding="utf-8") as f_json:
    json.dump(rubrica, f_json, ensure_ascii=False, indent=2)

# === SALVAR CSV (1 linha) ===
pd.DataFrame([rubrica]).to_csv(ARQUIVO_CSV, index=False)

# === INSERIR NO MONGO ===
client = MongoClient(MONGO_URI)
mongo_collection = client[DB][COLLECTION]
mongo_collection.insert_one(rubrica)

print("✅ Rubrica pedagógica geral do 9º ano (BNCC) registrada com sucesso.")
print(f"→ JSON salvo em: {ARQUIVO_JSON}")
print(f"→ CSV salvo em:  {ARQUIVO_CSV}")
print(f"→ Coleção MongoDB: {DB}.{COLLECTION}")

