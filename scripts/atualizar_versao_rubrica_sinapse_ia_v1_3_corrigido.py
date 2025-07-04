import json
import re
from datetime import datetime
import os

# Caminho original e novo
input_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_2_completa.json"
output_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_corrigida.json"

def carregar_json_com_tentativa_corrigir(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Erro de sintaxe JSON: {e.msg}")
        print(f"📍 Linha: {e.lineno}, Coluna: {e.colno}")
        with open(path, "r", encoding="utf-8") as f:
            texto = f.read()

        # Corrigir vírgulas faltantes antes de fechamento de lista ou dicionário
        texto_corrigido = re.sub(r'(\}\s*\n)(\s*\])', r'\1,\2', texto)
        texto_corrigido = re.sub(r'(\}\s*\n)(\s*\})', r'\1,\2', texto_corrigido)

        # Nova tentativa
        try:
            return json.loads(texto_corrigido)
        except Exception as e2:
            print("❌ Não foi possível corrigir automaticamente o JSON.")
            raise e2

def atualizar_versao(json_data):
    json_data["versao"] = "v1.3"
    json_data["timestamp"] = datetime.utcnow().isoformat()
    return json_data

def salvar_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Executando tudo
try:
    data = carregar_json_com_tentativa_corrigir(input_json)
    data = atualizar_versao(data)
    salvar_json(output_json, data)
    print(f"✅ Rubrica corrigida e salva em: {output_json}")
except Exception as erro:
    print(f"❌ Erro ao processar rubrica: {erro}")

