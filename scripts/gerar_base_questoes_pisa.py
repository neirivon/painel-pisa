import json
import pandas as pd
import os

# =============================
# Caminho base (modo cloud)
# =============================
PASTA_SAIDA = "painel_pisos.path.join(a, "u")tilos.path.join(s, "d")ados_clouos.path.join(d, "r")espostas"
os.makedirs(PASTA_SAIDA, exist_ok=True)

# =============================
# Questões adaptadas do PISA
# =============================
questoes = [
    # LEITURA
    {
        "area": "Leitura",
        "codigo": "L01",
        "pergunta": "A prefeitura de sua cidade publicou um novo regulamento para o transporte escolar. Ele deve garantir o acesso equitativo de todos os alunos, especialmente os das zonas rurais. Com base nesse regulamento, discuta os principais desafios e benefícios para os estudantes da sua região.",
        "resumo_resposta_correta": "Descreve desigualdade de acesso, destaca melhorias no trajeto e segurança.",
        "tags_rubrica": ["Contextualização", "Análise Crítica", "Solução Proposta"]
    },
    {
        "area": "Leitura",
        "codigo": "L02",
        "pergunta": "Leia uma notícia sobre um novo aplicativo de leitura digital adotado nas escolas públicas. Com base nisso, analise os impactos positivos e possíveis limitações dessa medida.",
        "resumo_resposta_correta": "Aponta facilidade de acesso, mas ressalta carência tecnológica de algumas famílias.",
        "tags_rubrica": ["Análise de Texto", "Leitura Digital", "Inclusão"]
    },
    {
        "area": "Leitura",
        "codigo": "L03",
        "pergunta": "Um poema sobre a vida no campo foi apresentado em sala de aula. Que relações você consegue estabelecer entre esse poema e a realidade da sua comunidade?",
        "resumo_resposta_correta": "Relaciona versos do poema com aspectos culturais e cotidianos do campo local.",
        "tags_rubrica": ["Interpretação", "Relação Texto-Realidade", "Expressão"]
    },

    # MATEMÁTICA
    {
        "area": "Matemática",
        "codigo": "M01",
        "pergunta": "Durante um evento cultural da sua região, 12 municípios contribuíram proporcionalmente com recursos. O total arrecadado foi de R$ 360.000. Explique como dividir esse valor de forma justa com base no número de estudantes de cada município e quais desafios essa divisão poderia apresentar.",
        "resumo_resposta_correta": "Usa regra de três para divisão proporcional. Menciona desigualdades populacionais.",
        "tags_rubrica": ["Raciocínio Proporcional", "Resolução de Problemas", "Justiça"]
    },
    {
        "area": "Matemática",
        "codigo": "M02",
        "pergunta": "Um gráfico mostra a evolução da taxa de alfabetização no Brasil. Analise esse gráfico e discuta o que ele revela sobre a educação ao longo dos anos.",
        "resumo_resposta_correta": "Identifica crescimento, relaciona com políticas públicas e desigualdades regionais.",
        "tags_rubrica": ["Leitura de Gráficos", "Tendência", "Argumentação Quantitativa"]
    },
    {
        "area": "Matemática",
        "codigo": "M03",
        "pergunta": "Uma pesquisa revelou que 40% dos alunos da escola utilizam transporte público, 35% vão a pé e 25% usam transporte escolar. Proponha uma maneira de representar esses dados visualmente e comente os possíveis motivos dessa distribuição.",
        "resumo_resposta_correta": "Sugere gráfico de setores e interpreta os dados relacionando com infraestrutura local.",
        "tags_rubrica": ["Estatística", "Visualização", "Contextualização"]
    },

    # CIÊNCIAS
    {
        "area": "Ciências",
        "codigo": "C01",
        "pergunta": "As águas do rio Paranaíba têm apresentado variações na qualidade segundo estudos recentes. Proponha uma ação educativa local para envolver os estudantes e a comunidade na preservação ambiental da bacia hidrográfica.",
        "resumo_resposta_correta": "Sugere projeto escolar de monitoramento da água com envolvimento comunitário.",
        "tags_rubrica": ["Sustentabilidade", "Engajamento", "Educação Ambiental"]
    },
    {
        "area": "Ciências",
        "codigo": "C02",
        "pergunta": "Um agricultor usa pesticidas em excesso na plantação. Quais os impactos dessa prática e quais alternativas sustentáveis poderiam ser adotadas?",
        "resumo_resposta_correta": "Aponta contaminação do solo e propõe controle biológico como alternativa.",
        "tags_rubrica": ["Ciência aplicada", "Saúde ambiental", "Soluções"]
    },
    {
        "area": "Ciências",
        "codigo": "C03",
        "pergunta": "A pandemia de COVID-19 trouxe à tona a importância da vacinação. Explique como as vacinas funcionam e por que são fundamentais para a saúde pública.",
        "resumo_resposta_correta": "Descreve o mecanismo das vacinas e a imunidade coletiva.",
        "tags_rubrica": ["Imunização", "Saúde Coletiva", "Compreensão científica"]
    }
]

# =============================
# Salvar JSON e CSV no local correto
# =============================
with open(os.path.join(PASTA_SAIDA, "questoes_pisa_completas.json"), "w", encoding="utf-8") as f:
    json.dump(questoes, f, ensure_ascii=False, indent=2)

df = pd.DataFrame(questoes)
df.to_csv(os.path.join(PASTA_SAIDA, "questoes_pisa_completas.csv"), index=False)

# =============================
# Salvar respostas exemplo por área (txt)
# =============================
respostas_txt = ""

for q in questoes:
    respostas_txt += f"Área: {q['area']} | Código: {q['codigo']}\n"
    respostas_txt += f"Pergunta: {q['pergunta']}\n"
    respostas_txt += f"- ✅ Resposta Correta (resumida): {q['resumo_resposta_correta']}\n"
    respostas_txt += f"- ⚠️ Resposta com erros: [Inclui ideias desconexas ou erros conceituais]\n"
    respostas_txt += f"- ❌ Resposta fora do tema: [Totalmente alheia ao conteúdo da pergunta]\n\n"

with open(os.path.join(PASTA_SAIDA, "respostas_exemplo_por_area.txt"), "w", encoding="utf-8") as f:
    f.write(respostas_txt)

print("✅ Arquivos salvos em:", PASTA_SAIDA)

