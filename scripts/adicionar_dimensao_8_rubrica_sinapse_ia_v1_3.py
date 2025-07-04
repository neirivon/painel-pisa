import json
from datetime import datetime

# Caminhos dos arquivos
entrada = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3.json"
saida = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_completa.json"

# Nova dimensão a ser adicionada
nova_dimensao = {
    "dimensao": "Pertencimento e Equidade Territorial (CTC + EJI + ESCS)",
    "fonte": "Adaptado de BRASIL. MEC. Diretrizes para Educação Escolar Quilombola (2012), Educação do Campo (2010), Educação Escolar Indígena (2012) e BNCC (2017).",
    "nota": "Adaptação realizada pelo autor deste trabalho em 2025.",
    "finalidade": "Analisar a consciência crítica, o reconhecimento da diversidade e o protagonismo dos estudantes na valorização dos territórios, identidades e direitos.",
    "niveis": [
        {
            "nota": 1,
            "nome": "Emergente",
            "descricao": "Apresenta desconhecimento ou negação da diversidade étnica, regional e de gênero, reproduzindo estigmas ou silêncios históricos."
        },
        {
            "nota": 2,
            "nome": "Intermediário",
            "descricao": "Reconhece a diversidade cultural e social no território escolar, mas ainda com limitações na participação ativa e crítica."
        },
        {
            "nota": 3,
            "nome": "Proficiente",
            "descricao": "Valoriza identidades diversas e atua com respeito e empatia, propondo ações que favoreçam a equidade no ambiente escolar e comunitário."
        },
        {
            "nota": 4,
            "nome": "Avançado",
            "descricao": "Lidera ou protagoniza ações de afirmação de direitos, memória coletiva e justiça territorial, com foco na superação das desigualdades."
        }
    ],
    "exemplos": [
        "Estudantes de comunidades quilombolas em Gurinhatã desenvolvem um projeto de mapeamento cultural da região com valorização da memória oral e patrimônio local.",
        "Jovens indígenas em São João das Missões propõem um plano de acessibilidade curricular bilíngue, garantindo a valorização da língua e cultura originária.",
        "Alunos de escolas do campo em Monte Alegre de Minas criam uma feira territorial com produtos, saberes e práticas tradicionais da agricultura familiar local."
    ]
}

try:
    # Carregar JSON existente
    with open(entrada, "r", encoding="utf-8") as f:
        rubrica = json.load(f)

    # Adicionar nova dimensão
    rubrica["dimensoes"].append(nova_dimensao)

    # Atualizar timestamp
    rubrica["timestamp"] = datetime.now().isoformat()

    # Salvar novo JSON
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(rubrica, f, ensure_ascii=False, indent=2)

    print("✅ Nova dimensão adicionada com sucesso!")
    print(f"📁 Arquivo salvo em: {saida}")

except Exception as e:
    print("❌ Erro ao adicionar nova dimensão:")
    print(e)

