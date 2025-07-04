from IPython.display import display, Markdown

# Redefinir conteúdo após reset
rubrica_md = """
# 📊 Rubrica Avaliativa Integrada – PISA/SAEB

| Critério                  | Descrição                                                                 | Indicadores (PISA/SAEB)                                                  | Nível Bloom Associado     | Sinalização de Ação                                                                 |
|--------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------|---------------------------|-------------------------------------------------------------------------------------|
| **Domínio de Leitura**   | Capacidade de interpretar, localizar e inferir informações em textos.     | - PISA: PV1READ < 400<br>- SAEB: Língua Portuguesa < 225                 | Compreender / Analisar    | 🔴 Necessita intervenção urgente com metodologias de leitura crítica.              |
| **Raciocínio Matemático**| Resolver problemas envolvendo números e operações.                         | - PISA: PV1MATH < 420<br>- SAEB: Matemática < 225                        | Aplicar / Analisar        | 🟠 Reforço com estratégias ativas e resolução de problemas.                         |
| **Capacidade Científica**| Interpretar fenômenos naturais com base em evidências.                     | - PISA: PV1SCIE < 430<br>- SAEB: Ciências < 225                          | Analisar / Avaliar        | 🟡 Projetos investigativos e interdisciplinares.                                   |
| **Desempenho Socioeconômico**| Relação entre contexto ESCS e desempenho.                               | - ESCS < 0,0 e desempenho abaixo da média nacional                       | Avaliar                   | 🔵 Ações de equidade e reforço com materiais inclusivos.                            |
| **Pensamento Crítico**   | Demonstração de ideias, argumentação e propostas inovadoras.               | - Textos com predominância de nível **Criar** (Taxonomia de Bloom)      | Criar                     | 🟢 Ampliar projetos, currículo por competências, feiras e laboratórios.            |

## 📌 Legenda de Sinalização:
- 🔴 Crítico – intervenção urgente
- 🟠 Atenção – reforço necessário
- 🟡 Potencial – desenvolver com foco pedagógico
- 🔵 Equidade – estratégias compensatórias
- 🟢 Excelente – replicação e ampliação

**Fontes**:  
- OCDE. *Relatórios Técnicos PISA (2000–2022)*  
- INEP. *Relatórios Nacionais PISA e Microdados SAEB*  
- Anderson, L. W., & Krathwohl, D. R. (2001). *A Taxonomia de Bloom Revisada*
"""

display(Markdown(rubrica_md))

