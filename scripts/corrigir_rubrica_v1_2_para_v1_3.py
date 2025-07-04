import json
import re
from datetime import datetime

input_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_2_completa.json"
output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3.json"

def corrigir_json_malformado(texto):
    # Corrige vírgulas faltando antes de ']', '}'
    texto = re.sub(r'(\}\s*)(\s*[\]])', r'\1,\2', texto)
    texto = re.sub(r'(\}\s*)(\s*\})', r'\1,\2', texto)
    texto = re.sub(r'(\]\s*)(\s*\})', r'\1,\2', texto)
    return texto

def carregar_e_corrigir(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        with open(path, "r", encoding="utf-8") as f:
            texto = f.read()
        texto_corrigido = corrigir_json_malformado(texto)
        try:
            return json.loads(texto_corrigido)
        except json.JSONDecodeError as e2:
            print(f"❌ Ainda inválido após tentativa de correção. Linha {e2.lineno}, coluna {e2.colno}")
            raise

def atualizar_versao(dados):
    dados["versao"] = "v1.3"
    dados["timestamp"] = datetime.utcnow().isoformat()
    return dados

def salvar_json(dados, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

try:
    rubrica = carregar_e_corrigir(input_path)
    rubrica = atualizar_versao(rubrica)
    salvar_json(rubrica, output_path)
    print(f"✅ Rubrica salva com sucesso em: {output_path}")
except Exception as e:
    print(f"❌ Erro ao corrigir e salvar rubrica: {e}")

