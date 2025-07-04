# scriptos.path.join(s, "g")erar_rubricas_sinapse_tmap.py

import pandas as pd
import os
from datetime import datetime

# Caminho corrigido para salvar a saída
pasta_output = "dados_processadoos.path.join(s, "t")map"
os.makedirs(pasta_output, exist_ok=True)

# Dados simulados – aqui você pode substituir com a lógica que gerar rubricas reais
rubricas = [
    {
        "Município": "Uberlândia",
        "proficiência_simulada": 460.2,
        "nível_proficiencia": "Avançado",
        "estrategia_pedagogica": "🔍 Investigação guiada com uso de dados reais sobre o município.",
        "taxonomia_bloom": "Análise",
        "metodologia_ativa": "Aprendizagem baseada em projetos",
        "perfil_neuro": "Visual – Lógico",
        "dua": "♿ Recursos multimodais e responsivos",
        "timestamp": datetime.now().isoformat()
    },
    {
        "Município": "Patos de Minas",
        "proficiência_simulada": 423.5,
        "nível_proficiencia": "Essencial",
        "estrategia_pedagogica": "🧩 Estudo de caso sobre agricultura local com mapas e gráficos.",
        "taxonomia_bloom": "Aplicação",
        "metodologia_ativa": "Estudo de caso",
        "perfil_neuro": "Multimodal",
        "dua": "♿ Alternativas visuais e textuais",
        "timestamp": datetime.now().isoformat()
    },
    {
        "Município": "Ituiutaba",
        "proficiência_simulada": 388.9,
        "nível_proficiencia": "Inicial",
        "estrategia_pedagogica": "🎯 Uso de jogos educativos para compreensão de conceitos básicos.",
        "taxonomia_bloom": "Compreensão",
        "metodologia_ativa": "Gamificação",
        "perfil_neuro": "Sinestésico",
        "dua": "♿ Elementos gráficos interativos",
        "timestamp": datetime.now().isoformat()
    }
]

# Salvar como CSV
df = pd.DataFrame(rubricas)
csv_path = os.path.join(pasta_output, "rubricas_pedagogicas_tmap.csv")
df.to_csv(csv_path, index=False, encoding="utf-8")

print("✅ Rubricas pedagógicas geradas com sucesso.")
print(f"📄 Arquivo CSV: {csv_path}")

