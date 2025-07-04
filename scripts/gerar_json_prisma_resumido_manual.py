import json

# Lista dos 27 itens reais do PRISMA 2020 resumido
itens = [
    {"numero": 1, "titulo": "Title", "descricao": "Identify the report as a systematic review."},
    {"numero": 2, "titulo": "Abstract", "descricao": "See the PRISMA 2020 for Abstracts checklist."},
    {"numero": 3, "titulo": "Rationale", "descricao": "Describe the rationale for the review in the context of existing knowledge."},
    {"numero": 4, "titulo": "Objectives", "descricao": "Provide an explicit statement of the objective(s) or question(s) the review addresses."},
    {"numero": 5, "titulo": "Eligibility criteria", "descricao": "Specify the inclusion and exclusion criteria for the review and how studies were grouped for the syntheses."},
    {"numero": 6, "titulo": "Information sources", "descricao": "Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies. Specify the date when each source was last searched or consulted."},
    {"numero": 7, "titulo": "Search strategy", "descricao": "Present the full search strategies for all databases, registers and websites, including any filters and limits used."},
    {"numero": 8, "titulo": "Selection process", "descricao": "Specify the methods used to decide whether a study met the inclusion criteria of the review, including how many reviewers screened each record and each report retrieved, whether they worked independently, and if applicable, details of automation tools used in the process."},
    {"numero": 9, "titulo": "Data collection process", "descricao": "Specify the methods used to collect data from reports, including how many reviewers collected data from each report, whether they worked independently, any processes for obtaining or confirming data from study investigators, and if applicable, details of automation tools used in the process."},
    {"numero": 10, "titulo": "Data items (outcomes)", "descricao": "List and define all outcomes for which data were sought. Specify whether all results that were compatible with each outcome domain in each study were sought, and if not, the methods used to decide which results to collect."},
    {"numero": 11, "titulo": "Data items (other variables)", "descricao": "List and define all other variables for which data were sought (e.g. participant and intervention characteristics, funding sources). Describe any assumptions made about any missing or unclear information."},
    {"numero": 12, "titulo": "Study risk of bias assessment", "descricao": "Specify the methods used to assess risk of bias in the included studies, including details of the tool(s) used, how many reviewers assessed each study and whether they worked independently, and if applicable, details of automation tools used in the process."},
    {"numero": 13, "titulo": "Effect measures", "descricao": "Specify for each outcome the effect measure(s) (e.g. risk ratio, mean difference) used in the synthesis or presentation of results."},
    {"numero": 14, "titulo": "Synthesis methods", "descricao": "Describe the processes used to decide which studies were eligible for each synthesis. Describe any methods required to prepare the data for presentation or synthesis. Describe any methods used to tabulate or visually display results. Describe methods used to synthesize results and rationale. Describe methods to explore heterogeneity and any sensitivity analyses."},
    {"numero": 15, "titulo": "Reporting bias assessment", "descricao": "Describe any methods used to assess risk of bias due to missing results in a synthesis (arising from reporting biases)."},
    {"numero": 16, "titulo": "Certainty assessment", "descricao": "Describe any methods used to assess certainty (or confidence) in the body of evidence for an outcome."},
    {"numero": 17, "titulo": "Study selection", "descricao": "Describe the results of the search and selection process, ideally using a flow diagram. Cite studies that might appear to meet the inclusion criteria, but which were excluded, and explain why they were excluded."},
    {"numero": 18, "titulo": "Study characteristics", "descricao": "Cite each included study and present its characteristics."},
    {"numero": 19, "titulo": "Risk of bias in studies", "descricao": "Present assessments of risk of bias for each included study."},
    {"numero": 20, "titulo": "Results of individual studies", "descricao": "For all outcomes, present summary statistics for each group and an effect estimate with its precision, ideally using structured tables or plots."},
    {"numero": 21, "titulo": "Results of syntheses", "descricao": "Summarise the characteristics and risk of bias among contributing studies. Present results of all statistical syntheses conducted and investigations of heterogeneity. Present results of sensitivity analyses."},
    {"numero": 22, "titulo": "Reporting biases", "descricao": "Present assessments of risk of bias due to missing results (arising from reporting biases) for each synthesis assessed."},
    {"numero": 23, "titulo": "Certainty of evidence", "descricao": "Present assessments of certainty (or confidence) in the body of evidence for each outcome assessed."},
    {"numero": 24, "titulo": "Discussion", "descricao": "Provide interpretation of results in context of other evidence. Discuss limitations of the evidence and review processes. Discuss implications for practice, policy, and future research."},
    {"numero": 25, "titulo": "Registration and protocol", "descricao": "Provide registration info including register name and number. Indicate where the protocol can be accessed. Describe any amendments."},
    {"numero": 26, "titulo": "Support", "descricao": "Describe sources of financial or non-financial support and the role of the funders or sponsors."},
    {"numero": 27, "titulo": "Competing interests and availability", "descricao": "Declare any competing interests. Report availability of data, code and other materials used in the review."}
]

# Montagem do dicionário final
output = {
    "versao": "PRISMA 2020",
    "tipo": "resumido",
    "fonte": "Página oficial do PRISMA",
    "referencia_abnt": "PAGE, M. J. et al. PRISMA 2020 checklist. PRISMA, 2021. Disponível em: <https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf>. Acesso em: 06 jun. 2025.",
    "url": "https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf",
    "itens": itens
}

# Caminho de saída
json_output_path = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/prisma/prisma_checklist_resumido_populado.json"

# Salva o JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✔ Checklist PRISMA 2020 resumido salvo em: {json_output_path}")
print(f"✔ Total de itens: {len(itens)}")

