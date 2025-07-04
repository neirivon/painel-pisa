
import os
import json
import fitz
import pandas as pd
import unicodedata
import warnings
from textwrap import wrap
from transformers import pipeline
from keybert import KeyBERT

warnings.simplefilter("ignore", ResourceWarning)

CAMINHO_PDFS = "/home/neirivon/backup_dados_pesados/INEP_novo/RELATORIOS/"

with open(os.path.join("/home/neirivon/SINAPSE2.0/PISA/dados_processados/rubricas", "rubrica_sinapse_7dimensoes.json"), "r", encoding="utf-8") as f:
    rubrica = json.load(f)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
kw_model = KeyBERT()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def limpar_texto(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("utf-8")
    return texto.strip().replace("\n", " ").replace("\xa0", " ")

def extrair_texto_pdf(caminho_pdf):
    doc = fitz.open(caminho_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    return limpar_texto(texto)

def extrair_trecho(texto, ano):
    ano = str(ano)
    trecho = ""
    if ano == "2000":
        if "introducao" in texto:
            trecho = texto.split("introducao", 1)[-1][:3000]
        else:
            trecho = texto[:3000]
        return trecho, "Introdução"
    elif ano == "2003":
        return texto[:4000], "Documento completo (8 páginas)"
    elif ano == "2006":
        return texto.split("introducao", 1)[-1][:3000], "Introdução"
    elif ano == "2009":
        return texto.split("1 o pisa", 1)[-1][:3000], "Seção '1 O PISA'"
    elif ano == "2012":
        return texto.split("introducao", 1)[-1][:3000], "Introdução"
    elif ano == "2015":
        return texto.split("introducao", 1)[-1][:3000], "Introdução"
    elif ano == "2018":
        return texto.split("introducao", 1)[-1][:3000], "Introdução"
    elif ano == "2022":
        if "qual foi o desempenho dos estudantes brasileiros de 15 anos no teste" in texto:
            trecho = texto.split("qual foi o desempenho dos estudantes brasileiros de 15 anos no teste", 1)[-1][:3000]
        else:
            trecho = texto[:3000]
        return trecho, "Desempenho 2022"
    else:
        return texto[:3000], "Trecho padrão"

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
            try:
                texto_completo = extrair_texto_pdf(caminho).lower()
                trecho, descricao_trecho = extrair_trecho(texto_completo, ano)
                partes = wrap(trecho, 800)
                resumos = []
                for parte in partes[:3]:
                    resultado = summarizer(parte, max_length=200, min_length=80, do_sample=False)
                    resumos.append(resultado[0]["summary_text"])
                resumo = " ".join(resumos)
                palavras_chave = [kw[0] for kw in kw_model.extract_keywords(trecho, top_n=5)]
                avaliacoes = prever_dimensoes_ia(resumo, rubrica)

                print(f"✅ {arquivo} → {descricao_trecho}")

                resultados_finais.append({
                    "arquivo": caminho,
                    "ano": ano,
                    "trecho_extraido": descricao_trecho,
                    "resumo": resumo,
                    "palavras_chave": palavras_chave,
                    "avaliacoes": avaliacoes
                })

            except Exception as e:
                print(f"❌ Erro ao processar {arquivo}: {e}")
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
print("✅ Análise personalizada finalizada com sucesso.")
