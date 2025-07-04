from pymongo import MongoClient

# Conectar ao MongoDB dockerizado
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["avaliacao_rar_sinapse_ia"]

# Dados A5 e A6 por juiz
avaliacoes_a5_a6 = {
    "Dirceu Nogueira de Sales Duarte Júnior": {
        "apoio_metacognicao": "4",
        "engajamento_estudantil": "4",
        "comentario_a5_a6": "A rubrica estimula fortemente a reflexão crítica do aluno e propõe estratégias que favorecem o protagonismo estudantil."
    },
    "Fernanda Costa": {
        "apoio_metacognicao": "3",
        "engajamento_estudantil": "3",
        "comentario_a5_a6": "Há incentivo à metacognição, mas faltam instruções mais claras. O engajamento é mencionado, mas pouco operacionalizado."
    },
    "Eduardo Denuncio": {
        "apoio_metacognicao": "4",
        "engajamento_estudantil": "4",
        "comentario_a5_a6": "A dimensão promove excelente articulação entre reflexão, ação e engajamento, com propostas aplicáveis em sala de aula."
    },
    "Lucas Almeida": {
        "apoio_metacognicao": "4",
        "engajamento_estudantil": "3",
        "comentario_a5_a6": "Metacognição bem estruturada. O engajamento é citado, mas poderia ser melhor evidenciado nos exemplos."
    },
    "Sandra Regina": {
        "apoio_metacognicao": "3",
        "engajamento_estudantil": "4",
        "comentario_a5_a6": "Utiliza bem metodologias ativas que promovem engajamento. Poderia aprofundar estratégias de autorregulação do pensamento."
    },
    "Beatriz Monteiro": {
        "apoio_metacognicao": "3",
        "engajamento_estudantil": "3",
        "comentario_a5_a6": "O texto é sensível à inclusão e participação, mas falta estrutura para fomentar metacognição de forma clara."
    },
    "Rodrigo Bastos": {
        "apoio_metacognicao": "4",
        "engajamento_estudantil": "4",
        "comentario_a5_a6": "A dimensão conecta bem território, tempo e comunidade à autorreflexão e à participação ativa dos estudantes."
    },
    "Mariana Lopes": {
        "apoio_metacognicao": "4",
        "engajamento_estudantil": "3",
        "comentario_a5_a6": "Permite que os professores desenvolvam ações metacognitivas. O engajamento poderia ser fortalecido com práticas mais participativas."
    }
}

# Atualizar os documentos no banco
for nome_juiz, dados in avaliacoes_a5_a6.items():
    resultado = colecao.update_one(
        {"juiz_avaliador": nome_juiz},
        {"$set": dados}
    )
    print(f"✅ {nome_juiz} — Modificados: {resultado.modified_count}")

client.close()

