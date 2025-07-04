
import os
import json
import fitz
import pandas as pd
import warnings
from textwrap import wrap
from transformers import pipeline
from keybert import KeyBERT

warnings.simplefilter("ignore", ResourceWarning)

CAMINHO_PDFS = "/home/neirivon/backup_dados_pesados/INEP_novo/RELATORIOS/"

with open(os.path.join("/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas", "rubrica_sinapse_7dimensoes.json"), "r", encoding="utf-8") as f:
    rubrica = json.load(f)

# GPU ativada (device padrão)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
kw_model = KeyBERT()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return texto

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

resultados_finais = []

for root, _, files in os.walk(CAMINHO_PDFS):
    for arquivo in files:
        if arquivo.endswith(".pdf"):
            caminho = os.path.join(root, arquivo)
            try:
                texto = extrair_texto_pdf(caminho).strip().replace("\n", " ")
                if not texto or len(texto) < 300:
                    print(f"⛔️ Texto vazio ou muito curto em {arquivo}")
                    continue

                print(f"🧪 Verificando: {arquivo} → processando...")
                partes = wrap(texto, 800)
                resumos = []
                for parte in partes[:3]:
                    resultado = summarizer(parte, max_length=200, min_length=80, do_sample=False)
                    resumos.append(resultado[0]["summary_text"])
                resumo = " ".join(resumos)

                palavras_chave = [kw[0] for kw in kw_model.extract_keywords(texto[:2000], top_n=5)]
                avaliacoes = prever_dimensoes_ia(resumo, rubrica)

                resultado = {
                    "arquivo": caminho,
                    "resumo": resumo,
                    "palavras_chave": palavras_chave,
                    "avaliacoes": avaliacoes
                }
                resultados_finais.append(resultado)

            except Exception as e:
                print(f"❌ Erro ao processar {arquivo}: {e}")
                continue

# Salvar resultados finais
saida_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/avaliacoes_rubrica_sinapse.json"
saida_csv = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/avaliacoes_rubrica_sinapse.csv"

with open(saida_json, "w", encoding="utf-8") as fjson:
    json.dump(resultados_finais, fjson, indent=2, ensure_ascii=False)

linhas_csv = []
for r in resultados_finais:
    for av in r["avaliacoes"]:
        linhas_csv.append({
            "arquivo": r["arquivo"],
            "dimensao": av["dimensao"],
            "nivel": av["nivel"],
            "titulo": av["titulo"],
            "descricao": av["descricao"],
            "palavras_chave": ", ".join(r["palavras_chave"]),
            "resumo": r["resumo"][:300] + "..."
        })

df_csv = pd.DataFrame(linhas_csv)
df_csv.to_csv(saida_csv, index=False)
print("✅ Análise finalizada. Resultados salvos como JSON e CSV.")
