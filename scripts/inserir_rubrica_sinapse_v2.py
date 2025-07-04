from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_rubrica_sinapse_v2.py

import json
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import os

# === Conexão com o MongoDB ===
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["sinapse_9ano_todas_v2"]

# === Nova Rubrica SINAPSE com CTC ===
rubrica = [
    {
        "dimensao": "🧠 Taxonomia de Bloom (Nível cognitivo esperado)",
        "emergente": "Recordar ou reconhecer informações simples.",
        "inicial": "Compreender significados e interpretar textos ou situações.",
        "essencial": "Aplicar conhecimentos em contextos familiares.",
        "avancado": "Analisar estruturas, relações ou causas.",
        "inovador": "Avaliar e criar soluções com autonomia.",
    },
    {
        "dimensao": "📘 Taxonomia SOLO (Profundidade conceitual da habilidade)",
        "emergente": "Pré-estrutural – Não compreende o conceito.",
        "inicial": "Uni-estrutural – Um único aspecto compreendido.",
        "essencial": "Multi-estrutural – Vários conceitos isolados.",
        "avancado": "Relacional – Conecta e sintetiza informações.",
        "inovador": "Abstrato estendido – Transfere e generaliza ideias.",
    },
    {
        "dimensao": "🌱 Metodologia ativa (Estratégia ativa recomendada)",
        "emergente": "Aula expositiva tradicional, centrada no professor.",
        "inicial": "Leitura orientada com apoio.",
        "essencial": "Problematização e resolução de desafios contextualizados.",
        "avancado": "Projetos colaborativos ou interdisciplinares.",
        "inovador": "Gamificação com avaliação formativa e engajamento contínuo.",
    },
    {
        "dimensao": "🧠 Perfil Neuropsicopedagógico (Estilo de aprendizagem e suporte metacognitivo)",
        "emergente": "Suporte puramente instrucional, sem adaptação.",
        "inicial": "Preferência auditiva ou verbal pouco explorada.",
        "essencial": "Integração de estilos visuais, lógicos ou afetivos.",
        "avancado": "Apoio metacognitivo explícito (planejar, monitorar, revisar).",
        "inovador": "Abordagem personalizada com foco no desenvolvimento integral.",
    },
    {
        "dimensao": "♿ DUA – Desenho Universal para Aprendizagem (Grau de universalidade da prática pedagógica)",
        "emergente": "Uma única forma de apresentar conteúdo.",
        "inicial": "Duas formas, sem engajamento diferenciado.",
        "essencial": "Uso moderado dos 3 princípios (representação, engajamento, expressão).",
        "avancado": "Recursos variados e adaptativos com mediação ativa.",
        "inovador": "Prática universal, inclusiva, com múltiplos canais e feedback contínuo.",
    },
    {
        "dimensao": "📍 CTC - Contextualização Territorial e Cultural (Prática pedagógica orientada por dados locais)",
        "emergente": "Ausência de contextualização – A prática pedagógica é totalmente genérica, sem consideração pelas características culturais, históricas, ambientais ou sociais do território. Não há diálogo com a realidade local nem envolvimento da comunidade.",
        "inicial": "Contextualização incipiente – Há reconhecimento inicial do contexto local, mas as atividades são limitadas e pouco significativas. Algumas referências ao ambiente próximo surgem de forma superficial, sem planejamento intencional.",
        "essencial": "Contextualização técnica e parcial – Atividades adaptadas às necessidades gerais do grupo com base em dados básicos sobre o território. Esforços ainda incipientes para envolver comunidade e diversidade cultural.",
        "avancado": "Práticas integradas ao território e cultura local – Projetos e atividades com base na realidade local, envolvendo história, saberes tradicionais, meio ambiente e participação comunitária.",
        "inovador": "Educação territorialmente responsiva e co-construída – Ação pedagógica enraizada na realidade local, com dados qualitativos e parcerias comunitárias para planejamento e avaliação contínuos.",
    },
]

# Adicionar metadata comum (versão e timestamp)
for item in rubrica:
    item["versao"] = "v2"
    item["timestamp_versao"] = datetime.utcnow().isoformat()
    item["fonte"] = "Elaborado pelos autores. Baseado em: Bloom, Biggs, CAST, Vygotsky, Sobel, Boaventura, DUA e práticas da Educação Contextualizada. 2025."

# Inserir no MongoDB
colecao.drop()
colecao.insert_many(rubrica)

# === Salvar como JSON (sem o campo _id do MongoDB) ===
rubrica_limpa = [{k: v for k, v in item.items() if k != "_id"} for item in rubrica]

json_path = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v2.json"
os.makedirs(os.path.dirname(json_path), exist_ok=True)
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(rubrica_limpa, f, ensure_ascii=False, indent=2)

# === Salvar como CSV ===
csv_path = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_9ano_todas_v2.csv"
pd.DataFrame(rubrica).to_csv(csv_path, index=False)

client.close()

print("✅ Rubrica SINAPSE v2 inserida com sucesso.")
print(f"📄 JSON: {json_path}")
print(f"📄 CSV:  {csv_path}")
print("🌐 MongoDB: rubricas.sinapse_9ano_todas_v2")

