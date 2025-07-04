# scriptos.path.join(s, "r")ubrica_sinapse_v6_adaptada.py

import os
import pandas as pd
import json

# Estrutura da Rubrica SINAPSE v6 ajustada para nota máxima por IA e professores humanos
rubrica_v6_adaptada = [
    {
        "dimensao": "Taxonomia de Bloom",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Demonstra reconhecimento ou repetição de conceitos sem elaboração." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Compreende os conceitos e os reorganiza de forma básica." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Aplica e analisa conceitos em novos contextos com coerência." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Cria, avalia e propõe ideias originais com profundidade crítica." }
        ]
    },
    {
        "dimensao": "Taxonomia SOLO",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Expressa uma única ideia desconectada (uniestrutural)." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Lista ideias múltiplas sem articulação entre elas (multiestrutural)." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Conecta ideias de forma lógica e estruturada (relacional)." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Generaliza, extrapola ou sintetiza com abstração (abstrato estendido)." }
        ]
    },
    {
        "dimensao": "Perfil Neuropsicopedagógico",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Apresenta dificuldades na organização, coesão e clareza textual." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Expressa com estrutura básica e vocabulário funcional." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Demonstra fluidez, coerência e inferência entre ideias." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Elabora textos com abstrações, metáforas e pensamento complexo." }
        ]
    },
    {
        "dimensao": "DUA – Desenho Universal para Aprendizagem",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Utiliza uma forma limitada de representação e expressão." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Apresenta ideias com vocabulário acessível e poucos recursos." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Integra textos, imagens e outras linguagens para reforçar ideias." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Explora múltiplas formas expressivas com clareza e intencionalidade." }
        ]
    },
    {
        "dimensao": "Metodologia Ativa",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Demonstra resposta passiva, sem tentativa de ação." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Aponta estratégia simples com alguma conexão ao problema." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Aplica estratégias para resolver, adaptar ou propor soluções." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Inova, problematiza ou colabora com soluções críticas e bem fundamentadas." }
        ]
    },
    {
        "dimensao": "Pertencimento e Equidade Territorial (CTC + ESCS)",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Ignora ou não reconhece elementos do território e cultura local." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Reconhece o território, mas ainda sem articulação crítica." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Relaciona saberes escolares com a vivência cultural e local." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Valoriza criticamente o território e propõe soluções com protagonismo sociocultural." }
        ]
    }
]

# Exportar dados para CSV e JSON
linhas = []
for item in rubrica_v6_adaptada:
    for rub in item["rubricas"]:
        linhas.append({
            "Dimensão": item["dimensao"],
            "Nível": rub["nivel"],
            "Nome do Nível": rub["titulo"],
            "Descritor": rub["descricao"]
        })

df = pd.DataFrame(linhas)

saida_dir = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "d")ados_processadoos.path.join(s, "r")ubricas/"))
os.makedirs(saida_dir, exist_ok=True)

csv_path = os.path.join(saida_dir, "rubrica_sinapse_v6_adaptada.csv")
json_path = os.path.join(saida_dir, "rubrica_sinapse_v6_adaptada.json")

df.to_csv(csv_path, index=False)
df.to_json(json_path, orient="records", indent=2)

csv_path, json_path

