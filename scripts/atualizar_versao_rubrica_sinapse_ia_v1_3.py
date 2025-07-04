# ~/SINAPSE2.0/PISA/scripts/atualizar_versao_rubrica_sinapse_ia_v1_3.py

import json
from datetime import datetime

input_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_2_completa.json"
output_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_completa.json"

try:
    with open(input_json, "r", encoding="utf-8") as f:
        rubrica = json.load(f)

    # Atualiza versão e timestamp
    rubrica["versao"] = "v1.3"
    rubrica["timestamp"] = datetime.now().isoformat()

    # Ajusta campo 'nome' caso esteja ausente
    rubrica["nome"] = rubrica.get("nome", "rubrica_sinapse_ia")

    # Corrige campos obrigatórios ausentes nas dimensões
    for d in rubrica.get("dimensoes", []):
        if "finalidade" not in d:
            d["finalidade"] = "Finalidade ainda não definida para esta dimensão."
        if "origem" not in d:
            d["origem"] = "Origem não especificada."
        if "fonte" not in d:
            d["fonte"] = "Fonte não especificada."

        # Corrige campo "niveis" se vier como "descritores"
        if "niveis" not in d and "descritores" in d:
            d["niveis"] = []
            for i, (nivel_nome, desc) in enumerate(d["descritores"].items(), start=1):
                d["niveis"].append({
                    "nota": i,
                    "nome": nivel_nome,
                    "descricao": desc
                })
            del d["descritores"]

    # Salva nova versão
    with open(output_json, "w", encoding="utf-8") as f_out:
        json.dump(rubrica, f_out, ensure_ascii=False, indent=2)

    print(f"✅ Rubrica atualizada com sucesso e salva como: {output_json}")

except Exception as e:
    print(f"❌ Erro ao atualizar rubrica: {e}")

