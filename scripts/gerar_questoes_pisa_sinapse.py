# scriptos.path.join(s, "g")erar_questoes_pisa_sinapse.py

import os
import json
import pandas as pd

# Dados manualmente estruturados a partir do .txt
questoes = [
    # LEITURA
    {
        "area": "Leitura",
        "numero": 1,
        "pergunta": "A prefeitura de sua cidade publicou um novo regulamento para o transporte escolar. Ele deve garantir o acesso equitativo de todos os alunos, especialmente os das zonas rurais. Com base nesse regulamento, discuta os principais desafios e benefícios para os estudantes da sua região.",
        "resposta_correta": "O novo regulamento beneficia estudantes da zona rural ao garantir acesso regular às escolas, mas enfrenta desafios como infraestrutura e orçamento limitado.",
        "resposta_com_erros": "O novo regulamento pretende ajudar os alunos, mas não leva em conta a falta de ônibus ou as estradas precárias corretamente.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    {
        "area": "Leitura",
        "numero": 2,
        "pergunta": "Leia um artigo de opinião sobre redes sociais e debata como essas plataformas influenciam a opinião pública em sua comunidade escolar.",
        "resposta_correta": "As redes sociais influenciam fortemente a opinião pública escolar ao amplificar temas sensíveis e disseminar informações sem verificação crítica.",
        "resposta_com_erros": "As redes sociais são importantes mas não sei bem como elas afetam a opinião dos colegas da escola.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    {
        "area": "Leitura",
        "numero": 3,
        "pergunta": "Um poema lido em sala expressa sentimentos de exclusão. Analise como o uso da linguagem poética colabora para essa sensação.",
        "resposta_correta": "O uso de metáforas e repetições no poema reforça sentimentos de exclusão e solidão do eu lírico.",
        "resposta_com_erros": "O poema usa algumas palavras que parecem tristes, mas não dá pra saber se ele quer dizer exclusão mesmo.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    # MATEMÁTICA
    {
        "area": "Matemática",
        "numero": 1,
        "pergunta": "Durante um evento cultural da sua região, 12 municípios contribuíram proporcionalmente com recursos. O total arrecadado foi de R$ 360.000. Explique como dividir esse valor de forma justa com base no número de estudantes de cada município e quais desafios essa divisão poderia apresentar.",
        "resposta_correta": "O valor deve ser dividido proporcionalmente ao número de estudantes, o que requer conhecer os dados populacionais. Pode haver conflitos sobre critérios de proporcionalidade.",
        "resposta_com_erros": "O dinheiro deve ser dividido igualmente para todos, mesmo que alguns municípios tenham mais alunos.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    {
        "area": "Matemática",
        "numero": 2,
        "pergunta": "Uma escola planeja construir uma quadra poliesportiva e precisa estimar os custos. Descreva como a matemática pode ajudar na elaboração desse orçamento.",
        "resposta_correta": "A matemática ajuda ao calcular área, volume de materiais, custos por metro quadrado e prever despesas extras com base em estimativas.",
        "resposta_com_erros": "Usa a matemática para medir o campo e depois colocar qualquer preço nos materiais.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    {
        "area": "Matemática",
        "numero": 3,
        "pergunta": "Compare duas formas diferentes de representar a mesma informação: gráfico de barras e tabela numérica. Qual facilita a interpretação?",
        "resposta_correta": "O gráfico facilita a visualização de tendências, enquanto a tabela é útil para dados exatos. A escolha depende do objetivo.",
        "resposta_com_erros": "Gráficos são mais legais e tabelas são difíceis de entender sempre.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    # CIÊNCIAS
    {
        "area": "Ciências",
        "numero": 1,
        "pergunta": "As águas do rio Paranaíba têm apresentado variações na qualidade segundo estudos recentes. Proponha uma ação educativa local para envolver os estudantes e a comunidade na preservação ambiental da bacia hidrográfica.",
        "resposta_correta": "Organizar mutirões escolares de coleta de resíduos e palestras sobre preservação, com foco na conscientização local.",
        "resposta_com_erros": "Ajudar com lixeiras e pedir pra não jogar lixo, mas não sei bem o que fazer além disso.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    {
        "area": "Ciências",
        "numero": 2,
        "pergunta": "Uma campanha nacional incentiva o uso racional de energia. Explique como as escolas podem participar dessa campanha com ações práticas.",
        "resposta_correta": "Escolas podem promover uso consciente de luz e eletrônicos, realizar campanhas de economia e oficinas de energia renovável.",
        "resposta_com_erros": "Apagar as luzes ajuda. Também usar menos celular. Acho que é isso.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    },
    {
        "area": "Ciências",
        "numero": 3,
        "pergunta": "Com o aumento da emissão de gases do efeito estufa, como as atitudes individuais e coletivas podem minimizar esse problema?",
        "resposta_correta": "Atitudes como reduzir consumo de carne, priorizar transporte coletivo e reutilizar materiais contribuem para a redução dos gases.",
        "resposta_com_erros": "As pessoas precisam fazer alguma coisa, tipo não usar carro e tal.",
        "resposta_fora_tema": "Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas."
    }
]

# Caminhos
os.makedirs("dados_processadoos.path.join(s, "r")ubricas", exist_ok=True)
path_json = "dados_processadoos.path.join(s, "r")ubricaos.path.join(s, "q")uestoes_pisa_sinapse.json"
path_csv = "dados_processadoos.path.join(s, "r")ubricaos.path.join(s, "q")uestoes_pisa_sinapse.csv"

# Salvar JSON
with open(path_json, "w", encoding="utf-8") as f:
    json.dump(questoes, f, ensure_ascii=False, indent=2)

# Salvar CSV
df = pd.DataFrame(questoes)
df.to_csv(path_csv, index=False, encoding="utf-8")

print("✅ Arquivos gerados com sucesso.")

