# scripts/extrator_inep_pdf_to_mongo_corrigido.py

import os
import json
import pandas as pd
from pdfminer.high_level import extract_text
from painel_pisa.utils.conexao_mongo import salvar_mongodb
from painel_pisa.utils.config import CONFIG

# Lista com os parâmetros por edição
PDFS = [
    {"ano": 2000, "arquivo": "2000/inep_2000.pdf", "pag_ini": 8, "pag_fim": 89},
    {"ano": 2003, "arquivo": "2003/inep_2003.pdf", "pag_ini": 1, "pag_fim": 8},
    {"ano": 2006, "arquivo": "2006/inep_2006.pdf", "pag_ini": 15, "pag_fim": 151},
    {"ano": 2009, "arquivo": "2009/inep_2009.pdf", "pag_ini": 13, "pag_fim": 125},
    {"ano": 2012, "arquivo": "2012/inep_2012.pdf", "pag_ini": 10, "pag_fim": 64},
    {"ano": 2015, "arquivo": "2015/inep_2015.pdf", "pag_ini": 19, "pag_fim": 271},
    {"ano": 2018, "arquivo": "2018/inep_2018.pdf", "pag_ini": 19, "pag_fim": 181},
    {"ano": 2022, "arquivo": "2022/inep_2022.pdf", "pag_ini": 8, "pag_fim": 21},
]

PASTA_PDF = os.path.expanduser("~/backup_dados_pesados/INEP_novo/RELATORIOS/")
PASTA_SAIDA = os.path.join(CONFIG["CAMINHO_DADOS"], "relatorios_inep")
os.makedirs(PASTA_SAIDA, exist_ok=True)

def extrair_paragrafos(texto):
    brutos = texto.split("\n\n")
    return [p.strip().replace("\n", " ") for p in brutos if len(p.strip()) > 30]

def processar_pdf(ano, caminho_pdf, pag_ini, pag_fim):
    print(f"📄 Extraindo INEP {ano} — páginas {pag_ini}-{pag_fim}...")
    texto = extract_text(caminho_pdf, page_numbers=range(pag_ini - 1, pag_fim))
    paragrafos = extrair_paragrafos(texto)

    dados = [{"ano": ano, "paragrafo": p, "ordem": i + 1} for i, p in enumerate(paragrafos)]

    salvar_mongodb(dados, nome_colecao=f"inep_{ano}", nome_banco="relatorios_inep")

    # Exportar JSON e CSV
    with open(os.path.join(PASTA_SAIDA, f"relatorio_inep_{ano}.json"), "w", encoding="utf-8") as f:
        # Remove _id se estiver presente
       for d in dados:
           d.pop("_id", None)

       json.dump(dados, f, ensure_ascii=False, indent=2)

    pd.DataFrame(dados).to_csv(os.path.join(PASTA_SAIDA, f"relatorio_inep_{ano}.csv"), index=False)
    print(f"✅ INEP {ano} salvo com {len(dados)} parágrafos.")

def main():
    for pdf in PDFS:
        caminho_pdf = os.path.join(PASTA_PDF, pdf["arquivo"])
        processar_pdf(pdf["ano"], caminho_pdf, pdf["pag_ini"], pdf["pag_fim"])

if __name__ == "__main__":
    main()
