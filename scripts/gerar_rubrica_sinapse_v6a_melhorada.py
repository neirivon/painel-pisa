# gerar_rubrica_sinapse_v6a_melhorada.py

import json
from datetime import datetime
from pathlib import Path

rubrica_melhorada = {
    "nome": "Rubrica SINAPSE",
    "versao": "v6a-melhorada",
    "descricao": (
        "Rubrica aprimorada com base na avaliação formativa da versão v6a. "
        "Inclui padronização de títulos de dimensões, enriquecimento de exemplos, "
        "comentários pedagógicos e sugestões de uso. Estrutura alinhada à BNCC, DUA, "
        "PISA OCDE, Metodologias Ativas e princípios de Equidade e Contextualização."
    ),
    "data_criacao": datetime.utcnow().isoformat(),
    "dimensoes": [
        {
            "sigla": "BNCC",
            "nome": "BNCC – Base Nacional Comum Curricular",
            "nota_avaliacao": 4,
            "comentario": "Excelente alinhamento com o currículo nacional; exemplos práticos e evolutivos.",
            "niveis": [
                {
                    "nivel": 1,
                    "titulo": "Desalinhado",
                    "descricao": "A prática ou proposta não se conecta com as habilidades da BNCC.",
                    "exemplos": [
                        "Apresenta conteúdo descontextualizado, sem relação com habilidades específicas.",
                        "Ignora os objetos de conhecimento previstos para o ano/série."
                    ]
                },
                {
                    "nivel": 2,
                    "titulo": "Emergente",
                    "descricao": "Há tentativas de aproximação com a BNCC, mas de forma parcial ou genérica.",
                    "exemplos": [
                        "Inclui menções vagas às competências gerais da BNCC.",
                        "Utiliza objetivos que não dialogam diretamente com os códigos de habilidade."
                    ]
                },
                {
                    "nivel": 3,
                    "titulo": "Alinhado",
                    "descricao": "A proposta reflete as habilidades da BNCC de forma coerente.",
                    "exemplos": [
                        "Cada atividade está associada a um código de habilidade específico da BNCC.",
                        "Planejamento explícito com foco nas competências e habilidades do ano escolar."
                    ]
                },
                {
                    "nivel": 4,
                    "titulo": "Inovador",
                    "descricao": "Integra a BNCC com abordagens interdisciplinares e inovadoras.",
                    "exemplos": [
                        "Promove projetos interdisciplinares com múltiplas habilidades e competências.",
                        "Aplica metodologias inovadoras para desenvolver habilidades da BNCC em profundidade."
                    ]
                }
            ]
        },
        {
            "sigla": "CTC",
            "nome": "CTC – Contextualização Territorial e Cultural",
            "nota_avaliacao": 4,
            "comentario": "Promove aprendizagem contextualizada e valoriza a cultura local de forma clara e eficaz.",
            "niveis": [
                {
                    "nivel": 1,
                    "titulo": "Desconectado",
                    "descricao": "Não considera os saberes ou realidades do território.",
                    "exemplos": [
                        "Trabalha com conteúdos totalmente genéricos, sem menção à realidade local.",
                        "Desvaloriza ou ignora práticas culturais da comunidade."
                    ]
                },
                {
                    "nivel": 2,
                    "titulo": "Conector Inicial",
                    "descricao": "Reconhece o território, mas ainda sem aprofundamento crítico.",
                    "exemplos": [
                        "Inclui mapas locais em atividades, mas sem discussão crítica sobre o espaço.",
                        "Relata aspectos culturais regionais, mas como curiosidade isolada."
                    ]
                },
                {
                    "nivel": 3,
                    "titulo": "Integrador",
                    "descricao": "Integra elementos culturais e sociais ao currículo de forma significativa.",
                    "exemplos": [
                        "Analisa dados socioeconômicos do território em aulas de matemática e geografia.",
                        "Convida lideranças locais para atividades escolares."
                    ]
                },
                {
                    "nivel": 4,
                    "titulo": "Transformador Comunitário",
                    "descricao": "Utiliza o conhecimento local como base para transformação social e aprendizado crítico.",
                    "exemplos": [
                        "Desenvolve projetos escolares com impacto direto na comunidade.",
                        "Debate políticas públicas locais em articulação com os conteúdos escolares."
                    ]
                }
            ]
        }
        # DUA, EJI, Metodologia Ativa podem seguir mesmo padrão. Você pode duplicar e expandir conforme o modelo acima.
    ]
}

# Salvando em JSON
caminho_arquivo = Path("~/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_v6a_melhorada.json").expanduser()
with open(caminho_arquivo, "w", encoding="utf-8") as f:
    json.dump(rubrica_melhorada, f, ensure_ascii=False, indent=2)

print(f"✅ Rubrica SINAPSE v6a melhorada salva em: {caminho_arquivo}")

