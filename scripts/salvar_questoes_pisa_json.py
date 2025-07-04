# scriptos.path.join(s, "s")alvar_questoes_pisa_json.py

import json
import os

questoes = [
    {
        "area": "Leitura",
        "numero": 1,
        "pergunta": "A prefeitura de sua cidade publicou um novo regulamento para o transporte escolar. Ele deve garantir o acesso equitativo de todos os alunos, especialmente os das zonas rurais. Com base nesse regulamento, discuta os principais desafios e benefícios para os estudantes da sua região.",
        "resposta_correta": "O novo regulamento beneficia estudantes da zona rural ao garantir acesso regular às escolas, mas enfrenta desafios como infraestrutura e orçamento limitado."
    },
    {
        "area": "Leitura",
        "numero": 2,
        "pergunta": "Um jornal local publicou uma matéria sobre a importância da leitura diária para o desempenho escolar. Como essa prática pode impactar os estudantes do Ensino Fundamental?",
        "resposta_correta": "A leitura diária desenvolve vocabulário, interpretação de texto e pensamento crítico, melhorando o desempenho nas demais disciplinas."
    },
    {
        "area": "Leitura",
        "numero": 3,
        "pergunta": "Durante uma roda de leitura, alunos do 9º ano discutiram a representatividade nos livros didáticos. Qual a importância de se ver representado nas histórias e textos escolares?",
        "resposta_correta": "A representatividade promove pertencimento, autoestima e engajamento com o conteúdo, além de valorizar a diversidade cultural."
    },
    {
        "area": "Matemática",
        "numero": 1,
        "pergunta": "Durante um evento cultural da sua região, 12 municípios contribuíram proporcionalmente com recursos. O total arrecadado foi de R$ 360.000. Explique como dividir esse valor de forma justa com base no número de estudantes de cada município e quais desafios essa divisão poderia apresentar.",
        "resposta_correta": "A divisão deve considerar o número de estudantes proporcionalmente. O desafio é obter dados precisos e garantir equidade entre municípios."
    },
    {
        "area": "Matemática",
        "numero": 2,
        "pergunta": "A escola recebeu 5 mil reais para investir em materiais didáticos. Se cada turma receber a mesma quantia e há 10 turmas, quanto cada uma receberá? Como garantir que o uso seja eficiente?",
        "resposta_correta": "Cada turma receberá R$ 500,00. A eficiência depende de planejamento e consulta aos professores sobre as necessidades."
    },
    {
        "area": "Matemática",
        "numero": 3,
        "pergunta": "Um gráfico mostrou que o consumo de energia elétrica aumentou 15% em um ano. Como interpretar esse dado no cotidiano da escola e propor ações?",
        "resposta_correta": "O aumento indica maior gasto e necessidade de economizar. Pode-se realizar campanhas de conscientização sobre uso racional."
    },
    {
        "area": "Ciências",
        "numero": 1,
        "pergunta": "As águas do rio Paranaíba têm apresentado variações na qualidade segundo estudos recentes. Proponha uma ação educativa local para envolver os estudantes e a comunidade na preservação ambiental da bacia hidrográfica.",
        "resposta_correta": "Organizar campanhas com os estudantes para monitoramento da água e promover ações de conscientização com a comunidade local."
    },
    {
        "area": "Ciências",
        "numero": 2,
        "pergunta": "A escola quer promover um projeto sobre alimentação saudável. Como os conhecimentos científicos podem contribuir com a escolha de alimentos mais nutritivos?",
        "resposta_correta": "A ciência fornece dados sobre nutrientes e impacto dos alimentos na saúde, ajudando na escolha de uma dieta equilibrada."
    },
    {
        "area": "Ciências",
        "numero": 3,
        "pergunta": "Durante uma feira de ciências, alunos pesquisaram sobre fontes renováveis de energia. Por que é importante desenvolver essas fontes na sua região?",
        "resposta_correta": "Fontes renováveis reduzem impacto ambiental e dependência de combustíveis fósseis, sendo mais sustentáveis e seguras."
    }
]

output_path = os.path.join(os.path.dirname(__file__), "..", "dados_processados", "respostas", "questoes_pisa_sinapse.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(questoes, f, ensure_ascii=False, indent=2)

print("✅ Arquivo salvo em:", output_path)

