# scriptos.path.join(s, "c")onverter_rubrica_para_v6a_padrao.py

import json
import pandas as pd
import os

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARQUIVO_ORIGINAL = os.path.join(BASE_DIR, "dados_processados", "rubricas", "rubrica_sinapse_v6_adaptada.json")
ARQUIVO_CORRIGIDO_JSON = os.path.join(BASE_DIR, "dados_processados", "rubricas", "rubrica_sinapse_v6a_corrigida.json")
ARQUIVO_CORRIGIDO_CSV = os.path.join(BASE_DIR, "dados_processados", "rubricas", "rubrica_sinapse_v6a_corrigida.csv")

# Verificação
if not os.path.exists(ARQUIVO_ORIGINAL):
    raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO_ORIGINAL}")

# Conversão das chaves
with open(ARQUIVO_ORIGINAL, "r", encoding="utf-8") as f:
    dados = json.load(f)

corrigido = []
for item in dados:
    novo = {
        "dimensao": item.get("Dimensão", "").strip(),
        "nivel": item.get("Nível", item.get("nivel", None)),
        "titulo": item.get("Nome do Nível", item.get("titulo", "")).strip(),
        "descricao": item.get("Descritor", item.get("descricao", "")).strip()
    }
    corrigido.append(novo)

# Salvar JSON corrigido
with open(ARQUIVO_CORRIGIDO_JSON, "w", encoding="utf-8") as f:
    json.dump(corrigido, f, ensure_ascii=False, indent=2)

# Salvar CSV corrigido
df = pd.DataFrame(corrigido)
df.to_csv(ARQUIVO_CORRIGIDO_CSV, index=False)

print("✅ Rubrica corrigida com sucesso!")
print(f"📄 JSON: {ARQUIVO_CORRIGIDO_JSON}")
print(f"📄 CSV: {ARQUIVO_CORRIGIDO_CSV}")
