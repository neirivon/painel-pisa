# scriptos.path.join(s, "c")riar_questoes_pisa_tri_mineiro_completas.py

import json
import os

# Lista das 9 questões PISA contextualizadas com 3 por área
questoes = [
    # LEITURA
    {
        "questao_id": "L1",
        "area": "Leitura",
        "pergunta": "A Prefeitura de Uberaba lançou um edital para revitalização do Museu do Zebu. Com base em um trecho do jornal local que relata o valor histórico do museu, explique por que a revitalização é importante para a identidade da região.",
        "resposta_modelo": "A revitalização do Museu do Zebu é importante pois resgata a memória histórica da pecuária local, um dos pilares econômicos e culturais da região.",
        "resposta_mediana": "O museu é importante porque fala das coisas antigas da região.",
        "resposta_inadequada": "Eu nunca fui nesse museu. Acho que nem sei onde fica.",
        "dimensoes_avaliadas": ["CTC + ESCS", "Taxonomia de Bloom"]
    },
    {
        "questao_id": "L2",
        "area": "Leitura",
        "pergunta": "O jornal de Ituiutaba publicou uma crônica sobre a importância das feiras livres para a cultura local. Relacione o papel das feiras com a construção da identidade da cidade.",
        "resposta_modelo": "As feiras são espaços onde se compartilham saberes e tradições alimentares, reforçando a cultura local e o pertencimento social.",
        "resposta_mediana": "Feiras são importantes porque vendem comida boa.",
        "resposta_inadequada": "Minha vó vai na feira, mas eu não gosto do cheiro.",
        "dimensoes_avaliadas": ["CTC + ESCS", "Perfil Neuropsicopedagógico"]
    },
    {
        "questao_id": "L3",
        "area": "Leitura",
        "pergunta": "Leia um trecho sobre o desenvolvimento urbano de Uberlândia. Como o texto apresenta os desafios enfrentados pela cidade com o crescimento populacional?",
        "resposta_modelo": "O texto mostra problemas como trânsito, consumo de água e pressão sobre serviços públicos, reforçando a importância do planejamento urbano.",
        "resposta_mediana": "Uberlândia cresceu e agora tem mais problemas com ônibus.",
        "resposta_inadequada": "Eu prefiro cidade pequena com fazenda.",
        "dimensoes_avaliadas": ["Bloom", "DUA"]
    },

    # MATEMÁTICA
    {
        "questao_id": "M1",
        "area": "Matemática",
        "pergunta": "Durante a Fenamilho em Patos de Minas, cada visitante consome em média 1,2 kg de alimentos. Se a expectativa é de 85 mil visitantes, estime quantas toneladas de alimentos serão consumidas durante o evento.",
        "resposta_modelo": "85.000 x 1,2 = 102.000 kg = 102 toneladas. Mostra impacto econômico e logístico do evento.",
        "resposta_mediana": "Dá umas 100 mil quilos.",
        "resposta_inadequada": "Nunca fui na Fenamilho.",
        "dimensoes_avaliadas": ["Taxonomia SOLO", "DUA"]
    },
    {
        "questao_id": "M2",
        "area": "Matemática",
        "pergunta": "Em uma plantação de café em Araguari, um agricultor colhe 28 sacas por hectare. Se ele possui 15 hectares, quantas sacas ele colherá no total?",
        "resposta_modelo": "Ele colherá 420 sacas, pois 28 x 15 = 420.",
        "resposta_mediana": "Dá umas 400 sacas, mais ou menos.",
        "resposta_inadequada": "Não gosto de café nem de matemática.",
        "dimensoes_avaliadas": ["Taxonomia de Bloom", "Metodologia Ativa"]
    },
    {
        "questao_id": "M3",
        "area": "Matemática",
        "pergunta": "Durante a ExpoZebu em Uberaba, foram vendidos 1.250 ingressos na sexta-feira e 2.340 no sábado. Qual a diferença entre os dois dias e o total vendido no fim de semana?",
        "resposta_modelo": "Diferença: 1.090. Total: 3.590 ingressos.",
        "resposta_mediana": "Sábado vendeu mais. Juntando dá quase 4 mil.",
        "resposta_inadequada": "ExpoZebu só tem boi. Nunca fui.",
        "dimensoes_avaliadas": ["Taxonomia SOLO", "DUA"]
    },

    # CIÊNCIAS
    {
        "questao_id": "C1",
        "area": "Ciências",
        "pergunta": "Em cidades como Ituiutaba e Araxá, a falta de chuvas afeta a agricultura. Cite uma ação que os moradores dessas regiões podem adotar para preservar os recursos hídricos.",
        "resposta_modelo": "Instalar cisternas e evitar desperdícios contribui para a sustentabilidade hídrica.",
        "resposta_mediana": "Dá pra economizar água e não tomar banho demorado.",
        "resposta_inadequada": "Chove pouco mesmo. Não tem o que fazer.",
        "dimensoes_avaliadas": ["Metodologia Ativa", "CTC + ESCS"]
    },
    {
        "questao_id": "C2",
        "area": "Ciências",
        "pergunta": "No Triângulo Mineiro, muitos rios estão com baixo volume. Explique como a ação humana influencia diretamente na diminuição do nível dos rios.",
        "resposta_modelo": "Uso excessivo da água, desmatamento e poluição reduzem o volume dos rios.",
        "resposta_mediana": "As pessoas pegam muita água dos rios.",
        "resposta_inadequada": "Rios secam por causa do calor, uai.",
        "dimensoes_avaliadas": ["CTC + ESCS", "Taxonomia SOLO"]
    },
    {
        "questao_id": "C3",
        "area": "Ciências",
        "pergunta": "Uma escola de Monte Carmelo iniciou a coleta seletiva. Explique como essa ação pode contribuir com o meio ambiente e com a comunidade local.",
        "resposta_modelo": "Reduz lixo em aterros, permite reciclagem, gera renda e educação ambiental.",
        "resposta_mediana": "Ajuda o meio ambiente porque o lixo vai pro lugar certo.",
        "resposta_inadequada": "Na minha escola nem tem lixo direito.",
        "dimensoes_avaliadas": ["Neuropsicopedagógico", "DUA"]
    }
]

# Caminho de saída
saida = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "P")ISos.path.join(A, "d")ados_processadoos.path.join(s, "q")uestoes/"))
os.makedirs(saida, exist_ok=True)
arquivo_json = os.path.join(saida, "questoes_pisa_tri_mineiro_completas.json")

with open(arquivo_json, "w", encoding="utf-8") as f:
    json.dump(questoes, f, indent=2, ensure_ascii=False)

print("✅ Arquivo criado com sucesso!")
print(f"🧾 JSON: {arquivo_json}")

