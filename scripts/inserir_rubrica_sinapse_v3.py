from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scripos.path.join(t, "i")nserir_rubrica_sinapse_v3.py

import json
import csv
import os
from datetime import datetime
from pymongo import MongoClient
import pandas as pd

# === Caminhos ===
CAMINHO_SAIDA_JSON = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v3.json"
CAMINHO_SAIDA_CSV = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v3.csv"

# === Rubrica v3 SINAPSE ===
rubrica = [
    {
        "dimensao": "Taxonomia de Bloom",
        "versao": "v3",
        "fonte": "Elaborado pelos autores com base em BLOOM, B. S. Taxonomy of Educational Objectives. 1956.",
        "timestamp_versao": datetime.utcnow().isoformat(),
        "niveis": [
            {"nivel": "1", "nome": "Memorização", "descricao": "Recordação de fatos ou conceitos simples sem compreensão profunda."},
            {"nivel": "2", "nome": "Compreensão", "descricao": "Interpretação de significados, explicações ou exemplos com base em informações fornecidas."},
            {"nivel": "3", "nome": "Aplicação", "descricao": "Uso de conhecimento em situações novas ou na resolução de problemas simples."},
            {"nivel": "4", "nome": "Análise", "descricao": "Divisão de conceitos em partes, identificação de padrões, relações e inferências."},
            {"nivel": "5", "nome": "Síntese", "descricao": "Reorganização de informações para propor algo novo, como projetos ou planos."},
            {"nivel": "6", "nome": "Avaliação", "descricao": "Capacidade de emitir julgamentos críticos com base em critérios definidos."}
        ]
    },
    {
        "dimensao": "Taxonomia SOLO",
        "versao": "v3",
        "fonte": "Adaptado de BIGGS, J.; COLLIS, K. F. (1982). Evaluating the Quality of Learning.",
        "timestamp_versao": datetime.utcnow().isoformat(),
        "niveis": [
            {"nivel": "1", "nome": "Pré-estrutural", "descricao": "Sem compreensão relevante ou informação desconexa."},
            {"nivel": "2", "nome": "Uniestrutural", "descricao": "Compreensão de um único conceito ou aspecto."},
            {"nivel": "3", "nome": "Multiestrutural", "descricao": "Conhecimento de vários conceitos sem conexão explícita entre eles."},
            {"nivel": "4", "nome": "Relacional", "descricao": "Conexão entre conceitos formando uma estrutura coerente."},
            {"nivel": "5", "nome": "Abstrato estendido", "descricao": "Generalização e aplicação em novos contextos, além da estrutura aprendida."}
        ]
    },
    {
        "dimensao": "Metodologia Ativa Sugerida",
        "versao": "v3",
        "fonte": "Inspirado em Moran, J. M. (2007). A educação que desejamos.",
        "timestamp_versao": datetime.utcnow().isoformat(),
        "niveis": [
            {"nivel": "1", "nome": "Expositivo", "descricao": "Aulas centradas no professor, foco em transmissão de conteúdo."},
            {"nivel": "2", "nome": "Tarefas dirigidas", "descricao": "Atividades com pouca autonomia, guiadas por roteiros fixos."},
            {"nivel": "3", "nome": "Projetos orientados", "descricao": "Trabalhos com algum grau de investigação e colaboração."},
            {"nivel": "4", "nome": "Aprendizagem baseada em problemas", "descricao": "Desafios reais resolvidos com pesquisa, criatividade e colaboração."},
            {"nivel": "5", "nome": "Gamificação ou STEAM", "descricao": "Interatividade, ludicidade, ciência e protagonismo estudantil."}
        ]
    },
    {
        "dimensao": "Perfil Neuropsicopedagógico",
        "versao": "v3",
        "fonte": "Baseado em OLIVEIRA, C. R.; CEREJA, S. L. (2021). Fundamentos da Neuropsicopedagogia.",
        "timestamp_versao": datetime.utcnow().isoformat(),
        "niveis": [
            {"nivel": "1", "nome": "Baixa motivação", "descricao": "Pouco engajamento; dificuldades em sustentar atenção."},
            {"nivel": "2", "nome": "Memória auditiva ou sequencial", "descricao": "Aprende melhor por repetição e ritmo."},
            {"nivel": "3", "nome": "Perfil visual ou espacial", "descricao": "Processa melhor com imagens, esquemas, vídeos."},
            {"nivel": "4", "nome": "Raciocínio lógico predominante", "descricao": "Boa compreensão por lógica, estruturação e organização."},
            {"nivel": "5", "nome": "Alta autonomia e motivação intrínseca", "descricao": "Aprende por interesse, autorregulado, crítico e participativo."}
        ]
    },
    {
        "dimensao": "♿ DUA – Desenho Universal para Aprendizagem",
        "versao": "v3",
        "fonte": "CAST (2018). Universal Design for Learning Guidelines version 2.2.",
        "timestamp_versao": datetime.utcnow().isoformat(),
        "niveis": [
            {"nivel": "1", "nome": "Baixa acessibilidade", "descricao": "Barreiras sensoriais, físicas ou cognitivas presentes."},
            {"nivel": "2", "nome": "Ajustes pontuais", "descricao": "Adaptações feitas de forma isolada para alguns estudantes."},
            {"nivel": "3", "nome": "Acessibilidade parcial", "descricao": "Uso moderado de recursos como audiovisuais ou leitores."},
            {"nivel": "4", "nome": "Práticas inclusivas intencionais", "descricao": "Planejamento inclui múltiplos meios e estratégias."},
            {"nivel": "5", "nome": "Acessibilidade universal", "descricao": "Todos aprendem por múltiplos caminhos e recursos inclusivos."}
        ]
    },
    {
        "dimensao": "CTC – Contextualização Territorial e Cultural",
        "versao": "v3",
        "fonte": "Elaborado pelos autores. Referências: David Sobel, Petrônio Mendes, Walter Rodney, Boaventura de Sousa Santos.",
        "timestamp_versao": datetime.utcnow().isoformat(),
        "niveis": [
            {"nivel": "1", "nome": "Ausência de contextualização", "descricao": "Prática pedagógica genérica, sem vínculo territorial ou cultural."},
            {"nivel": "2", "nome": "Contextualização incipiente", "descricao": "Referências locais esparsas e pouco integradas."},
            {"nivel": "3", "nome": "Contextualização parcial", "descricao": "Atividades adaptadas com base em dados básicos do território."},
            {"nivel": "4", "nome": "Práticas integradas à cultura local", "descricao": "Projetos com base em história, saberes, meio ambiente e participação comunitária."},
            {"nivel": "5", "nome": "Educação territorialmente responsiva", "descricao": "Planejamento e avaliação feitos com a comunidade e com base em dados locais."}
        ]
    }
]

# === Salvar JSON ===
with open(CAMINHO_SAIDA_JSON, "w", encoding="utf-8") as f:
    json.dump(rubrica, f, ensure_ascii=False, indent=2)

# === Salvar CSV ===
linhas_csv = []
for bloco in rubrica:
    for nivel in bloco["niveis"]:
        linhas_csv.append({
            "Dimensão": bloco["dimensao"],
            "Versão": bloco["versao"],
            "Fonte": bloco["fonte"],
            "Nível": nivel["nivel"],
            "Nome do Nível": nivel["nome"],
            "Descrição": nivel["descricao"],
            "Timestamp": bloco["timestamp_versao"]
        })

df_csv = pd.DataFrame(linhas_csv)
df_csv.to_csv(CAMINHO_SAIDA_CSV, index=False, encoding="utf-8")

# === Inserir no MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["sinapse_9ano_todas_v3"]
colecao.delete_many({})
colecao.insert_many(rubrica)
client.close()

print("✅ Rubrica SINAPSE v3 inserida com sucesso.")
print(f"📄 JSON: {CAMINHO_SAIDA_JSON}")
print(f"📄 CSV:  {CAMINHO_SAIDA_CSV}")
print(f"🌐 MongoDB: rubricas.sinapse_9ano_todas_v3")

