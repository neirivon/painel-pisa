# scripts/gerar_questoes_pisa_tmap_json_csv.py

import json
import csv
import os

# Caminhos absolutos
JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"
CSV_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/gabarito_professor.csv"

# Garante que a pasta existe
os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)

# Questões adaptadas do PISA 2022 para o TMAP
questoes = [
    {
        "disciplina": "Leitura",
        "pergunta_original": "Qual é a mensagem principal do texto sobre a importância da leitura na juventude?",
        "pergunta_adaptada_tmap": "Por que é importante ler quando somos jovens, especialmente em nossa comunidade no Triângulo Mineiro e Alto Paranaíba (TMAP)?",
        "resposta_modelo": "A leitura desenvolve o pensamento crítico e nos ajuda a entender melhor o mundo, além de valorizar nossa cultura regional.",
        "rubrica_pedagogica": "rubrica_sinapse_pedagogica_professor (v1.4)",
        "fonte": "OCDE/PISA 2022",
        "ano": 2022,
        "versao": "v1.4",
        "publico": "aluno"
    },
    {
        "disciplina": "Matemática",
        "pergunta_original": "Pedro precisa dividir igualmente 12 litros de suco entre 4 garrafas. Quantos litros cabem em cada garrafa?",
        "pergunta_adaptada_tmap": "No TMAP, uma família quer dividir 12 litros de suco entre 4 garrafas iguais para uma festa na escola. Quantos litros vão em cada garrafa?",
        "resposta_modelo": "Cada garrafa terá 3 litros, pois 12 dividido por 4 é igual a 3.",
        "rubrica_pedagogica": "rubrica_sinapse_pedagogica_professor (v1.4)",
        "fonte": "OCDE/PISA 2022",
        "ano": 2022,
        "versao": "v1.4",
        "publico": "aluno"
    },
    {
        "disciplina": "Ciências",
        "pergunta_original": "Explique como as árvores ajudam a melhorar a qualidade do ar nas cidades.",
        "pergunta_adaptada_tmap": "No TMAP, como as árvores da nossa região podem melhorar a qualidade do ar e a saúde das pessoas?",
        "resposta_modelo": "As árvores absorvem gás carbônico e liberam oxigênio, além de filtrar poeira e poluentes, contribuindo para um ar mais limpo.",
        "rubrica_pedagogica": "rubrica_sinapse_pedagogica_professor (v1.4)",
        "fonte": "OCDE/PISA 2022",
        "ano": 2022,
        "versao": "v1.4",
        "publico": "aluno"
    }
]

# Salvar em JSON
with open(JSON_PATH, "w", encoding="utf-8") as f_json:
    json.dump(questoes, f_json, indent=2, ensure_ascii=False)
print(f"✅ JSON salvo com sucesso em: {JSON_PATH}")

# Exportar para CSV
campos = [
    "disciplina", "pergunta_original", "pergunta_adaptada_tmap",
    "resposta_modelo", "rubrica_pedagogica", "fonte", "ano", "versao", "publico"
]

with open(CSV_PATH, "w", encoding="utf-8", newline="") as f_csv:
    writer = csv.DictWriter(f_csv, fieldnames=campos)
    writer.writeheader()
    for q in questoes:
        writer.writerow(q)
print(f"✅ CSV salvo com sucesso em: {CSV_PATH}")

