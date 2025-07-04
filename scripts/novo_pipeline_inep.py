import pymongo
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import textwrap

# Configuração do MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_ORIGINAL = "relatorios_inep_pisa"
COLLECTION_ANALISADA = "relatorios_inep_pisa_bloom_nova"

# Mapeamento de rótulos da Taxonomia de Bloom
bloom_labels = {
    1: "Lembrar",
    2: "Compreender",
    3: "Aplicar",
    4: "Analisar",
    5: "Avaliar",
    6: "Criar"
}

rubricas = {
    1: "Promover atividades de recuperação de fatos e definições básicas, como quizzes rápidos.",
    2: "Incentivar resumos, paráfrases e mapas mentais para entendimento de conceitos.",
    3: "Propor exercícios práticos para aplicação dos conhecimentos em novos contextos.",
    4: "Estimular comparação, categorização e identificação de relações entre conceitos.",
    5: "Implementar julgamentos críticos fundamentados e comparações baseadas em critérios.",
    6: "Propor criação de novos produtos, ideias ou projetos inovadores com base nos conhecimentos."
}

def carregar_modelo():
    print("🚀 Carregando modelo BERT para análise de Bloom...")
    modelo_nome = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(modelo_nome)
    model = AutoModelForSequenceClassification.from_pretrained(modelo_nome, num_labels=6)
    classificacao = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)
    return classificacao, tokenizer

def dividir_texto(texto, tokenizer, limite_tokens=512):
    tokens = tokenizer(texto, truncation=False, return_tensors="pt")["input_ids"][0]
    partes = []
    for i in range(0, len(tokens), limite_tokens):
        parte_tokens = tokens[i:i+limite_tokens]
        parte_texto = tokenizer.decode(parte_tokens, skip_special_tokens=True)
        partes.append(parte_texto)
    return partes

def processar_relatorio():
    print("🚀 Iniciando novo processamento do Relatório INEP...")
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    doc = db[COLLECTION_ORIGINAL].find_one({"ano": 2000})
    if not doc:
        print("❌ Relatório INEP 2000 não encontrado.")
        client.close()
        return

    elementos = doc.get("elementos", [])
    novos_documentos = []

    classificacao, tokenizer = carregar_modelo()

    for elem in elementos:
        if elem.get("tipo") == "texto" and elem.get("conteudo"):
            texto = elem["conteudo"]

            partes = dividir_texto(texto, tokenizer)

            scores_aggregados = []

            for parte in partes:
                resultado = classificacao(parte, truncation=True)[0]
                label_str = resultado['label']
                score = resultado['score']
                if label_str.startswith('LABEL_'):
                    label_idx = int(label_str.split('_')[-1]) + 1
                    scores_aggregados.append((label_idx, score))

            if scores_aggregados:
                melhor_label, melhor_score = max(scores_aggregados, key=lambda x: x[1])
            else:
                melhor_label, melhor_score = 1, 0.0

            doc_novo = {
                "ano": 2000,
                "texto": texto,
                "nivel_bloom": f"{melhor_label} - {bloom_labels.get(melhor_label, 'Desconhecido')}",
                "confiança": melhor_score,
                "rubrica": rubricas.get(melhor_label, "Rubrica não encontrada."),
                "area_pisa_relacionada": None,
                "media_brasil": None,
                "media_ocde": None,
                "triangulacao": "pendente"
            }
            novos_documentos.append(doc_novo)

    if novos_documentos:
        db[COLLECTION_ANALISADA].drop()
        db[COLLECTION_ANALISADA].insert_many(novos_documentos)
        print(f"✅ Nova coleção '{COLLECTION_ANALISADA}' criada com {len(novos_documentos)} documentos.")
    else:
        print("⚠️ Nenhum texto processado.")

    client.close()

if __name__ == "__main__":
    processar_relatorio()

