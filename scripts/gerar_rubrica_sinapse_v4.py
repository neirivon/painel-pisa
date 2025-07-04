import pandas as pd
from datetime import datetime
import json
import os

# Estrutura comum com exemplos por nível para as 6 dimensões
rubrica_v4 = [
    {
        "dimensao": "Taxonomia de Bloom",
        "icone": "🧠",
        "versao": "v4",
        "fonte": "Elaborado pelos autores. Referências: Bloom (1956), Anderson & Krathwohl (2001).",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {
                "nivel": "1",
                "nome": "Emergente",
                "descricao": "Recordar ou reconhecer informações simples.",
                "exemplo": "Listar as operações básicas (adição, subtração etc.)."
            },
            {
                "nivel": "2",
                "nome": "Inicial",
                "descricao": "Compreender significados e interpretar textos ou situações.",
                "exemplo": "Explicar com suas palavras a ideia principal de um parágrafo."
            },
            {
                "nivel": "3",
                "nome": "Essencial",
                "descricao": "Aplicar conhecimentos em contextos familiares.",
                "exemplo": "Resolver um problema de porcentagem em uma compra simulada."
            },
            {
                "nivel": "4",
                "nome": "Avançado",
                "descricao": "Analisar estruturas, relações ou causas.",
                "exemplo": "Comparar dois pontos de vista em um debate escolar."
            },
            {
                "nivel": "5",
                "nome": "Inovador",
                "descricao": "Avaliar e criar soluções com autonomia.",
                "exemplo": "Criar uma campanha de conscientização sobre o uso racional da água."
            }
        ]
    },
    {
        "dimensao": "Taxonomia SOLO",
        "icone": "📐",
        "versao": "v4",
        "fonte": "Elaborado pelos autores. Referências: Biggs & Collis (1982).",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {
                "nivel": "1",
                "nome": "Pré-estrutural",
                "descricao": "Não há compreensão do conceito.",
                "exemplo": "Responder a uma questão sem coerência com o tema proposto."
            },
            {
                "nivel": "2",
                "nome": "Uniestrutural",
                "descricao": "Compreensão de um único aspecto.",
                "exemplo": "Apontar um dado isolado em um gráfico."
            },
            {
                "nivel": "3",
                "nome": "Multiestrutural",
                "descricao": "Compreensão de vários aspectos sem conexão entre eles.",
                "exemplo": "Listar causas e consequências sem relacioná-las."
            },
            {
                "nivel": "4",
                "nome": "Relacional",
                "descricao": "Estabelece conexões e relações entre os conceitos.",
                "exemplo": "Relacionar dados do censo com impactos sociais."
            },
            {
                "nivel": "5",
                "nome": "Abstrato Estendido",
                "descricao": "Transfere conhecimento para novos contextos.",
                "exemplo": "Propor um plano para melhorar a mobilidade urbana com base em dados da cidade."
            }
        ]
    },
    {
        "dimensao": "Metodologia Ativa",
        "icone": "🛠️",
        "versao": "v4",
        "fonte": "Elaborado pelos autores. Referências: Moran (2015), Bacich & Moran (2018).",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {
                "nivel": "1",
                "nome": "Emergente",
                "descricao": "Prática expositiva, centrada no professor.",
                "exemplo": "Aula apenas com quadro e fala do docente."
            },
            {
                "nivel": "2",
                "nome": "Inicial",
                "descricao": "Introdução pontual de estratégias ativas.",
                "exemplo": "Uso de quiz interativo ao final da aula."
            },
            {
                "nivel": "3",
                "nome": "Essencial",
                "descricao": "Metodologias aplicadas com mediação do professor.",
                "exemplo": "Estudo de caso em grupos com roteiro guiado."
            },
            {
                "nivel": "4",
                "nome": "Avançado",
                "descricao": "Estudantes realizam tarefas complexas com autonomia.",
                "exemplo": "Projeto maker de ciências sobre sustentabilidade local."
            },
            {
                "nivel": "5",
                "nome": "Inovador",
                "descricao": "Metodologia centrada no protagonismo e autoria.",
                "exemplo": "Hackathon de soluções pedagógicas desenvolvidas por alunos."
            }
        ]
    },
    {
        "dimensao": "Perfil Neuropsicopedagógico",
        "icone": "🧬",
        "versao": "v4",
        "fonte": "Elaborado pelos autores. Referências: Fonseca (2014), Oliveira (2017).",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {
                "nivel": "1",
                "nome": "Emergente",
                "descricao": "Não há consideração do perfil do aluno.",
                "exemplo": "Atividade padrão, igual para todos os estudantes."
            },
            {
                "nivel": "2",
                "nome": "Inicial",
                "descricao": "Reconhecimento inicial de estilos cognitivos.",
                "exemplo": "Apresentação com elementos visuais para alunos com dificuldade de abstração."
            },
            {
                "nivel": "3",
                "nome": "Essencial",
                "descricao": "Adaptação conforme estilos de aprendizagem.",
                "exemplo": "Proposta de múltiplos caminhos para resolução de um problema lógico."
            },
            {
                "nivel": "4",
                "nome": "Avançado",
                "descricao": "Planejamento com base em avaliações diagnósticas.",
                "exemplo": "Uso de mapas mentais e gamificação para alunos com perfil visual e motivacional."
            },
            {
                "nivel": "5",
                "nome": "Inovador",
                "descricao": "Customização contínua e responsiva.",
                "exemplo": "Roteiros personalizados com base em perfil neuroeducacional detectado por IA."
            }
        ]
    },
    {
        "dimensao": "DUA – Desenho Universal para Aprendizagem",
        "icone": "♿",
        "versao": "v4",
        "fonte": "Elaborado pelos autores. Referências: CAST (2018), Brasil (2020).",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {
                "nivel": "1",
                "nome": "Emergente",
                "descricao": "Acessibilidade não considerada.",
                "exemplo": "Material apenas em texto impresso, sem adaptação."
            },
            {
                "nivel": "2",
                "nome": "Inicial",
                "descricao": "Alguns recursos de acessibilidade usados.",
                "exemplo": "Slides com imagens e legenda textual simples."
            },
            {
                "nivel": "3",
                "nome": "Essencial",
                "descricao": "Oferece múltiplas formas de representação.",
                "exemplo": "Vídeo, áudio e texto sobre o mesmo conteúdo."
            },
            {
                "nivel": "4",
                "nome": "Avançado",
                "descricao": "Adaptação ativa conforme necessidade.",
                "exemplo": "Propostas visuais e gamificadas para estudantes com dislexia."
            },
            {
                "nivel": "5",
                "nome": "Inovador",
                "descricao": "Planejamento inclusivo desde o início.",
                "exemplo": "Projeto curricular com múltiplos meios, engajamento e expressão desde o início."
            }
        ]
    },
    {
        "dimensao": "CTC – Contextualização Territorial e Cultural",
        "icone": "🌍",
        "versao": "v4",
        "fonte": "Elaborado pelos autores. Referências: Sobel (2004), Santos (2006), Mendes (2011).",
        "timestamp_versao": datetime.now().isoformat(),
        "niveis": [
            {
                "nivel": "1",
                "nome": "Ausência de contextualização",
                "descricao": "Prática pedagógica genérica, sem conexão com o território.",
                "exemplo": "Aula sobre clima sem relacionar com o clima da região onde vivem os estudantes."
            },
            {
                "nivel": "2",
                "nome": "Contextualização incipiente",
                "descricao": "Reconhecimento superficial do contexto.",
                "exemplo": "Citar um exemplo local sem desenvolver conexão crítica."
            },
            {
                "nivel": "3",
                "nome": "Contextualização técnica e parcial",
                "descricao": "Adaptação baseada em dados genéricos do território.",
                "exemplo": "Uso de dados socioeconômicos regionais em uma tabela, sem envolvimento comunitário."
            },
            {
                "nivel": "4",
                "nome": "Práticas integradas ao território e cultura local",
                "descricao": "Integração ativa da realidade local ao currículo.",
                "exemplo": "Projeto interdisciplinar sobre a história do bairro feito com participação da comunidade."
            },
            {
                "nivel": "5",
                "nome": "Educação territorialmente responsiva e co-construída",
                "descricao": "Planejamento participativo com base em dados locais e culturais.",
                "exemplo": "Estudantes elaboram propostas educativas baseadas em entrevistas e mapas locais."
            }
        ]
    }
]

# Salvar como JSON e CSV
os.makedirs("dados_processadoos.path.join(s, "b")ncc", exist_ok=True)

# JSON
with open("dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v4.json", "w", encoding="utf-8") as f:
    json.dump(rubrica_v4, f, ensure_ascii=False, indent=2)

# CSV (achatado)
rows = []
for dim in rubrica_v4:
    for nivel in dim["niveis"]:
        row = {
            "dimensao": dim["dimensao"],
            "icone": dim["icone"],
            "versao": dim["versao"],
            "fonte": dim["fonte"],
            "timestamp_versao": dim["timestamp_versao"],
            "nivel": nivel["nivel"],
            "nome_nivel": nivel["nome"],
            "descricao": nivel["descricao"],
            "exemplo": nivel["exemplo"]
        }
        rows.append(row)

df_csv = pd.DataFrame(rows)
csv_path = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v4.csv"
df_csv.to_csv(csv_path, index=False, encoding="utf-8")

print("✅ Rubrica SINAPSE v4 gerada com sucesso.")
print(f"📄 JSON: {csv_path.replace('.csv', '.json')}")
print(f"📄 CSV:  {csv_path}")

