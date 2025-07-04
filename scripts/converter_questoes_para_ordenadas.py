# scriptos.path.join(s, "c")onverter_questoes_para_ordenadas.py

import json
import os

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENTRADA = os.path.join(BASE_DIR, "dados_processados", "questoes", "questoes_pisa_tri_mineiro_completas.json")
SAIDA = os.path.join(BASE_DIR, "dados_processados", "questoes", "questoes_pisa_ordenadas.json")

# Verifica se o arquivo existe
if not os.path.exists(ENTRADA):
    raise FileNotFoundError(f"Arquivo de entrada não encontrado: {ENTRADA}")

# Carrega e converte
with open(ENTRADA, "r", encoding="utf-8") as f:
    questoes_raw = json.load(f)

questoes_convertidas = []
for q in questoes_raw:
    nova = {
        "area": q.get("Área", "").strip().lower(),
        "questao_id": q.get("Questão ID", "").strip(),
        "pergunta": q.get("Pergunta", "").strip(),
        "resposta_modelo": q.get("Resposta Modelo", "").strip(),
        "resposta_mediana": q.get("Resposta Mediana", "").strip(),
        "resposta_inadequada": q.get("Resposta Inadequada", "").strip(),
        "dimensoes": [dim.strip() for dim in q.get("Dimensões", "").split(",")]
    }
    questoes_convertidas.append(nova)

# Salva o novo arquivo
with open(SAIDA, "w", encoding="utf-8") as f:
    json.dump(questoes_convertidas, f, ensure_ascii=False, indent=2)

print("✅ Questões convertidas e ordenadas com sucesso!")
print(f"🧾 Arquivo salvo em: {SAIDA}")
