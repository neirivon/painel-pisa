# scripts/corrigir_questoes_pisa_tmap_json.py

import json
import os

# Caminho absoluto para evitar erros no Streamlit Cloud
JSON_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/questoes_pisa_tmap.json"

def corrigir_json_questoes(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            dados = json.load(f)

        if isinstance(dados, list) and isinstance(dados[0], str):
            print("🔧 Corrigindo formato: lista de strings → lista de dicionários")
            dados_corrigidos = [json.loads(q) for q in dados if q.strip().startswith("{")]
        else:
            print("✅ O arquivo já está no formato correto.")
            return

        # Sobrescreve o arquivo com dados corrigidos e identação
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dados_corrigidos, f, ensure_ascii=False, indent=2)

        print(f"✅ Correção concluída e salva em: {path}")
    except Exception as e:
        print(f"❌ Erro ao processar o JSON: {e}")

if __name__ == "__main__":
    corrigir_json_questoes(JSON_PATH)

