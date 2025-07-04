import json
from datetime import datetime

# Caminhos
input_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_2_completa.json"
output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3.json"

try:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Atualiza versão e timestamp
    data["versao"] = "v1.3"
    data["timestamp"] = datetime.now().isoformat()

    for dim in data["dimensoes"]:
        # Padronização da origem e fonte
        dim["origem"] = "Adaptado de SAEB (2017) e PISA (2022)."
        dim["fonte"] = "Fonte: BRASIL. INEP. Resultados SAEB 2017. OCDE. Relatório PISA 2022."

        # Adiciona finalidade se ausente
        if "finalidade" not in dim:
            if "Comunicação" in dim["dimensao"]:
                dim["finalidade"] = "Avaliar a habilidade de expressar ideias com clareza, coerência e adequação aos gêneros e contextos comunicativos."
            elif "Raciocínio" in dim["dimensao"]:
                dim["finalidade"] = "Verificar a capacidade de resolver problemas por meio da lógica, pensamento crítico e estratégias matemáticas."
            elif "Engajamento" in dim["dimensao"]:
                dim["finalidade"] = "Analisar o comprometimento do estudante com o coletivo escolar e sua responsabilidade social e ética."
            elif "Saberes Científicos" in dim["dimensao"]:
                dim["finalidade"] = "Avaliar como o estudante articula conhecimentos científicos e culturais em sua formação cidadã."

        # Padroniza nomes dos níveis
        for nivel in dim["niveis"]:
            nome_original = nivel["nome"]
            nivel["nome"] = nivel["nome"].split(" ")[0]  # Remove "(1)", "(2)", etc.

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("✅ Rubrica v1.3 atualizada com sucesso!")

except Exception as e:
    print(f"❌ Erro ao atualizar rubrica: {e}")

