import json
import csv
import os

JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"
CSV_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/gabarito_professor.csv"

os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    dados_raw = json.load(f)

with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    campos = ['disciplina', 'pergunta_adaptada_tmap', 'resposta_modelo']
    writer = csv.DictWriter(csvfile, fieldnames=campos)
    writer.writeheader()

    for idx, item in enumerate(dados_raw):
        try:
            questao = json.loads(item) if isinstance(item, str) else item
            if isinstance(questao, dict):
                writer.writerow({
                    'disciplina': questao.get('disciplina', ''),
                    'pergunta_adaptada_tmap': questao.get('pergunta_adaptada_tmap', ''),
                    'resposta_modelo': questao.get('resposta_modelo', '')
                })
            else:
                print(f"⚠️ Linha {idx + 1} não é dicionário após json.loads.")
        except json.JSONDecodeError:
            print(f"❌ Erro de decodificação na linha {idx + 1}: não é um JSON válido.")

print(f"✅ CSV corrigido e salvo com sucesso em: {CSV_PATH}")

