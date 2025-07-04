from pymongo import MongoClient
from datetime import datetime

# Conexão com MongoDB dockerizado
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["rubricas"]
colecao = db["avaliacao_rar_sinapse_ia"]

avaliacoes = [
    {
        "juiz_avaliador": "Dirceu Nogueira de Sales Duarte Júnior",
        "email_do_juiz_avaliador": "dirceu@ufu.br",
        "dimensao_avaliada": "Progressão Cognitiva Emocional",
        "clareza_e_objetividade": "4",
        "coerencia_entre_descritores": "4",
        "adequacao_a_pratica_pedagogica": "4",
        "alinhamento_entidades_normativas_e_avaliativas": "4",
        "originalidade_e_contribuicao": "4",
        "comentario": "Exemplar",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8014:e4e4:d387:fa63"
    },
    {
        "juiz_avaliador": "Fernanda Costa",
        "email_do_juiz_avaliador": "fernanda@ufu.br",
        "dimensao_avaliada": "Desenvolvimento da Autonomia e Protagonismo",
        "clareza_e_objetividade": "3",
        "coerencia_entre_descritores": "4",
        "adequacao_a_pratica_pedagogica": "3",
        "alinhamento_entidades_normativas_e_avaliativas": "4",
        "originalidade_e_contribuicao": "3",
        "comentario": "Possui bons exemplos, mas poderia detalhar mais sobre o protagonismo estudantil.",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8024:e4e4:d387:fa63"
    },
    {
        "juiz_avaliador": "Eduardo Denuncio",
        "email_do_juiz_avaliador": "eduardo@ufu.br",
        "dimensao_avaliada": "Interdisciplinaridade e Transversalidade",
        "clareza_e_objetividade": "4",
        "coerencia_entre_descritores": "3",
        "adequacao_a_pratica_pedagogica": "4",
        "alinhamento_entidades_normativas_e_avaliativas": "4",
        "originalidade_e_contribuicao": "4",
        "comentario": "Muito bem estruturada para integrar projetos interdisciplinares.",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8034:e4e4:d387:fa63"
    },
    {
        "juiz_avaliador": "Lucas Almeida",
        "email_do_juiz_avaliador": "lucas@ufu.br",
        "dimensao_avaliada": "Progressão Cognitiva Educacional",
        "clareza_e_objetividade": "4",
        "coerencia_entre_descritores": "4",
        "adequacao_a_pratica_pedagogica": "3",
        "alinhamento_entidades_normativas_e_avaliativas": "4",
        "originalidade_e_contribuicao": "4",
        "comentario": "Os níveis estão bem estruturados e conectados com a Taxonomia de Bloom.",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8064:e4a4:d377:fa63"
    },
    {
        "juiz_avaliador": "Sandra Regina",
        "email_do_juiz_avaliador": "sandra@ufu.br",
        "dimensao_avaliada": "Diversidade de Abordagens Didáticas",
        "clareza_e_objetividade": "3",
        "coerencia_entre_descritores": "4",
        "adequacao_a_pratica_pedagogica": "4",
        "alinhamento_entidades_normativas_e_avaliativas": "3",
        "originalidade_e_contribuicao": "4",
        "comentario": "Abrange bem metodologias ativas como gamificação e problematização.",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8074:e4a4:d377:fa63"
    },
    {
        "juiz_avaliador": "Beatriz Monteiro",
        "email_do_juiz_avaliador": "beatriz@ufu.br",
        "dimensao_avaliada": "Inclusão e Acessibilidade (DUA)",
        "clareza_e_objetividade": "4",
        "coerencia_entre_descritores": "3",
        "adequacao_a_pratica_pedagogica": "4",
        "alinhamento_entidades_normativas_e_avaliativas": "4",
        "originalidade_e_contribuicao": "3",
        "comentario": "A dimensão respeita o Desenho Universal para Aprendizagem e tem bons exemplos inclusivos.",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8084:e4a4:d377:fa63"
    },
    {
        "juiz_avaliador": "Rodrigo Bastos",
        "email_do_juiz_avaliador": "rodrigo@ufu.br",
        "dimensao_avaliada": "Contextualização Crítica (CTC)",
        "clareza_e_objetividade": "3",
        "coerencia_entre_descritores": "3",
        "adequacao_a_pratica_pedagogica": "4",
        "alinhamento_entidades_normativas_e_avaliativas": "4",
        "originalidade_e_contribuicao": "4",
        "comentario": "Explora bem a articulação entre território, tempo e comunidade.",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8094:e4a4:d377:fa63"
    },
    {
        "juiz_avaliador": "Mariana Lopes",
        "email_do_juiz_avaliador": "mariana@ufu.br",
        "dimensao_avaliada": "Taxonomia SOLO (Profundidade)",
        "clareza_e_objetividade": "4",
        "coerencia_entre_descritores": "4",
        "adequacao_a_pratica_pedagogica": "3",
        "alinhamento_entidades_normativas_e_avaliativas": "4",
        "originalidade_e_contribuicao": "3",
        "comentario": "A dimensão está bem definida e facilita a aplicação prática por professores.",
        "hash": "",
        "data": datetime.utcnow().isoformat(),
        "navegador": "Mozilla/5.0",
        "sistema_operacional": "Linux x86_64",
        "idioma": "pt-BR",
        "ip_publico": "2804:1e68:c211:6b02:8104:e4a4:d377:fa63"
    }
]

resultado = colecao.insert_many(avaliacoes)
print("Documentos inseridos com os IDs:", resultado.inserted_ids)

client.close()

