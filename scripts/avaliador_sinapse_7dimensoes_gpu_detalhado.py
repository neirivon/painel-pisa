
import os
import json
import fitz
import pandas as pd
import unicodedata
import warnings
from transformers import pipeline
from keybert import KeyBERT
from textwrap import wrap

warnings.simplefilter("ignore", ResourceWarning)

CAMINHO_PDFS = "/home/neirivon/backup_dados_pesados/INEP_novo/RELATORIOS/"

with open(os.path.join("/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas", "rubrica_sinapse_7dimensoes.json"), "r", encoding="utf-8") as f:
    rubrica = json.load(f)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
kw_model = KeyBERT()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

paginas_por_edicao = {
    "2000": (12, 18, "Introdução"),
    "2003": (1, 8, "Documento completo"),
    "2006": (15, 18, "Introdução"),
    "2009": (13, 19, "Seção '1 O PISA'"),
    "2012": (12, 17, "Introdução"),
    "2015": (18, 25, "Introdução"),
    "2018": (19, 33, "Introdução"),
    "2022": (8, 21, "Desempenho 2022")
}

def limpar_texto(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    return texto.replace("\n", " ").replace("\xa0", " ").strip()

def extrair_paginas_pdf(caminho_pdf, pagina_inicio, pagina_fim):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for i in range(pagina_inicio - 1, min(pagina_fim, len(doc))):
        texto += doc[i].get_text()
    return limpar_texto(texto)

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
            ano = os.path.basename(os.path.dirname(caminho))
            if ano not in paginas_por_edicao:
                continue
            pagina_inicio, pagina_fim, trecho_desc = paginas_por_edicao[ano]
            try:
                texto = extrair_paginas_pdf(caminho, pagina_inicio, pagina_fim)
                partes = wrap(texto, 1000)
                resumos = []
                for parte in partes[:3]:
                    resultado = summarizer(parte, max_length=250, min_length=80, do_sample=False)
                    resumos.append(resultado[0]["summary_text"])
                resumo_final = " ".join(resumos)
                palavras_chave = [kw[0] for kw in kw_model.extract_keywords(texto[:3000], top_n=5)]
                avaliacoes = prever_dimensoes_ia(resumo_final, rubrica)

                print(f"✅ {arquivo} → {trecho_desc}")

                resultados_finais.append({
                    "arquivo": caminho,
                    "ano": ano,
                    "trecho_extraido": trecho_desc,
                    "resumo": resumo_final,
                    "palavras_chave": palavras_chave,
                    "avaliacoes": avaliacoes
                })

            except Exception as e:
                print(f"❌ Erro em {arquivo}: {e}")
                continue

saida_json = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/avaliacoes_rubrica_sinapse.json"
saida_csv = "/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas/avaliacoes_rubrica_sinapse.csv"

with open(saida_json, "w", encoding="utf-8") as fjson:
    json.dump(resultados_finais, fjson, indent=2, ensure_ascii=False)

linhas_csv = []
for r in resultados_finais:
    for av in r["avaliacoes"]:
        linhas_csv.append({
            "arquivo": r["arquivo"],
            "ano": r["ano"],
            "trecho_extraido": r["trecho_extraido"],
            "dimensao": av["dimensao"],
            "nivel": av["nivel"],
            "titulo": av["titulo"],
            "descricao": av["descricao"],
            "palavras_chave": ", ".join(r["palavras_chave"]),
            "resumo": r["resumo"][:400] + "..."
        })

df_csv = pd.DataFrame(linhas_csv)
df_csv.to_csv(saida_csv, index=False)
print("✅ Análise com resumos detalhados finalizada com sucesso.")
