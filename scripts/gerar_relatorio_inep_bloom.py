import pymongo
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Configurações MongoDB
MONGO_URI = "mongodbos.path.join(:, "/")admin:admin123@localhost:2701os.path.join(7, "?")authSource=admin"
DB_NAME = "pisa"
COLLECTION_SECOES = "relatorios_inep_pisa_secoes"
COLLECTION_DESTINO = "relatorios_inep_pisa_bloom"

# IA: Modelo e tokenizer
modelo_nome = "bert-base-uncased"  # ou "roberta-base"
tokenizer = AutoTokenizer.from_pretrained(modelo_nome)
model = AutoModelForSequenceClassification.from_pretrained(modelo_nome, num_labels=6)
classificador = pipeline("text-classification", model=model, tokenizer=tokenizer, return_all_scores=True)

# Mapa de labels corrigido para 1 a 6
mapa_labels = {
    "LABEL_0": "1 - Lembrar",
    "LABEL_1": "2 - Compreender",
    "LABEL_2": "3 - Aplicar",
    "LABEL_3": "4 - Analisar",
    "LABEL_4": "5 - Avaliar",
    "LABEL_5": "6 - Criar"
}

rubricas = {
    "1 - Lembrar": "Promover atividades de recuperação de fatos e definições básicas, como quizzes rápidos.",
    "2 - Compreender": "Incentivar resumos, paráfrases e mapas mentais para entendimento de conceitos.",
    "3 - Aplicar": "Propor resolução de problemas e casos práticos no contexto brasileiro.",
    "4 - Analisar": "Estimular debates críticos e identificação de falhaos.path.join(s, "f")orças nos argumentos.",
    "5 - Avaliar": "Implementar julgamentos críticos fundamentados e comparações baseadas em critérios.",
    "6 - Criar": "Desafiar os estudantes a propor projetos inovadores e soluções originais para problemas educacionais."
}

def inferir_bloom(texto):
    resultado = classificador(texto[:512])  # Corta se ultrapassar 512 tokens
    scores = resultado[0]
    scores_ordenados = sorted(scores, key=lambda x: x['score'], reverse=True)
    label_detectada = scores_ordenados[0]['label']
    nivel_bloom = mapa_labels.get(label_detectada, "Desconhecido")
    rubrica = rubricas.get(nivel_bloom, "Rubrica não definida.")
    return nivel_bloom, scores_ordenados[0]['score'], rubrica

def gerar_analises():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]

    print("🚀 Carregando elementos das seções...")
    documento = db[COLLECTION_SECOES].find_one({"ano": 2000})

    if not documento:
        print("❌ Documento de seções não encontrado!")
        return

    secoes = documento.get("secoes", [])
    novos_docs = []

    for secao in secoes:
        nome_secao = secao.get("secao", "Desconhecido")
        elementos = secao.get("elementos", [])

        for elem in elementos:
            if elem.get("tipo") == "texto":
                texto = elem.get("conteudo", "").strip()
                if len(texto) < 20:
                    continue  # Ignora textos curtos demais

                nivel_bloom, confianca, rubrica = inferir_bloom(texto)

                novo_doc = {
                    "ano": 2000,
                    "secao": nome_secao,
                    "pagina": elem.get("pagina", None),
                    "texto": texto,
                    "nivel_bloom": nivel_bloom,
                    "confiança": confianca,
                    "rubrica": rubrica,
                    "area_pisa_relacionada": None,
                    "media_brasil": None,
                    "media_ocde": None,
                    "triangulacao": "pendente"
                }

                novos_docs.append(novo_doc)

    if novos_docs:
        print(f"📥 Inserindo {len(novos_docs)} documentos na coleção {COLLECTION_DESTINO}...")
        db[COLLECTION_DESTINO].delete_many({"ano": 2000})  # Limpa dados antigos para segurança
        db[COLLECTION_DESTINO].insert_many(novos_docs)
        print(f"✅ Coleção {COLLECTION_DESTINO} atualizada com sucesso!")
    else:
        print("⚠️ Nenhum documento válido encontrado para inserir.")

    client.close()

if __name__ == "__main__":
    print("🚀 Iniciando geração da coleção relatorios_inep_pisa_bloom...")
    gerar_analises()

