import os
import json
import fitz
import pandas as pd
import warnings
from transformers import pipeline
from keybert import KeyBERT

# Ignorar avisos de recursos temporários
warnings.simplefilter("ignore", ResourceWarning)

# Caminho base onde estão os diretórios por edição do PISA
CAMINHO_PDFS = "/home/neirivon/backup_dados_pesados/INEP_novo/RELATORIOS/"

# Carregar estrutura da rubrica
with open(os.path.join("/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas", "rubrica_sinapse_7dimensoes.json"), "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# Modelos de IA
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
kw_model = KeyBERT()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Palavras-chave para filtrar conteúdo relevante
PALAVRAS_CHAVE = ["competência", "habilidade", "território", "metodologia ativa", "taxonomia", "inclusão", "neuropsico", "DUA", "BNCC"]

# Função para extrair texto
def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

# Inferência de dimensões da rubrica
def prever_dimensoes_ia(texto, rubrica):
    resultados = []
    for dimensao in sorted(set(d["dimensao"] for d in rubrica)):
        candidatos = [f'{d["titulo"]}: {d["descricao"]}' for d in rubrica if d["dimensao"] == dimensao]
        resultado = classifier(texto, candidate_labels=candidatos)
        melhor = resultado["labels"][0]
        for d in rubrica:
            if d["dimensao"] == dimensao and melhor.startswith(d["titulo"]):
                resultados.append({
                    "dimensao": dimensao,
                    "nivel": d["nivel"],
                    "titulo": d["titulo"],
                    "descricao": d["descricao"]
                })
                break
    return resultados

# Processar todos os PDFs nas subpastas
resultados_finais = []
for root, _, files in os.walk(CAMINHO_PDFS):
    for arquivo in files:
        if arquivo.endswith(".pdf"):
            caminho = os.path.join(root, arquivo)
            texto = extrair_texto_pdf(caminho).lower()

            print(f"🧪 Verificando: {arquivo} → processando...")
            if True:
                resumo = summarizer(texto[:3000], max_length=200, min_length=80, do_sample=False)[0]["summary_text"]
                palavras_chave = [kw[0] for kw in kw_model.extract_keywords(texto[:2000], top_n=5)]
                avaliacoes = prever_dimensoes_ia(resumo, rubrica)

                resultado = {
                    "arquivo": caminho,
                    "resumo": resumo,
                    "palavras_chave": palavras_chave,
                    "avaliacoes": avaliacoes
                }
                resultados_finais.append(resultado)

# Salvar resultados
with open(os.path.join("/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas", "avaliacoes_rubrica_sinapse.json"), "w", encoding="utf-8") as fjson:
    json.dump(resultados_finais, fjson, indent=2, ensure_ascii=False)

# Criar CSV simplificado
linhas_csv = []
for r in resultados_finais:
    for av in r["avaliacoes"]:
        linhas_csv.append({
            "arquivo": r["arquivo"],
            "dimensao": av["dimensao"],
            "nivel": av["nivel"],
            "titulo": av["titulo"],
            "descricao": av["descricao"],
            "palavras_chave": ", ".join(r["palavras_chave"])
        })

df_csv = pd.DataFrame(linhas_csv)
df_csv.to_csv(os.path.join("/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas", "avaliacoes_rubrica_sinapse.csv"), index=False)
print("✅ Análise finalizada. Resultados salvos como JSON e CSV.")
