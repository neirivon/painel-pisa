import json
import pandas as pd
from datetime import datetime
import os

# ========== CONFIGURAÇÃO ==========
timestamp_str = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
versao = "v1.0"
dimensao = "Contextualização Territorial e Cultural"

# ========== DADOS ==========
rubrica = [
    {
        "nivel": 1,
        "titulo": "Explorador Desconectado",
        "descricao": "Não reconhece nem menciona seu território ou aspectos culturais locais.",
        "exemplos": [
            "Descreve o problema de forma genérica, sem nenhuma referência à sua cidade ou cultura.",
            "Apresenta soluções importadas de outras realidades sem relação com o local."
        ]
    },
    {
        "nivel": 2,
        "titulo": "Conector Inicial",
        "descricao": "Faz referências vagas ou indiretas ao espaço, cultura ou comunidade.",
        "exemplos": [
            "Menciona \"minha cidade\" ou \"nossa região\" sem detalhamento.",
            "Usa termos genéricos como \"as pessoas daqui\" sem caracterização."
        ]
    },
    {
        "nivel": 3,
        "titulo": "Criador Contextualizado",
        "descricao": "Relaciona explicitamente o conteúdo à realidade territorial e cultural.",
        "exemplos": [
            "Aponta um problema local com base em dados regionais.",
            "Compara saberes escolares com práticas culturais da comunidade."
        ]
    },
    {
        "nivel": 4,
        "titulo": "Transformador Sociocultural",
        "descricao": "Propõe ações, reflexões ou soluções ancoradas em sua realidade local.",
        "exemplos": [
            "Sugere políticas públicas com base em necessidades da região.",
            "Apresenta proposta de intervenção com valorização cultural local."
        ]
    }
]

# ========== FORMATAÇÃO ==========
for item in rubrica:
    item["dimensao"] = dimensao
    item["versao"] = versao
    item["timestamp"] = timestamp_str

# ========== SALVAR ==========
os.makedirs("dados_processados/rubricas", exist_ok=True)

# Salvar JSON
with open("dados_processados/rubricas/rubrica_ctc.json", "w", encoding="utf-8") as f_json:
    json.dump(rubrica, f_json, ensure_ascii=False, indent=2)

# Salvar CSV
df = pd.DataFrame([{
    "dimensao": item["dimensao"],
    "nivel": item["nivel"],
    "titulo": item["titulo"],
    "descricao": item["descricao"],
    "exemplo_1": item["exemplos"][0],
    "exemplo_2": item["exemplos"][1],
    "versao": item["versao"],
    "timestamp": item["timestamp"]
} for item in rubrica])

df.to_csv("dados_processados/rubricas/rubrica_ctc.csv", index=False, encoding="utf-8")

print("✅ Rubrica CTC salva com sucesso em JSON e CSV.")

