import json
from datetime import datetime

# Caminhos dos arquivos
entrada = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_completa.json"
saida = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_padronizada.json"

# Dicionário com os novos metadados para cada dimensão
novos_metadados = {
    "Progressão Cognitiva Educacional": {
        "fonte": "Adaptado de Anderson e Krathwohl (2001), com base em Bloom (1956).",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "Taxonomia de Bloom"
    },
    "Perfil Socioeconômico e Contextual": {
        "fonte": "Adaptado de BRASIL. INEP. Indicadores contextuais do SAEB (2017).",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "ESCS + Rubrica SAEB"
    },
    "Autonomia e Autorregulação da Aprendizagem": {
        "fonte": "Adaptado de BRASIL. MEC. BNCC (2017) e SAEB (2017), com apoio em Flavell (1979) sobre metacognição.",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "BNCC + SAEB + Neuropsicopedagogia"
    },
    "Capacidade de Comunicação e Expressão": {
        "fonte": "Adaptado de BRASIL. INEP. Resultados SAEB (2017) e OCDE. Relatório PISA (2022).",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "SAEB + PISA + Rubrica de Linguagens"
    },
    "Raciocínio Lógico e Solução de Problemas": {
        "fonte": "Adaptado de BRASIL. INEP. SAEB (2017) e OCDE. PISA (2022).",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "Rubrica SAEB + Taxonomia SOLO + PISA"
    },
    "Engajamento e Responsabilidade Social": {
        "fonte": "Adaptado de OCDE (2022), BRASIL. INEP (2017), com apoio em autores como Paulo Freire (1996).",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "SAEB + PISA + Freire + Justiça Social"
    },
    "Relacionamento com Saberes Científicos e Culturais": {
        "fonte": "Adaptado de BRASIL. INEP. Resultados SAEB (2017) e OCDE. Relatório PISA (2022), com apoio da BNCC (2017).",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "BNCC + SAEB + PISA + Rubrica CTC"
    },
    "Pertencimento e Equidade Territorial (CTC + EJI + ESCS)": {
        "fonte": "Adaptado de BRASIL. MEC. Diretrizes para Educação Escolar Quilombola (2012), Educação do Campo (2010), Educação Escolar Indígena (2012) e BNCC (2017).",
        "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
        "rubrica(s) de origem": "CTC + EJI + ESCS"
    }
}

try:
    with open(entrada, "r", encoding="utf-8") as f:
        rubrica = json.load(f)

    for dim in rubrica["dimensoes"]:
        nome = dim.get("dimensao")
        if nome in novos_metadados:
            # Remover campo 'origem' e atualizar campos conforme novo padrão
            dim.pop("origem", None)
            dim["fonte"] = novos_metadados[nome]["fonte"]
            dim["nota"] = novos_metadados[nome]["nota"]
            dim["rubrica(s) de origem"] = novos_metadados[nome]["rubrica(s) de origem"]

    rubrica["timestamp"] = datetime.now().isoformat()

    with open(saida, "w", encoding="utf-8") as f:
        json.dump(rubrica, f, ensure_ascii=False, indent=2)

    print("✅ Rubrica atualizada com metadados padronizados.")
    print(f"📁 Arquivo salvo em: {saida}")

except Exception as e:
    print("❌ Erro ao aplicar reformulações:")
    print(e)

