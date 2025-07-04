import json
from datetime import datetime

entrada_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_padronizada.json"
saida_txt = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/relatorio_avaliacao_rubrica_v1_3.txt"

criterios = [
    {
        "criterio": "Clareza na formulação da dimensão",
        "descricao": "A dimensão está bem definida e compreensível?",
        "peso": 1.0
    },
    {
        "criterio": "Aderência à fonte científica",
        "descricao": "A dimensão tem citação bibliográfica padronizada (ABNT)?",
        "peso": 1.0
    },
    {
        "criterio": "Transparência na origem",
        "descricao": "Está claro de qual rubrica foi derivada (ex: Bloom, SAEB, etc)?",
        "peso": 1.0
    },
    {
        "criterio": "Aplicabilidade prática (exemplos)",
        "descricao": "Os exemplos são contextualizados, realistas e diversos?",
        "peso": 1.0
    }
]

def avaliar_dimensao(dim):
    nota_total = 0
    relatorio = []

    if len(dim.get("dimensao", "")) > 5:
        relatorio.append(("Clareza na formulação da dimensão", 4, "Definição clara e objetiva."))
        nota_total += 4
    else:
        relatorio.append(("Clareza na formulação da dimensão", 2, "Descrição genérica ou pouco informativa."))
        nota_total += 2

    if "fonte" in dim and "Adaptado de" in dim["fonte"]:
        relatorio.append(("Aderência à fonte científica", 4, "Fonte citada conforme ABNT."))
        nota_total += 4
    else:
        relatorio.append(("Aderência à fonte científica", 2, "Fonte ausente ou fora do padrão."))
        nota_total += 2

    if "rubrica_origem" in dim and isinstance(dim["rubrica_origem"], list) and len(dim["rubrica_origem"]) > 0:
        relatorio.append(("Transparência na origem", 4, "Rubrica de origem explicitada."))
        nota_total += 4
    else:
        relatorio.append(("Transparência na origem", 2, "Rubrica de origem não identificada."))
        nota_total += 2

    exemplos = dim.get("exemplos", [])
    if isinstance(exemplos, list) and len(exemplos) >= 3:
        relatorio.append(("Aplicabilidade prática (exemplos)", 4, "Exemplos bem contextualizados."))
        nota_total += 4
    else:
        relatorio.append(("Aplicabilidade prática (exemplos)", 2, "Poucos ou nenhum exemplo prático."))
        nota_total += 2

    media = round(nota_total / len(criterios), 2)
    return media, relatorio

with open(entrada_json, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

with open(saida_txt, "w", encoding="utf-8") as f:
    f.write("RELATÓRIO DE AVALIAÇÃO — Rubrica SINAPSE IA v1.3\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("-" * 70 + "\n\n")

    for dim in rubrica["dimensoes"]:
        media, avaliacoes = avaliar_dimensao(dim)

        f.write(f"🔹 Dimensão: {dim['dimensao']}\n")
        f.write(f"Nota final: {media} de 4.0\n")

        for crit, nota, justificativa in avaliacoes:
            f.write(f"  - {crit}: {nota}/4\n")
            f.write(f"    ➤ Justificativa: {justificativa}\n")
            if nota < 4:
                f.write(f"    ✔️ Ação sugerida: Ajustar para atingir excelência.\n")

        f.write("\n" + "-" * 70 + "\n\n")

