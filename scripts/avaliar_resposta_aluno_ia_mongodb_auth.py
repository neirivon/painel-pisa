import json
from datetime import datetime
from pymongo import MongoClient
from transformers import pipeline

# === Configuração de caminhos e autenticação MongoDB ===
CAMINHO_RUBRICA = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/rubrica_sinapse_ia_v1_3_padronizada.json"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/?authSource=admin"
DB_NAME = "pisa"
COLLECTION_NAME = "avaliacoes_ia"
DIMENSAO_ALVO = "Engajamento e Responsabilidade Social"

# === Carregar a rubrica
with open(CAMINHO_RUBRICA, "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# === Extrair os níveis da dimensão específica
dimensao = next((d for d in rubrica["dimensoes"] if d["dimensao"] == DIMENSAO_ALVO), None)
niveis = dimensao["niveis"] if dimensao else []

# === Pipeline leve de análise de sentimento (modelo multilíngue)
sentimento_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# === Análise de sentimento com categorização
def analisar_sentimento(texto):
    resultado = sentimento_pipeline(texto)[0]
    estrelas = int(resultado["label"][0])
    if estrelas <= 2:
        return "negativo", resultado["score"]
    elif estrelas == 3:
        return "neutro", resultado["score"]
    else:
        return "positivo", resultado["score"]

# === Inferência de nível com palavras-chave
def inferir_nivel(texto):
    texto = texto.lower()
    if any(p in texto for p in ["lider", "transformar", "solidariedade", "comunidade"]):
        return "Avançado", 0.85
    elif any(p in texto for p in ["projeto", "grupo", "resolver", "compromisso"]):
        return "Proficiente", 0.75
    elif any(p in texto for p in ["ajudar", "colaborar", "quando", "solicitado"]):
        return "Intermediário", 0.65
    else:
        return "Emergente", 0.55

# === Geração de feedback baseado no nível e sentimento
def gerar_feedback(nivel, sentimento):
    if sentimento == "negativo":
        return "Você demonstrou esforço, mesmo enfrentando desafios. Continue buscando parcerias e apoio em sua jornada escolar!"
    elif nivel == "Avançado":
        return "Excelente! Seu engajamento social é inspirador e contribui para um ambiente escolar melhor."
    elif nivel == "Proficiente":
        return "Muito bom! Você mostra responsabilidade com o coletivo. Que tal propor novas ações com seus colegas?"
    elif nivel == "Intermediário":
        return "Você já está no caminho certo! Com mais iniciativa, poderá impactar ainda mais sua comunidade escolar."
    else:
        return "Toda contribuição é importante. Que tal começar com pequenas ações e observar o impacto que você pode causar?"

# === Entrada de resposta manual (ou adapte para CSV)
resposta_aluno = input("Digite a resposta do aluno: ")

# === Processamento
nivel, confianca_nivel = inferir_nivel(resposta_aluno)
sentimento, confianca_sent = analisar_sentimento(resposta_aluno)
feedback = gerar_feedback(nivel, sentimento)

# === Documento final
registro = {
    "versao_rubrica": rubrica["versao"],
    "dimensao": DIMENSAO_ALVO,
    "resposta_aluno": resposta_aluno,
    "nivel_inferido": nivel,
    "confianca_nivel": round(confianca_nivel, 3),
    "sentimento_ia": sentimento,
    "confianca_sentimento": round(confianca_sent, 3),
    "feedback_automatico": feedback,
    "timestamp": datetime.now().isoformat(),
    "modo": "cloud",
    "avaliador": "nlptown/bert-base + heurística_keywords"
}

# === Inserir no MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[COLLECTION_NAME]
    col.insert_one(registro)
    print("✅ Registro salvo com sucesso no MongoDB.")
except Exception as e:
    print(f"❌ Erro ao salvar no MongoDB: {e}")
finally:
    client.close()

