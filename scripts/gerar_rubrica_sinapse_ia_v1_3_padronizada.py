import json
from datetime import datetime

rubrica = {
    "nome": "rubrica_sinapse_ia",
    "versao": "v1.3",
    "base": "SAEB 2017 + PISA 2022",
    "modelo": "LLAMA3 + análise pedagógica",
    "timestamp": datetime.now().isoformat(),
    "dimensoes": []
}

def adicionar_dimensao(dimensao, fonte, nota, rubrica_origem, niveis, exemplos):
    rubrica["dimensoes"].append({
        "dimensao": dimensao,
        "fonte": fonte,
        "nota": nota,
        "rubrica_origem": rubrica_origem,
        "niveis": niveis,
        "exemplos": exemplos
    })

# 1. Progressão Cognitiva Educacional
adicionar_dimensao(
    "Progressão Cognitiva Educacional",
    "Adaptado de Anderson e Krathwohl (2001), com base em Bloom (1956).",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["Taxonomia de Bloom"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Lida apenas com informações simples, memorizadas ou repetidas, com baixa mobilização cognitiva."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Compreende conceitos básicos e consegue aplicá-los com apoio em situações familiares."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Analisa criticamente, estabelece relações e propõe explicações com base em dados ou conceitos."},
        {"nota": 4, "nome": "Avançado", "descricao": "Cria soluções inovadoras, faz sínteses e aplica conhecimentos de forma autônoma e transferível."}
    ],
    [
        "Alunos de Uberlândia elaboram um gráfico sobre a variação do clima na região e interpretam suas implicações no cotidiano.",
        "Turma de Ituiutaba desenvolve um projeto sobre o uso racional da água nas propriedades agrícolas do município.",
        "Estudantes de Patos de Minas apresentam soluções para o descarte correto de lixo em feiras livres da cidade."
    ]
)

# 2. Perfil Socioeconômico e Contextual
adicionar_dimensao(
    "Perfil Socioeconômico e Contextual",
    "Adaptado de BRASIL. INEP. Indicadores contextuais do SAEB (2017).",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["ESCS", "Rubrica SAEB"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Apresenta limitações severas de acesso e estímulo no contexto familiar e comunitário."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Vivencia condições mínimas de estrutura e apoio escolar/familiar, com participação eventual."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Apresenta estabilidade socioeconômica e utiliza recursos comunitários e escolares com autonomia."},
        {"nota": 4, "nome": "Avançado", "descricao": "Integra-se de forma ativa aos espaços escolares e sociais, com protagonismo e acesso ampliado a bens culturais e educacionais."}
    ],
    [
        "Estudantes de Araguari desenvolvem uma horta comunitária com apoio das famílias e da escola.",
        "Jovens da zona rural de Monte Alegre de Minas relatam a importância do transporte escolar para garantir frequência.",
        "Alunos de Iturama realizam visitas a museus e espaços culturais locais, integrando saberes escolares e regionais."
    ]
)

# 3. Autonomia e Autorregulação da Aprendizagem
adicionar_dimensao(
    "Autonomia e Autorregulação da Aprendizagem",
    "Adaptado de BRASIL. MEC. BNCC (2017) e SAEB (2017), com apoio em Flavell (1979) sobre metacognição.",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["BNCC", "SAEB", "Neuropsicopedagogia"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Depende inteiramente de orientações externas para realizar atividades."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Realiza tarefas com ajuda parcial, demonstrando esforço para se organizar."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Planeja suas ações, avalia resultados e corrige estratégias de forma crescente."},
        {"nota": 4, "nome": "Avançado", "descricao": "Demonstra domínio da gestão do próprio tempo, objetivos e estratégias de aprendizagem."}
    ],
    [
        "Alunos de Frutal criam cronogramas de estudos semanais sem mediação direta de professores.",
        "Estudantes de Sacramento organizam grupos de estudo autônomos para se prepararem para a OBMEP.",
        "Turmas de Canápolis fazem autoavaliações mensais de desempenho e ajustam suas rotinas escolares."
    ]
)

# 4. Capacidade de Comunicação e Expressão
adicionar_dimensao(
    "Capacidade de Comunicação e Expressão",
    "Adaptado de BRASIL. INEP. Resultados SAEB (2017) e OCDE. Relatório PISA (2022).",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["SAEB", "PISA", "Rubrica de Linguagens"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Expressa-se com vocabulário restrito, apresentando dificuldades de coesão, clareza e organização textual."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Comunica ideias em contextos conhecidos com vocabulário funcional, demonstrando estrutura básica de expressão."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Organiza e expressa argumentos de forma coerente e adequada ao gênero e situação comunicativa."},
        {"nota": 4, "nome": "Avançado", "descricao": "Produz discursos orais e escritos com riqueza vocabular, domínio discursivo e argumentação sólida, com foco social e educativo."}
    ],
    [
        "Alunos de Itapagipe fazem podcasts sobre a história dos quilombos do Triângulo Mineiro.",
        "Estudantes de Campina Verde produzem cartas argumentativas para reivindicar melhorias na escola.",
        "Turmas de Prata apresentam seminários sobre culturas tradicionais do Alto Paranaíba."
    ]
)

# As dimensões 5, 6, 7 e 8 continuam logo abaixo...
# 5. Raciocínio Lógico e Solução de Problemas
adicionar_dimensao(
    "Raciocínio Lógico e Solução de Problemas",
    "Adaptado de BRASIL. INEP. SAEB (2017) e OCDE. PISA (2022).",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["Rubrica SAEB", "Taxonomia SOLO", "PISA"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Aplica procedimentos simples sob mediação, com dificuldade em generalizar padrões ou inferir estratégias."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Resolve problemas estruturados com apoio, utilizando técnicas previamente ensinadas."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Aplica estratégias variadas com autonomia para resolver desafios do cotidiano escolar e comunitário."},
        {"nota": 4, "nome": "Avançado", "descricao": "Cria soluções originais para problemas reais, articulando dados, lógica e criatividade com base em múltiplas abordagens."}
    ],
    [
        "Alunos de Coromandel resolvem problemas matemáticos usando dados da produção de leite local.",
        "Estudantes de Patrocínio simulam cálculos para organizar a logística de uma feira de ciências.",
        "Turmas de Tupaciguara desenvolvem jogos lógicos inspirados em desafios do cotidiano da cidade."
    ]
)

# 6. Engajamento e Responsabilidade Social
adicionar_dimensao(
    "Engajamento e Responsabilidade Social",
    "Adaptado de OCDE (2022), BRASIL. INEP (2017), com apoio em autores como Paulo Freire (1996).",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["SAEB", "PISA", "Freire", "Justiça Social"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Participa de forma limitada e reativa, com baixo envolvimento nas ações coletivas escolares."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Colabora quando solicitado, demonstrando sensibilidade inicial para ações em grupo e ética social."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Compromete-se ativamente com propostas coletivas e busca resolver conflitos de forma empática e construtiva."},
        {"nota": 4, "nome": "Avançado", "descricao": "Lidera ações sociais e educativas com intencionalidade transformadora e compromisso com o bem coletivo local."}
    ],
    [
        "Estudantes de Nova Ponte organizam campanha de arrecadação de agasalhos no inverno.",
        "Alunos de Conceição das Alagoas realizam mutirão para revitalizar espaços da escola.",
        "Turmas de Uberaba promovem debates sobre combate ao racismo em comunidades locais."
    ]
)

# 7. Relacionamento com Saberes Científicos e Culturais
adicionar_dimensao(
    "Relacionamento com Saberes Científicos e Culturais",
    "Adaptado de BRASIL. INEP. Resultados SAEB (2017) e OCDE. Relatório PISA (2022), com apoio da BNCC (2017).",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["BNCC", "SAEB", "PISA", "Rubrica CTC"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Participa de atividades culturais e científicas como espectador, sem articulação crítica ou aprofundamento."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Reconhece saberes tradicionais e científicos com apoio docente, valorizando a diversidade de fontes e práticas."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Relaciona de forma autônoma conhecimentos escolares com manifestações culturais e científicas locais."},
        {"nota": 4, "nome": "Avançado", "descricao": "Integra criticamente saberes diversos, propondo soluções e ações educativas de valorização territorial e cultural."}
    ],
    [
        "Alunos de Araxá fazem uma releitura científica das propriedades terapêuticas da lama da região.",
        "Estudantes de Lagoa Formosa elaboram projetos sobre festas religiosas como patrimônio imaterial.",
        "Turmas de Perdizes comparam técnicas de cultivo tradicionais com a agricultura de precisão."
    ]
)

# 8. Pertencimento e Equidade Territorial (CTC + EJI + ESCS)
adicionar_dimensao(
    "Pertencimento e Equidade Territorial (CTC + EJI + ESCS)",
    "Adaptado de BRASIL. MEC. BNCC (2017), CNE/CEB (2011), DCNs para Educação do Campo (2010) e Quilombola (2012).",
    "Adaptação realizada pelo autor deste trabalho em 2025.",
    ["CTC", "EJI", "ESCS", "Rubrica de Justiça Social"],
    [
        {"nota": 1, "nome": "Emergente", "descricao": "Apresenta baixa identificação com a cultura local e ausência de reconhecimento territorial ou étnico."},
        {"nota": 2, "nome": "Intermediário", "descricao": "Demonstra respeito à diversidade, mas ainda com postura passiva frente às desigualdades."},
        {"nota": 3, "nome": "Proficiente", "descricao": "Reconhece as desigualdades históricas e atua em projetos de valorização de grupos sub-representados."},
        {"nota": 4, "nome": "Avançado", "descricao": "Assume postura ativa na promoção da equidade, identidade territorial e justiça social em contextos diversos."}
    ],
    [
        "Estudantes de comunidades quilombolas em Gurinhatã desenvolvem um projeto de mapeamento cultural da região com valorização da memória oral e patrimônio local.",
        "Jovens indígenas em São João das Missões propõem um plano de acessibilidade e representatividade no grêmio estudantil.",
        "Alunos de escolas do campo em Monte Alegre de Minas criam uma feira territorial com produtos, saberes e práticas tradicionais da agricultura familiar local."
    ]
)

# === Salvar JSON ===
with open("rubrica_sinapse_ia_v1_3_padronizada.json", "w", encoding="utf-8") as f:
    json.dump(rubrica, f, ensure_ascii=False, indent=2)

print("✅ Rubrica v1.3 padronizada salva com sucesso!")


