from painel_pisa.utils.conexao_mongo import conectar_mongo
from painel_pisa.utils.config import CONFIG
from datetime import datetime
import pandas as pd
from pymongo import MongoClient
import os

# Exemplo de feedbacks para a rubrica v4
feedbacks = [
    {
        "professor": "Anônimo 1",
        "dimensao": "Taxonomia de Bloom",
        "forca": "Clareza e exemplos contextualizados",
        "sugestao": "Diferenciar habilidades cognitivas verbais e não-verbais",
        "timestamp": datetime.now().isoformat()
    },
    {
        "professor": "Anônimo 2",
        "dimensao": "DUA – Desenho Universal para Aprendizagem",
        "forca": "Acessibilidade e múltiplas formas de engajamento",
        "sugestao": "Indicar tecnologias assistivas gratuitas",
        "timestamp": datetime.now().isoformat()
    }
]

# === Modo de execução: local (MongoDB) ou cloud (CSV)
modo_execucao = "local"  # ou "cloud"

if modo_execucao == "local":
    client = conectar_mongo(nome_banco="saeb")[1]
    db = client["rubricas"]
    collection = db["feedback_v4"]
    collection.insert_many(feedbacks)
    client.close()
    print("✅ Feedbacks inseridos no MongoDB com sucesso: rubricas.feedback_v4")
else:
    os.makedirs("feedback_coletado", exist_ok=True)
    df_feedback = pd.DataFrame(feedbacks)
    df_feedback.to_csv("feedback_coletados.path.join(o, "f")eedback_rubrica_v4.csv", index=False, encoding="utf-8")
    print("✅ Feedbacks salvos no arquivo: feedback_coletados.path.join(o, "f")eedback_rubrica_v4.csv")

