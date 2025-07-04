from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "i")nserir_rubrica_sinapse_dim_CTC.py

import json
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
import os

# === Dados da rubrica
rubrica = [
    {
        "dimensao": "Contextualização Territorial e Cultural",
        "nivel": 1,
        "nome_nivel": "Ausência de contextualização",
        "descritor": "A prática pedagógica é totalmente genérica, sem consideração pelas características culturais, históricas, ambientais ou sociais do território. Não há diálogo com a realidade local nem envolvimento da comunidade.",
        "indicadores": [],
        "versao": "v1",
        "timestamp": datetime.utcnow().isoformat(),
        "fonte": "Elaborado pelos autores. Referências: David Sobel, Petrônio Mendes, Walter Rodney, Boaventura de Sousa Santos."
    },
    {
        "dimensao": "Contextualização Territorial e Cultural",
        "nivel": 2,
        "nome_nivel": "Contextualização incipiente",
        "descritor": "Há reconhecimento inicial do contexto local, mas as atividades são limitadas e pouco significativas. Algumas referências ao ambiente próximo podem surgir de forma superficial, sem planejamento intencional.",
        "indicadores": [
            "Citações pontuais sobre a localidade",
            "Ausência de projetos comunitários"
        ],
        "versao": "v1",
        "timestamp": datetime.utcnow().isoformat(),
        "fonte": "Elaborado pelos autores. Referências: David Sobel, Petrônio Mendes, Walter Rodney, Boaventura de Sousa Santos."
    },
    {
        "dimensao": "Contextualização Territorial e Cultural",
        "nivel": 3,
        "nome_nivel": "Contextualização técnica e parcial",
        "descritor": "Atividades são adaptadas às necessidades gerais do grupo, com base em informações básicas sobre o território (como renda média, infraestrutura). Há esforços para incluir temas locais, mas ainda falta envolver a comunidade e considerar diversidade cultural e identitária.",
        "indicadores": [
            "Dados demográficos são considerados",
            "Projetos esporádicos com temas locais"
        ],
        "versao": "v1",
        "timestamp": datetime.utcnow().isoformat(),
        "fonte": "Elaborado pelos autores. Referências: David Sobel, Petrônio Mendes, Walter Rodney, Boaventura de Sousa Santos."
    },
    {
        "dimensao": "Contextualização Territorial e Cultural",
        "nivel": 4,
        "nome_nivel": "Práticas integradas ao território e cultura local",
        "descritor": "A escola desenvolve projetos e atividades com base nas especificidades do local, incorporando história, língua(s), saberes tradicionais, questões ambientais e realidades socioeconômicas. Há diálogo constante com a comunidade e uso de recursos locais.",
        "indicadores": [
            "Projetos com base em dados locais",
            "Participação de lideranças comunitárias",
            "Uso de saberes tradicionais em sala"
        ],
        "versao": "v1",
        "timestamp": datetime.utcnow().isoformat(),
        "fonte": "Elaborado pelos autores. Referências: David Sobel, Petrônio Mendes, Walter Rodney, Boaventura de Sousa Santos."
    },
    {
        "dimensao": "Contextualização Territorial e Cultural",
        "nivel": 5,
        "nome_nivel": "Educação territorialmente responsiva e co-construída",
        "descritor": "A prática pedagógica é profundamente enraizada na realidade local e construída em parceria com a comunidade. São utilizados dados qualitativos e quantitativos (como pesquisa participativa, mapas colaborativos, narrativas locais) para planejar, implementar e avaliar o ensino. Promove protagonismo comunitário e valorização da identidade local.",
        "indicadores": [
            "Mapeamento cultural comunitário",
            "Coautoria de alunos e famílias nos projetos",
            "Uso de dados geográficos, históricos e narrativas locais"
        ],
        "versao": "v1",
        "timestamp": datetime.utcnow().isoformat(),
        "fonte": "Elaborado pelos autores. Referências: David Sobel, Petrônio Mendes, Walter Rodney, Boaventura de Sousa Santos."
    }
]

# === Criar diretório de saída
os.makedirs("dados_processadoos.path.join(s, "b")ncc", exist_ok=True)

# === Salvar em JSON
json_path = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_dim_contextualizacao.json"
with open(json_path, "w", encoding="utf-8") as jf:
    json.dump(rubrica, jf, ensure_ascii=False, indent=2)
print(f"💾 JSON salvo em: {json_path}")

# === Salvar em CSV
df = pd.DataFrame(rubrica)
csv_path = "dados_processadoos.path.join(s, "b")ncos.path.join(c, "r")ubrica_sinapse_dim_contextualizacao.csv"
df.to_csv(csv_path, index=False)
print(f"💾 CSV salvo em: {csv_path}")

# === Inserir no MongoDB
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
colecao = db["sinapse_dim_CTC"]

# Limpar coleção antiga (opcional)
colecao.delete_many({})

# Inserir nova versão
colecao.insert_many(rubrica)
print("🌐 Dados inseridos na coleção: rubricas.sinapse_dim_CTC")

# Encerrar conexão
client.close()
print("🏁 Fim da execução.")

