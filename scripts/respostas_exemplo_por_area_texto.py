import os

# Diretório de destino
caminho_saida = "dados_processadoos.path.join(s, "r")ubricas"
os.makedirs(caminho_saida, exist_ok=True)

# Caminho completo do arquivo
arquivo_txt = os.path.join(caminho_saida, "respostas_exemplo_por_area.txt")

# Conteúdo completo
conteudo = """
Área: Leitura
Pergunta: A prefeitura de sua cidade publicou um novo regulamento para o transporte escolar. Ele deve garantir o acesso equitativo de todos os alunos, especialmente os das zonas rurais. Com base nesse regulamento, discuta os principais desafios e benefícios para os estudantes da sua região.
✅ Correta: O novo regulamento beneficia estudantes da zona rural ao garantir acesso regular às escolas, mas enfrenta desafios como infraestrutura e orçamento limitado.
❌ Com erros: O regulamento ajuda alunos das cidades pequenas, mas não resolve tudo porque pode faltar ônibus ou motorista para pegar todo mundo.
❌ Fora do tema: Gosto muito de esportes e acho que todos deveriam praticar mais atividades físicas.

Pergunta: A escola da sua cidade decidiu reformular o currículo para incluir mais atividades de leitura crítica. Explique como essa mudança pode impactar o aprendizado dos alunos.
✅ Correta: A leitura crítica ajuda os alunos a desenvolverem pensamento analítico, interpretação de textos e maior compreensão social.
❌ Com erros: A leitura crítica é legal porque a gente lê mais livros e tem menos matemática, o que é bom pra quem gosta de português.
❌ Fora do tema: Acho que a cantina da escola devia vender sucos naturais e não só refrigerantes.

Pergunta: Um jornal local publicou uma matéria com opiniões diferentes sobre a proibição do uso de celulares em sala de aula. Com base no texto, argumente sua posição sobre o tema.
✅ Correta: A proibição de celulares pode melhorar a concentração, mas é importante discutir formas pedagógicas de integrar a tecnologia à sala de aula.
❌ Com erros: Celular é ruim pra aula porque os alunos jogam e não prestam atenção, então tem que tirar mesmo.
❌ Fora do tema: Eu gosto de usar celular para escutar música, principalmente rap nacional.

Área: Matemática
Pergunta: Durante um evento cultural da sua região, 12 municípios contribuíram proporcionalmente com recursos. O total arrecadado foi de R$ 360.000. Explique como dividir esse valor de forma justa com base no número de estudantes de cada município e quais desafios essa divisão poderia apresentar.
✅ Correta: A divisão proporcional garante justiça, mas é preciso ter dados confiáveis do número de estudantes por município para evitar desigualdades.
❌ Com erros: Dividir igual pra todo mundo é justo porque todo mundo participou, mesmo que tenha mais ou menos aluno.
❌ Fora do tema: Minha cidade faz ótimas festas juninas com comidas típicas e quadrilhas animadas.

Pergunta: Uma escola precisa comprar 300 livros com um orçamento de R$ 4.500. Qual seria o custo médio por livro e como lidar com variações de preço?
✅ Correta: O custo médio por livro é R$ 15. É necessário negociar preços com fornecedores e prever margem para livros mais caros.
❌ Com erros: Dá pra comprar uns livros baratos e outros caros, e aí vê no que dá no final.
❌ Fora do tema: Livros de romance são os melhores, principalmente os de drama e mistério.

Pergunta: Uma pesquisa sobre hábitos alimentares revelou que 25% dos alunos preferem lanches saudáveis. Crie uma proposta de cardápio baseada nesses dados.
✅ Correta: A proposta deve incluir frutas, sucos naturais e alimentos integrais, atendendo aos 25% e incentivando hábitos saudáveis para todos.
❌ Com erros: Comer saudável é importante, então pode ter salada todo dia, mesmo que ninguém goste.
❌ Fora do tema: Prefiro jogar videogame à tarde do que pensar no que vou comer no lanche.

Área: Ciências
Pergunta: As águas do rio Paranaíba têm apresentado variações na qualidade segundo estudos recentes. Proponha uma ação educativa local para envolver os estudantes e a comunidade na preservação ambiental da bacia hidrográfica.
✅ Correta: Promover campanhas de conscientização nas escolas, visitas ao rio e projetos de coleta de resíduos são estratégias educativas eficazes.
❌ Com erros: Tem que limpar o rio com sabão ou fazer as crianças pegarem o lixo com a mão.
❌ Fora do tema: Seria bom se tivesse mais parquinhos na cidade para as crianças brincarem ao ar livre.

Pergunta: Uma escola realizou um experimento para medir a quantidade de dióxido de carbono em diferentes ambientes. Analise os resultados e explique o que pode ser feito para melhorar a qualidade do ar.
✅ Correta: Ambientes fechados tendem a concentrar mais CO₂, por isso é importante ventilar as salas e usar plantas para purificar o ar.
❌ Com erros: Dá pra usar desodorante pra deixar o ar com cheiro bom e aí resolve tudo.
❌ Fora do tema: Acho que as pessoas deveriam andar mais de bicicleta para fazer exercício.

Pergunta: Uma cidade registrou aumento de doenças transmitidas por mosquitos. Elabore uma proposta de intervenção para reduzir os focos do mosquito.
✅ Correta: Ações como mutirões de limpeza, orientação nas escolas e fiscalização de criadouros podem reduzir a incidência de doenças.
❌ Com erros: Dá pra usar spray nas ruas que os mosquitos somem, e a prefeitura devia comprar mais veneno.
❌ Fora do tema: Na minha casa todo mundo gosta de assistir novela depois do jantar.
"""

# Salvando no arquivo
with open(arquivo_txt, "w", encoding="utf-8") as f:
    f.write(conteudo.strip())

print(f"✅ Arquivo gerado: {arquivo_txt}")

