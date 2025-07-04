# scriptos.path.join(s, "g")erar_rubricas_avaliar_rubricas_v1_json_csv.py

import pandas as pd
import json
import os
from datetime import datetime

# Estrutura da Rubrica de Avaliação de Rubricas v1
rubrica_v1 = [
    {
        "dimensao": "Clareza e Objetividade",
        "descricao": "Avalia se os critérios da rubrica são redigidos de forma clara, compreensível e objetiva.",
        "versao": "v1",
        "autor": "Professor Dr. Bruno Pereira Garcês",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {"nivel": "1", "descricao": "Critérios confusos, subjetivos ou vagos."},
            {"nivel": "2", "descricao": "Critérios parcialmente compreensíveis ou com termos genéricos."},
            {"nivel": "3", "descricao": "Critérios claros, mas com possibilidade de múltiplas interpretações."},
            {"nivel": "4", "descricao": "Critérios totalmente claros, objetivos e bem definidos."}
        ]
    },
    {
        "dimensao": "Coerência Pedagógica",
        "descricao": "Verifica se os critérios e os níveis da rubrica estão alinhados com os objetivos de aprendizagem.",
        "versao": "v1",
        "autor": "Professor Dr. Bruno Pereira Garcês",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {"nivel": "1", "descricao": "Critérios desconectados dos objetivos de aprendizagem."},
            {"nivel": "2", "descricao": "Parcialmente coerente com os objetivos propostos."},
            {"nivel": "3", "descricao": "Critérios coerentes com os objetivos educacionais."},
            {"nivel": "4", "descricao": "Totalmente alinhada com os objetivos pedagógicos e metodológicos."}
        ]
    },
    {
        "dimensao": "Aplicabilidade Prática",
        "descricao": "Considera se a rubrica pode ser facilmente aplicada por diferentes professores em diferentes contextos.",
        "versao": "v1",
        "autor": "Professor Dr. Bruno Pereira Garcês",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {"nivel": "1", "descricao": "De difícil aplicação, com critérios abstratos ou inconsistentes."},
            {"nivel": "2", "descricao": "Aplicação parcial, com exemplos insuficientes ou genéricos."},
            {"nivel": "3", "descricao": "Aplicável com apoio, exemplos ou formação prévia."},
            {"nivel": "4", "descricao": "Aplicação fácil, imediata e adaptável."}
        ]
    },
    {
        "dimensao": "Abrangência e Equidade",
        "descricao": "Avalia se a rubrica contempla diferentes estilos de aprendizagem, níveis cognitivos e inclusão.",
        "versao": "v1",
        "autor": "Professor Dr. Bruno Pereira Garcês",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {"nivel": "1", "descricao": "Excludente ou limitada a um perfil específico de aluno."},
            {"nivel": "2", "descricao": "Abrangente apenas em alguns aspectos (ex: cognitivo, mas não afetivo)."},
            {"nivel": "3", "descricao": "Contempla diversidade de estilos e ritmos com ressalvas."},
            {"nivel": "4", "descricao": "Abrangente, equitativa e promotora de inclusão."}
        ]
    }
]

# Criar diretório de destino
os.makedirs("dados_processadoos.path.join(s, "r")ubricas", exist_ok=True)

# Salvar JSON
json_path = "dados_processadoos.path.join(s, "r")ubricaos.path.join(s, "a")valiar_rubricas_v1.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(rubrica_v1, f, ensure_ascii=False, indent=2)

# Preparar CSV achatado
rows = []
for dim in rubrica_v1:
    for nivel in dim["niveis"]:
        rows.append({
            "dimensao": dim["dimensao"],
            "descricao_dimensao": dim["descricao"],
            "nivel": nivel["nivel"],
            "descricao_nivel": nivel["descricao"],
            "versao": dim["versao"],
            "autor": dim["autor"],
            "timestamp_versao": dim["timestamp_versao"]
        })

df = pd.DataFrame(rows)
csv_path = "dados_processadoos.path.join(s, "r")ubricaos.path.join(s, "a")valiar_rubricas_v1.csv"
df.to_csv(csv_path, index=False, encoding="utf-8")

print("✅ Rubrica de Avaliação de Rubricas v1 salva com sucesso.")
print(f"📄 JSON: {json_path}")
print(f"📄 CSV:  {csv_path}")
print("👤 Autor: Professor Dr. Bruno Pereira Garcês")

