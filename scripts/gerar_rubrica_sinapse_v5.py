from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
# scriptos.path.join(s, "g")erar_rubrica_sinapse_v5.py

import os
import json
import pandas as pd
from pymongo import MongoClient

# Estrutura da Rubrica SINAPSE v5
rubricas_v5 = [
    {
        "dimensao": "Perfil Neuropsicopedagógico",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Demonstra dificuldades na organização do pensamento e pouca clareza na expressão." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Estrutura frases com lógica básica e expressa ideias com esforço visível." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Apresenta fluidez e conexões claras entre ideias, com coerência textual." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Utiliza analogias, inferência e linguagem simbólica com intencionalidade." },
            { "nivel": 5, "titulo": "Autor Reflexivo", "descricao": "Expressa pensamento complexo com abstração, empatia cognitiva e domínio verbal." }
        ]
    },
    {
        "dimensao": "DUA – Desenho Universal para Aprendizagem",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Usa linguagem simples e linear, com pouca variação ou representação visual." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Utiliza vocabulário compreensível com alguns exemplos e ilustrações." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Explora diferentes meios (textos, imagens, comparações) para representar ideias." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Integra múltiplas formas de linguagem com intencionalidade e clareza." },
            { "nivel": 5, "titulo": "Autor Reflexivo", "descricao": "Cria narrativas multimodais com propósito pedagógico e inclusão sensível." }
        ]
    },
    {
        "dimensao": "Metodologia Ativa",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Apresenta resposta passiva, sem tentativa de resolução ou ação." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Aponta um conceito ou experiência com início de contextualização." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Aplica estratégia conhecida, com relação ao contexto do problema." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Problematiza a situação e propõe alternativas inovadoras." },
            { "nivel": 5, "titulo": "Autor Reflexivo", "descricao": "Integra solução crítica, colaborativa e fundamentada na realidade." }
        ]
    },
    {
        "dimensao": "Taxonomia SOLO",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Apresenta uma única ideia desconectada (uniestrutural)." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Lista informações ou ideias múltiplas sem conexão (multiestrutural)." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Relaciona conceitos de forma lógica (relacional)." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Generaliza e transfere conhecimento (abstrato estendido)." },
            { "nivel": 5, "titulo": "Autor Reflexivo", "descricao": "Apresenta síntese conceitual original e crítica profunda do tema." }
        ]
    },
    {
        "dimensao": "Taxonomia de Bloom",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Responde com base em lembrança ou repetição literal." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Compreende e reestrutura com organização lógica." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Aplica e analisa conceitos com conexão prática." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Avalia criticamente e argumenta com base em dadoos.path.join(s, "c")ontexto." },
            { "nivel": 5, "titulo": "Autor Reflexivo", "descricao": "Cria novas soluções, generalizações ou hipóteses." }
        ]
    },
    {
        "dimensao": "CTC – Contextualização Territorial e Cultural",
        "rubricas": [
            { "nivel": 1, "titulo": "Explorador em Desenvolvimento", "descricao": "Ignora ou desconhece o contexto cultural e territorial." },
            { "nivel": 2, "titulo": "Construtor de Ideias", "descricao": "Reconhece elementos locais, mas sem aprofundar relações." },
            { "nivel": 3, "titulo": "Criador de Conexões", "descricao": "Relaciona o conteúdo ao território com base contextual." },
            { "nivel": 4, "titulo": "Transformador de Saberes", "descricao": "Integra saberes locais na argumentação ou proposta." },
            { "nivel": 5, "titulo": "Autor Reflexivo", "descricao": "Valoriza criticamente o território como fonte legítima de saber e transformação social." }
        ]
    }
]

# Flatten e exportação
flat_data = [
    {
        "dimensao": item["dimensao"],
        "nivel": rub["nivel"],
        "titulo": rub["titulo"],
        "descricao": rub["descricao"]
    }
    for item in rubricas_v5
    for rub in item["rubricas"]
]

df = pd.DataFrame(flat_data)

# Diretório de saída
saida_dir = os.path.expanduser(os.path.join(os.getenv("HOME"), "SINAPSE2.os.path.join(0, "d")ados_processadoos.path.join(s, "r")ubricas/"))
os.makedirs(saida_dir, exist_ok=True)

# Caminhos dos arquivos
csv_path = os.path.join(saida_dir, "rubrica_sinapse_v5.csv")
json_path = os.path.join(saida_dir, "rubrica_sinapse_v5.json")

# Exportação
df.to_csv(csv_path, index=False)
df.to_json(json_path, orient="records", indent=2)

# Inserção no MongoDB local
client = conectar_mongo(nome_banco="saeb")[1]
db = client["rubricas"]
collection = db["sinapse_todas_v5"]
collection.delete_many({})
collection.insert_many(flat_data)

client.close()  # ✅ fecha a conexão com o MongoDB

print("✅ Rubrica SINAPSE v5 salva em CSV, JSON e inserida no MongoDB com sucesso!")
print(f"📄 CSV: {csv_path}")
print(f"🧾 JSON: {json_path}")
print(f"🗂️ MongoDB: rubricas.sinapse_todas_v5")

print("✅ Rubrica SINAPSE v5 salva em CSV, JSON e inserida no MongoDB com sucesso!")
print(f"📄 CSV: {csv_path}")
print(f"🧾 JSON: {json_path}")
print(f"🗂️ MongoDB: rubricas.sinapse_todas_v5")

