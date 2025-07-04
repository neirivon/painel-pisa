import json
from datetime import datetime

OUTPUT_PATH = "/home/neirivon/SINAPSE2.0/PISA/painel_pisa/dados_cloud/rubrica_sinapse_pedagogica_aluno.json"

rubrica_aluno = {
    "nome": "rubrica_sinapse_pedagogica_aluno",
    "versao": "v1.4",
    "publico": "aluno",
    "tipo": "pedagogica",
    "timestamp": datetime.now().isoformat(),
    "objetivo": "Orientar o aluno com base em cada dimensão da rubrica SINAPSE aplicada às questões do PISA 2022 adaptadas ao TMPA.",
    "dimensoes": [
        {
            "dimensao": "Capacidade de Comunicação e Expressão",
            "orientacao": "Explique suas ideias com clareza. Use palavras que ajudem o leitor a entender o que você quer dizer. Se possível, dê exemplos."
        },
        {
            "dimensao": "Raciocínio Lógico e Solução de Problemas",
            "orientacao": "Mostre como você pensou para resolver a questão. Explique o que fez e por quê. Se usou um cálculo ou uma regra, diga qual foi."
        },
        {
            "dimensao": "Relacionamento com Saberes Científicos e Culturais",
            "orientacao": "Tente relacionar o tema da questão com algo que você conhece da sua região, cultura ou comunidade. Isso mostra que você entende o conteúdo de forma mais ampla."
        },
        {
            "dimensao": "Progressão Cognitiva Educacional",
            "orientacao": "Procure ir além do básico: pense, conecte ideias, justifique suas respostas. Tente analisar e criar soluções próprias sempre que puder."
        },
        {
            "dimensao": "Engajamento e Responsabilidade Social",
            "orientacao": "Reflita sobre como o tema da questão pode ajudar a melhorar sua escola ou comunidade. Mostre que você se importa e tem ideias para contribuir."
        },
        {
            "dimensao": "Autonomia e Autorregulação da Aprendizagem",
            "orientacao": "Seja sincero na sua resposta. Planeje antes de escrever e revise depois. Isso mostra que você está aprendendo a aprender."
        },
        {
            "dimensao": "Perfil Socioeconômico e Contextual",
            "orientacao": "Pense em como o seu dia a dia influencia o que você sabe. Use experiências reais para explicar sua resposta, se fizer sentido."
        },
        {
            "dimensao": "Pertencimento e Equidade Territorial (CTC + EJI + ESCS)",
            "orientacao": "Fale com orgulho da sua cultura, território ou comunidade. Respeite as diferenças e mostre que todos têm valor."
        }
    ]
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(rubrica_aluno, f, ensure_ascii=False, indent=2)

print(f"✅ Rubrica pedagógica do aluno salva em: {OUTPUT_PATH}")

